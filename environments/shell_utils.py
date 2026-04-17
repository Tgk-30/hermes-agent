"""Helpers for safely constructing shell commands in RL/test environments."""

from __future__ import annotations

import base64
import shlex
from pathlib import Path


def quote_shell_path(path: str | Path) -> str:
    """Shell-quote a filesystem path or other literal argument."""
    return shlex.quote(str(path))


def build_python_script_command(
    script_text: str,
    *,
    script_path: str | Path = "/tmp/hermes_env_script.py",
    cwd: str | Path | None = None,
    python_executable: str = "python3",
) -> str:
    """Build a shell-safe command that writes and executes Python source.

    The script body is base64-encoded before being embedded in the shell command
    so quotes, backticks, ``$()`` and similar shell metacharacters are treated as
    literal script text instead of being interpolated by the shell.
    """
    encoded = base64.b64encode(script_text.encode("utf-8")).decode("ascii")
    script_path_str = str(script_path)
    writer = (
        "import base64, pathlib; "
        f"path = pathlib.Path({script_path_str!r}); "
        "path.parent.mkdir(parents=True, exist_ok=True); "
        f"path.write_bytes(base64.b64decode({encoded!r}))"
    )
    command = (
        f"{shlex.quote(str(python_executable))} -c {shlex.quote(writer)}"
        f" && {shlex.quote(str(python_executable))} {quote_shell_path(script_path_str)}"
    )
    if cwd is not None:
        return f"cd {quote_shell_path(cwd)} && {command}"
    return command
