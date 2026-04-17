"""Tests for Hermes maintenance cleanup helpers."""

import os
import sqlite3
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from hermes_cli import maintenance


def test_cleanup_retention_artifacts_prunes_old_debug_files(tmp_path, monkeypatch):
    home = tmp_path / ".hermes"
    sessions_dir = home / "sessions"
    logs_dir = home / "logs"
    cron_output_dir = home / "cron" / "output" / "job-1"
    sessions_dir.mkdir(parents=True)
    logs_dir.mkdir(parents=True)
    cron_output_dir.mkdir(parents=True)

    config = {
        "maintenance": {
            "retention": {
                "request_dump_days": 1,
                "session_days": 1,
                "log_days": 1,
                "cron_output_days": 1,
            }
        }
    }
    monkeypatch.setattr(maintenance, "load_config", lambda: config)
    monkeypatch.setattr(maintenance, "get_hermes_home", lambda: home)

    old_request_dump = sessions_dir / "request_dump_abc.json"
    old_session_log = sessions_dir / "session_abc.json"
    old_transcript = sessions_dir / "abc.jsonl"
    current_sessions_index = sessions_dir / "sessions.json"
    old_rotated_log = logs_dir / "gateway.log.1"
    current_log = logs_dir / "gateway.log"
    old_cron_output = cron_output_dir / "20260415T100000.md"
    current_cron_output = cron_output_dir / "20260416T100000.md"

    old_request_dump.write_text("{}", encoding="utf-8")
    old_session_log.write_text("{}", encoding="utf-8")
    old_transcript.write_text("[]", encoding="utf-8")
    current_sessions_index.write_text("{}", encoding="utf-8")
    old_rotated_log.write_text("rotated", encoding="utf-8")
    current_log.write_text("current", encoding="utf-8")
    old_cron_output.write_text("# old output", encoding="utf-8")
    current_cron_output.write_text("# current output", encoding="utf-8")

    for path in (old_request_dump, old_session_log, old_transcript, old_rotated_log, old_cron_output):
        ts = (datetime.now() - timedelta(days=3)).timestamp()
        os.utime(path, (ts, ts))

    result = maintenance.cleanup_retention_artifacts(home, force=True)

    assert result["request_dumps"] == 1
    assert result["session_logs"] == 1
    assert result["session_transcripts"] == 1
    assert result["rotated_logs"] == 1
    assert result["cron_outputs"] == 1
    assert result["memory_artifacts"] == 0
    assert result["sqlite_checkpoints"] == 0
    assert result["sqlite_vacuums"] == 0
    assert result["total"] == 5
    assert not old_request_dump.exists()
    assert not old_session_log.exists()
    assert not old_transcript.exists()
    assert not old_rotated_log.exists()
    assert not old_cron_output.exists()
    assert current_sessions_index.exists()
    assert current_log.exists()
    assert current_cron_output.exists()


def test_cleanup_retention_artifacts_prunes_memory_exports_and_keeps_live_sqlite(tmp_path, monkeypatch):
    home = tmp_path / ".hermes"
    memory_dir = home / "memory"
    memories_dir = home / "memories"
    export_dir = memory_dir / "exports"
    backup_dir = memories_dir / "backups"
    export_dir.mkdir(parents=True)
    backup_dir.mkdir(parents=True)

    config = {
        "maintenance": {
            "retention": {
                "memory_artifact_days": 1,
            }
        }
    }
    monkeypatch.setattr(maintenance, "load_config", lambda: config)
    monkeypatch.setattr(maintenance, "get_hermes_home", lambda: home)

    live_state_db = home / "state.db"
    live_memory_db = memory_dir / "localhybrid.sqlite"
    for db_path in (live_state_db, live_memory_db):
        conn = sqlite3.connect(str(db_path))
        conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, value TEXT)")
        conn.execute("INSERT INTO t (value) VALUES ('live')")
        conn.commit()
        conn.close()

    old_export = export_dir / "memory-export.jsonl"
    old_backup = backup_dir / "memory-backup.tar.gz"
    current_export = export_dir / "current-export.jsonl"
    current_backup = backup_dir / "current-backup.tar.gz"
    old_export.write_text("{}", encoding="utf-8")
    old_backup.write_text("backup", encoding="utf-8")
    current_export.write_text("{}", encoding="utf-8")
    current_backup.write_text("backup", encoding="utf-8")

    old_ts = (datetime.now() - timedelta(days=3)).timestamp()
    for path in (old_export, old_backup):
        os.utime(path, (old_ts, old_ts))

    result = maintenance.cleanup_retention_artifacts(home, force=True)

    assert result["memory_artifacts"] == 2
    assert result["sqlite_checkpoints"] == 2
    assert result["sqlite_vacuums"] == 0
    assert not old_export.exists()
    assert not old_backup.exists()
    assert current_export.exists()
    assert current_backup.exists()
    assert live_state_db.exists()
    assert live_memory_db.exists()


def test_maintain_sqlite_file_vacuums_only_when_requested(monkeypatch, tmp_path):
    path = tmp_path / "artifact.sqlite"
    path.write_text("sqlite", encoding="utf-8")

    statements: list[str] = []

    class FakeConnection:
        def execute(self, sql):
            statements.append(sql)
            return MagicMock()

        def close(self):
            statements.append("CLOSE")

    monkeypatch.setattr(maintenance.sqlite3, "connect", lambda *args, **kwargs: FakeConnection())

    checkpointed, vacuumed = maintenance._maintain_sqlite_file(path, vacuum=True)

    assert checkpointed == 1
    assert vacuumed == 1
    assert "PRAGMA busy_timeout=5000" in statements
    assert "PRAGMA wal_checkpoint(PASSIVE)" in statements
    assert "VACUUM" in statements
    assert statements[-1] == "CLOSE"
