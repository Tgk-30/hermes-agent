"""Import-safety tests for the Discord gateway adapter."""

import builtins
import importlib
import sys

import gateway.platforms as platforms_pkg


class TestDiscordImportSafety:
    def test_module_imports_even_when_discord_dependency_is_missing(self, monkeypatch):
        original_import = builtins.__import__
        original_module = sys.modules.get("gateway.platforms.discord")
        had_original_module = "gateway.platforms.discord" in sys.modules
        had_package_attr = hasattr(platforms_pkg, "discord")
        original_package_attr = getattr(platforms_pkg, "discord", None)

        def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "discord" or name.startswith("discord."):
                raise ImportError("discord unavailable for test")
            return original_import(name, globals, locals, fromlist, level)

        monkeypatch.delitem(sys.modules, "gateway.platforms.discord", raising=False)
        monkeypatch.setattr(builtins, "__import__", fake_import)

        try:
            module = importlib.import_module("gateway.platforms.discord")
        finally:
            if had_original_module:
                sys.modules["gateway.platforms.discord"] = original_module
            else:
                sys.modules.pop("gateway.platforms.discord", None)
            if had_package_attr:
                setattr(platforms_pkg, "discord", original_package_attr)
            elif hasattr(platforms_pkg, "discord"):
                delattr(platforms_pkg, "discord")

        assert module.DISCORD_AVAILABLE is False
        assert module.discord is None
