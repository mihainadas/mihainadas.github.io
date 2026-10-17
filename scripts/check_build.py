"""Check generated pages whose absence would not fail HTMLProofer."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from zoneinfo import ZoneInfo
from html.parser import HTMLParser
from pathlib import Path
from html import escape


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
POSTS = ROOT / "_posts"
MATHJAX_SOURCE = "https://cdn.jsdelivr.net/npm/mathjax@4/tex-chtml.js"
THESIS_POSTS = (
    ("2025/04/29/three-million-stories-sparse-sample.html", "Three Million Stories Are Still a Sparse Sample"),
    ("2026/05/02/interval-belongs-to-comparison.html", "The Interval Belongs to the Comparison"),
    ("2026/08/27/judges-rank-systems-not-items.html", "The Panel Was Weak on Items and Useful for Ranking Systems"),
    ("2026/08/27/change-one-slot-watch-what-else-moves.html", "Change One Slot, Watch What Else Moves"),
    ("2026/08/27/small-model-diacritics-noise.html", "When Noisy Text Changes the Winning Model"),
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

    expected = []
    for _, source, text in published_sources():
        stamp = next((front_matter_value(text, key) for key in ("feed_date", "published_at", "date") if front_matter_value(text, key)), None)
        publication = datetime.fromisoformat(stamp)
        if publication.tzinfo is None:
            publication = publication.replace(tzinfo=ZoneInfo("Europe/Bucharest"))
        if publication <= feed_updated:
            expected.append((publication, front_matter_value(text, "title")))
    limit_match = re.search(r"(?m)^\s*posts_limit:\s*(\d+)", (ROOT / "_config.yml").read_text(encoding="utf-8"))
    limit = int(limit_match.group(1)) if limit_match else 20
    actual_titles = {entry.findtext("atom:title", namespaces=namespace) for entry in root.findall("atom:entry", namespace)}
    ordered = sorted(expected, key=lambda row: row[0], reverse=True)
    # Publication times may tie at the cutoff. Require every strictly newer item.
    cutoff = ordered[min(limit, len(ordered)) - 1][0]
    required = {title for published, title in ordered if published > cutoff}
    eligible = {title for published, title in ordered if published >= cutoff}
    if not required.issubset(actual_titles) or not actual_titles.issubset(eligible) or len(actual_titles) != min(limit, len(ordered)):
        fail("feed omits recent publications or includes older entries ahead of them")


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


def front_matter_value(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", text)
    return match.group(1).strip("\"'") if match else None


def published_sources() -> list[tuple[datetime, Path, str]]:
    """Use front-matter dates, not filename order, and omit future/draft posts."""
    now = datetime.now(ZoneInfo("Europe/Bucharest"))
    posts = []
    for source in POSTS.glob("*.md"):
        text = source.read_text(encoding="utf-8")
        stamp = datetime.fromisoformat(front_matter_value(text, "date"))
        if stamp.tzinfo is None:
            stamp = stamp.replace(tzinfo=ZoneInfo("Europe/Bucharest"))
        if stamp <= now and front_matter_value(text, "published") != "false" and front_matter_value(text, "draft") != "true":
            posts.append((stamp, source, text))
    return sorted(posts, key=lambda item: item[0], reverse=True)


def audit_math_pages() -> None:
    loader = f'<script defer src="{MATHJAX_SOURCE}"></script>'
    math_pages = 0
    sources = [source for _, source, _ in published_sources()] + [p for p in sorted(list(ROOT.glob("*.md")) + list((ROOT / "ro").rglob("*.md"))) if front_matter_value(p.read_text(encoding="utf-8"), "layout")]
    for source in sources:
        source_text = source.read_text(encoding="utf-8")
        post_date = front_matter_value(source_text, "date")
        if source.parent == POSTS:
            if not post_date or not re.fullmatch(r"\d{4}-\d{2}-\d{2}.*", post_date):
                fail(f"post date is missing or invalid in {source.name}")
            date_part = post_date[:10].replace("-", "/")
            slug = source.stem[11:]
            relative = f"{date_part}/{slug}.html"
        else:
            permalink = front_matter_value(source_text, "permalink")
            if permalink and permalink.endswith(".html"):
                relative = permalink.lstrip("/")
            else:
                relative = permalink.strip("/") + "/index.html" if permalink else "index.html"
        rendered = read(relative)
        declared_math = front_matter_value(source_text, "math") == "true"
        if declared_math:
            math_pages += 1
            if rendered.count(loader) != 1:
                fail(f"MathJax loader missing or duplicated in {relative}")
            if not re.search(r"(?<!\\)\\(?:\(|\[)", rendered):
                fail(f"Markdown did not preserve math delimiters in {relative}")
            display_openings = len(re.findall(r"(?<!\\)\\\[", rendered))
            display_closings = len(re.findall(r"(?<!\\)\\\]", rendered))
            intact_displays = len(
                re.findall(r"<p>\s*\\\[.*?\\\]\s*</p>", rendered, re.DOTALL)
            )
            if display_openings != display_closings or display_openings != intact_displays:
                fail(f"Markdown split or damaged display math in {relative}")
        elif loader in rendered:
            fail(f"MathJax loaded on a page without mathematics: {relative}")
        if 'class="equation"' in rendered:
            fail(f"legacy code-styled equation remains in {relative}")

    if math_pages < 1:
        fail("generated site has no declared math pages")


class LanguageMetadata(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.lang = None
        self.canonicals = []
        self.alternates = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.lang = values.get("lang")
        if tag == "link" and values.get("rel") == "canonical":
            self.canonicals.append(values.get("href"))
        if tag == "link" and values.get("rel") == "alternate" and values.get("hreflang"):
            self.alternates.append((values["hreflang"], values.get("href")))


def audit_localized_html(text: str, lang: str, canonical: str, alternates: dict[str, str]) -> None:
    metadata = LanguageMetadata()
    metadata.feed(text)
    if metadata.lang != lang or metadata.canonicals != [canonical]:
        fail("localized page has a missing language or incorrect self-canonical URL")
    if len(metadata.alternates) != len(alternates) or dict(metadata.alternates) != alternates:
        fail("localized page lacks exact reciprocal language metadata")


def audit_localized_pages(feed: str, sitemap: str) -> None:
    english_sources = list(ROOT.glob("*.md")) + list(POSTS.glob("*.md"))
    editions = sorted((ROOT / "ro").rglob("*.md"))
    notes = []
    for edition in editions:
        source_text = edition.read_text(encoding="utf-8")
        reference = front_matter_value(source_text, "translation_source")
        if not reference:
            continue
        original = ROOT / reference
        if original not in english_sources:
            fail(f"localized page has an invalid English source: {edition.name}")
        original_text = original.read_text(encoding="utf-8")
        english_url = front_matter_value(source_text, "translation_source_url")
        romanian_url = front_matter_value(source_text, "permalink")
        alternates = {"en": "https://mihainadas.github.io" + english_url, "ro": "https://mihainadas.github.io" + romanian_url}
        for lang, url in (("en", english_url), ("ro", romanian_url)):
            relative = url.lstrip("/") + ("index.html" if url.endswith("/") else "")
            rendered = read(relative)
            audit_localized_html(rendered, lang, alternates[lang], alternates)
            counterpart = romanian_url if lang == "en" else english_url
            if 'class="language-note"' not in rendered or f'href="{counterpart}"' not in rendered:
                fail(f"exact language switch is missing in {relative}")
            if sitemap.count(alternates[lang]) != 1:
                fail(f"localized URL is missing or duplicated in the sitemap: {relative}")
        rendered_ro = read(romanian_url.strip("/") + "/index.html")
        if front_matter_value(source_text, "layout") == "translated-post":
            notes.append(front_matter_value(source_text, "title"))
            if "Ce ar merita explicat mai clar?" not in rendered_ro or "Where did I lose you?" in rendered_ro:
                fail("Romanian article feedback is not localized")
            posting = next((item for item in json_ld_records(romanian_url, rendered_ro) if item.get("@type") == "BlogPosting"), {})
            if posting.get("inLanguage") != "ro" or posting.get("translationOfWork", {}).get("url") != alternates["en"]:
                fail("Romanian article lost its language or source-work metadata")
            if alternates["ro"] in feed:
                fail("Romanian edition was duplicated in the English feed")
    landing = read("ro/index.html")
    audit_localized_html(landing, "ro", "https://mihainadas.github.io/ro/", {})
    if len(notes) < 2 or any(escape(title, quote=False) not in landing for title in notes):
        fail("Romanian landing page lost a published edition")


class PageAssets(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.images: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "img":
            self.images.append(dict(attrs))


def audit_editorial_assets(home: str) -> None:
    parser = PageAssets()
    parser.feed(home)
    images = [image for image in parser.images if (image.get("src") or "").startswith("/assets/editorial/")]
    if len(images) != 2:
        fail("homepage lost its two editorial studies")
    for image in images:
        if not image.get("alt") or image.get("width") != "1440" or image.get("height") != "960":
            fail("editorial artwork lacks descriptive alt text or intrinsic dimensions")
        variants = [entry.strip().split() for entry in image.get("srcset", "").split(",")]
        if len(variants) != 3 or {entry[-1] for entry in variants if entry} != {"480w", "960w", "1440w"}:
            fail("editorial artwork lost its responsive sources")
        for entry in variants:
            source = entry[0]
            if not source.startswith("/assets/editorial/") or not source.endswith(".webp"):
                fail("editorial artwork uses a remote or non-WebP source")
            path = SITE / source.lstrip("/")
            if not path.is_file() or path.stat().st_size > 200_000:
                fail(f"editorial artwork is missing or exceeds 200 KB: {source}")
        if "structure-" in image["src"] and (image.get("fetchpriority") != "high" or image.get("loading") == "lazy"):
            fail("hero artwork must load eagerly with high priority")
        if "signal-" in image["src"] and image.get("loading") != "lazy":
            fail("below-fold artwork must load lazily")
    for name in ("manrope-latin", "newsreader-latin", "newsreader-italic-latin"):
        path = SITE / "assets" / "fonts" / f"{name}.woff2"
        if not path.is_file() or path.stat().st_size > 100_000:
            fail(f"self-hosted font is missing or exceeds 100 KB: {name}")


def main() -> int:
    engineering = read("engineering/index.html")
    article = read("2026/08/27/three-emulator-bugs.html")
    about = read("about/index.html")
    home = read("index.html")
    feed = read("feed.xml")
    sitemap = read("sitemap.xml")
    theme_script = read("assets/theme.js")
    research = read("research/index.html")
    papers = read("papers/index.html")
    applied_note = read("2026/10/17/deep-research-needs-evidence-budget.html")
    audit_feed_chronology(feed)
    audit_math_pages()
    audit_editorial_assets(home)
    audit_localized_pages(feed, sitemap)

    issue_numbers = [int(value) for value in re.findall(r'data-issue="(\d+)"', papers)]
    groups = json.loads((ROOT / "_data" / "papers.json").read_text(encoding="utf-8"))
    expected_issues = {paper["issue"] for group in groups for paper in group["papers"]}
    if len(issue_numbers) != len(expected_issues) or set(issue_numbers) != expected_issues:
        fail("rendered applied-papers map lost or duplicated an issue")
    if papers.count("Deep Research Needs an Evidence Budget") != 1:
        fail("applied-papers page does not list the published note exactly once")
    if "Four budgets make the process inspectable" not in applied_note:
        fail("applied-papers note body was not rendered")
    if "a-rubric-is-a-control-system" in sitemap:
        fail("unpublished applied-papers draft leaked into the sitemap")

    notebooks = read("lab-notebooks/index.html")
    if '<nav class="site-nav"' not in notebooks or "/lab-notebooks/" not in home:
        fail("notebook collection lost the blog navigation or homepage route")
    archive = read("archive/index.html")
    post_records = published_sources()
    if archive.count("data-filter-item") != len(post_records):
        fail("archive lost a published post")
    for rendered in (papers, archive):
        if "data-filter-list" not in rendered or "data-status" not in rendered:
            fail("discovery page lost its filter controls or accessible status")
    latest_title = front_matter_value(post_records[0][2], "title")
    now = re.search(r'<div class="now-latest">(.*?)</div>', home, re.DOTALL)
    if not now or escape(latest_title, quote=False) not in now.group(1):
        fail("homepage no longer shows the latest eligible note")
    for thread_id, post_type in (("engineering", "engineering note"), ("research", "research note"), ("papers", "applied research note")):
        block = re.search(rf'<article class="thread" data-thread="{thread_id}">(.*?)</article>', home, re.DOTALL)
        expected_title = next(front_matter_value(text, "title") for _, _, text in post_records if front_matter_value(text, "post_type") == post_type)
        if not block or escape(expected_title, quote=False) not in block.group(1):
            fail(f"homepage thread {thread_id} lost its latest eligible note")
    notebooks_data = json.loads((ROOT / "_data" / "notebooks.json").read_text(encoding="utf-8"))
    for label in (f"{len(post_records)} field notes", f"{len(expected_issues)} papers mapped", f"{len(notebooks_data)} executable notebooks"):
        if label not in home:
            fail(f"homepage count disagrees with source data: {label}")
    if '<meta property="og:image"' not in home or not (SITE / "assets/social-card.png").exists():
        fail("social preview image is missing")
    for _, post_source, text in post_records:
        date_part = front_matter_value(text, "date")[:10].replace("-", "/")
        rendered = read(f"{date_part}/{post_source.stem[11:]}.html")
        if 'class="post-continuation"' not in rendered:
            fail(f"post lacks onward navigation: {post_source.name}")

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
    selected = re.search(
        r'<section aria-labelledby="selected-heading">(.*?)</section>', home, re.DOTALL
    )
    if not selected or selected.group(1).count("/2026/08/27/three-emulator-bugs.html") != 1:
        fail("homepage does not feature the selected engineering article exactly once")
    if "The hard part was not landing three fixes" not in article:
        fail("new article body was not rendered")
    if audit_figures("2026/08/27/three-emulator-bugs.html", article) != 1:
        fail("new article does not exercise the shared figure system exactly once")
    if '<title type="html">The Panel Was Weak on Items and Useful for Ranking Systems</title>' in feed:
        judge_entry = atom_entry(feed, "The Panel Was Weak on Items and Useful for Ranking Systems")
        if "<published>2026-08-27T09:11:56+03:00</published>" not in judge_entry:
            fail("feed publishes the judge retrospective under its event date")
    for url in (
        "https://mihainadas.github.io/engineering/",
        "https://mihainadas.github.io/2026/08/27/three-emulator-bugs.html",
        "https://mihainadas.github.io/papers/",
        "https://mihainadas.github.io/2026/10/17/deep-research-needs-evidence-budget.html",
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
