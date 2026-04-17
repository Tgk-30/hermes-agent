"""Tests for platform-note wording in gateway/session.py."""

from gateway.config import Platform
from gateway.session import SessionContext, SessionSource, build_session_context_prompt


def test_discord_platform_note_mentions_tool_based_admin_capability():
    context = SessionContext(
        source=SessionSource(platform=Platform.DISCORD, chat_id="123", chat_name="general", chat_type="channel", user_id="42", user_name="Brendan"),
        connected_platforms=[Platform.DISCORD],
        home_channels={},
    )

    prompt = build_session_context_prompt(context)

    assert "Some Discord-specific admin/history actions may be available via exposed tools" in prompt
    assert "Do not promise unsupported bulk moderation or server-management actions" in prompt
