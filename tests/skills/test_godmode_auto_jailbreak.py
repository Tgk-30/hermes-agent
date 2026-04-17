from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[2]
    / "skills"
    / "red-teaming"
    / "godmode"
    / "scripts"
    / "auto_jailbreak.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("godmode_auto_jailbreak", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_claude_4_models_deprioritize_boundary_inversion() -> None:
    mod = load_module()

    config = mod._strategy_config_for_model("anthropic/claude-sonnet-4-20250514")

    assert config["order"][:3] == ["refusal_inversion", "prefill_only", "parseltongue"]
    assert config["order"][-1] == "boundary_inversion"


def test_legacy_claude_models_keep_boundary_inversion_first() -> None:
    mod = load_module()

    config = mod._strategy_config_for_model("anthropic/claude-3.5-sonnet")

    assert config["order"][0] == "boundary_inversion"
