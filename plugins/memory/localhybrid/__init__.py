from __future__ import annotations

import hashlib
import json
import logging
import math
import os
import queue
import re
import sqlite3
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from agent.memory_provider import MemoryProvider

logger = logging.getLogger(__name__)

_DEFAULT_EMBEDDING_MODEL = "gemini-embedding-2-preview"
_CONTEXT_BLOCK_RE = re.compile(
    r"<(?:memory-context|localhybrid-context)>[\s\S]*?</(?:memory-context|localhybrid-context)>\s*",
    re.IGNORECASE,
)
_WHITESPACE_RE = re.compile(r"\s+")
_QUERY_TOKEN_RE = re.compile(r"[A-Za-z0-9_]{2,}")
_TRIVIAL_MESSAGES = {
    "ok", "okay", "thanks", "thank you", "cool", "nice", "sure", "yep", "yes", "no", "?", "kk",
}
_SYSTEM_NOTIFICATION_PREFIXES = (
    "[system:",
    "[system note:",
    "system note:",
)


def _default_config() -> dict:
    return {
        "auto_recall": True,
        "auto_capture": True,
        "embedding_model": _DEFAULT_EMBEDDING_MODEL,
        "max_prefetch_results": 8,
        "max_scan_rows": 2000,
        "session_ttl_hours": 36,
        "vector_weight": 0.55,
        "text_weight": 0.35,
        "recency_weight": 0.10,
        "min_score": 0.28,
        "max_content_chars": 3000,
    }


def _config_path(hermes_home: str) -> Path:
    return Path(hermes_home) / "memory" / "localhybrid.json"


def _as_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _safe_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _load_localhybrid_config(hermes_home: str) -> dict:
    cfg = _default_config()
    path = _config_path(hermes_home)
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                cfg.update(data)
        except Exception:
            logger.debug("Failed to parse %s", path, exc_info=True)

    cfg["auto_recall"] = _as_bool(cfg.get("auto_recall"), True)
    cfg["auto_capture"] = _as_bool(cfg.get("auto_capture"), True)
    cfg["embedding_model"] = str(cfg.get("embedding_model") or _DEFAULT_EMBEDDING_MODEL).strip() or _DEFAULT_EMBEDDING_MODEL
    cfg["max_prefetch_results"] = max(1, _safe_int(cfg.get("max_prefetch_results"), 8))
    cfg["max_scan_rows"] = max(50, _safe_int(cfg.get("max_scan_rows"), 2000))
    cfg["session_ttl_hours"] = max(1, _safe_int(cfg.get("session_ttl_hours"), 36))
    cfg["vector_weight"] = max(0.0, _safe_float(cfg.get("vector_weight"), 0.55))
    cfg["text_weight"] = max(0.0, _safe_float(cfg.get("text_weight"), 0.35))
    cfg["recency_weight"] = max(0.0, _safe_float(cfg.get("recency_weight"), 0.10))
    total = cfg["vector_weight"] + cfg["text_weight"] + cfg["recency_weight"]
    if total <= 0:
        cfg["vector_weight"], cfg["text_weight"], cfg["recency_weight"] = 0.55, 0.35, 0.10
    else:
        cfg["vector_weight"] /= total
        cfg["text_weight"] /= total
        cfg["recency_weight"] /= total
    cfg["min_score"] = max(0.0, min(1.0, _safe_float(cfg.get("min_score"), 0.28)))
    cfg["max_content_chars"] = max(200, _safe_int(cfg.get("max_content_chars"), 3000))
    return cfg


def _save_localhybrid_config(config: dict, hermes_home: str) -> None:
    path = _config_path(hermes_home)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _normalize_model_name(model: str) -> str:
    model = (model or "").strip()
    if not model:
        return _DEFAULT_EMBEDDING_MODEL
    return model if model.startswith("models/") else f"models/{model}"


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def _pack_vector(values: Iterable[float]) -> bytes:
    import array

    arr = array.array("f", [float(v) for v in values])
    return arr.tobytes()


def _unpack_vector(blob: bytes) -> list[float]:
    import array

    arr = array.array("f")
    arr.frombytes(blob)
    return list(arr)


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na <= 0 or nb <= 0:
        return 0.0
    return dot / (na * nb)


def _strip_context(text: str) -> str:
    return _CONTEXT_BLOCK_RE.sub("", text or "").strip()


