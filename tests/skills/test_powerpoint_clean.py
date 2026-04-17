from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path
from xml.dom import minidom as xml_minidom


SCRIPT_PATH = (
    Path(__file__).resolve().parents[2]
    / "skills"
    / "productivity"
    / "powerpoint"
    / "scripts"
    / "clean.py"
)


def load_module():
    defusedxml_pkg = types.ModuleType("defusedxml")
    defusedxml_minidom = types.ModuleType("defusedxml.minidom")
    defusedxml_minidom.parse = xml_minidom.parse
    defusedxml_pkg.minidom = defusedxml_minidom
    sys.modules.setdefault("defusedxml", defusedxml_pkg)
    sys.modules["defusedxml.minidom"] = defusedxml_minidom

    spec = importlib.util.spec_from_file_location("powerpoint_clean", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_remove_orphaned_slides_handles_prefixed_relationship_tags(tmp_path: Path) -> None:
    mod = load_module()

    pres_path = tmp_path / "ppt" / "presentation.xml"
    pres_rels_path = tmp_path / "ppt" / "_rels" / "presentation.xml.rels"
    slide1_path = tmp_path / "ppt" / "slides" / "slide1.xml"
    slide2_path = tmp_path / "ppt" / "slides" / "slide2.xml"
    slide2_rels_path = tmp_path / "ppt" / "slides" / "_rels" / "slide2.xml.rels"

    slide2_rels_path.parent.mkdir(parents=True)
    pres_rels_path.parent.mkdir(parents=True, exist_ok=True)

    pres_path.write_text(
        """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<p:presentation xmlns:p=\"http://schemas.openxmlformats.org/presentationml/2006/main\" xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\">
  <p:sldIdLst>
    <p:sldId id=\"256\" r:id=\"rId1\"/>
  </p:sldIdLst>
</p:presentation>
""",
        encoding="utf-8",
    )
    pres_rels_path.write_text(
        """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<pr:Relationships xmlns:pr=\"http://schemas.openxmlformats.org/package/2006/relationships\">
  <pr:Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide\" Target=\"slides/slide1.xml\"/>
  <pr:Relationship Id=\"rId2\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide\" Target=\"slides/slide2.xml\"/>
</pr:Relationships>
""",
        encoding="utf-8",
    )
    slide1_path.write_text("<slide/>", encoding="utf-8")
    slide2_path.write_text("<slide/>", encoding="utf-8")
    slide2_rels_path.write_text("<Relationships/>", encoding="utf-8")

    removed = mod.remove_orphaned_slides(tmp_path)

    assert slide1_path.exists()
    assert not slide2_path.exists()
    assert not slide2_rels_path.exists()
    assert "ppt/slides/slide2.xml" in removed
    assert "ppt/slides/_rels/slide2.xml.rels" in removed
    assert "ppt/slides/slide1.xml" not in removed

    rels_text = pres_rels_path.read_text(encoding="utf-8")
    assert "slide1.xml" in rels_text
    assert "slide2.xml" not in rels_text


def test_update_content_types_handles_prefixed_override_tags(tmp_path: Path) -> None:
    mod = load_module()

    content_types_path = tmp_path / "[Content_Types].xml"
    content_types_path.write_text(
        """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<ct:Types xmlns:ct=\"http://schemas.openxmlformats.org/package/2006/content-types\">
  <ct:Override PartName=\"/ppt/slides/slide1.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.presentationml.slide+xml\"/>
  <ct:Override PartName=\"/ppt/slides/slide2.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.presentationml.slide+xml\"/>
</ct:Types>
""",
        encoding="utf-8",
    )

    mod.update_content_types(tmp_path, ["ppt/slides/slide2.xml"])

    updated = content_types_path.read_text(encoding="utf-8")
    assert "slide1.xml" in updated
    assert "slide2.xml" not in updated
