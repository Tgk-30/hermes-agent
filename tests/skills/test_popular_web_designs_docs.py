from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL_FILE = ROOT / "skills" / "creative" / "popular-web-designs" / "SKILL.md"
TEMPLATES_DIR = ROOT / "skills" / "creative" / "popular-web-designs" / "templates"


def test_popular_web_designs_does_not_reference_missing_generative_widgets_skill() -> None:
    assert "generative-widgets" not in SKILL_FILE.read_text(encoding="utf-8")

    offenders = [
        template.name
        for template in sorted(TEMPLATES_DIR.glob("*.md"))
        if "generative-widgets" in template.read_text(encoding="utf-8")
    ]

    assert offenders == []
