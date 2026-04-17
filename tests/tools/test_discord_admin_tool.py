"""Tests for tools/discord_admin_tool.py."""

import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from tools.discord_admin_tool import discord_admin_tool, _check_discord_admin, _handle_channel_create, _handle_channel_list_live, _channel_scope_check


def _run_async_immediately(coro):
    import asyncio
    return asyncio.run(coro)


class TestDiscordAdminTool:
    def test_unknown_action_returns_error(self):
        result = json.loads(discord_admin_tool({"action": "nope"}))
        assert "error" in result
        assert "Unknown action" in result["error"]

    def test_channel_list_reads_directory(self):
        fake_directory = {
            "updated_at": "2026-04-13T00:00:00",
            "platforms": {
                "discord": [
                    {"id": "123", "name": "general", "guild": "Guild", "type": "channel"},
                    {"id": "456", "name": "thread-a", "guild": "Guild", "type": "thread"},
                    {"id": "123:999", "name": "session-thread", "guild": "Guild", "type": "thread"},
                    {"id": "777", "name": "dm-ish", "guild": None, "type": "dm"},
                ]
            }
        }
        with patch("gateway.channel_directory.load_directory", return_value=fake_directory):
            result = json.loads(discord_admin_tool({"action": "channel_list"}))

        assert result["success"] is True
        assert result["updated_at"] == "2026-04-13T00:00:00"
        assert [ch["id"] for ch in result["channels"]] == ["123", "456"]
        assert result["channels"][1]["type"] == "thread"

    def test_channel_list_uses_live_scope_inside_discord_session(self):
        with patch("gateway.session_context.get_session_env", side_effect=lambda name, default='': {
            'HERMES_SESSION_PLATFORM': 'discord',
            'HERMES_SESSION_CHAT_ID': '123',
            'HERMES_SESSION_THREAD_ID': '',
            'HERMES_SESSION_CHAT_NAME': 'Guild A / #general',
        }.get(name, default)), \
             patch("tools.discord_admin_tool._handle_channel_list_live", new=AsyncMock(return_value={"success": True, "channels": [{"id": "123"}]})) as helper, \
             patch("model_tools._run_async", side_effect=_run_async_immediately):
            result = json.loads(discord_admin_tool({"action": "channel_list"}))

        assert result["success"] is True
        assert [ch["id"] for ch in result["channels"]] == ["123"]
        helper.assert_awaited_once()

    def test_channel_list_disallows_guild_override_inside_discord_session(self):
        with patch("gateway.session_context.get_session_env", side_effect=lambda name, default='': {
            'HERMES_SESSION_PLATFORM': 'discord',
            'HERMES_SESSION_CHAT_ID': '123',
            'HERMES_SESSION_THREAD_ID': '',
            'HERMES_SESSION_CHAT_NAME': 'Guild A / #general',
        }.get(name, default)):
            result = json.loads(discord_admin_tool({"action": "channel_list", "guild_id": "999"}))

        assert "error" in result
        assert "guild_id override" in result["error"]

    def test_channel_read_dispatches_async_helper(self):
        with patch("tools.discord_admin_tool._handle_channel_read", new=AsyncMock(return_value={"success": True, "messages": []})) as helper, \
             patch("model_tools._run_async", side_effect=_run_async_immediately):
            result = json.loads(discord_admin_tool({"action": "channel_read", "channel_id": "123"}))

        assert result["success"] is True
        helper.assert_awaited_once()

    def test_thread_create_dispatches_async_helper(self):
        with patch("tools.discord_admin_tool._handle_thread_create", new=AsyncMock(return_value={"success": True, "thread_id": "999"})) as helper, \
             patch("model_tools._run_async", side_effect=_run_async_immediately):
            result = json.loads(discord_admin_tool({"action": "thread_create", "channel_id": "123", "name": "Planning"}))

        assert result["success"] is True
        assert result["thread_id"] == "999"
        helper.assert_awaited_once()

    def test_channel_create_dispatches_async_helper(self):
        with patch("tools.discord_admin_tool._handle_channel_create", new=AsyncMock(return_value={"success": True, "channel_id": "777"})) as helper, \
             patch("model_tools._run_async", side_effect=_run_async_immediately):
            result = json.loads(discord_admin_tool({"action": "channel_create", "guild_id": "123", "name": "ops-war-room"}))

        assert result["success"] is True
        assert result["channel_id"] == "777"
        helper.assert_awaited_once()

    def test_pin_message_dispatches_async_helper(self):
        with patch("tools.discord_admin_tool._handle_pin_message", new=AsyncMock(return_value={"success": True})) as helper, \
             patch("model_tools._run_async", side_effect=_run_async_immediately):
            result = json.loads(discord_admin_tool({"action": "pin_message", "channel_id": "123", "message_id": "456"}))

        assert result["success"] is True
        helper.assert_awaited_once()

    def test_check_discord_admin_true_inside_discord_session(self):
        with patch("gateway.session_context.get_session_env", return_value="discord"), \
             patch("tools.discord_admin_tool._discord_token_from_config", return_value=("token", SimpleNamespace())):
            assert _check_discord_admin() is True


