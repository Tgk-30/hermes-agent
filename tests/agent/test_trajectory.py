"""Tests for agent.trajectory helpers."""

import json
from pathlib import Path

from agent.trajectory import has_incomplete_scratchpad, save_trajectory


def test_has_incomplete_scratchpad_counts_tags():
    assert not has_incomplete_scratchpad("")
    assert not has_incomplete_scratchpad("plain text")
    assert has_incomplete_scratchpad("<REASONING_SCRATCHPAD>open only")
    assert not has_incomplete_scratchpad(
        "<REASONING_SCRATCHPAD>balanced</REASONING_SCRATCHPAD>"
    )
    assert has_incomplete_scratchpad(
        "<REASONING_SCRATCHPAD>outer <REASONING_SCRATCHPAD>nested"
    )


def test_save_trajectory_falls_back_to_temp_dir(monkeypatch, tmp_path):
    payload = [{"role": "user", "content": "hello"}]
    primary = tmp_path / "missing" / "trajectory.jsonl"

    monkeypatch.setattr("agent.trajectory.tempfile.gettempdir", lambda: str(tmp_path))

    save_trajectory(payload, "demo-model", True, filename=str(primary))

    fallback_root = tmp_path / "hermes-trajectories"
    matches = list(fallback_root.glob("*/trajectory.jsonl"))
    assert len(matches) == 1
    fallback = matches[0]
    assert fallback.exists()

    saved = [json.loads(line) for line in fallback.read_text().splitlines() if line]
    assert len(saved) == 1
    assert saved[0]["conversations"] == payload
    assert saved[0]["model"] == "demo-model"
    assert saved[0]["completed"] is True


def test_save_trajectory_fallback_uses_unique_source_path(monkeypatch, tmp_path):
    payload = [{"role": "user", "content": "hello"}]
    primary_a = tmp_path / "missing-a" / "trajectory.jsonl"
    primary_b = tmp_path / "missing-b" / "trajectory.jsonl"

    monkeypatch.setattr("agent.trajectory.tempfile.gettempdir", lambda: str(tmp_path))

    save_trajectory(payload, "demo-model", True, filename=str(primary_a))
    save_trajectory(payload, "demo-model", True, filename=str(primary_b))

    matches = sorted(Path(tmp_path, "hermes-trajectories").glob("*/trajectory.jsonl"))
    assert len(matches) == 2
    assert len({match.parent.name for match in matches}) == 2
