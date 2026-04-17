import subprocess
from pathlib import Path
from unittest.mock import MagicMock

import hermes_cli.memory_setup as memory_setup


def _write_fake_plugin(monkeypatch, tmp_path: Path, provider_name: str, manifest: str) -> Path:
    repo_root = tmp_path / "repo"
    fake_module = repo_root / "hermes_cli" / "memory_setup.py"
    fake_module.parent.mkdir(parents=True, exist_ok=True)
    fake_module.write_text("# fake memory_setup module path\n", encoding="utf-8")

    plugin_dir = repo_root / "plugins" / "memory" / provider_name
    plugin_dir.mkdir(parents=True, exist_ok=True)
    (plugin_dir / "plugin.yaml").write_text(manifest, encoding="utf-8")

    monkeypatch.setattr(memory_setup, "__file__", str(fake_module))
    return plugin_dir


def test_load_plugin_manifest_reports_parse_errors(tmp_path, capsys):
    yaml_path = tmp_path / "plugin.yaml"
    yaml_path.write_text("pip_dependencies: [broken\n", encoding="utf-8")

    manifest = memory_setup._load_plugin_manifest(yaml_path, "demo")
    out = capsys.readouterr().out

    assert manifest is None
    assert "Failed to parse plugin.yaml" in out
    assert "demo" in out


def test_check_external_dependency_avoids_shell(monkeypatch, capsys):
    calls = []

    def fake_run(*args, **kwargs):
        calls.append((args, kwargs))
        raise FileNotFoundError

    monkeypatch.setattr(subprocess, "run", fake_run)

    memory_setup._check_external_dependency("ByteRover CLI", "brv --version", "brew install brv")
    out = capsys.readouterr().out

    assert calls[0][0][0] == ["brv", "--version"]
    assert "shell" not in calls[0][1]
    assert "ByteRover CLI" in out
    assert "brew install brv" in out


def test_check_external_dependency_reports_timeout_distinctly(monkeypatch, capsys):
    def fake_run(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd=["brv", "--version"], timeout=5)

    monkeypatch.setattr(subprocess, "run", fake_run)

    memory_setup._check_external_dependency("ByteRover CLI", "brv --version", "brew install brv")
    out = capsys.readouterr().out

    assert "timed out after 5s" in out
    assert "not found" not in out.lower()


def test_install_dependencies_still_checks_external_only_manifests(monkeypatch, tmp_path):
    _write_fake_plugin(
        monkeypatch,
        tmp_path,
        "external-only",
        """
external_dependencies:
  - name: ByteRover CLI
    check: brv --version
    install: brew install brv
""".strip()
        + "\n",
    )

    probe = MagicMock()
    monkeypatch.setattr(memory_setup, "_check_external_dependency", probe)

    memory_setup._install_dependencies("external-only")

    probe.assert_called_once_with("ByteRover CLI", "brv --version", "brew install brv")
