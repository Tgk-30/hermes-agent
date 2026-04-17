"""Regression tests for batch_runner tool-result classification."""

import sys
from pathlib import Path

# batch_runner uses relative imports, ensure project root is on path
sys.path.insert(0, str(Path(__file__).parent.parent))

from batch_runner import _extract_tool_stats


def _tool_messages(content: str):
    return [
        {
            "role": "assistant",
            "tool_calls": [{"id": "call-1", "function": {"name": "terminal"}}],
        },
        {"role": "tool", "tool_call_id": "call-1", "content": content},
    ]


def test_extract_tool_stats_flags_bracketed_error_prefixes():
    stats = _extract_tool_stats(_tool_messages("[ERROR] command failed"))

    assert stats["terminal"]["failure"] == 1
    assert stats["terminal"]["success"] == 0


def test_extract_tool_stats_flags_error_prefix_without_colon():
    stats = _extract_tool_stats(_tool_messages("Error command failed"))

    assert stats["terminal"]["failure"] == 1
    assert stats["terminal"]["success"] == 0


def test_extract_tool_stats_keeps_non_prefix_mentions_as_success():
    stats = _extract_tool_stats(_tool_messages("No error: recovered automatically"))

    assert stats["terminal"]["success"] == 1
    assert stats["terminal"]["failure"] == 0
