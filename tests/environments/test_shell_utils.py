import shlex
import subprocess
import sys


def test_quote_shell_path_matches_shlex_quote():
    from environments.shell_utils import quote_shell_path

    path = "~/tmp; echo hacked $(whoami)"
    assert quote_shell_path(path) == shlex.quote(path)


def test_build_python_script_command_treats_shell_metacharacters_as_literal(tmp_path):
    from environments.shell_utils import build_python_script_command

    injected = tmp_path / "pwned"
    injected_tick = tmp_path / "pwned_tick"
    script_path = tmp_path / "payload.py"
    script = (
        f'print("$(touch {injected})")\n'
        f'print("`touch {injected_tick}`")\n'
    )

    command = build_python_script_command(
        script,
        script_path=str(script_path),
        cwd=str(tmp_path),
        python_executable=sys.executable,
    )
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )

    assert result.returncode == 0
    assert "$(touch" in result.stdout
    assert "`touch" in result.stdout
    assert script_path.exists()
    assert not injected.exists()
    assert not injected_tick.exists()
