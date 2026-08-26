"""Check generated pages whose absence would not fail HTMLProofer."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(relative: str) -> str:
    path = SITE / relative
    if not path.exists():
        fail(f"generated page missing: {relative}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    engineering = read("engineering/index.html")
    article = read("2026/08/27/three-emulator-bugs.html")
    home = read("index.html")
    feed = read("feed.xml")
    sitemap = read("sitemap.xml")

    if engineering.count("Three Emulator Bugs, Three Different Tests") != 1:
        fail("engineering record does not contain the new article exactly once")
    if home.count("/2026/08/27/three-emulator-bugs.html") != 2:
        fail("homepage does not feature and list the new article")
    if "Three merged 86Box fixes" not in article:
        fail("new article body was not rendered")
    if feed.count('<title type="html">Three Emulator Bugs, Three Different Tests</title>') != 1:
        fail("global feed does not contain the new article exactly once")
    for url in (
        "https://mihainadas.github.io/engineering/",
        "https://mihainadas.github.io/2026/08/27/three-emulator-bugs.html",
    ):
        if sitemap.count(url) != 1:
            fail(f"sitemap does not contain {url} exactly once")

    for relative, text in (
        ("engineering/index.html", engineering),
        ("2026/08/27/three-emulator-bugs.html", article),
    ):
        if re.search(
            r"(?i)github\.com/klusai|\bklusai\b|"
            r"huggingface\.co/(?:datasets|models|spaces)/klusai(?:/|$)|"
            r"\b(?:RES|KLU)-\d+\b",
            text,
        ):
            fail(f"private program reference in generated page: {relative}")

    for path in SITE.rglob("*.html"):
        if re.search(r"(?i)github\.com/klusai(?:/|$)", path.read_text(encoding="utf-8")):
            fail(f"stealth repository link in generated page: {path.relative_to(SITE)}")

    print("generated site checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
