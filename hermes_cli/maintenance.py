"""Maintenance helpers for Hermes runtime artifacts.

Keeps cron tick locks tidy and prunes older debug/session/log artifacts
without touching the credential or bridge-security surfaces.
"""

from __future__ import annotations

import logging
import sqlite3
import time
from pathlib import Path
from typing import Any, Optional

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows fallback
    fcntl = None
    try:
        import msvcrt
    except ImportError:  # pragma: no cover - Windows fallback
        msvcrt = None

from hermes_constants import get_hermes_home
from hermes_cli.config import load_config

logger = logging.getLogger(__name__)

_DEFAULT_REQUEST_DUMP_RETENTION_DAYS = 14
_DEFAULT_SESSION_RETENTION_DAYS = 90
_DEFAULT_LOG_RETENTION_DAYS = 30
_DEFAULT_CRON_OUTPUT_RETENTION_DAYS = 90
_DEFAULT_MEMORY_ARTIFACT_RETENTION_DAYS = 30
_RETENTION_CLEANUP_INTERVAL_SECONDS = 3600
_LAST_RETENTION_CLEANUP_AT = 0.0
_SQLITE_KNOWN_ACTIVE_FILES = frozenset({
    "state.db",
    "hermes_state.db",
    "response_store.db",
    "memory_store.db",
    "retaindb_queue.db",
    "localhybrid.sqlite",
})
_SQLITE_ARTIFACT_DIR_NAMES = frozenset({
    "archive",
    "archives",
    "backup",
    "backups",
    "export",
    "exports",
    "snapshot",
    "snapshots",
})


def _coerce_positive_int(value: Any, default: int) -> int:
    try:
        coerced = int(float(value))
    except (TypeError, ValueError):
        return default
    return coerced if coerced > 0 else default


def _maintenance_retention_config(config: Optional[dict] = None) -> dict[str, int]:
    """Return effective retention windows in days.

    The helper reads a free-form ``maintenance.retention`` section when present
    and falls back to conservative defaults otherwise.
    """
    if config is None:
        try:
            config = load_config()
        except Exception:
            config = {}

    maintenance_cfg = config.get("maintenance", {}) if isinstance(config, dict) else {}
    retention_cfg = maintenance_cfg.get("retention", maintenance_cfg) if isinstance(maintenance_cfg, dict) else {}
    logging_cfg = config.get("logging", {}) if isinstance(config, dict) else {}

    return {
        "request_dump_days": _coerce_positive_int(
            retention_cfg.get("request_dump_days", retention_cfg.get("request_dumps_days", retention_cfg.get("request_dumps"))),
            _DEFAULT_REQUEST_DUMP_RETENTION_DAYS,
        ),
        "session_days": _coerce_positive_int(
            retention_cfg.get("session_days", retention_cfg.get("sessions_days")),
            _DEFAULT_SESSION_RETENTION_DAYS,
        ),
        "log_days": _coerce_positive_int(
            retention_cfg.get("log_days", retention_cfg.get("logs_days", logging_cfg.get("retention_days"))),
            _DEFAULT_LOG_RETENTION_DAYS,
        ),
        "cron_output_days": _coerce_positive_int(
            retention_cfg.get("cron_output_days", retention_cfg.get("cron_outputs_days")),
            _DEFAULT_CRON_OUTPUT_RETENTION_DAYS,
        ),
        "memory_artifact_days": _coerce_positive_int(
            retention_cfg.get(
                "memory_artifact_days",
                retention_cfg.get("memory_export_days", retention_cfg.get("memory_backup_days")),
            ),
            _DEFAULT_MEMORY_ARTIFACT_RETENTION_DAYS,
        ),
    }


def _prune_old_files(directory: Path, pattern: str, max_age_days: int, *, recursive: bool = False) -> int:
    """Delete files matching *pattern* older than *max_age_days*."""
    if max_age_days <= 0 or not directory.exists():
        return 0

    cutoff = time.time() - (max_age_days * 86400)
    removed = 0
    try:
        paths = directory.rglob(pattern) if recursive else directory.glob(pattern)
        for path in paths:
            try:
                if not path.is_file():
                    continue
                if path.stat().st_mtime >= cutoff:
                    continue
                path.unlink()
                removed += 1
            except FileNotFoundError:
                continue
            except Exception as exc:
                logger.debug("Failed to prune %s: %s", path, exc)
    except Exception as exc:
        logger.debug("Failed to scan %s for %s: %s", directory, pattern, exc)
    return removed


def _looks_like_sqlite_artifact(path: Path) -> bool:
    """Return True for backup/export SQLite artifacts, not live core DBs."""
    if not path.is_file():
        return False
    suffixes = path.suffixes
    if not suffixes:
        return False
    if suffixes[-1].lower() not in {".db", ".sqlite", ".sqlite3"}:
        return False

    if path.name in _SQLITE_KNOWN_ACTIVE_FILES:
        return False

    parts = {part.lower() for part in path.parts}
    name = path.name.lower()
    if parts & _SQLITE_ARTIFACT_DIR_NAMES:
        return True
    return any(token in name for token in ("backup", "export", "snapshot", "archive"))


