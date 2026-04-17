from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WHATSAPP_BRIDGE_DIR = ROOT / "scripts" / "whatsapp-bridge"


def test_baileys_lockfile_matches_manifest() -> None:
    package = json.loads((WHATSAPP_BRIDGE_DIR / "package.json").read_text(encoding="utf-8"))
    lock = json.loads((WHATSAPP_BRIDGE_DIR / "package-lock.json").read_text(encoding="utf-8"))

    manifest_spec = package["dependencies"]["@whiskeysockets/baileys"]
    lock_spec = lock["packages"][""]["dependencies"]["@whiskeysockets/baileys"]
    resolved = lock["packages"]["node_modules/@whiskeysockets/baileys"]["resolved"]

    assert lock_spec == manifest_spec
    assert resolved.endswith(f"#{manifest_spec.split('#', 1)[1]}")
