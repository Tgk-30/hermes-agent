from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


def test_rl_cli_import_loads_hermes_home_before_using_it(monkeypatch, tmp_path):
    hermes_home = tmp_path / ".hermes"
    hermes_home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))

    load_calls: list[tuple[Path, Path]] = []

    fake_env_loader = types.ModuleType("hermes_cli.env_loader")

    def fake_load_hermes_dotenv(*, hermes_home: Path, project_env: Path):
        load_calls.append((hermes_home, project_env))
        return []

    fake_env_loader.load_hermes_dotenv = fake_load_hermes_dotenv
    monkeypatch.setitem(sys.modules, "hermes_cli.env_loader", fake_env_loader)
    monkeypatch.setitem(sys.modules, "fire", types.SimpleNamespace(Fire=lambda *a, **k: None))

    fake_run_agent = types.ModuleType("run_agent")
    fake_run_agent.AIAgent = object
    monkeypatch.setitem(sys.modules, "run_agent", fake_run_agent)

    fake_rl_training_tool = types.ModuleType("tools.rl_training_tool")
    fake_rl_training_tool.get_missing_keys = lambda: []
    monkeypatch.setitem(sys.modules, "tools.rl_training_tool", fake_rl_training_tool)

    sys.modules.pop("rl_cli", None)
    module = importlib.import_module("rl_cli")

    assert module._hermes_home == hermes_home
    assert load_calls == [(hermes_home, REPO_ROOT / ".env")]
