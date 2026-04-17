import sys
from types import SimpleNamespace
from unittest.mock import patch


def _fake_run_agent_module(final_response: str):
    class FakeAgent:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def run_conversation(self, prompt: str):
            return {"final_response": final_response}

    return SimpleNamespace(AIAgent=FakeAgent)


def test_run_boot_agent_only_treats_exact_silent_marker_as_silent():
    from gateway.builtin_hooks import boot_md

    fake_module = _fake_run_agent_module("Status mention: [SILENT] should not suppress logs")

    with patch.dict(sys.modules, {"run_agent": fake_module}), patch.object(boot_md.logger, "info") as info_mock:
        boot_md._run_boot_agent("check status")

    assert any("boot-md completed:" in call.args[0] for call in info_mock.call_args_list)


def test_run_boot_agent_still_suppresses_exact_silent_marker():
    from gateway.builtin_hooks import boot_md

    fake_module = _fake_run_agent_module("  [SILENT]\n")

    with patch.dict(sys.modules, {"run_agent": fake_module}), patch.object(boot_md.logger, "info") as info_mock:
        boot_md._run_boot_agent("check status")

    assert any("nothing to report" in call.args[0] for call in info_mock.call_args_list)