def _sqlite_maintenance_target(path: Path) -> bool:
    """Return True when a SQLite file should be checkpointed."""
    return path.is_file() and path.suffix.lower() in {".db", ".sqlite", ".sqlite3"}


def _maintain_sqlite_file(path: Path, *, vacuum: bool = False) -> tuple[int, int]:
    """Checkpoint a SQLite file and optionally vacuum it.

    Returns (checkpoint_count, vacuum_count). Failures are logged and treated
    as a no-op so the cleanup pass remains best-effort.
    """
    if not _sqlite_maintenance_target(path):
        return 0, 0

    conn = None
    checkpointed = 0
    vacuumed = 0
    try:
        conn = sqlite3.connect(str(path), timeout=5)
        conn.execute("PRAGMA busy_timeout=5000")
        conn.execute("PRAGMA wal_checkpoint(PASSIVE)")
        checkpointed = 1
        if vacuum:
            conn.execute("VACUUM")
            vacuumed = 1
    except sqlite3.Error as exc:
        logger.debug("Failed to maintain sqlite file %s: %s", path, exc)
        return 0, 0
    except Exception as exc:
        logger.debug("Failed to maintain sqlite file %s: %s", path, exc)
        return 0, 0
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass
    return checkpointed, vacuumed


def _maintain_sqlite_artifacts(hermes_home: Path) -> dict[str, int]:
    """Checkpoint known SQLite files and vacuum obvious backup artifacts."""
    checkpointed = 0
    vacuumed = 0
    seen: set[Path] = set()

    candidate_paths = [
        hermes_home / "state.db",
        hermes_home / "hermes_state.db",
        hermes_home / "response_store.db",
        hermes_home / "memory_store.db",
        hermes_home / "retaindb_queue.db",
        hermes_home / "memory" / "localhybrid.sqlite",
    ]

    for base_dir in (hermes_home / "memory", hermes_home / "memories", hermes_home / "state-snapshots"):
        if not base_dir.exists():
            continue
        try:
            for path in base_dir.rglob("*"):
                if not _sqlite_maintenance_target(path):
                    continue
                candidate_paths.append(path)
        except Exception as exc:
            logger.debug("Failed to scan %s for sqlite maintenance: %s", base_dir, exc)

    for path in candidate_paths:
        if path in seen:
            continue
        seen.add(path)
        if not path.exists():
            continue
        checkpoint_count, vacuum_count = _maintain_sqlite_file(path, vacuum=_looks_like_sqlite_artifact(path))
        checkpointed += checkpoint_count
        vacuumed += vacuum_count

    return {
        "sqlite_checkpoints": checkpointed,
        "sqlite_vacuums": vacuumed,
    }


def _prune_memory_artifacts(directory: Path, max_age_days: int) -> int:
    """Prune obvious memory/export backup artifacts by mtime."""
    if max_age_days <= 0 or not directory.exists():
        return 0

    removed = 0
    for artifact_dir_name in _SQLITE_ARTIFACT_DIR_NAMES:
        artifact_dir = directory / artifact_dir_name
        removed += _prune_old_files(artifact_dir, "*", max_age_days, recursive=True)

    removed += _prune_old_files(directory, "*backup*", max_age_days, recursive=True)
    removed += _prune_old_files(directory, "*export*", max_age_days, recursive=True)
    removed += _prune_old_files(directory, "*.tar.gz", max_age_days, recursive=True)
    removed += _prune_old_files(directory, "*.tgz", max_age_days, recursive=True)
    removed += _prune_old_files(directory, "*.zip", max_age_days, recursive=True)
    removed += _prune_old_files(directory, "*.bak", max_age_days, recursive=True)
    removed += _prune_old_files(directory, "*.backup", max_age_days, recursive=True)
    removed += _prune_old_files(directory, "*.backup.*", max_age_days, recursive=True)
    return removed


