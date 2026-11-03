from __future__ import annotations

from email.utils import parsedate_to_datetime
from pathlib import Path
import re
import urllib.request
from urllib.parse import urlsplit, urlunsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
MEDIUM_FEED_URL = "https://medium.com/feed/@hassen.benchaaben01"

START_MARKER = "<!-- MEDIUM-POSTS:START -->"
END_MARKER = "<!-- MEDIUM-POSTS:END -->"


def _clean_url(url: str) -> str:
    parts = urlsplit(url.strip())
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def parse_medium_rss(xml_bytes: bytes, limit: int = 6) -> list[dict[str, str]]:
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return []

    posts: list[dict[str, str]] = []
    for item in root.findall(".//item")[:limit]:
        title_el = item.find("title")
        link_el = item.find("link")
        pub_el = item.find("pubDate")
        if title_el is None or link_el is None or not title_el.text or not link_el.text:
            continue

        date_str = ""
        if pub_el is not None and pub_el.text:
            try:
                dt = parsedate_to_datetime(pub_el.text.strip())
                date_str = dt.strftime("%b %Y")
            except (TypeError, ValueError):
                date_str = pub_el.text.strip()[:16]

        posts.append(
            {
                "date": date_str,
                "title": title_el.text.strip().replace("|", "·"),
                "url": _clean_url(link_el.text),
            }
        )
    return posts


def render_posts_table(posts: list[dict[str, str]]) -> str:
    lines = [
        "| Date | Post |",
        "| :--- | :--- |",
    ]
    for post in posts:
        lines.append(f"| {post['date']} | [{post['title']}]({post['url']}) |")
    return "\n".join(lines)


def update_readme_section(readme_text: str, posts: list[dict[str, str]]) -> str:
    if not posts:
        return readme_text
    pattern = re.compile(
        rf"({re.escape(START_MARKER)})(.*?)({re.escape(END_MARKER)})",
        re.DOTALL,
    )
    table_md = render_posts_table(posts)
    replacement = f"{START_MARKER}\n{table_md}\n{END_MARKER}"
    return pattern.sub(lambda _: replacement, readme_text, count=1)


def fetch_medium_rss(url: str = MEDIUM_FEED_URL) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; HassenChaabenReadmeBot/1.0)"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()


def main() -> None:
    if not README_PATH.exists():
        return
    original = README_PATH.read_text(encoding="utf-8")
    try:
        xml_bytes = fetch_medium_rss()
        posts = parse_medium_rss(xml_bytes)
    except Exception:
        posts = []

    updated = update_readme_section(original, posts)
    if updated != original:
        README_PATH.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
