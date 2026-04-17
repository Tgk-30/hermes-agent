#!/usr/bin/env python3
"""Cached chat codebase scan tool.

This tool treats "N agents" as N logical scan workers. Broad repo analysis is
done with cached chat-completion calls and deterministic local indexing; rich
Hermes agents remain the right follow-up for verification. Every worker result
is spooled to disk and the tool returns a compact manifest so large scans do not
truncate before the parent agent can aggregate them.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional

from tools.registry import registry, tool_error


PROMPT_VERSION = "scan-codebase-v1"
DEFAULT_WORKERS = 8
DEFAULT_MAX_CHARS_PER_SHARD = 90_000
DEFAULT_MAX_CHARS_PER_FILE = 18_000
DEFAULT_OUTPUT = "problems.md"

EXCLUDED_NAMES = {
    ".env",
    ".env.local",
    "auth.json",
    ".anthropic_oauth.json",
    ".netrc",
}
EXCLUDED_SUFFIXES = {
    ".7z",
    ".a",
    ".bin",
    ".bmp",
    ".bz2",
    ".class",
    ".db",
    ".dmg",
    ".exe",
    ".gif",
    ".ico",
    ".jar",
    ".jpeg",
    ".jpg",
    ".lock",
    ".mov",
    ".mp3",
    ".mp4",
    ".o",
    ".pdf",
    ".png",
    ".pyc",
    ".sqlite",
    ".tar",
    ".tgz",
    ".webp",
    ".zip",
}
EXCLUDED_PARTS = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "node_modules",
    "venv",
    "__pycache__",
}


def check_scan_codebase_requirements() -> bool:
    """Local scan orchestration is always available.

    Live model calls reuse Hermes' configured provider/runtime path. The tool's
    own file-hash response cache keeps repeated scans cheap and deterministic.
    """
    return True


def _now_scan_id() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _safe_int(value: Any, default: int, *, minimum: int = 1, maximum: int = 256) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, min(maximum, parsed))


def _resolve_root(path: str | None) -> Path:
    base = Path(path or ".").expanduser().resolve()
    if base.is_file():
        base = base.parent
    try:
        proc = subprocess.run(
            ["git", "-C", str(base), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return Path(proc.stdout.strip()).resolve()
    except Exception:
        pass
    return base


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _resolve_output_path(root: Path, output: str | None) -> Path:
    raw = Path(output or DEFAULT_OUTPUT).expanduser()
    path = raw if raw.is_absolute() else root / raw
    path = path.resolve()
    if not _is_relative_to(path, root):
        raise ValueError(f"Output path must stay under scan root: {root}")
    return path


def _scan_base_dir(root: Path) -> Path:
    # tmp/ is already ignored in this repository, and avoids writing scan state
    # into the user's global ~/.hermes runtime directory.
    return root / "tmp" / "hermes-scans"


def _path_is_excluded(rel: str) -> bool:
    p = Path(rel)
    parts = set(p.parts)
    name = p.name.lower()
    suffix = p.suffix.lower()
    if len(p.parts) >= 2 and p.parts[0] == "tmp" and p.parts[1] == "hermes-scans":
        return True
    if parts & EXCLUDED_PARTS:
        return True
    if name in EXCLUDED_NAMES:
        return True
    if suffix in EXCLUDED_SUFFIXES:
        return True
    if "secret" in name or "private-key" in name or name.endswith("_key"):
        return True
    return False


def _fallback_file_list(root: Path) -> List[str]:
    files: List[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            rel = path.relative_to(root).as_posix()
        except ValueError:
            continue
        if not _path_is_excluded(rel):
            files.append(rel)
    return sorted(files)


def _list_repo_files(root: Path) -> List[str]:
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), "ls-files"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if proc.returncode == 0:
            files = [
                line.strip()
                for line in proc.stdout.splitlines()
                if line.strip() and not _path_is_excluded(line.strip())
            ]
            if files:
                return sorted(files)
    except Exception:
        pass
    return _fallback_file_list(root)


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _file_record(root: Path, rel: str) -> Optional[Dict[str, Any]]:
    path = root / rel
    try:
        stat = path.stat()
        if not path.is_file():
            return None
        return {
            "path": rel,
            "size": stat.st_size,
            "sha256": _sha256_file(path),
        }
    except (OSError, ValueError):
        return None


def _build_inventory(root: Path) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for rel in _list_repo_files(root):
        rec = _file_record(root, rel)
        if rec is not None:
            records.append(rec)
    return records


def _make_shards(files: List[Dict[str, Any]], workers: int) -> List[List[Dict[str, Any]]]:
    if not files:
        return []
    shard_count = max(1, min(workers, len(files)))
    shards: List[List[Dict[str, Any]]] = [[] for _ in range(shard_count)]
    sizes = [0 for _ in range(shard_count)]
    for rec in sorted(files, key=lambda item: int(item.get("size", 0)), reverse=True):
        idx = min(range(shard_count), key=lambda i: sizes[i])
        shards[idx].append(rec)
        sizes[idx] += int(rec.get("size", 0))
    return [sorted(shard, key=lambda item: item["path"]) for shard in shards]


def _read_file_excerpt(root: Path, rel: str, *, max_chars: int) -> tuple[str, bool]:
    path = root / rel
    try:
        data = path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        return f"[Could not read file: {type(exc).__name__}: {exc}]", False
    if len(data) > max_chars:
        return data[:max_chars] + "\n[...truncated...]\n", True
    return data, False


def _build_shard_prompt(
    *,
    root: Path,
    shard_index: int,
    total_shards: int,
    files: List[Dict[str, Any]],
    focus: str,
    max_chars_per_shard: int,
    max_chars_per_file: int,
) -> str:
    remaining = max_chars_per_shard
    parts = [
        "You are a codebase audit worker.",
        f"Repository root: {root}",
        f"Shard: {shard_index + 1}/{total_shards}",
        f"Focus: {focus or 'general correctness, broken behavior, security, tests'}",
        "",
        "Return concise findings only. For each finding include severity, concrete file path, line number if visible, why it matters, and a suggested fix.",
        "If no concrete issue is found, say so. Do not invent line numbers.",
        "",
        "Files in this shard:",
    ]
    for rec in files:
        parts.append(f"- {rec['path']} ({rec['size']} bytes, sha256={rec['sha256'][:12]})")
    parts.append("\n--- File excerpts ---")

    for rec in files:
        if remaining <= 0:
            parts.append("\n[Shard character budget exhausted; remaining files listed above only.]")
            break
        rel = rec["path"]
        excerpt, truncated = _read_file_excerpt(
            root,
            rel,
            max_chars=min(max_chars_per_file, remaining),
        )
        remaining -= len(excerpt)
        marker = " truncated" if truncated else ""
        parts.append(f"\n### {rel}{marker}\n```text\n{excerpt}\n```")

    return "\n".join(parts)


def _stable_cache_key(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def _append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(text)


def _resolve_model_runtime(
    *,
    provider: Optional[str],
    model: Optional[str],
    parent_agent: Any = None,
) -> Dict[str, Any]:
    if parent_agent is not None and not provider:
        parent_api_key = getattr(parent_agent, "api_key", None)
        if not parent_api_key and hasattr(parent_agent, "_client_kwargs"):
            try:
                parent_api_key = parent_agent._client_kwargs.get("api_key")
            except Exception:
                parent_api_key = None
        runtime = {
            "provider": getattr(parent_agent, "provider", None),
            "api_mode": getattr(parent_agent, "api_mode", None),
            "base_url": getattr(parent_agent, "base_url", None),
            "api_key": parent_api_key,
        }
        if model or getattr(parent_agent, "model", None):
            runtime["model"] = model or getattr(parent_agent, "model", None)
        if runtime.get("base_url") and runtime.get("api_key"):
            return runtime

    from hermes_cli.runtime_provider import resolve_runtime_provider
    from hermes_cli.config import load_config

    runtime = resolve_runtime_provider(requested=provider)
    if model:
        runtime["model"] = model
    else:
        cfg = load_config().get("model", {})
        if isinstance(cfg, dict):
            runtime["model"] = cfg.get("default") or cfg.get("model") or ""
    return runtime


def _extract_anthropic_text(response: Any) -> str:
    chunks: List[str] = []
    for block in getattr(response, "content", []) or []:
        text = getattr(block, "text", None)
        if text:
            chunks.append(str(text))
        elif isinstance(block, dict) and block.get("text"):
            chunks.append(str(block["text"]))
    return "\n".join(chunks).strip()


def _call_anthropic_messages(
    *,
    runtime: Dict[str, Any],
    prompt: str,
    max_tokens: int,
) -> tuple[str, bool, str]:
    from agent.anthropic_adapter import build_anthropic_client, build_anthropic_kwargs

    provider = (runtime.get("provider") or "").strip().lower()
    model = runtime.get("model") or "claude-sonnet-4-6"
    base_url = runtime.get("base_url") or ""
    api_key = runtime.get("api_key") or ""
    client = build_anthropic_client(api_key, base_url)
    kwargs = build_anthropic_kwargs(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        tools=None,
        max_tokens=max_tokens,
        reasoning_config=None,
        preserve_dots=provider in {"minimax", "minimax-cn"},
        base_url=base_url,
    )
    response = client.messages.create(**kwargs)
    return _extract_anthropic_text(response), False, "anthropic_messages"


def _call_hermes_auxiliary_chat(
    *,
    runtime: Dict[str, Any],
    prompt: str,
    max_tokens: int,
) -> tuple[str, bool, str]:
    from agent.auxiliary_client import call_llm, extract_content_or_reasoning

    provider = (runtime.get("provider") or "").strip() or None
    base_url = (runtime.get("base_url") or "").strip() or None
    api_key = (runtime.get("api_key") or "").strip() or None

    # If runtime resolution handed us a concrete endpoint/key pair, use that
    # direct route. Otherwise let the auxiliary router resolve the named
    # provider from config/env, with main_runtime available for auto mode.
    if base_url and api_key:
        provider_arg = None
        base_url_arg = base_url
        api_key_arg = api_key
    else:
        provider_arg = provider
        base_url_arg = None
        api_key_arg = None

    response = call_llm(
        task=None,
        provider=provider_arg,
        model=runtime.get("model") or None,
        base_url=base_url_arg,
        api_key=api_key_arg,
        main_runtime=runtime,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=max_tokens,
        timeout=180,
    )
    return extract_content_or_reasoning(response).strip(), False, "hermes_auxiliary_chat"


def _call_model(
    *,
    runtime: Dict[str, Any],
    prompt: str,
    max_tokens: int,
) -> tuple[str, bool, str]:
    api_mode = (runtime.get("api_mode") or "chat_completions").strip()
    if api_mode == "anthropic_messages":
        return _call_anthropic_messages(runtime=runtime, prompt=prompt, max_tokens=max_tokens)
    if api_mode not in {"chat_completions", "codex_responses"}:
        raise ValueError(
            "scan_codebase only supports chat_completions, codex_responses, "
            f"or anthropic_messages routes, got {api_mode}"
        )
    return _call_hermes_auxiliary_chat(
        runtime=runtime,
        prompt=prompt,
        max_tokens=max_tokens,
    )


def _dry_run_result(shard_index: int, files: List[Dict[str, Any]], focus: str) -> str:
    sample = ", ".join(rec["path"] for rec in files[:5])
    extra = "" if len(files) <= 5 else f", and {len(files) - 5} more"
    return (
        f"DRY RUN shard {shard_index + 1}: inspected {len(files)} files for "
        f"{focus or 'general issues'}. Files: {sample}{extra}. No model call made."
    )


def _analyze_shard(
    *,
    root: Path,
    shard_index: int,
    total_shards: int,
    files: List[Dict[str, Any]],
    focus: str,
    runtime: Dict[str, Any],
    mode: str,
    cache_dir: Path,
    spool_dir: Path,
    max_chars_per_shard: int,
    max_chars_per_file: int,
    max_output_tokens: int,
) -> Dict[str, Any]:
    started = time.monotonic()
    cache_payload = {
        "prompt_version": PROMPT_VERSION,
        "provider": runtime.get("provider"),
        "api_mode": runtime.get("api_mode"),
        "model": runtime.get("model"),
        "focus": focus,
        "max_chars_per_shard": max_chars_per_shard,
        "max_chars_per_file": max_chars_per_file,
        "files": files,
    }
    cache_key = _stable_cache_key(cache_payload)
    cache_path = cache_dir / f"{cache_key}.md"
    task_path = spool_dir / f"task-{shard_index + 1:02d}.md"
    backend = "cache"
    cached = False
    status = "completed"
    error = None

    try:
        if cache_path.exists():
            result = cache_path.read_text(encoding="utf-8")
            cached = True
        elif mode == "dry_run":
            result = _dry_run_result(shard_index, files, focus)
            backend = "dry_run"
            _write_text_atomic(cache_path, result)
        else:
            prompt = _build_shard_prompt(
                root=root,
                shard_index=shard_index,
                total_shards=total_shards,
                files=files,
                focus=focus,
                max_chars_per_shard=max_chars_per_shard,
                max_chars_per_file=max_chars_per_file,
            )
            result, provider_cached, backend = _call_model(
                runtime=runtime,
                prompt=prompt,
                max_tokens=max_output_tokens,
            )
            cached = provider_cached
            _write_text_atomic(cache_path, result)
    except Exception as exc:
        status = "error"
        error = f"{type(exc).__name__}: {exc}"
        result = f"ERROR shard {shard_index + 1}: {error}"

    duration = round(time.monotonic() - started, 2)
    body = [
        f"# Task {shard_index + 1:02d}",
        "",
        f"- status: {status}",
        f"- cached: {str(cached).lower()}",
        f"- backend: {backend}",
        f"- duration_seconds: {duration}",
        f"- files: {len(files)}",
        f"- cache_key: {cache_key}",
    ]
    if error:
        body.append(f"- error: {error}")
    body.extend(["", "## Findings", "", result.strip(), ""])
    _write_text_atomic(task_path, "\n".join(body))
    return {
        "task_index": shard_index,
        "status": status,
        "cached": cached,
        "backend": backend,
        "duration_seconds": duration,
        "files": len(files),
        "bytes": sum(int(rec.get("size", 0)) for rec in files),
        "cache_key": cache_key,
        "result_path": str(task_path),
        "error": error,
    }


def _render_report(
    *,
    scan_id: str,
    root: Path,
    focus: str,
    runtime: Dict[str, Any],
    workers_requested: int,
    active_workers: int,
    results: List[Dict[str, Any]],
    manifest_path: Path,
) -> str:
    status_counts: Dict[str, int] = {}
    backend_counts: Dict[str, int] = {}
    for result in results:
        status_counts[result["status"]] = status_counts.get(result["status"], 0) + 1
        backend_counts[result["backend"]] = backend_counts.get(result["backend"], 0) + 1

    lines = [
        "",
        "---",
        "",
        f"## Cached Chat Codebase Scan {scan_id}",
        "",
        f"- Repository: `{root}`",
        f"- Focus: {focus or 'general correctness'}",
        f"- Provider: `{runtime.get('provider')}`",
        f"- API mode: `{runtime.get('api_mode')}`",
        f"- Model: `{runtime.get('model')}`",
        f"- Logical workers requested: {workers_requested}",
        f"- Active workers used: {active_workers}",
        f"- Manifest: `{manifest_path}`",
        f"- Status counts: `{json.dumps(status_counts, sort_keys=True)}`",
        f"- Backend counts: `{json.dumps(backend_counts, sort_keys=True)}`",
        "",
        "### Worker Findings",
        "",
    ]
    for result in results:
        rel = Path(result["result_path"])
        try:
            rel_text = rel.relative_to(root).as_posix()
        except ValueError:
            rel_text = str(rel)
        lines.append(
            f"- Task {result['task_index'] + 1:02d}: "
            f"{result['status']}, backend={result['backend']}, "
            f"cached={result['cached']}, files={result['files']}, "
            f"path=`{rel_text}`"
        )
    lines.extend(["", "Detailed per-worker reports are spooled on disk and are intentionally not inlined here to avoid truncation.", ""])
    return "\n".join(lines)


def scan_codebase(
    path: Optional[str] = None,
    workers: Optional[int] = None,
    focus: Optional[str] = None,
    output: Optional[str] = None,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    mode: Optional[str] = None,
    active_workers: Optional[int] = None,
    max_chars_per_shard: Optional[int] = None,
    max_chars_per_file: Optional[int] = None,
    max_output_tokens: Optional[int] = None,
    parent_agent=None,
) -> str:
    """Run a cached chat map/reduce scan and spool per-worker outputs."""
    try:
        root = _resolve_root(path)
        output_path = _resolve_output_path(root, output)
        worker_count = _safe_int(workers, DEFAULT_WORKERS, minimum=1, maximum=128)
        active = _safe_int(active_workers, worker_count, minimum=1, maximum=worker_count)
        focus_text = (focus or "").strip()
        scan_mode = (mode or "auto").strip().lower()
        if scan_mode == "auto":
            scan_mode = "chat"
        if scan_mode not in {"chat", "dry_run"}:
            return tool_error("mode must be 'auto', 'chat', or 'dry_run'")

        max_shard_chars = _safe_int(
            max_chars_per_shard,
            DEFAULT_MAX_CHARS_PER_SHARD,
            minimum=8_000,
            maximum=300_000,
        )
        max_file_chars = _safe_int(
            max_chars_per_file,
            DEFAULT_MAX_CHARS_PER_FILE,
            minimum=1_000,
            maximum=80_000,
        )
        max_tokens = _safe_int(max_output_tokens, 2500, minimum=256, maximum=16_000)

        inventory = _build_inventory(root)
        if not inventory:
            return tool_error(f"No scannable files found under {root}")

        shards = _make_shards(inventory, worker_count)
        scan_id = _now_scan_id()
        base_dir = _scan_base_dir(root)
        spool_dir = base_dir / scan_id
        cache_dir = base_dir / "cache"
        for directory in (spool_dir, cache_dir):
            directory.mkdir(parents=True, exist_ok=True)

        runtime = _resolve_model_runtime(provider=provider, model=model, parent_agent=parent_agent)
        if not runtime.get("model") and model:
            runtime["model"] = model

        results: List[Dict[str, Any]] = []
        with ThreadPoolExecutor(max_workers=min(active, len(shards))) as executor:
            futures = [
                executor.submit(
                    _analyze_shard,
                    root=root,
                    shard_index=i,
                    total_shards=len(shards),
                    files=shard,
                    focus=focus_text,
                    runtime=runtime,
                    mode=scan_mode,
                    cache_dir=cache_dir,
                    spool_dir=spool_dir,
                    max_chars_per_shard=max_shard_chars,
                    max_chars_per_file=max_file_chars,
                    max_output_tokens=max_tokens,
                )
                for i, shard in enumerate(shards)
            ]
            for future in as_completed(futures):
                results.append(future.result())
        results.sort(key=lambda item: item["task_index"])

        manifest = {
            "scan_id": scan_id,
            "root": str(root),
            "focus": focus_text,
            "output_path": str(output_path),
            "workers_requested": worker_count,
            "workers_actual": len(shards),
            "active_workers": min(active, len(shards)),
            "mode": scan_mode,
            "provider": runtime.get("provider"),
            "api_mode": runtime.get("api_mode"),
            "model": runtime.get("model"),
            "inventory_files": len(inventory),
            "inventory_bytes": sum(int(rec.get("size", 0)) for rec in inventory),
            "results": results,
        }
        manifest_path = spool_dir / "manifest.json"
        _write_text_atomic(manifest_path, json.dumps(manifest, indent=2, sort_keys=True))

        report = _render_report(
            scan_id=scan_id,
            root=root,
            focus=focus_text,
            runtime=runtime,
            workers_requested=worker_count,
            active_workers=min(active, len(shards)),
            results=results,
            manifest_path=manifest_path,
        )
        _append_text(output_path, report)

        status_counts: Dict[str, int] = {}
        backend_counts: Dict[str, int] = {}
        for result in results:
            status_counts[result["status"]] = status_counts.get(result["status"], 0) + 1
            backend_counts[result["backend"]] = backend_counts.get(result["backend"], 0) + 1
        return json.dumps({
            "ok": True,
            "scan_id": scan_id,
            "root": str(root),
            "output_path": str(output_path),
            "manifest_path": str(manifest_path),
            "workers_requested": worker_count,
            "workers_actual": len(shards),
            "active_workers": min(active, len(shards)),
            "status_counts": status_counts,
            "backend_counts": backend_counts,
            "results": [
                {
                    "task_index": r["task_index"],
                    "status": r["status"],
                    "cached": r["cached"],
                    "backend": r["backend"],
                    "result_path": r["result_path"],
                    "error": r["error"],
                }
                for r in results
            ],
        }, ensure_ascii=False)
    except Exception as exc:
        return tool_error(f"scan_codebase failed: {type(exc).__name__}: {exc}")


SCAN_CODEBASE_SCHEMA = {
    "name": "scan_codebase",
    "description": (
        "Scan a local codebase with N logical cached-chat workers. The tool "
        "indexes files locally, excludes credential-like files, caches shard "
        "analysis by file hashes, writes each worker report to disk, appends a "
        "compact final report to an output file, and returns a compact manifest. "
        "Use this before delegate_task for broad codebase audits."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Repository or folder path to scan. Defaults to current directory."},
            "workers": {"type": "integer", "description": "Number of logical scan workers/shards. Defaults to 8."},
            "focus": {"type": "string", "description": "Audit focus, e.g. memory architecture, auth, broken behavior."},
            "output": {"type": "string", "description": "Output markdown file under the repo root. Defaults to problems.md."},
            "provider": {"type": "string", "description": "Optional provider override, e.g. minimax, openrouter, custom:local."},
            "model": {"type": "string", "description": "Optional model override."},
            "mode": {"type": "string", "enum": ["auto", "chat", "dry_run"], "description": "auto/chat performs model calls; dry_run indexes, caches, and spools without network."},
            "active_workers": {"type": "integer", "description": "Maximum shard analyses active at once. Defaults to workers."},
            "max_chars_per_shard": {"type": "integer", "description": "Maximum prompt characters per shard."},
            "max_chars_per_file": {"type": "integer", "description": "Maximum characters included per file excerpt."},
            "max_output_tokens": {"type": "integer", "description": "Model output token cap per shard."},
        },
        "required": [],
    },
}


registry.register(
    name="scan_codebase",
    toolset="code_scan",
    schema=SCAN_CODEBASE_SCHEMA,
    handler=lambda args, **kw: scan_codebase(
        path=args.get("path"),
        workers=args.get("workers"),
        focus=args.get("focus"),
        output=args.get("output"),
        provider=args.get("provider"),
        model=args.get("model"),
        mode=args.get("mode"),
        active_workers=args.get("active_workers"),
        max_chars_per_shard=args.get("max_chars_per_shard"),
        max_chars_per_file=args.get("max_chars_per_file"),
        max_output_tokens=args.get("max_output_tokens"),
        parent_agent=kw.get("parent_agent"),
    ),
    check_fn=check_scan_codebase_requirements,
    emoji="🔎",
    max_result_size_chars=24_000,
)
