from pathlib import Path


def test_requirements_matches_security_pins_from_pyproject():
    requirements = Path("requirements.txt").read_text(encoding="utf-8")

    assert "requests>=2.33.0,<3" in requirements
    assert "PyJWT[crypto]>=2.12.0,<3" in requirements
