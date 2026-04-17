import json
import subprocess
from pathlib import Path

import tools.codebase_scan_tool as scan_mod
from tools.codebase_scan_tool import (
    _build_inventory,
    _path_is_excluded,
    scan_codebase,
)
from tools.registry import registry
from toolsets import resolve_toolset


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _init_git_repo(root: Path, files: dict[str, str]) -> None:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    for rel, text in files.items():
        _write(root, rel, text)
    subprocess.run(["git", "add", "."], cwd=root, check=True)


def _runtime() -> dict[str, str]:
    return {
        "provider": "test-provider",
        "api_mode": "chat_completions",
        "base_url": "",
        "api_key": "",
        "model": "test-model",
    }


def test_dry_run_spools_manifest_and_appends_report(tmp_path):
    _init_git_repo(
        tmp_path,
        {
            "src/app.py": "def run():\n    return 1\n",
            "src/memory.py": "class Memory:\n    pass\n",
            "README.md": "# test\n",
        },
    )

    result = json.loads(
        scan_codebase(
            path=str(tmp_path),
            workers=2,
            active_workers=2,
            focus="memory architecture",
            output="problems.md",
            mode="dry_run",
        )
    )

    assert result["ok"] is True
    assert result["workers_requested"] == 2
    assert result["workers_actual"] == 2
    assert result["active_workers"] == 2
    assert result["status_counts"] == {"completed": 2}
    assert result["backend_counts"] == {"dry_run": 2}

    manifest_path = Path(result["manifest_path"])
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["focus"] == "memory architecture"
    assert manifest["inventory_files"] == 3

    for item in result["results"]:
        task_path = Path(item["result_path"])
        assert task_path.exists()
        assert "DRY RUN shard" in task_path.read_text(encoding="utf-8")

    report = (tmp_path / "problems.md").read_text(encoding="utf-8")
    assert "Cached Chat Codebase Scan" in report
    assert "Detailed per-worker reports are spooled on disk" in report


def test_chat_mode_reuses_file_hash_cache_without_model_call(tmp_path, monkeypatch):
    _init_git_repo(tmp_path, {"src/app.py": "def run():\n    return 1\n"})
    scan_ids = iter(["scan-a", "scan-b"])
    calls = []

    monkeypatch.setattr(scan_mod, "_now_scan_id", lambda: next(scan_ids))
    monkeypatch.setattr(scan_mod, "_resolve_model_runtime", lambda **_: _runtime())

    def fake_call_model(*, runtime, prompt, max_tokens):
        calls.append(prompt)
        return "candidate finding", False, "fake_model"

    monkeypatch.setattr(scan_mod, "_call_model", fake_call_model)
    first = json.loads(
        scan_codebase(
            path=str(tmp_path),
            workers=1,
            output="problems.md",
            mode="chat",
        )
    )
    assert first["backend_counts"] == {"fake_model": 1}
    assert len(calls) == 1

    def fail_call_model(**kwargs):
        raise AssertionError("cache hit should avoid model call")

    monkeypatch.setattr(scan_mod, "_call_model", fail_call_model)
    second = json.loads(
        scan_codebase(
            path=str(tmp_path),
            workers=1,
            output="problems.md",
            mode="chat",
        )
    )
    assert second["backend_counts"] == {"cache": 1}
    assert second["results"][0]["cached"] is True


def test_cache_key_changes_when_tracked_file_changes(tmp_path, monkeypatch):
    _init_git_repo(tmp_path, {"src/app.py": "VALUE = 1\n"})
    scan_ids = iter(["scan-a", "scan-b"])
    calls = []

    monkeypatch.setattr(scan_mod, "_now_scan_id", lambda: next(scan_ids))
    monkeypatch.setattr(scan_mod, "_resolve_model_runtime", lambda **_: _runtime())

    def fake_call_model(*, runtime, prompt, max_tokens):
        calls.append(prompt)
        return f"call {len(calls)}", False, "fake_model"

    monkeypatch.setattr(scan_mod, "_call_model", fake_call_model)

    first = json.loads(scan_codebase(path=str(tmp_path), workers=1, mode="chat"))
    assert first["backend_counts"] == {"fake_model": 1}

    _write(tmp_path, "src/app.py", "VALUE = 2\n")

    second = json.loads(scan_codebase(path=str(tmp_path), workers=1, mode="chat"))
    assert second["backend_counts"] == {"fake_model": 1}
    assert len(calls) == 2


def test_inventory_excludes_credentials_and_scan_state(tmp_path):
    _init_git_repo(
        tmp_path,
        {
            "src/app.py": "print('ok')\n",
            "auth.json": '{"token": "secret"}\n',
            "keys/private-key.pem": "secret\n",
            "tmp/hermes-scans/cache/old.md": "old scan output\n",
        },
    )

    paths = {rec["path"] for rec in _build_inventory(tmp_path)}
    assert "src/app.py" in paths
    assert "auth.json" not in paths
    assert "keys/private-key.pem" not in paths
    assert "tmp/hermes-scans/cache/old.md" not in paths
    assert _path_is_excluded("tmp/hermes-scans/scan/task-01.md")


def test_output_path_must_stay_under_scan_root(tmp_path):
    _init_git_repo(tmp_path, {"src/app.py": "print('ok')\n"})

    result = json.loads(
        scan_codebase(
            path=str(tmp_path),
            output="../outside.md",
            mode="dry_run",
        )
    )

    assert "error" in result
    assert "Output path must stay under scan root" in result["error"]


def test_chat_model_route_uses_hermes_auxiliary_client(monkeypatch):
    calls = {}

    def fake_call_llm(**kwargs):
        calls.update(kwargs)
        return object()

    monkeypatch.setattr("agent.auxiliary_client.call_llm", fake_call_llm)
    monkeypatch.setattr(
        "agent.auxiliary_client.extract_content_or_reasoning",
        lambda response: "model output",
    )

    text, cached, backend = scan_mod._call_model(
        runtime={
            "provider": "openrouter",
            "api_mode": "chat_completions",
            "base_url": "https://example.test/v1",
            "api_key": "test-key",
            "model": "test-model",
        },
        prompt="scan this shard",
        max_tokens=321,
    )

    assert text == "model output"
    assert cached is False
    assert backend == "hermes_auxiliary_chat"
    assert calls["base_url"] == "https://example.test/v1"
    assert calls["api_key"] == "test-key"
    assert calls["provider"] is None
    assert calls["model"] == "test-model"
    assert calls["max_tokens"] == 321
    assert calls["main_runtime"]["provider"] == "openrouter"


def test_scan_codebase_is_registered_and_available_in_toolsets():
    entry = registry.get_entry("scan_codebase")
    assert entry is not None
    assert entry.toolset == "code_scan"
    assert "scan_codebase" in resolve_toolset("code_scan")
    assert "scan_codebase" in resolve_toolset("hermes-cli")
    assert "scan_codebase" in resolve_toolset("hermes-api-server")
