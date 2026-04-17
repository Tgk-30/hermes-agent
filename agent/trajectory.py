"""Trajectory saving utilities and static helpers.

_convert_to_trajectory_format stays as an AIAgent method (batch_runner.py
calls agent._convert_to_trajectory_format). Only the static helpers and
the file-write logic live here.
"""

import hashlib
import json
import logging
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def convert_scratchpad_to_think(content: str) -> str:
    """Convert <REASONING_SCRATCHPAD> tags to <think> tags."""
    if not content or "<REASONING_SCRATCHPAD>" not in content:
        return content
    return content.replace("<REASONING_SCRATCHPAD>", "<think>").replace("</REASONING_SCRATCHPAD>", "</think>")


def has_incomplete_scratchpad(content: str) -> bool:
    """Check if content has an opening <REASONING_SCRATCHPAD> without a closing tag."""
    if not content:
        return False
    return content.count("<REASONING_SCRATCHPAD>") > content.count("</REASONING_SCRATCHPAD>")


def _append_trajectory_entry(filename: str | Path, entry: Dict[str, Any]) -> None:
    """Append one JSONL entry to the requested file."""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def save_trajectory(trajectory: List[Dict[str, Any]], model: str,
                    completed: bool, filename: str = None):
    """Append a trajectory entry to a JSONL file.

    Args:
        trajectory: The ShareGPT-format conversation list.
        model: Model name for metadata.
        completed: Whether the conversation completed successfully.
        filename: Override output filename. Defaults to trajectory_samples.jsonl
                  or failed_trajectories.jsonl based on ``completed``.
    """
    if filename is None:
        filename = "trajectory_samples.jsonl" if completed else "failed_trajectories.jsonl"

    entry = {
        "conversations": trajectory,
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "completed": completed,
    }

    try:
        _append_trajectory_entry(filename, entry)
        logger.info("Trajectory saved to %s", filename)
    except Exception as e:
        primary = Path(filename).expanduser()
        fallback_key = hashlib.sha256(str(primary).encode("utf-8")).hexdigest()[:16]
        fallback = Path(tempfile.gettempdir()) / "hermes-trajectories" / fallback_key / primary.name
        logger.error("Failed to save trajectory to %s, retrying in %s: %s", filename, fallback, e)
        try:
            fallback.parent.mkdir(parents=True, exist_ok=True)
            _append_trajectory_entry(fallback, entry)
            logger.info("Trajectory saved to fallback %s", fallback)
        except Exception as fallback_error:
            logger.error("Failed to save trajectory to fallback %s: %s", fallback, fallback_error)
