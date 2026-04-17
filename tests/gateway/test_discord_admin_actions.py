"""Tests for Discord admin adapter helpers."""

from datetime import datetime, timezone
import importlib
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
import sys

import pytest

from gateway.config import PlatformConfig


def _ensure_discord_mock():
    """Install a lightweight discord module when discord.py isn't available."""
    if "discord" in sys.modules and hasattr(sys.modules["discord"], "__file__"):
        return

    discord_mod = MagicMock()
    discord_mod.Intents.default.return_value = MagicMock()
    discord_mod.Client = MagicMock
    discord_mod.File = MagicMock
    discord_mod.DMChannel = type("DMChannel", (), {})
    discord_mod.Thread = type("Thread", (), {})
    discord_mod.ForumChannel = type("ForumChannel", (), {})
    discord_mod.TextChannel = type("TextChannel", (), {})
    discord_mod.ChannelType = SimpleNamespace(public_thread="public_thread")
    discord_mod.MessageType = SimpleNamespace(default=0, reply=1)
    discord_mod.Forbidden = type("Forbidden", (Exception,), {})
    discord_mod.ui = SimpleNamespace(
        View=object,
        Select=object,
        Button=object,
        button=lambda *a, **k: (lambda fn: fn),
    )
    discord_mod.SelectOption = lambda **kwargs: SimpleNamespace(**kwargs)
    discord_mod.ButtonStyle = SimpleNamespace(success=1, primary=2, secondary=2, danger=3, green=1, grey=2, blurple=2, red=3)
    discord_mod.Color = SimpleNamespace(
        orange=lambda: 1,
        green=lambda: 2,
        blue=lambda: 3,
        red=lambda: 4,
        purple=lambda: 5,
        gold=lambda: 6,
        greyple=lambda: 7,
    )
    discord_mod.Interaction = object
    discord_mod.Embed = MagicMock
    discord_mod.http = SimpleNamespace(Route=MagicMock)
    discord_mod.opus = SimpleNamespace(is_loaded=lambda: True, load_opus=lambda *_: None, Decoder=MagicMock)
    discord_mod.utils = SimpleNamespace(MISSING=object())
    discord_mod.FFmpegPCMAudio = MagicMock
    discord_mod.PCMVolumeTransformer = MagicMock
    discord_mod.app_commands = SimpleNamespace(
        describe=lambda **kwargs: (lambda fn: fn),
        choices=lambda **kwargs: (lambda fn: fn),
        Choice=lambda **kwargs: SimpleNamespace(**kwargs),
        Group=MagicMock,
        Command=MagicMock,
    )

    ext_mod = MagicMock()
    commands_mod = MagicMock()
    commands_mod.Bot = MagicMock
    ext_mod.commands = commands_mod

    sys.modules["discord"] = discord_mod
    sys.modules["discord.ext"] = ext_mod
    sys.modules["discord.ext.commands"] = commands_mod


_ensure_discord_mock()

import gateway.platforms.discord as discord_platform  # noqa: E402
discord_platform = importlib.reload(discord_platform)
from gateway.platforms.discord import DiscordAdapter  # noqa: E402


class FakeTextChannel:
    def __init__(self, channel_id: int, name: str, guild=None, parent=None, type_value: int = 0, topic: str | None = None, nsfw: bool = False):
        self.id = channel_id
        self.name = name
        self.guild = guild
        self.parent = parent
        self.parent_id = getattr(parent, "id", None)
        self.type = type_value
        self.topic = topic
        self.nsfw = nsfw

    async def create_thread(self, **kwargs):
        return SimpleNamespace(id=999, name=kwargs["name"], send=AsyncMock())


class FakeVoiceChannel:
    def __init__(self, channel_id: int, name: str, guild=None):
        self.id = channel_id
        self.name = name
        self.guild = guild
        self.type = 2
        self.parent = None
        self.parent_id = None
        self.topic = None
        self.nsfw = False


