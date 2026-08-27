"""Check generated pages whose absence would not fail HTMLProofer."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
THESIS_POSTS = (
    ("2025/04/29/three-million-stories-sparse-sample.html", "Three Million Stories Are Still a Sparse Sample"),
    ("2026/05/02/interval-belongs-to-comparison.html", "The Interval Belongs to the Comparison"),
    ("2026/08/27/judges-rank-systems-not-items.html", "The Panel Was Weak on Items and Useful for Ranking Systems"),
    ("2026/08/27/change-one-slot-watch-what-else-moves.html", "Change One Slot, Watch What Else Moves"),
    ("2026/08/27/small-model-diacritics-noise.html", "The 2.4M-Parameter Model Won—Until the Text Got Noisy"),
    ("2026/08/27/adaptation-could-not-remove-scraper-artifact.html", "Ten Thousand Adaptation Steps Could Not Remove One Scraper Artifact"),
)


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


def atom_entry(feed: str, title: str) -> str:
    match = re.search(
        rf"<entry.*?<title type=\"html\">{re.escape(title)}</title>.*?</entry>",
        feed,
        re.DOTALL,
    )
    if not match:
        fail(f"feed entry missing: {title}")
    return match.group(0)


def audit_feed_chronology(feed: str) -> None:
    try:
        root = ET.fromstring(feed)
    except ET.ParseError as error:
        fail(f"invalid Atom feed: {error}")
    namespace = {"atom": "http://www.w3.org/2005/Atom"}
    feed_updated_text = root.findtext("atom:updated", namespaces=namespace)
    if not feed_updated_text:
        fail("feed lacks an updated timestamp")
    feed_updated = datetime.fromisoformat(feed_updated_text)
    published_dates: list[datetime] = []
    for entry in root.findall("atom:entry", namespace):
        published_text = entry.findtext("atom:published", namespaces=namespace)
        updated_text = entry.findtext("atom:updated", namespaces=namespace)
        if not published_text or not updated_text:
            fail("feed entry lacks published or updated timestamp")
        published = datetime.fromisoformat(published_text)
        updated = datetime.fromisoformat(updated_text)
        if published > feed_updated or updated > feed_updated:
            fail("feed entry timestamp is later than the feed update")
        published_dates.append(published)
    if published_dates != sorted(published_dates, reverse=True):
        fail("feed entries are not ordered by publication timestamp")


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
    theme_script = read("assets/theme.js")
    research = read("research/index.html")
    audit_feed_chronology(feed)

    theme_bootstrap = home.find('window.localStorage.getItem("mihainadas-theme")')
    stylesheet = home.find('/assets/main.css')
    if theme_bootstrap < 0 or stylesheet < 0 or theme_bootstrap > stylesheet:
        fail("theme preference is not applied before the stylesheet")
    if 'id="theme-preference"' not in home:
        fail("homepage is missing the theme preference control")
    for value, label in (("system", "System"), ("light", "Light"), ("dark", "Dark")):
        if f'<option value="{value}">{label}</option>' not in home:
            fail(f"theme preference control is missing its {label} option")
    for required in (
        'window.matchMedia("(prefers-color-scheme: dark)")',
        'window.localStorage.setItem(storageKey, preference)',
        'window.localStorage.removeItem(storageKey)',
        'root.setAttribute("data-theme", preference)',
        'root.removeAttribute("data-theme")',
    ):
        if required not in theme_script:
            fail(f"theme script lost required behavior: {required}")

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
    if "The hard part was not landing three fixes" not in article:
        fail("new article body was not rendered")
    if audit_figures("2026/08/27/three-emulator-bugs.html", article) != 1:
        fail("new article does not exercise the shared figure system exactly once")
    if feed.count('<title type="html">Three Emulator Bugs, Three Different Tests</title>') != 1:
        fail("global feed does not contain the new article exactly once")
    judge_entry = atom_entry(feed, "The Panel Was Weak on Items and Useful for Ranking Systems")
    if "<published>2026-08-27T09:11:56+03:00</published>" not in judge_entry:
        fail("feed publishes the judge retrospective under its event date")
    for url in (
        "https://mihainadas.github.io/engineering/",
        "https://mihainadas.github.io/2026/08/27/three-emulator-bugs.html",
    ):
        if sitemap.count(url) != 1:
            fail(f"sitemap does not contain {url} exactly once")

    for relative, title in THESIS_POSTS:
        rendered = read(relative)
        if title not in rendered:
            fail(f"thesis-series title was not rendered in {relative}")
        if rendered.count('class="series-note"') != 1:
            fail(f"thesis-series navigation missing in {relative}")
        if audit_figures(relative, rendered) != 1:
            fail(f"thesis-series figure missing or duplicated in {relative}")
        public_url = f"https://mihainadas.github.io/{relative}"
        if sitemap.count(public_url) != 1:
            fail(f"sitemap does not contain {public_url} exactly once")
        if title not in research:
            fail(f"research index is missing thesis-series title: {title}")
        atom_entry(feed, title)

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

    for path in SITE.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".html", ".xml", ".svg", ".js", ".css"}:
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"(?i)\bklusai\b|github\.com/klusai(?:/|$)|huggingface\.co/(?:datasets|models|spaces)/klusai(?:/|$)", text):
            fail(f"stealth program reference in generated artifact: {path.relative_to(SITE)}")

    print("generated site checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
