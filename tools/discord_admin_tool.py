"""Discord Admin Tool -- Discord-specific admin/history helpers.

Restores a subset of the old OpenClaw Discord management surface:
- list channels
- read channel/thread history
- create threads
- pin messages

This is intentionally separate from send_message, which remains the generic
cross-platform send/list primitive.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional
from urllib.parse import urlencode


DISCORD_ADMIN_SCHEMA = {
    "name": "discord_admin",
    "description": (
        "Discord-specific admin/history helper. Use for listing channels, reading "
        "channel or thread history, creating channels or threads, and pinning "
        "messages. This tool is Discord-only and is intended to restore some of the "
        "old OpenClaw message-tool behavior."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["channel_list", "channel_read", "channel_create", "thread_create", "pin_message"],
                "description": "Discord admin action to perform.",
            },
            "guild_id": {
                "type": "string",
                "description": "Optional guild/server ID for channel_list when you want a live guild-scoped list.",
            },
            "channel_id": {
                "type": "string",
                "description": "Discord channel ID (or thread ID for read/pin). Required for channel_read, thread_create, and pin_message.",
            },
            "message_id": {
                "type": "string",
                "description": "Discord message ID. Required for pin_message.",
            },
            "name": {
                "type": "string",
                "description": "Channel or thread name. Required for channel_create and thread_create.",
            },
            "category_id": {
                "type": "string",
                "description": "Optional Discord category ID to place a newly created channel under.",
            },
            "topic": {
                "type": "string",
                "description": "Optional channel topic for channel_create.",
            },
            "nsfw": {
                "type": "boolean",
                "description": "Whether the new channel should be marked NSFW. Used by channel_create.",
            },
            "message": {
                "type": "string",
                "description": "Optional seed message used before creating a thread from that message.",
            },
            "limit": {
                "type": "integer",
                "description": "How many recent messages to read (1-100). Default 20.",
            },
            "auto_archive_duration": {
                "type": "integer",
                "description": "Thread auto-archive minutes. One of 60, 1440, 4320, 10080. Default 1440.",
            },
        },
        "required": ["action"],
    },
}

_VALID_THREAD_AUTO_ARCHIVE_MINUTES = {60, 1440, 4320, 10080}


def _current_discord_scope() -> dict[str, Any]:
    from gateway.session_context import get_session_env

    platform = get_session_env("HERMES_SESSION_PLATFORM", "")
    if platform != "discord":
        return {"active": False}

    chat_id = str(get_session_env("HERMES_SESSION_CHAT_ID", "") or "").strip()
    thread_id = str(get_session_env("HERMES_SESSION_THREAD_ID", "") or "").strip()
    chat_name = str(get_session_env("HERMES_SESSION_CHAT_NAME", "") or "").strip()
    source_channel_id = thread_id or chat_id

    ids = {v for v in (chat_id, thread_id) if v}
    return {
        "active": True,
        "chat_id": chat_id,
        "thread_id": thread_id,
        "chat_name": chat_name,
        "source_channel_id": source_channel_id,
        "allowed_ids": ids,
    }


def _load_directory_channels() -> list[dict[str, Any]]:
    from gateway.channel_directory import load_directory

    directory = load_directory()
    raw_channels = directory.get("platforms", {}).get("discord", []) or []
    return [
        ch for ch in raw_channels
        if isinstance(ch, dict)
        and str(ch.get("id", "")).isdigit()
        and ch.get("type") in {"channel", "thread"}
    ]


def _normalize_live_channel(ch: dict[str, Any], *, guild_id: str | None = None) -> dict[str, Any] | None:
    if not isinstance(ch, dict) or not ch.get("id"):
        return None
    resolved_guild_id = ch.get("guild_id") or guild_id
    return {
        "id": str(ch.get("id")),
        "name": ch.get("name"),
        "guild_id": str(resolved_guild_id) if resolved_guild_id is not None else None,
        "type": _discord_channel_type_name(ch.get("type")),
        "parent_id": str(ch.get("parent_id")) if ch.get("parent_id") is not None else None,
        "topic": ch.get("topic"),
        "nsfw": bool(ch.get("nsfw", False)),
    }


async def _fetch_channel_metadata(channel_id: str, token: str) -> dict[str, Any]:
    url = f"https://discord.com/api/v10/channels/{channel_id}"
    result = await _discord_api_request("GET", url, token)
    if not result.get("success"):
        return result
    channel = result.get("data")
    if not isinstance(channel, dict):
        return {"error": f"Discord channel lookup for {channel_id} returned an invalid payload"}
    return {"success": True, "channel": channel}


async def _resolve_current_scope_guild(token: str) -> dict[str, Any]:
    scope = _current_discord_scope()
    if not scope.get("active"):
        return {"success": True, "guild_id": None, "source_channel_id": None}

    source_channel_id = str(scope.get("source_channel_id") or "").strip()
    if not source_channel_id:
        return {"error": "Current Discord session is missing a source channel ID"}

    result = await _fetch_channel_metadata(source_channel_id, token)
    if not result.get("success"):
        return result

    guild_id = (result.get("channel") or {}).get("guild_id")
    if not guild_id:
        return {"error": "Current Discord session is not attached to a server"}

    return {
        "success": True,
        "guild_id": str(guild_id),
        "source_channel_id": source_channel_id,
        "channel": result.get("channel"),
    }


async def _channel_scope_check(channel_id: str, token: str) -> dict[str, Any]:
    scope = _current_discord_scope()
    if not scope.get("active"):
        return {"success": True, "in_scope": True}

    channel_id = str(channel_id)
    if channel_id in scope["allowed_ids"]:
        return {"success": True, "in_scope": True}

    current_scope = await _resolve_current_scope_guild(token)
    if not current_scope.get("success"):
        return current_scope

    target = await _fetch_channel_metadata(channel_id, token)
    if not target.get("success"):
        return target

    target_guild_id = ((target.get("channel") or {}).get("guild_id"))
    in_scope = bool(target_guild_id) and str(target_guild_id) == str(current_scope.get("guild_id"))
    return {
        "success": True,
        "in_scope": in_scope,
        "guild_id": str(target_guild_id) if target_guild_id is not None else None,
    }


def _discord_channel_type_name(type_value: Any) -> str:
    mapping = {
        0: "channel",
        1: "dm",
        2: "voice",
        3: "dm",
        4: "category",
        5: "announcement",
        10: "thread",
        11: "thread",
        12: "thread",
        13: "stage",
        14: "directory",
        15: "forum",
        16: "media",
    }
    return mapping.get(type_value, str(type_value))


async def _discord_api_request(method: str, url: str, token: str, *, payload: Optional[dict] = None):
    try:
        import aiohttp
    except ImportError:
        return {"error": "aiohttp not installed. Run: pip install aiohttp"}

    try:
        from gateway.platforms.base import resolve_proxy_url, proxy_kwargs_for_aiohttp
        from tools.send_message_tool import _error

        proxy = resolve_proxy_url(platform_env_var="DISCORD_PROXY")
        sess_kw, req_kw = proxy_kwargs_for_aiohttp(proxy)
        headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30), **sess_kw) as session:
            async with session.request(method, url, headers=headers, json=payload, **req_kw) as resp:
                body_text = await resp.text()
                if resp.status not in (200, 201, 204):
                    return _error(f"Discord API error ({resp.status}): {body_text}")
                if resp.status == 204 or not body_text.strip():
                    return {"success": True, "status": resp.status}
                try:
                    data = json.loads(body_text)
                except Exception:
                    data = body_text
                return {"success": True, "status": resp.status, "data": data}
    except Exception as e:  # pragma: no cover - defensive wrapper
        from tools.send_message_tool import _error
        return _error(f"Discord API request failed: {e}")


def _discord_token_from_config() -> tuple[str | None, Any | None]:
    from gateway.config import Platform, load_gateway_config

    config = load_gateway_config()
    pconfig = config.platforms.get(Platform.DISCORD)
    if not pconfig or not getattr(pconfig, "enabled", False):
        return None, None
    token = getattr(pconfig, "token", None)
    if not token:
        return None, pconfig
    return str(token), pconfig


def _handle_channel_list(args: Dict[str, Any]) -> dict:
    guild_id = str(args.get("guild_id") or "").strip()
    scope = _current_discord_scope()
    if guild_id and scope.get("active"):
        return {"error": "guild_id override is not allowed inside Discord sessions; use the current server scope instead"}
    if guild_id or scope.get("active"):
        return {"defer_async": "channel_list_live", "guild_id": guild_id}

    from gateway.channel_directory import load_directory

    directory = load_directory()
    channels = _load_directory_channels()
    return {
        "success": True,
        "updated_at": directory.get("updated_at"),
        "channels": channels,
    }


async def _handle_channel_list_live(args: Dict[str, Any]) -> dict:
    guild_id = str(args.get("guild_id") or "").strip()

    token, _pconfig = _discord_token_from_config()
    if not token:
        return {"error": "Discord is not configured or token is missing"}

    if not guild_id:
        scoped_guild = await _resolve_current_scope_guild(token)
        if not scoped_guild.get("success"):
            return scoped_guild
        guild_id = str(scoped_guild.get("guild_id") or "").strip()
    if not guild_id:
        return {"error": "guild_id is required for live guild channel listing"}

    channels_url = f"https://discord.com/api/v10/guilds/{guild_id}/channels"
    channels_result = await _discord_api_request("GET", channels_url, token)
    if not channels_result.get("success"):
        return channels_result

    live_channels = []
    seen_ids = set()
    for ch in channels_result.get("data") or []:
        normalized = _normalize_live_channel(ch, guild_id=guild_id)
        if not normalized:
            continue
        if normalized["id"] in seen_ids:
            continue
        seen_ids.add(normalized["id"])
        live_channels.append(normalized)

    threads_url = f"https://discord.com/api/v10/guilds/{guild_id}/threads/active"
    threads_result = await _discord_api_request("GET", threads_url, token)
    if threads_result.get("success"):
        for ch in (threads_result.get("data") or {}).get("threads", []) or []:
            normalized = _normalize_live_channel(ch, guild_id=guild_id)
            if not normalized:
                continue
            if normalized["id"] in seen_ids:
                continue
            seen_ids.add(normalized["id"])
            live_channels.append(normalized)

    return {"success": True, "guild_id": guild_id, "channels": live_channels}


async def _handle_channel_read(args: Dict[str, Any]) -> dict:
    channel_id = str(args.get("channel_id") or "").strip()
    if not channel_id:
        return {"error": "channel_id is required for channel_read"}

    limit = args.get("limit", 20)
    try:
        limit = max(1, min(100, int(limit)))
    except Exception:
        limit = 20

    token, _pconfig = _discord_token_from_config()
    if not token:
        return {"error": "Discord is not configured or token is missing"}

    scope_check = await _channel_scope_check(channel_id, token)
    if not scope_check.get("success"):
        return scope_check
    if not scope_check.get("in_scope", False):
        return {"error": "channel_read target is outside the current Discord session scope"}

    query = urlencode({"limit": limit})
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages?{query}"
    result = await _discord_api_request("GET", url, token)
    if not result.get("success"):
        return result

    messages = []
    for msg in result.get("data") or []:
        if not isinstance(msg, dict):
            continue
        author = msg.get("author") or {}
        attachments = msg.get("attachments") or []
        messages.append(
            {
                "id": str(msg.get("id")),
                "author": author.get("global_name") or author.get("username") or author.get("id"),
                "author_id": author.get("id"),
                "content": msg.get("content", ""),
                "timestamp": msg.get("timestamp"),
                "reply_to": ((msg.get("message_reference") or {}).get("message_id")),
                "attachments": [
                    {
                        "id": str(att.get("id")),
                        "filename": att.get("filename"),
                        "url": att.get("url"),
                    }
                    for att in attachments
                    if isinstance(att, dict)
                ],
            }
        )

    return {"success": True, "channel_id": channel_id, "messages": messages}


async def _handle_channel_create(args: Dict[str, Any]) -> dict:
    guild_id = str(args.get("guild_id") or "").strip()
    name = str(args.get("name") or "").strip()
    if not name:
        return {"error": "name is required for channel_create"}

    token, _pconfig = _discord_token_from_config()
    if not token:
        return {"error": "Discord is not configured or token is missing"}

    scope = _current_discord_scope()
    if scope.get("active"):
        current_scope = await _resolve_current_scope_guild(token)
        if not current_scope.get("success"):
            return current_scope
        current_guild_id = str(current_scope.get("guild_id") or "").strip()
        if guild_id and guild_id != current_guild_id:
            return {"error": "channel_create guild_id is outside the current Discord session scope"}
        guild_id = current_guild_id

    if not guild_id:
        return {"error": "guild_id is required for channel_create"}

    payload = {
        "name": name,
        "type": 0,
        "nsfw": bool(args.get("nsfw", False)),
    }
    category_id = str(args.get("category_id") or "").strip()
    topic = str(args.get("topic") or "").strip()
    if category_id:
        payload["parent_id"] = category_id
    if topic:
        payload["topic"] = topic

    url = f"https://discord.com/api/v10/guilds/{guild_id}/channels"
    result = await _discord_api_request("POST", url, token, payload=payload)
    if not result.get("success"):
        return result
    data = result.get("data") or {}
    return {
        "success": True,
        "guild_id": guild_id,
        "channel_id": str(data.get("id")),
        "channel_name": data.get("name") or name,
        "category_id": str(data.get("parent_id")) if data.get("parent_id") is not None else (category_id or None),
        "topic": data.get("topic") or topic or None,
        "nsfw": bool(data.get("nsfw", payload["nsfw"])),
    }


async def _handle_thread_create(args: Dict[str, Any]) -> dict:
    channel_id = str(args.get("channel_id") or "").strip()
    name = str(args.get("name") or "").strip()
    if not channel_id:
        return {"error": "channel_id is required for thread_create"}
    if not name:
        return {"error": "name is required for thread_create"}

    auto_archive_duration = args.get("auto_archive_duration", 1440)
    try:
        auto_archive_duration = int(auto_archive_duration)
    except Exception:
        auto_archive_duration = 1440
    if auto_archive_duration not in _VALID_THREAD_AUTO_ARCHIVE_MINUTES:
        allowed = ", ".join(str(v) for v in sorted(_VALID_THREAD_AUTO_ARCHIVE_MINUTES))
        return {"error": f"auto_archive_duration must be one of: {allowed}"}

    token, _pconfig = _discord_token_from_config()
    if not token:
        return {"error": "Discord is not configured or token is missing"}

    scope_check = await _channel_scope_check(channel_id, token)
    if not scope_check.get("success"):
        return scope_check
    if not scope_check.get("in_scope", False):
        return {"error": "thread_create target is outside the current Discord session scope"}

    seed_content = (str(args.get("message") or "").strip() or "🧵 Thread created by Hermes.")
    seed_url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    seed_payload = {
        "content": seed_content,
        "allowed_mentions": {"parse": []},
    }
    send_result = await _discord_api_request("POST", seed_url, token, payload=seed_payload)
    if not send_result.get("success"):
        return send_result
    seed_data = send_result.get("data") or {}
    seed_message_id = seed_data.get("id")
    if not seed_message_id:
        return {"error": "Discord seed message succeeded but no message_id was returned"}

    url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{seed_message_id}/threads"
    payload = {"name": name, "auto_archive_duration": auto_archive_duration}
    result = await _discord_api_request("POST", url, token, payload=payload)
    if not result.get("success"):
        cleanup_url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{seed_message_id}"
        try:
            await _discord_api_request("DELETE", cleanup_url, token)
        except Exception:
            pass
        return result
    data = result.get("data") or {}
    return {
        "success": True,
        "thread_id": str(data.get("id")),
        "thread_name": data.get("name") or name,
        "seed_message_id": str(seed_message_id),
        "parent_channel_id": channel_id,
    }


async def _handle_pin_message(args: Dict[str, Any]) -> dict:
    channel_id = str(args.get("channel_id") or "").strip()
    message_id = str(args.get("message_id") or "").strip()
    if not channel_id:
        return {"error": "channel_id is required for pin_message"}
    if not message_id:
        return {"error": "message_id is required for pin_message"}

    token, _pconfig = _discord_token_from_config()
    if not token:
        return {"error": "Discord is not configured or token is missing"}

    scope_check = await _channel_scope_check(channel_id, token)
    if not scope_check.get("success"):
        return scope_check
    if not scope_check.get("in_scope", False):
        return {"error": "pin_message target is outside the current Discord session scope"}

    url = f"https://discord.com/api/v10/channels/{channel_id}/pins/{message_id}"
    result = await _discord_api_request("PUT", url, token)
    if not result.get("success"):
        return result
    return {"success": True, "channel_id": channel_id, "message_id": message_id, "pinned": True}


def discord_admin_tool(args, **kw):
    action = str(args.get("action") or "").strip().lower()
    if not action:
        return json.dumps({"error": "action is required"})

    if action == "channel_list":
        result = _handle_channel_list(args)
        if result.get("defer_async") == "channel_list_live":
            from model_tools import _run_async
            result = _run_async(_handle_channel_list_live(args))
        return json.dumps(result)

    from model_tools import _run_async

    if action == "channel_read":
        return json.dumps(_run_async(_handle_channel_read(args)))
    if action == "channel_create":
        return json.dumps(_run_async(_handle_channel_create(args)))
    if action == "thread_create":
        return json.dumps(_run_async(_handle_thread_create(args)))
    if action == "pin_message":
        return json.dumps(_run_async(_handle_pin_message(args)))

    return json.dumps({"error": f"Unknown action: {action}"})


def _check_discord_admin():
    """Gate discord_admin on Discord session or a running gateway with Discord enabled."""
    from gateway.session_context import get_session_env

    platform = get_session_env("HERMES_SESSION_PLATFORM", "")
    if platform:
        if platform != "discord":
            return False
        token, _pconfig = _discord_token_from_config()
        return bool(token)

    try:
        from gateway.status import is_gateway_running
        if not is_gateway_running():
            return False
        from gateway.config import Platform, load_gateway_config
        config = load_gateway_config()
        pconfig = config.platforms.get(Platform.DISCORD)
        return bool(pconfig and getattr(pconfig, "enabled", False) and getattr(pconfig, "token", None))
    except Exception:
        return False


from tools.registry import registry

registry.register(
    name="discord_admin",
    toolset="messaging",
    schema=DISCORD_ADMIN_SCHEMA,
    handler=discord_admin_tool,
    check_fn=_check_discord_admin,
    emoji="🧵",
)