class FakeCategoryChannel:
    def __init__(self, channel_id: int, name: str, guild=None):
        self.id = channel_id
        self.name = name
        self.guild = guild
        self.type = 4
        self.parent = None
        self.parent_id = None
        self.topic = None
        self.nsfw = False


class FakeThreadChannel:
    def __init__(self, channel_id: int, name: str, guild=None, parent=None):
        self.id = channel_id
        self.name = name
        self.guild = guild
        self.parent = parent
        self.parent_id = getattr(parent, "id", None)
        self.type = 11
        self.topic = None
        self.nsfw = False
        self.send = AsyncMock()


class FakeAttachment:
    def __init__(self, attachment_id: int, filename: str, url: str):
        self.id = attachment_id
        self.filename = filename
        self.url = url


class FakeHistoryChannel(FakeTextChannel):
    def __init__(self, *args, messages=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._messages = list(messages or [])

    def history(self, *, limit: int = 20):
        async def _iter():
            for message in self._messages[:limit]:
                yield message

        return _iter()


class FakeForbiddenHistoryChannel(FakeTextChannel):
    def history(self, *, limit: int = 20):
        async def _iter():
            raise PermissionError("missing permissions")
            yield  # pragma: no cover

        return _iter()


@pytest.fixture
def adapter(monkeypatch):
    monkeypatch.setattr(discord_platform.discord, "DMChannel", type("FakeDMChannel", (), {}), raising=False)

    config = PlatformConfig(enabled=True, token="fake-token")
    adapter = DiscordAdapter(config)
    adapter._client = SimpleNamespace(guilds=[])
    return adapter


@pytest.mark.asyncio
async def test_list_channels_admin_returns_normalized_channels_and_threads(adapter):
    guild = SimpleNamespace(id=1, name="Hermes Guild")
    category = FakeCategoryChannel(55, "Ops", guild=guild)
    parent = FakeTextChannel(101, "general", guild=guild, topic="Main room")
    voice = FakeVoiceChannel(202, "Town Hall", guild=guild)
    thread = FakeThreadChannel(303, "Sprint Planning", guild=guild, parent=parent)
    guild.channels = [category, parent, voice]
    guild.threads = [thread]
    adapter._client.guilds = [guild]

    result = await adapter.list_channels_admin()

    assert result["success"] is True
    by_id = {entry["id"]: entry for entry in result["channels"]}
    assert by_id["55"]["type"] == "category"
    assert by_id["55"]["thread_capable"] is False
    assert by_id["101"]["type"] == "channel"
    assert by_id["101"]["guild"] == "Hermes Guild"
    assert by_id["101"]["thread_capable"] is True
    assert by_id["202"]["type"] == "voice"
    assert by_id["303"]["type"] == "thread"
    assert by_id["303"]["parent_id"] == "101"
    assert by_id["303"]["parent_name"] == "general"


@pytest.mark.asyncio
async def test_read_channel_history_admin_returns_normalized_records(adapter):
    author = SimpleNamespace(id=7, display_name="Brendan", name="brendan")
    first = SimpleNamespace(
        id=1001,
        author=author,
        content="First post",
        created_at=datetime(2026, 4, 13, 10, 0, tzinfo=timezone.utc),
        reference=None,
        attachments=[FakeAttachment(55, "notes.txt", "https://example.com/notes.txt")],
    )
    second = SimpleNamespace(
        id=1002,
        author=author,
        content="Reply",
        created_at=datetime(2026, 4, 13, 10, 5, tzinfo=timezone.utc),
        reference=SimpleNamespace(message_id=1001),
        attachments=[],
    )
    channel = FakeHistoryChannel(101, "general", messages=[second, first])
    adapter._client.get_channel = lambda channel_id: channel if channel_id == 101 else None

    result = await adapter.read_channel_history_admin("101", limit=5)

    assert result["success"] is True
    assert result["channel_id"] == "101"
    assert result["messages"][0]["id"] == "1002"
    assert result["messages"][0]["reply_to"] == 1001
    assert result["messages"][1]["attachments"][0]["filename"] == "notes.txt"
    assert result["messages"][1]["author"] == "Brendan"


@pytest.mark.asyncio
async def test_read_channel_history_admin_handles_permission_failure(adapter):
    channel = FakeForbiddenHistoryChannel(101, "private-room")
    adapter._client.get_channel = lambda channel_id: channel if channel_id == 101 else None

    result = await adapter.read_channel_history_admin("101", limit=5)

    assert "error" in result
    assert "Missing permission" in result["error"]


@pytest.mark.asyncio
async def test_create_thread_admin_creates_seeded_thread(adapter):
    parent = FakeTextChannel(101, "general")
    created_thread = SimpleNamespace(id=404, name="Planning", send=AsyncMock())
    parent.create_thread = AsyncMock(return_value=created_thread)
    adapter._client.get_channel = lambda channel_id: parent if channel_id == 101 else None

    result = await adapter.create_thread_admin("101", "Planning", message="Kickoff")

    assert result["success"] is True
    assert result["thread_id"] == "404"
    created_thread.send.assert_awaited_once_with("Kickoff")
    parent.create_thread.assert_awaited_once_with(
        name="Planning",
        auto_archive_duration=1440,
        reason="Requested by Hermes discord_admin tool",
        type=discord_platform.discord.ChannelType.public_thread,
    )


@pytest.mark.asyncio
async def test_create_channel_admin_creates_text_channel_under_category(adapter):
    category = SimpleNamespace(id=55, name="Ops")
    created_channel = SimpleNamespace(id=777, name="ops-war-room")
    guild = SimpleNamespace(id=1, name="Hermes Guild", create_text_channel=AsyncMock(return_value=created_channel))
    adapter._client.get_guild = lambda guild_id: guild if guild_id == 1 else None
    adapter._client.get_channel = lambda channel_id: category if channel_id == 55 else None

    result = await adapter.create_channel_admin("1", "ops-war-room", category_id="55", topic="War room", nsfw=True)

    assert result["success"] is True
    assert result["channel_id"] == "777"
    guild.create_text_channel.assert_awaited_once_with(
        name="ops-war-room",
        category=category,
        topic="War room",
        nsfw=True,
        reason="Requested by Hermes discord_admin tool",
    )


@pytest.mark.asyncio
async def test_create_channel_admin_fetches_uncached_category(adapter):
    category = SimpleNamespace(id=55, name="Ops")
    created_channel = SimpleNamespace(id=777, name="ops-war-room")
    guild = SimpleNamespace(id=1, name="Hermes Guild", create_text_channel=AsyncMock(return_value=created_channel))
    adapter._client.get_guild = lambda guild_id: guild if guild_id == 1 else None
    adapter._client.get_channel = lambda _channel_id: None
    adapter._client.fetch_channel = AsyncMock(return_value=category)

    result = await adapter.create_channel_admin("1", "ops-war-room", category_id="55")

    assert result["success"] is True
    adapter._client.fetch_channel.assert_awaited_once_with(55)
    guild.create_text_channel.assert_awaited_once_with(
        name="ops-war-room",
        category=category,
        topic=None,
        nsfw=False,
        reason="Requested by Hermes discord_admin tool",
    )


@pytest.mark.asyncio
async def test_pin_message_admin_pins_message(adapter):
    message = SimpleNamespace(pin=AsyncMock())
    channel = SimpleNamespace(fetch_message=AsyncMock(return_value=message))
    adapter._client.get_channel = lambda channel_id: channel if channel_id == 101 else None

    result = await adapter.pin_message_admin("101", "202")

    assert result == {"success": True, "channel_id": "101", "message_id": "202", "pinned": True}
    channel.fetch_message.assert_awaited_once_with(202)
    message.pin.assert_awaited_once_with(reason="Requested by Hermes discord_admin tool")
