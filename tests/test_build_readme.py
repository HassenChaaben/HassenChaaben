from pathlib import Path
import sys
import xml.etree.ElementTree as ET
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_readme import (
    parse_medium_rss,
    render_posts_table,
    update_readme_section,
)

SAMPLE_RSS = b"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <item>
      <title>AI Periodic Table</title>
      <link>https://medium.com/@hassen.benchaaben01/ai-periodic-table-ed1696cb7c4c?source=rss-75d01414516f------2</link>
      <pubDate>Sun, 11 Jan 2026 01:58:27 GMT</pubDate>
    </item>
  </channel>
</rss>
"""


def test_parse_medium_rss_strips_tracking_and_formats_date():
    posts = parse_medium_rss(SAMPLE_RSS)
    assert len(posts) == 1
    assert posts[0]["date"] == "Jan 2026"
    assert posts[0]["title"] == "AI Periodic Table"
    assert (
        posts[0]["url"]
        == "https://medium.com/@hassen.benchaaben01/ai-periodic-table-ed1696cb7c4c"
    )


def test_update_readme_section_is_idempotent_and_preserves_on_empty():
    original = (
        "Header\n"
        "<!-- MEDIUM-POSTS:START -->\n"
        "| Date | Post |\n| :--- | :--- |\n| Jan 2026 | [Old](https://example.com) |\n"
        "<!-- MEDIUM-POSTS:END -->\n"
        "Footer\n"
    )
    posts = [
        {
            "date": "Jan 2026",
            "title": "AI Periodic Table",
            "url": "https://medium.com/@hassen.benchaaben01/ai-periodic-table-ed1696cb7c4c",
        }
    ]
    updated = update_readme_section(original, posts)
    assert "[AI Periodic Table](https://medium.com/@hassen.benchaaben01/ai-periodic-table-ed1696cb7c4c)" in updated
    assert update_readme_section(updated, posts) == updated
    # Empty list (e.g. offline fallback) preserves existing content
    assert update_readme_section(updated, []) == updated


def test_svg_assets_are_valid_xml_and_camo_safe():
    expected_svgs = [
        "hero-card.svg",
        "bento-phases.svg",
        "experience-card.svg",
        "badge-portfolio.svg",
        "badge-linkedin.svg",
        "badge-medium.svg",
        "badge-email.svg",
    ]
    for name in expected_svgs:
        svg_path = ROOT / "assets" / name
        assert svg_path.exists(), f"Missing SVG asset: {name}"
        content = svg_path.read_text(encoding="utf-8")
        ET.fromstring(content)
        assert "LabMACS" not in content
        assert "Researcher" not in content


def test_readme_contains_all_v5_requirements_and_excludes_forbidden_terms():
    readme_path = ROOT / "README.md"
    assert readme_path.exists()
    text = readme_path.read_text(encoding="utf-8")

    # Forbidden terms per user instruction
    assert "LabMACS" not in text
    assert "Researcher" not in text

    # Required identity & experience strings
    assert "UNIVPM" in text
    assert "Master's student" in text
    assert "Junior AI Engineer" in text
    assert "Part-Time" in text or "Part-time" in text
    assert "AI Specialist" in text
    assert "SQOIN" in text
    assert "Omdena" in text

    # Required links & repos
    assert "https://www.hassenbenchaaben.me/" in text
    assert "https://www.linkedin.com/in/hassen-ben-chaaben/" in text
    assert "https://medium.com/@hassen.benchaaben01" in text
    assert "hassen.benchaaben01@gmail.com" in text
    assert "Micosoft_office_google_antigravity_plugin" in text
    assert "MonAgent" in text
    assert "Mini_Rag_Application" in text
    assert "IntreccIAmi_Computer_Vision_Project" in text
    assert "<!-- MEDIUM-POSTS:START -->" in text
    assert "<!-- MEDIUM-POSTS:END -->" in text