def _clean_text(text: str, *, max_chars: int = 3000) -> str:
    text = _strip_context(text or "")
    text = text.replace("\x00", " ")
    text = _WHITESPACE_RE.sub(" ", text).strip()
    if len(text) > max_chars:
        keep = max_chars - 32
        text = text[:keep].rstrip() + " …[truncated]"
    return text


def _preview(text: str, limit: int = 220) -> str:
    text = _clean_text(text, max_chars=limit)
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def _query_to_fts(query: str) -> str:
    terms = []
    seen = set()
    for token in _QUERY_TOKEN_RE.findall(query or ""):
        token = token.lower()
        if token in seen:
            continue
        seen.add(token)
        terms.append(token)
    return " OR ".join(terms[:8])


def _read_dotenv_value(path: Path, key: str) -> Optional[str]:
    if not path.exists():
        return None
    try:
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() != key:
                continue
            value = v.strip().strip('"').strip("'")
            return value or None
    except Exception:
        logger.debug("Failed to read dotenv value %s from %s", key, path, exc_info=True)
    return None


def _extract_curated_entries(raw: str) -> list[str]:
    raw = (raw or "").strip()
    if not raw:
        return []
    if "\n§\n" in raw:
        return [part.strip() for part in raw.split("\n§\n") if part.strip()]

    lines = raw.splitlines()
    entries: list[str] = []
    current: list[str] = []
    for line in lines:
        if line.startswith("- ["):
            if current:
                entries.append("\n".join(current).strip())
            current = [line]
        elif current and (line.startswith("  ") or not line.startswith("#")):
            current.append(line)
    if current:
        entries.append("\n".join(current).strip())
    return entries if entries else [raw]


