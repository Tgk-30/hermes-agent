"""Compatibility BuiltinMemoryProvider.

Hermes still injects built-in MEMORY.md/USER.md directly via MemoryStore in
run_agent.py, but parts of the memory plugin interface and test suite expect a
builtin provider class to exist. This lightweight adapter keeps that contract
stable while the built-in file-backed memory remains on the direct path.
"""

from __future__ import annotations

from typing import Any, Dict, List

from agent.memory_provider import MemoryProvider


class BuiltinMemoryProvider(MemoryProvider):
    """Minimal builtin provider shim for MemoryManager compatibility."""

    def __init__(self) -> None:
        self._session_id = ""
        self._init_kwargs: Dict[str, Any] = {}

    @property
    def name(self) -> str:
        return "builtin"

    def is_available(self) -> bool:
        return True

    def initialize(self, session_id: str, **kwargs) -> None:
        self._session_id = session_id
        self._init_kwargs = dict(kwargs)

    def system_prompt_block(self) -> str:
        # Built-in file memory is still injected directly by run_agent.py.
        return ""

    def prefetch(self, query: str, *, session_id: str = "") -> str:
        return ""

    def queue_prefetch(self, query: str, *, session_id: str = "") -> None:
        return None

    def sync_turn(self, user_content: str, assistant_content: str, *, session_id: str = "") -> None:
        return None

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        return []

    def handle_tool_call(self, tool_name: str, args: Dict[str, Any], **kwargs) -> str:
        raise NotImplementedError("BuiltinMemoryProvider does not expose tools via MemoryManager yet")

    def shutdown(self) -> None:
        return None
