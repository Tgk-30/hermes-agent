import re
import threading
import time

import pytest

from plugins.memory.localhybrid import LocalHybridMemoryProvider


KEYWORDS = [
    "brendan",
    "concise",
    "pairing",
    "pipeline",
    "research",
    "theorem",
    "memory",
    "compaction",
    "workspace",
    "agent",
]


def fake_request_embedding(self, text: str, *, task_type: str):
    text_lc = text.lower()
    return [1.0 if kw in text_lc else 0.0 for kw in KEYWORDS]


@pytest.fixture
def provider_factory(monkeypatch, tmp_path):
    providers = []

    def _make(
        *,
        agent_identity: str = "main",
        user_id: str = "discord-user",
        platform: str = "discord",
        workspace: str = "workspace-main",
        session_id: str = "session-1",
    ):
        p = LocalHybridMemoryProvider()
        p.initialize(
            session_id,
            hermes_home=str(tmp_path),
            platform=platform,
            user_id=user_id,
            agent_identity=agent_identity,
            agent_workspace=workspace,
        )
        providers.append(p)
        return p

    yield _make

    for provider in providers:
        provider.shutdown()


def _wait(provider: LocalHybridMemoryProvider):
    provider._write_queue.join()
    time.sleep(0.02)


def test_lexical_recall_without_embeddings(monkeypatch, provider_factory):
    monkeypatch.delenv("GEMINI_EMBEDDINGS_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    provider = provider_factory()
    provider.on_memory_write("add", "user", "Brendan prefers short direct answers.")
    _wait(provider)

    recalled = provider.prefetch("short direct answers")
    assert "Brendan prefers short direct answers" in recalled
    assert "User-global memory" in recalled


def test_system_prompt_explains_explicit_memory_lane_semantics():
    provider = LocalHybridMemoryProvider()

    prompt = provider.system_prompt_block().lower()

    assert "target='memory'" in prompt
    assert "memory.md" in prompt
    assert "agent-private lane" in prompt
    assert "target='user'" in prompt
    assert "user-global lane" in prompt
    assert "shared recall" not in prompt


def test_agent_private_isolation_but_user_global_shares(monkeypatch, provider_factory):
    monkeypatch.setenv("GEMINI_EMBEDDINGS_API_KEY", "test-key")
    monkeypatch.setattr(LocalHybridMemoryProvider, "_request_embedding", fake_request_embedding)

    main = provider_factory(agent_identity="main")
    research = provider_factory(agent_identity="research")

    main.sync_turn(
        "Please remember the pairing pipeline fix for the main agent.",
        "Stored the pairing pipeline fix for the main agent.",
    )
    _wait(main)

    leaked = research.prefetch("pairing pipeline fix")
    assert "pairing pipeline fix" not in leaked.lower()

    main.on_memory_write("add", "user", "Brendan likes concise answers.")
    _wait(main)

    shared = research.prefetch("concise answers")
    assert "Brendan likes concise answers" in shared


def test_compaction_checkpoint_survives_session_rollover(monkeypatch, provider_factory):
    monkeypatch.setenv("GEMINI_EMBEDDINGS_API_KEY", "test-key")
    monkeypatch.setattr(LocalHybridMemoryProvider, "_request_embedding", fake_request_embedding)

    provider = provider_factory(agent_identity="main")
    provider.on_pre_compress(
        [
            {"role": "user", "content": "Need the new memory system to survive compaction cleanly."},
            {"role": "assistant", "content": "I am replacing it with a local hybrid memory provider."},
            {"role": "user", "content": "Also keep agent isolation strong."},
        ]
    )
    provider._session_id = "session-2"

    recalled = provider.prefetch("survive compaction isolation")
    assert "Compaction checkpoint" in recalled
    assert "survive compaction" in recalled.lower()


def test_stress_recall_keeps_agents_isolated(monkeypatch, provider_factory):
    monkeypatch.setenv("GEMINI_EMBEDDINGS_API_KEY", "test-key")
    monkeypatch.setattr(LocalHybridMemoryProvider, "_request_embedding", fake_request_embedding)

    main = provider_factory(agent_identity="main")
    research = provider_factory(agent_identity="research")

    for idx in range(80):
        main.sync_turn(
            f"Main agent pairing pipeline memory item {idx} for Brendan.",
            "Stored under the main agent lane.",
        )
        research.sync_turn(
            f"Research agent theorem search memory item {idx} for Brendan.",
            "Stored under the research agent lane.",
        )

    _wait(main)
    _wait(research)

    main_recall = main.prefetch("pairing pipeline")
    research_recall = research.prefetch("theorem search")

    assert "pairing pipeline" in main_recall.lower()
    assert "theorem search" not in main_recall.lower()
    assert "theorem search" in research_recall.lower()
    assert "pairing pipeline" not in research_recall.lower()


def test_explicit_memory_target_stays_agent_private(monkeypatch, provider_factory):
    monkeypatch.delenv("GEMINI_EMBEDDINGS_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    main = provider_factory(agent_identity="main")
    research = provider_factory(agent_identity="research")

    main.on_memory_write("add", "memory", "Main agent keeps the Discord repair checklist.")
    _wait(main)

    main_recall = main.prefetch("discord repair checklist")
    research_recall = research.prefetch("discord repair checklist")

    assert "discord repair checklist" in main_recall.lower()
    assert "discord repair checklist" not in research_recall.lower()


def test_curated_memory_imports_use_expected_lanes(monkeypatch, tmp_path):
    import tools.memory_tool as memory_tool

    memory_dir = tmp_path / "curated"
    memory_dir.mkdir()
    (memory_dir / "USER.md").write_text("Brendan likes concise answers.", encoding="utf-8")
    (memory_dir / "MEMORY.md").write_text("Main agent keeps the Discord repair checklist.", encoding="utf-8")
    monkeypatch.setattr(memory_tool, "get_memory_dir", lambda: memory_dir)

    provider = LocalHybridMemoryProvider()
    try:
        provider.initialize(
            "session-1",
            hermes_home=str(tmp_path),
            platform="discord",
            user_id="discord-user",
            agent_identity="main",
            agent_workspace="workspace-main",
        )
        _wait(provider)

        rows = provider._db.execute(
            "SELECT source, lane, content FROM memory_items WHERE source IN ('curated_user', 'curated_memory')"
        ).fetchall()
    finally:
        provider.shutdown()

    assert any(
        row["source"] == "curated_user"
        and row["lane"] == "user_global"
        and "concise answers" in row["content"].lower()
        for row in rows
    )
    assert any(
        row["source"] == "curated_memory"
        and row["lane"] == "agent_private"
        and "discord repair checklist" in row["content"].lower()
        for row in rows
    )


def test_workspace_isolation_prevents_cross_project_leak(monkeypatch, provider_factory):
    monkeypatch.delenv("GEMINI_EMBEDDINGS_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    vpstudio = provider_factory(agent_identity="main", workspace="/tmp/VPStudio")
    thesis = provider_factory(agent_identity="main", workspace="/tmp/thesis")

    vpstudio.on_memory_write("add", "memory", "VPStudio uses the visionOS capture pipeline.")
    _wait(vpstudio)

    vpstudio_recall = vpstudio.prefetch("visionOS capture pipeline")
    thesis_recall = thesis.prefetch("visionOS capture pipeline")

    assert "visionos capture pipeline" in vpstudio_recall.lower()
    assert "visionos capture pipeline" not in thesis_recall.lower()


def test_concurrent_stress_writes_remain_isolated(monkeypatch, provider_factory):
    monkeypatch.delenv("GEMINI_EMBEDDINGS_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    main = provider_factory(agent_identity="main", session_id="main-session")
    research = provider_factory(agent_identity="research", session_id="research-session")

    def _spam(provider, prefix: str):
        for idx in range(60):
            provider.sync_turn(
                f"{prefix} memory item {idx} for Brendan.",
                f"Stored {prefix} item {idx}.",
            )

    threads = [
        threading.Thread(target=_spam, args=(main, "main-pipeline")),
        threading.Thread(target=_spam, args=(research, "research-theorem")),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    _wait(main)
    _wait(research)

    main_recall = main.prefetch("main pipeline")
    research_recall = research.prefetch("research theorem")

    assert "main-pipeline" in main_recall.lower()
    assert "research-theorem" not in main_recall.lower()
    assert "research-theorem" in research_recall.lower()
    assert "main-pipeline" not in research_recall.lower()


def test_sync_turn_skips_background_watch_notifications(monkeypatch, provider_factory):
    monkeypatch.delenv("GEMINI_EMBEDDINGS_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    provider = provider_factory()
    provider.sync_turn(
        '[SYSTEM: Background process proc_deadbeef matched watch pattern "WAVE_RESULT". '
        'Command: source venv/bin/activate && python runner.py Matched output: '
        'WAVE_RESULT {"done": 1}]',
        'Still running. Wave 1 complete.',
    )
    _wait(provider)

    rows = provider._db.execute("SELECT source, content FROM memory_items WHERE source = 'turn'").fetchall()

    assert rows == []