class LocalHybridMemoryProvider(MemoryProvider):
    def __init__(self):
        self._config = _default_config()
        self._hermes_home = Path.home() / ".hermes"
        self._db_path = self._hermes_home / "memory" / "localhybrid.sqlite"
        self._db: Optional[sqlite3.Connection] = None
        self._platform = "cli"
        self._user_scope = "local-user"
        self._agent_identity = "default"
        self._workspace = "hermes"
        self._session_id = ""
        self._embedding_model = _DEFAULT_EMBEDDING_MODEL
        self._embedding_key = ""
        self._embedding_failure_until = 0.0
        self._write_enabled = True
        self._write_queue: "queue.Queue[Optional[dict]]" = queue.Queue()
        self._stop_event = threading.Event()
        self._worker: Optional[threading.Thread] = None
        self._turn_counter = 0

    @property
    def name(self) -> str:
        return "localhybrid"

    def is_available(self) -> bool:
        return True

    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "embedding_model",
                "description": "Embedding model (Gemini/Google)",
                "default": _DEFAULT_EMBEDDING_MODEL,
            },
            {
                "key": "auto_recall",
                "description": "Automatically recall relevant memory before each turn",
                "choices": [True, False],
                "default": True,
            },
            {
                "key": "auto_capture",
                "description": "Automatically capture conversation turns into memory",
                "choices": [True, False],
                "default": True,
            },
            {
                "key": "max_prefetch_results",
                "description": "Maximum memories to inject per turn",
                "default": 8,
            },
            {
                "key": "session_ttl_hours",
                "description": "TTL in hours for session continuity/checkpoint memories",
                "default": 36,
            },
        ]

    def save_config(self, values: Dict[str, Any], hermes_home: str) -> None:
        cfg = _load_localhybrid_config(hermes_home)
        if values:
            cfg.update(values)
        _save_localhybrid_config(cfg, hermes_home)

    def initialize(self, session_id: str, **kwargs) -> None:
        self._hermes_home = Path(kwargs.get("hermes_home") or (Path.home() / ".hermes")).expanduser()
        self._config = _load_localhybrid_config(str(self._hermes_home))
        self._db_path = self._hermes_home / "memory" / "localhybrid.sqlite"
        self._platform = str(kwargs.get("platform") or "cli")
        self._user_scope = str(kwargs.get("user_id") or "local-user")
        self._agent_identity = str(kwargs.get("agent_identity") or "default")
        self._workspace = str(kwargs.get("agent_workspace") or "hermes")
        self._session_id = session_id or ""
        agent_context = str(kwargs.get("agent_context") or "primary")
        self._write_enabled = agent_context not in {"cron", "flush", "subagent"}
        self._embedding_model = _normalize_model_name(self._config.get("embedding_model") or _DEFAULT_EMBEDDING_MODEL)
        self._embedding_key = self._resolve_embedding_key()

        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._db = self._open_connection(self._db_path)
        self._ensure_schema(self._db)
        self._cleanup_expired(self._db)

        self._stop_event.clear()
        if not (self._worker and self._worker.is_alive()):
            self._worker = threading.Thread(
                target=self._worker_loop,
                name="localhybrid-memory-worker",
                daemon=True,
            )
            self._worker.start()

        self._ingest_curated_memory()

    def system_prompt_block(self) -> str:
        embeddings_state = "on" if self._embedding_key else "off"
        return (
            "LocalHybrid memory is active. It uses local SQLite-backed retrieval with "
            f"agent-scoped lanes (recent continuity, agent-private, workspace-shared, user-global). "
            f"Embeddings are {embeddings_state}; lexical retrieval remains available even if embeddings fail. "
            "Use the built-in memory tool for explicit durable facts: target='memory' writes and MEMORY.md "
            "imports stay in this agent-private lane, while target='user' writes go to the user-global lane."
        )

    def on_turn_start(self, turn_number: int, message: str, **kwargs) -> None:
        self._turn_counter = turn_number
        if not self._db:
            return
        if turn_number % 10 == 0:
            try:
                self._cleanup_expired(self._db)
            except Exception:
                logger.debug("localhybrid cleanup failed", exc_info=True)

    def prefetch(self, query: str, *, session_id: str = "") -> str:
        if not self._db or not self._config.get("auto_recall", True):
            return ""
        query = _clean_text(query or "", max_chars=600)
        if not query:
            return ""

        try:
            results = self._search(query)
        except Exception:
            logger.warning("localhybrid prefetch failed", exc_info=True)
            return ""

        if not results:
            return ""
        return self._format_prefetch(results)

    def queue_prefetch(self, query: str, *, session_id: str = "") -> None:
        # Intentionally no-op. This provider serves recall from durable local state.
        return None

    def sync_turn(self, user_content: str, assistant_content: str, *, session_id: str = "") -> None:
        if not self._write_enabled or not self._config.get("auto_capture", True):
            return
        user_text = _clean_text(user_content or "", max_chars=self._config["max_content_chars"])
        assistant_text = _clean_text(assistant_content or "", max_chars=self._config["max_content_chars"])
        if not self._should_capture_turn(user_text, assistant_text):
            return
        content = f"User: {user_text}\nAssistant: {assistant_text}"
        self._enqueue_store(
            lane="agent_private",
            source="turn",
            content=content,
            session_id=session_id or self._session_id,
            metadata={"kind": "turn"},
        )

    def on_session_end(self, messages: List[Dict[str, Any]]) -> None:
        checkpoint = self._build_checkpoint(messages, label="Session checkpoint")
        if checkpoint:
            self._store_checkpoint_sync(checkpoint, source="session_checkpoint")

    def on_pre_compress(self, messages: List[Dict[str, Any]]) -> str:
        checkpoint = self._build_checkpoint(messages, label="Compaction checkpoint")
        if checkpoint:
            self._store_checkpoint_sync(checkpoint, source="compaction_checkpoint")
        return ""

    def on_memory_write(self, action: str, target: str, content: str) -> None:
        if action not in {"add", "replace"} or not content:
            return
        lane = "user_global" if target == "user" else "agent_private"
        self._enqueue_store(
            lane=lane,
            source=f"explicit_{target}",
            content=_clean_text(content, max_chars=self._config["max_content_chars"]),
            session_id=self._session_id,
            pinned=True,
            metadata={"action": action, "target": target},
        )

    def on_delegation(self, task: str, result: str, *, child_session_id: str = "", **kwargs) -> None:
        task_text = _clean_text(task or "", max_chars=800)
        result_text = _clean_text(result or "", max_chars=1200)
        if not task_text or not result_text:
            return
        content = f"Delegated task: {task_text}\nResult: {result_text}"
        self._enqueue_store(
            lane="agent_private",
            source="delegation",
            content=content,
            session_id=child_session_id or self._session_id,
            metadata={"kind": "delegation"},
        )

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        return []

    def shutdown(self) -> None:
        self._stop_event.set()
        try:
            self._write_queue.put_nowait(None)
        except Exception:
            pass
        if self._worker and self._worker.is_alive():
            self._worker.join(timeout=5)
        self._worker = None
        if self._db is not None:
            try:
                self._db.close()
            except Exception:
                pass
            self._db = None

    # ------------------------------------------------------------------
    # Internal plumbing
    # ------------------------------------------------------------------

    def _resolve_embedding_key(self) -> str:
        for env_name in ("GEMINI_EMBEDDINGS_API_KEY", "GOOGLE_API_KEY", "GEMINI_API_KEY"):
            value = os.getenv(env_name)
            if value:
                return value.strip()
        for env_path in (self._hermes_home / ".env", Path.home() / ".openclaw" / ".env"):
            for env_name in ("GEMINI_EMBEDDINGS_API_KEY", "GOOGLE_API_KEY", "GEMINI_API_KEY"):
                value = _read_dotenv_value(env_path, env_name)
                if value:
                    return value.strip()
        return ""

    def _open_connection(self, path: Path) -> sqlite3.Connection:
        conn = sqlite3.connect(str(path), timeout=30, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def _ensure_schema(self, conn: sqlite3.Connection) -> None:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS memory_items (
                id TEXT PRIMARY KEY,
                lane TEXT NOT NULL,
                platform TEXT NOT NULL,
                user_scope TEXT NOT NULL,
                agent_identity TEXT NOT NULL,
                workspace TEXT NOT NULL,
                session_id TEXT NOT NULL DEFAULT '',
                source TEXT NOT NULL,
                content TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                embedding BLOB,
                embedding_model TEXT NOT NULL DEFAULT '',
                pinned INTEGER NOT NULL DEFAULT 0,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                expires_at REAL,
                retrieval_count INTEGER NOT NULL DEFAULT 0,
                last_accessed REAL,
                metadata_json TEXT NOT NULL DEFAULT '{}',
                UNIQUE(lane, platform, user_scope, agent_identity, workspace, source, content_hash)
            );

            CREATE INDEX IF NOT EXISTS idx_memory_scope
            ON memory_items(platform, user_scope, agent_identity, workspace, lane, created_at DESC);

            CREATE INDEX IF NOT EXISTS idx_memory_expires_at
            ON memory_items(expires_at);

            CREATE TABLE IF NOT EXISTS embedding_cache (
                cache_key TEXT PRIMARY KEY,
                model TEXT NOT NULL,
                vector BLOB NOT NULL,
                created_at REAL NOT NULL
            );

            CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts
            USING fts5(memory_id UNINDEXED, content, tokenize='porter unicode61');
            """
        )
        conn.commit()

    def _enqueue_store(
        self,
        *,
        lane: str,
        source: str,
        content: str,
        session_id: str,
        metadata: Optional[dict] = None,
        pinned: bool = False,
        expires_at: Optional[float] = None,
        allow_embedding: bool = True,
    ) -> None:
        content = _clean_text(content, max_chars=self._config["max_content_chars"])
        if not content:
            return
        payload = {
            "lane": lane,
            "source": source,
            "content": content,
            "session_id": session_id or "",
            "metadata": metadata or {},
            "pinned": pinned,
            "expires_at": expires_at,
            "allow_embedding": allow_embedding,
        }
        self._write_queue.put(payload)

    def _worker_loop(self) -> None:
        conn = self._open_connection(self._db_path)
        try:
            while not self._stop_event.is_set() or not self._write_queue.empty():
                try:
                    payload = self._write_queue.get(timeout=0.2)
                except queue.Empty:
                    continue
                try:
                    if payload:
                        self._store_item_sync(conn, **payload)
                except Exception:
                    logger.warning("localhybrid worker write failed", exc_info=True)
                finally:
                    self._write_queue.task_done()
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def _scope_values_for_lane(self, lane: str, session_id: str = "") -> tuple[str, str, str, str, str]:
        platform = self._platform
        user_scope = self._user_scope
        if lane == "user_global":
            return platform, user_scope, "", "", ""
        if lane == "workspace_shared":
            return platform, user_scope, "", self._workspace, ""
        if lane == "session_ephemeral":
            return platform, user_scope, self._agent_identity, self._workspace, session_id or self._session_id
        return platform, user_scope, self._agent_identity, self._workspace, session_id or self._session_id

    def _make_memory_id(
        self,
        *,
        lane: str,
        source: str,
        platform: str,
        user_scope: str,
        agent_identity: str,
        workspace: str,
        content_hash: str,
    ) -> str:
        basis = "|".join([lane, source, platform, user_scope, agent_identity, workspace, content_hash])
        return hashlib.md5(basis.encode("utf-8", errors="ignore")).hexdigest()

    def _store_item_sync(
        self,
        conn: sqlite3.Connection,
        *,
        lane: str,
        source: str,
        content: str,
        session_id: str,
        metadata: Optional[dict] = None,
        pinned: bool = False,
        expires_at: Optional[float] = None,
        allow_embedding: bool = True,
    ) -> None:
        content = _clean_text(content, max_chars=self._config["max_content_chars"])
        if not content:
            return
        platform, user_scope, agent_identity, workspace, scoped_session_id = self._scope_values_for_lane(lane, session_id)
        now = time.time()
        content_hash = _sha256(content)
        memory_id = self._make_memory_id(
            lane=lane,
            source=source,
            platform=platform,
            user_scope=user_scope,
            agent_identity=agent_identity,
            workspace=workspace,
            content_hash=content_hash,
        )
        embedding_bytes = None
        embedding_model = ""
        if allow_embedding and self._embedding_key:
            vector = self._get_embedding(conn, content, task_type="RETRIEVAL_DOCUMENT")
            if vector:
                embedding_bytes = _pack_vector(vector)
                embedding_model = self._embedding_model

        conn.execute(
            """
            INSERT INTO memory_items (
                id, lane, platform, user_scope, agent_identity, workspace, session_id,
                source, content, content_hash, embedding, embedding_model, pinned,
                created_at, updated_at, expires_at, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(lane, platform, user_scope, agent_identity, workspace, source, content_hash)
            DO UPDATE SET
                session_id = excluded.session_id,
                content = excluded.content,
                embedding = COALESCE(excluded.embedding, memory_items.embedding),
                embedding_model = CASE
                    WHEN excluded.embedding_model != '' THEN excluded.embedding_model
                    ELSE memory_items.embedding_model
                END,
                pinned = CASE WHEN excluded.pinned > memory_items.pinned THEN excluded.pinned ELSE memory_items.pinned END,
                updated_at = excluded.updated_at,
                expires_at = excluded.expires_at,
                metadata_json = excluded.metadata_json
            """,
            (
                memory_id,
                lane,
                platform,
                user_scope,
                agent_identity,
                workspace,
                scoped_session_id,
                source,
                content,
                content_hash,
                embedding_bytes,
                embedding_model,
                1 if pinned else 0,
                now,
                now,
                expires_at,
                json.dumps(metadata or {}, sort_keys=True),
            ),
        )
        conn.execute("DELETE FROM memory_fts WHERE memory_id = ?", (memory_id,))
        conn.execute("INSERT INTO memory_fts(memory_id, content) VALUES (?, ?)", (memory_id, content))
        conn.commit()

    def _get_embedding(self, conn: sqlite3.Connection, text: str, *, task_type: str) -> Optional[list[float]]:
        if not self._embedding_key:
            return None
        now = time.time()
        if now < self._embedding_failure_until:
            return None
        text = _clean_text(text, max_chars=4000)
        if not text:
            return None
        cache_key = f"{self._embedding_model}|{task_type}|{_sha256(text)}"
        row = conn.execute(
            "SELECT vector FROM embedding_cache WHERE cache_key = ?",
            (cache_key,),
        ).fetchone()
        if row and row[0]:
            return _unpack_vector(row[0])

        try:
            vector = self._request_embedding(text, task_type=task_type)
        except Exception:
            self._embedding_failure_until = time.time() + 300
            logger.warning("localhybrid embeddings failed; falling back to lexical-only for 300s", exc_info=True)
            return None

        if not vector:
            return None
        conn.execute(
            "INSERT OR REPLACE INTO embedding_cache(cache_key, model, vector, created_at) VALUES (?, ?, ?, ?)",
            (cache_key, self._embedding_model, _pack_vector(vector), now),
        )
        conn.commit()
        return vector

    def _request_embedding(self, text: str, *, task_type: str) -> list[float]:
        model_name = _normalize_model_name(self._embedding_model)
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:embedContent"
        payload = {
            "model": model_name,
            "content": {"parts": [{"text": text}]},
            "taskType": task_type,
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            endpoint + "?key=" + urllib.parse.quote(self._embedding_key),
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        values = ((body.get("embedding") or {}).get("values")) or []
        if not values:
            raise RuntimeError(f"No embedding returned for model {model_name}")
        return [float(v) for v in values]

    def _visible_to_current_agent(self, row: sqlite3.Row) -> bool:
        lane = row["lane"]
        if lane == "user_global":
            return True
        if lane == "workspace_shared":
            return row["workspace"] == self._workspace
        if lane in {"agent_private", "session_ephemeral"}:
            return row["workspace"] == self._workspace and row["agent_identity"] == self._agent_identity
        return False

    def _search(self, query: str) -> list[dict]:
        assert self._db is not None
        now = time.time()
        max_results = self._config["max_prefetch_results"]
        max_scan_rows = self._config["max_scan_rows"]
        text_scores: dict[str, float] = {}
        vector_scores: dict[str, float] = {}
        candidate_rows: dict[str, sqlite3.Row] = {}

        fts_query = _query_to_fts(query)
        if fts_query:
            try:
                rows = self._db.execute(
                    """
                    SELECT mi.*, bm25(memory_fts) AS rank
                    FROM memory_fts
                    JOIN memory_items mi ON mi.id = memory_fts.memory_id
                    WHERE memory_fts MATCH ?
                      AND mi.platform = ?
                      AND mi.user_scope = ?
                      AND (mi.expires_at IS NULL OR mi.expires_at > ?)
                    ORDER BY rank
                    LIMIT ?
                    """,
                    (fts_query, self._platform, self._user_scope, now, max_results * 8),
                ).fetchall()
            except sqlite3.OperationalError:
                rows = []

            filtered = [row for row in rows if self._visible_to_current_agent(row)]
            count = len(filtered)
            for idx, row in enumerate(filtered):
                denom = max(1, count - 1)
                text_scores[row["id"]] = max(text_scores.get(row["id"], 0.0), 1.0 - (idx / denom if denom else 0.0))
                candidate_rows[row["id"]] = row

        query_vector = self._get_embedding(self._db, query, task_type="RETRIEVAL_QUERY")
        if query_vector:
            rows = self._db.execute(
                """
                SELECT *
                FROM memory_items
                WHERE platform = ?
                  AND user_scope = ?
                  AND embedding IS NOT NULL
                  AND (expires_at IS NULL OR expires_at > ?)
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (self._platform, self._user_scope, now, max_scan_rows),
            ).fetchall()
            for row in rows:
                if not self._visible_to_current_agent(row):
                    continue
                blob = row["embedding"]
                if not blob:
                    continue
                score = (max(-1.0, min(1.0, _cosine_similarity(query_vector, _unpack_vector(blob)))) + 1.0) / 2.0
                if score <= 0:
                    continue
                vector_scores[row["id"]] = max(vector_scores.get(row["id"], 0.0), score)
                candidate_rows[row["id"]] = row

        if not candidate_rows:
            rows = self._db.execute(
                """
                SELECT *
                FROM memory_items
                WHERE platform = ?
                  AND user_scope = ?
                  AND (expires_at IS NULL OR expires_at > ?)
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (self._platform, self._user_scope, now, max_results * 4),
            ).fetchall()
            query_lc = query.lower()
            for row in rows:
                if not self._visible_to_current_agent(row):
                    continue
                content_lc = (row["content"] or "").lower()
                if query_lc in content_lc or any(token in content_lc for token in _QUERY_TOKEN_RE.findall(query_lc)):
                    candidate_rows[row["id"]] = row
                    text_scores[row["id"]] = max(text_scores.get(row["id"], 0.0), 0.45)

        scored = []
        vw = self._config["vector_weight"]
        tw = self._config["text_weight"]
        rw = self._config["recency_weight"]
        for memory_id, row in candidate_rows.items():
            age_hours = max(0.0, (now - float(row["created_at"])) / 3600.0)
            recency_score = 1.0 / (1.0 + age_hours / 24.0)
            lane_bonus = 0.05 if row["lane"] == "session_ephemeral" else (0.02 if row["lane"] == "agent_private" else 0.0)
            final_score = (
                vw * vector_scores.get(memory_id, 0.0)
                + tw * text_scores.get(memory_id, 0.0)
                + rw * recency_score
                + lane_bonus
            )
            if final_score < self._config["min_score"]:
                continue
            scored.append(
                {
                    "id": memory_id,
                    "lane": row["lane"],
                    "content": row["content"],
                    "score": round(final_score, 4),
                    "created_at": float(row["created_at"]),
                }
            )

        scored.sort(key=lambda item: (item["score"], item["created_at"]), reverse=True)
        deduped = []
        seen_hashes = set()
        for item in scored:
            content_hash = _sha256(item["content"])
            if content_hash in seen_hashes:
                continue
            seen_hashes.add(content_hash)
            deduped.append(item)
            if len(deduped) >= max_results:
                break

        if deduped:
            self._db.executemany(
                "UPDATE memory_items SET retrieval_count = retrieval_count + 1, last_accessed = ? WHERE id = ?",
                [(now, item["id"]) for item in deduped],
            )
            self._db.commit()
        return deduped

    def _format_prefetch(self, results: list[dict]) -> str:
        labels = {
            "session_ephemeral": "Recent continuity",
            "agent_private": "This agent's memory",
            "workspace_shared": "Shared workspace memory",
            "user_global": "User-global memory",
        }
        grouped: dict[str, list[str]] = {lane: [] for lane in labels}
        for item in results:
            grouped.setdefault(item["lane"], []).append(_preview(item["content"]))

        sections = []
        for lane in ("session_ephemeral", "agent_private", "workspace_shared", "user_global"):
            lines = grouped.get(lane) or []
            if not lines:
                continue
            body = "\n".join(f"- {line}" for line in lines[:3])
            sections.append(f"{labels[lane]}:\n{body}")

        if not sections:
            return ""
        return "Relevant memory:\n" + "\n\n".join(sections)

    def _cleanup_expired(self, conn: sqlite3.Connection) -> None:
        now = time.time()
        expired = conn.execute(
            "SELECT id FROM memory_items WHERE expires_at IS NOT NULL AND expires_at <= ?",
            (now,),
        ).fetchall()
        if expired:
            conn.executemany("DELETE FROM memory_fts WHERE memory_id = ?", [(row["id"],) for row in expired])
        conn.execute("DELETE FROM memory_items WHERE expires_at IS NOT NULL AND expires_at <= ?", (now,))
        conn.commit()

    def _should_capture_turn(self, user_text: str, assistant_text: str) -> bool:
        if not user_text or not assistant_text:
            return False
        if user_text.lower().startswith(_SYSTEM_NOTIFICATION_PREFIXES):
            return False
        combined = (user_text + " " + assistant_text).strip()
        if len(combined) < 40:
            return False
        if user_text.lower() in _TRIVIAL_MESSAGES and len(assistant_text) < 120:
            return False
        if assistant_text.strip() == "HEARTBEAT_OK":
            return False
        return True

    def _build_checkpoint(self, messages: List[Dict[str, Any]], *, label: str) -> str:
        if not messages:
            return ""
        parts: list[str] = []
        for msg in messages[-18:]:
            role = msg.get("role")
            if role not in {"user", "assistant", "tool"}:
                continue
            content = _clean_text(msg.get("content") or "", max_chars=700 if role != "tool" else 400)
            if not content:
                continue
            if role == "tool":
                parts.append(f"[tool] {content}")
            else:
                parts.append(f"[{role}] {content}")
        if not parts:
            return ""
        joined = "\n".join(parts)
        return f"{label}:\n{joined}"

    def _store_checkpoint_sync(self, checkpoint: str, *, source: str) -> None:
        if not checkpoint or not self._db:
            return
        expires_at = time.time() + (self._config["session_ttl_hours"] * 3600)
        self._store_item_sync(
            self._db,
            lane="session_ephemeral",
            source=source,
            content=checkpoint,
            session_id=self._session_id,
            metadata={"kind": source},
            expires_at=expires_at,
            allow_embedding=False,
        )

    def _ingest_curated_memory(self) -> None:
        if not self._db:
            return
        try:
            from tools.memory_tool import get_memory_dir
        except Exception:
            return
        mem_dir = get_memory_dir()
        if not mem_dir.exists():
            return

        for filename, lane, source in (
            ("USER.md", "user_global", "curated_user"),
            ("MEMORY.md", "agent_private", "curated_memory"),
        ):
            path = mem_dir / filename
            if not path.exists():
                continue
            try:
                raw = path.read_text(encoding="utf-8")
            except Exception:
                continue
            for entry in _extract_curated_entries(raw):
                self._enqueue_store(
                    lane=lane,
                    source=source,
                    content=entry,
                    session_id="",
                    pinned=True,
                    metadata={"filename": filename},
                    allow_embedding=False,
                )


__all__ = [
    "LocalHybridMemoryProvider",
    "_load_localhybrid_config",
    "_save_localhybrid_config",
]
