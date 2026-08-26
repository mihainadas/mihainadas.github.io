"""Check generated pages whose absence would not fail HTMLProofer."""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
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


def json_ld_records(relative: str, text: str) -> list[dict]:
    records = []
    for block in re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', text, re.DOTALL
    ):
        try:
            records.append(json.loads(block))
        except json.JSONDecodeError as error:
            fail(f"invalid JSON-LD in {relative}: {error}")
    return records


class FigureAudit(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.figures: list[dict] = []
        self.current: dict | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        classes = set((values.get("class") or "").split())
        if tag == "figure" and "content-figure" in classes:
            self.current = {"images": [], "sources": [], "caption": False}
            self.figures.append(self.current)
        elif self.current is not None and tag == "img":
            self.current["images"].append(values)
        elif self.current is not None and tag == "source":
            self.current["sources"].append(values)
        elif self.current is not None and tag == "figcaption":
            self.current["caption"] = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "figure" and self.current is not None:
            self.current = None


def audit_figures(relative: str, text: str) -> int:
    parser = FigureAudit()
    parser.feed(text)
    for figure in parser.figures:
        if len(figure["images"]) != 1 or not figure["caption"]:
            fail(f"content figure lacks one image and caption in {relative}")
        image = figure["images"][0]
        if not image.get("alt") or not image.get("src", "").startswith("/assets/figures/"):
            fail(f"content figure has invalid alt text or source in {relative}")
        for dimension in ("width", "height"):
            if not (image.get(dimension) or "").isdigit():
                fail(f"content figure lacks numeric {dimension} in {relative}")
        if image.get("loading") != "lazy" or image.get("decoding") != "async":
            fail(f"content figure lost loading safeguards in {relative}")
        for source in figure["sources"]:
            if not source.get("srcset", "").startswith("/assets/figures/"):
                fail(f"content figure has nonlocal mobile source in {relative}")
            if not (source.get("width") or "").isdigit() or not (source.get("height") or "").isdigit():
                fail(f"content figure mobile source lacks dimensions in {relative}")
    return len(parser.figures)


def main() -> int:
    engineering = read("engineering/index.html")
    article = read("2026/08/27/three-emulator-bugs.html")
    about = read("about/index.html")
    home = read("index.html")
    feed = read("feed.xml")
    sitemap = read("sitemap.xml")

    if about.count('class="career-thread"') != 1:
        fail("About page does not contain exactly one career-thread diagram")
    if about.count('class="career-thread__year"') != 4:
        fail("career-thread diagram does not contain its four stages")
    if 'id="career-thread-title"' not in about or "Public engineering" not in about:
        fail("career-thread diagram lost its semantic title or parallel engineering stage")
    if "The operating roles continue alongside the PhD" not in about:
        fail("career-thread diagram lost its factual caption")

    home_records = json_ld_records("index.html", home)
    person = next((record for record in home_records if record.get("@type") == "Person"), None)
    if not person:
        fail("homepage is missing Person identity metadata")
    if person.get("name") != "Mihai Dan Nadăș" or person.get("alternateName") != "Mihai Nadăș":
        fail("Person identity metadata does not connect the professional and publishing names")
    for required in (
        "https://github.com/mihainadas",
        "https://www.linkedin.com/in/mihainadas",
        "https://orcid.org/0009-0003-3467-3262",
    ):
        if required not in person.get("sameAs", []):
            fail(f"Person identity metadata is missing {required}")

    article_records = json_ld_records("2026/08/27/three-emulator-bugs.html", article)
    posting = next(
        (record for record in article_records if record.get("@type") == "BlogPosting"), None
    )
    if not posting or posting.get("author", {}).get("@id") != person.get("@id"):
        fail("article author metadata does not reference the canonical person identity")

    if engineering.count("Three Emulator Bugs, Three Different Tests") != 1:
        fail("engineering record does not contain the new article exactly once")
    if home.count("/2026/08/27/three-emulator-bugs.html") != 2:
        fail("homepage does not feature and list the new article")
    if "Three merged 86Box fixes" not in article:
        fail("new article body was not rendered")
    if audit_figures("2026/08/27/three-emulator-bugs.html", article) != 1:
        fail("new article does not exercise the shared figure system exactly once")
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
