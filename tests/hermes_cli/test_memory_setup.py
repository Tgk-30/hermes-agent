from types import SimpleNamespace

import pytest


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("HERMES_HOME", str(tmp_path))
    return tmp_path


def test_cmd_status_reads_localhybrid_native_config(_isolate, capsys, monkeypatch):
    from hermes_cli.config import save_config
    from hermes_cli.memory_setup import cmd_status
    from plugins.memory.localhybrid import _save_localhybrid_config, LocalHybridMemoryProvider
    import hermes_cli.memory_setup as memory_setup

    save_config(
        {
            "memory": {
                "provider": "localhybrid",
                "localhybrid": {
                    "auto_recall": True,
                    "max_prefetch_results": 99,
                    "embedding_provider": "stale-config",
                },
            }
        }
    )
    _save_localhybrid_config(
        {
            "auto_recall": False,
            "max_prefetch_results": 3,
            "embedding_provider": "google",
        },
        str(_isolate),
    )

    provider = LocalHybridMemoryProvider()
    monkeypatch.setattr(
        memory_setup,
        "_get_available_providers",
        lambda: [("localhybrid", "Local SQLite hybrid memory", provider)],
    )

    cmd_status(SimpleNamespace())
    out = capsys.readouterr().out

    assert "Provider:  localhybrid" in out
    assert "auto_recall: False" in out
    assert "max_prefetch_results: 3" in out
    assert "embedding_provider: google" in out
    assert "max_prefetch_results: 99" not in out