def cleanup_stale_cron_tick_locks(lock_dir: Optional[Path] = None) -> int:
    """Remove stale ``.tick.gw*.lock`` files left behind by crashed tickers.

    The file is only removed after the helper can take the lock itself, which
    keeps live tickers untouched.
    """
    lock_dir = lock_dir or (get_hermes_home() / "cron")
    if not lock_dir.exists():
        return 0

    removed = 0
    for lock_path in lock_dir.glob(".tick.gw*.lock"):
        if not lock_path.is_file():
            continue
        if lock_path.is_symlink():
            continue

        lock_fd = None
        try:
            lock_fd = open(lock_path, "a+")
            if fcntl:
                fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                lock_path.unlink(missing_ok=True)
                removed += 1
            elif msvcrt:
                lock_fd.seek(0, 2)
                if lock_fd.tell() == 0:
                    lock_fd.seek(0)
                    lock_fd.write(" ")
                    lock_fd.flush()
                    lock_fd.seek(0)
                msvcrt.locking(lock_fd.fileno(), msvcrt.LK_NBLCK, 1)
                msvcrt.locking(lock_fd.fileno(), msvcrt.LK_UNLCK, 1)
                lock_fd.close()
                lock_fd = None
                lock_path.unlink(missing_ok=True)
                removed += 1
        except (OSError, IOError):
            # Another process still holds the lock; leave it alone.
            continue
        except Exception as exc:
            logger.debug("Failed to clean stale tick lock %s: %s", lock_path, exc)
        finally:
            if lock_fd is not None:
                try:
                    if fcntl:
                        fcntl.flock(lock_fd, fcntl.LOCK_UN)
                except Exception:
                    pass
                try:
                    lock_fd.close()
                except Exception:
                    pass

    return removed


def cleanup_retention_artifacts(
    hermes_home: Optional[Path] = None,
    *,
    config: Optional[dict] = None,
    request_dump_days: Optional[int] = None,
    session_days: Optional[int] = None,
    log_days: Optional[int] = None,
    cron_output_days: Optional[int] = None,
    memory_artifact_days: Optional[int] = None,
    force: bool = False,
) -> dict[str, int]:
    """Prune old request dumps, session artifacts, and rotated logs.

    The helper is throttled to run at most once per hour by default so the
    scheduler can call it opportunistically without adding much overhead.
    """
    global _LAST_RETENTION_CLEANUP_AT

    now = time.time()
    if not force and now - _LAST_RETENTION_CLEANUP_AT < _RETENTION_CLEANUP_INTERVAL_SECONDS:
        return {
            "request_dumps": 0,
            "session_logs": 0,
            "session_transcripts": 0,
            "rotated_logs": 0,
            "cron_outputs": 0,
            "memory_artifacts": 0,
            "sqlite_checkpoints": 0,
            "sqlite_vacuums": 0,
            "total": 0,
        }

    _LAST_RETENTION_CLEANUP_AT = now

    retention = _maintenance_retention_config(config)
    request_dump_days = request_dump_days or retention["request_dump_days"]
    session_days = session_days or retention["session_days"]
    log_days = log_days or retention["log_days"]
    cron_output_days = cron_output_days or retention["cron_output_days"]
    memory_artifact_days = memory_artifact_days or retention["memory_artifact_days"]

    hermes_home = hermes_home or get_hermes_home()
    sessions_dir = hermes_home / "sessions"
    logs_dir = hermes_home / "logs"
    cron_output_dir = hermes_home / "cron" / "output"
    memory_dir = hermes_home / "memory"
    memories_dir = hermes_home / "memories"

    request_dumps = _prune_old_files(sessions_dir, "request_dump_*.json", request_dump_days)
    session_logs = _prune_old_files(sessions_dir, "session_*.json", session_days)
    session_transcripts = _prune_old_files(sessions_dir, "*.jsonl", session_days)
    rotated_logs = _prune_old_files(logs_dir, "*.log.[0-9]*", log_days)
    cron_outputs = _prune_old_files(cron_output_dir, "*.md", cron_output_days, recursive=True)
    memory_artifacts = _prune_memory_artifacts(memory_dir, memory_artifact_days)
    memory_artifacts += _prune_memory_artifacts(memories_dir, memory_artifact_days)
    sqlite_maintenance = _maintain_sqlite_artifacts(hermes_home)

    total = (
        request_dumps
        + session_logs
        + session_transcripts
        + rotated_logs
        + cron_outputs
        + memory_artifacts
        + sqlite_maintenance["sqlite_checkpoints"]
        + sqlite_maintenance["sqlite_vacuums"]
    )
    if total:
        logger.info(
            "Maintenance cleanup removed %d artifact(s) "
            "(request dumps=%d, session logs=%d, transcripts=%d, rotated logs=%d, cron outputs=%d, "
            "memory artifacts=%d, sqlite checkpoints=%d, sqlite vacuums=%d)",
            total,
            request_dumps,
            session_logs,
            session_transcripts,
            rotated_logs,
            cron_outputs,
            memory_artifacts,
            sqlite_maintenance["sqlite_checkpoints"],
            sqlite_maintenance["sqlite_vacuums"],
        )

    return {
        "request_dumps": request_dumps,
        "session_logs": session_logs,
        "session_transcripts": session_transcripts,
        "rotated_logs": rotated_logs,
        "cron_outputs": cron_outputs,
        "memory_artifacts": memory_artifacts,
        "sqlite_checkpoints": sqlite_maintenance["sqlite_checkpoints"],
        "sqlite_vacuums": sqlite_maintenance["sqlite_vacuums"],
        "total": total,
    }