@pytest.mark.asyncio
async def test_channel_list_live_includes_active_threads():
    responses = [
        {"success": True, "data": [{"id": "101", "name": "general", "type": 0}]},
        {"success": True, "data": {"threads": [{"id": "202", "name": "planning", "type": 11, "parent_id": "101"}] }},
    ]
    with patch("tools.discord_admin_tool._discord_token_from_config", return_value=("token", SimpleNamespace())), \
         patch("tools.discord_admin_tool._discord_api_request", new=AsyncMock(side_effect=responses)):
        result = await _handle_channel_list_live({"guild_id": "555"})

    assert result["success"] is True
    assert {ch["id"] for ch in result["channels"]} == {"101", "202"}
    by_id = {ch["id"]: ch for ch in result["channels"]}
    assert by_id["202"]["type"] == "thread"
    assert by_id["202"]["parent_id"] == "101"


@pytest.mark.asyncio
async def test_channel_scope_check_uses_guild_ids_not_session_guild_name():
    responses = [
        {"success": True, "data": {"id": "123", "guild_id": "1", "name": "general"}},
        {"success": True, "data": {"id": "456", "guild_id": "2", "name": "other-general"}},
    ]
    with patch("gateway.session_context.get_session_env", side_effect=lambda name, default='': {
        'HERMES_SESSION_PLATFORM': 'discord',
        'HERMES_SESSION_CHAT_ID': '123',
        'HERMES_SESSION_THREAD_ID': '',
        'HERMES_SESSION_CHAT_NAME': 'Same Name Guild / #general',
    }.get(name, default)), \
         patch("tools.discord_admin_tool._discord_api_request", new=AsyncMock(side_effect=responses)):
        result = await _channel_scope_check("456", "token")

    assert result["success"] is True
    assert result["in_scope"] is False
    assert result["guild_id"] == "2"


@pytest.mark.asyncio
async def test_channel_create_rejects_cross_guild_override_inside_discord_session():
    with patch("gateway.session_context.get_session_env", side_effect=lambda name, default='': {
        'HERMES_SESSION_PLATFORM': 'discord',
        'HERMES_SESSION_CHAT_ID': '123',
        'HERMES_SESSION_THREAD_ID': '',
        'HERMES_SESSION_CHAT_NAME': 'Guild A / #general',
    }.get(name, default)), \
         patch("tools.discord_admin_tool._discord_token_from_config", return_value=("token", SimpleNamespace())), \
         patch("tools.discord_admin_tool._resolve_current_scope_guild", new=AsyncMock(return_value={"success": True, "guild_id": "1"})):
        result = await _handle_channel_create({"guild_id": "2", "name": "ops-war-room"})

    assert "error" in result
    assert "outside the current Discord session scope" in result["error"]
