"""Fast, dependency-free checks for posts and code fences."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    from scripts.check_books import check_books
    from scripts.check_media import validate_media
    from scripts.check_professional import validate_professional
except ModuleNotFoundError:
    from check_books import check_books
    from check_media import validate_media
    from check_professional import validate_professional


ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"
PAPER_MAP = ROOT / "papers.md"
PUBLIC_ENGINEERING_FILES = (
    ROOT / "index.md",
    ROOT / "about.md",
    ROOT / "engineering.md",
    ROOT / "_posts" / "2026-08-27-three-emulator-bugs.md",
)
ARTIFACT_DATES = {
    "2025-04-29-tf1-arxiv-release.md": date(2025, 4, 29),
    "2025-09-09-tf2-preprint-release.md": date(2025, 9, 9),
    "2026-01-15-tf3-romanian-microfiction.md": date(2026, 1, 15),
}
THESIS_SERIES = (
    "2025-04-29-three-million-stories-sparse-sample.md",
    "2026-05-02-interval-belongs-to-comparison.md",
    "2026-08-22-judges-rank-systems-not-items.md",
    "2026-08-27-change-one-slot-watch-what-else-moves.md",
    "2026-08-27-small-model-diacritics-noise.md",
    "2026-08-27-adaptation-could-not-remove-scraper-artifact.md",
)
MIN_OPENING_PARAGRAPH_WORDS = 12
MIN_OPENING_TOTAL_WORDS = 60
MATHJAX_SOURCE = "https://cdn.jsdelivr.net/npm/mathjax@4/tex-chtml.js"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def opening_prose_paragraphs(text: str) -> tuple[str, ...]:
    """Return substantive prose paragraphs before the first level-two heading."""

    parts = text.split("---", 2)
    body = parts[2] if len(parts) == 3 else ""
    opening = re.split(r"(?m)^##\s+", body, maxsplit=1)[0]
    opening = re.sub(r"```.*?```|~~~.*?~~~", "", opening, flags=re.DOTALL)
    opening = re.sub(r"{%.*?%}|<!--.*?-->", "", opening, flags=re.DOTALL)
    opening = re.sub(r"\\\\\[.*?\\\\\]", "", opening, flags=re.DOTALL)

    paragraphs: list[str] = []
    for block in re.split(r"\n\s*\n", opening):
        lines = []
        for line in block.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith((">", "- ", "* ", "|")):
                continue
            lines.append(stripped)
        paragraph = " ".join(lines)
        if len(re.findall(r"\b[\w'-]+\b", paragraph)) >= MIN_OPENING_PARAGRAPH_WORDS:
            paragraphs.append(paragraph)
    return tuple(paragraphs)


def math_markup_error(text: str) -> str | None:
    """Validate Markdown-safe MathJax delimiters outside code spans and fences."""

    parts = text.split("---", 2)
    body = parts[2] if len(parts) == 3 else text
    body = re.sub(r"```.*?```|~~~.*?~~~", "", body, flags=re.DOTALL)
    body = re.sub(r"`+[^`\n]*`+", "", body)

    markdown_escaped_tex = set('#{}!|_:+-.<>*()[]')
    for match in re.finditer(r"(?<!\\)(\\+)(.)", body):
        if match.group(2) in markdown_escaped_tex and len(match.group(1)) != 2:
            return "TeX punctuation must use two source backslashes so Markdown preserves it"

    if re.search(r"(?<!\\)\$\$", body):
        return "display math must use the canonical escaped \\\\[...\\\\] delimiters"

    tokens = re.findall(r"\\\\(?:\(|\)|\[|\])", body)
    stack: list[str] = []
    pairs = {")": "(", "]": "["}
    for token in tokens:
        delimiter = token[-1]
        if delimiter in "([":
            if stack:
                return "math delimiters may not be nested"
            stack.append(delimiter)
        elif not stack or stack.pop() != pairs[delimiter]:
            return f"unmatched math delimiter: \\\\{delimiter}"
    if stack:
        return f"unclosed math delimiter: \\\\{stack[-1]}"
    return None


def contains_math(text: str) -> bool:
    parts = text.split("---", 2)
    body = parts[2] if len(parts) == 3 else text
    body = re.sub(r"```.*?```|~~~.*?~~~", "", body, flags=re.DOTALL)
    body = re.sub(r"`+[^`\n]*`+", "", body)
    return bool(re.search(r"\\\\(?:\(|\[)", body))


def check_posts() -> None:
    for path in sorted(POSTS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if "\ufffc" in text:
            fail(f"object-replacement character in {path.name}")
        if "http://mihainadas.github.io" in text:
            fail(f"insecure internal link in {path.name}")
        if re.search(r"(?i)happy (coding|learning)!|excited to share", text):
            fail(f"promotional stock phrase in {path.name}")

        math_error = math_markup_error(text)
        if math_error:
            fail(f"{math_error} in {path.name}")
        declared_math = front_matter_value(text, "math")
        uses_math = contains_math(text)
        if uses_math and declared_math != "true":
            fail(f"math markup requires 'math: true' in {path.name}")
        if declared_math == "true" and not uses_math:
            fail(f"math is enabled but unused in {path.name}")
        if declared_math not in {None, "true"}:
            fail(f"math front matter must be true or omitted in {path.name}")

        reviewed = front_matter_value(text, "context_reviewed")
        try:
            date.fromisoformat(reviewed or "")
        except ValueError:
            fail(f"context_reviewed must be an ISO date in {path.name}")

        opening = opening_prose_paragraphs(text)
        opening_words = sum(len(re.findall(r"\b[\w'-]+\b", paragraph)) for paragraph in opening)
        if len(opening) < 2 or opening_words < MIN_OPENING_TOTAL_WORDS:
            fail(
                f"opening context is too thin in {path.name}: "
                f"need two prose paragraphs and {MIN_OPENING_TOTAL_WORDS} words before the first H2"
            )

        for index, match in enumerate(re.finditer(r"```python\n(.*?)```", text, re.DOTALL), start=1):
            try:
                ast.parse(match.group(1))
            except SyntaxError as error:
                fail(f"invalid Python fence {index} in {path.name}: {error}")

    for filename, earliest in ARTIFACT_DATES.items():
        path = POSTS / filename
        if not path.exists():
            fail(f"expected chronology-correct post missing: {filename}")
        actual = date.fromisoformat(filename[:10])
        if actual < earliest:
            fail(f"{filename} predates its artifact")


def front_matter_value(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", text)
    return match.group(1).strip("\"'") if match else None


def language_source_signature(text: str) -> str:
    """Fingerprint content and material declarations, not review-only metadata."""
    parts = text.split("---", 2)
    content = [
        front_matter_value(text, "title"),
        front_matter_value(text, "description"),
        front_matter_value(text, "evidence_status"),
        front_matter_value(text, "math"),
        front_matter_value(text, "post_type"),
        parts[2] if len(parts) == 3 else text,
    ]
    return hashlib.sha256(json.dumps(content, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def localized_sources(root: Path) -> list[Path]:
    return sorted(set(root.glob("*.md")) | set((root / "_posts").glob("*.md")) | set((root / "ro").rglob("*.md")))


def source_url(path: Path, text: str, root: Path) -> str:
    if path.parent == root / "_posts":
        stamp = front_matter_value(text, "date")
        if not stamp or not re.match(r"\d{4}-\d{2}-\d{2}", stamp):
            fail(f"translation source lacks a valid post date: {path.name}")
        return f"/{stamp[:10].replace('-', '/')}/{path.stem[11:]}.html"
    return front_matter_value(text, "permalink") or "/"


def check_localization(root: Path | None = None) -> None:
    root = root or ROOT
    records = {}
    groups = {}
    for path in localized_sources(root):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n") or not front_matter_value(text, "layout"):
            continue
        records[path] = text
        lang = front_matter_value(text, "lang") or "en"
        if lang not in {"en", "ro"}:
            fail(f"unsupported page language in {path.relative_to(root)}")
        key = front_matter_value(text, "translation_key")
        if key:
            peers = groups.setdefault(key, {})
            if lang in peers:
                fail(f"duplicate {lang} edition for {key}")
            peers[lang] = path
        reviewed = front_matter_value(text, "editorial_reviewed")
        post_date = front_matter_value(text, "date") or ""
        if path.parent == root / "_posts" and post_date[:10] >= "2026-10-17" and not reviewed:
            fail(f"new post requires a completed editorial review: {path.name}")
        if reviewed:
            try:
                review_date = date.fromisoformat(reviewed)
            except ValueError:
                fail(f"invalid editorial review date in {path.name}")
            if review_date > datetime.now(ZoneInfo("Europe/Bucharest")).date():
                fail(f"editorial review is future-dated in {path.name}")
            if "—" in text:
                fail(f"em dash in editorially reviewed file: {path.name}")

    for key, peers in groups.items():
        if set(peers) != {"en", "ro"}:
            fail(f"translation group {key} must contain exactly one English and one Romanian edition")
        if not front_matter_value(records[peers["ro"]], "translation_source"):
            fail(f"Romanian edition lacks its English source: {key}")

    for path, text in records.items():
        reference = front_matter_value(text, "translation_source")
        if not reference:
            continue
        relative = Path(reference)
        if relative.is_absolute() or ".." in relative.parts:
            fail(f"unsafe translation source in {path.name}")
        source = root / relative
        if source not in records or (front_matter_value(records[source], "lang") or "en") != "en":
            fail(f"translation source is missing or not English: {path.name}")
        original = records[source]
        key = front_matter_value(text, "translation_key")
        if not key or key != front_matter_value(original, "translation_key") or groups[key].get("ro") != path:
            fail(f"translation pair does not match its declared source: {path.name}")
        if front_matter_value(text, "translation_source_url") != source_url(source, original, root):
            fail(f"translation points to the wrong original URL: {path.name}")
        if front_matter_value(text, "translation_source_sha256") != language_source_signature(original):
            fail(f"translation is stale; review it against the changed English source: {path.name}")
        for field in ("context_reviewed", "translation_reviewed", "editorial_reviewed"):
            try:
                stamp = date.fromisoformat(front_matter_value(text, field) or "")
            except ValueError:
                fail(f"{field} must record a completed review in {path.name}")
            if stamp > datetime.now(ZoneInfo("Europe/Bucharest")).date():
                fail(f"future review date in {path.name}")
        paragraphs = opening_prose_paragraphs(text)
        if len(paragraphs) < 2 or sum(len(re.findall(r"\b[\w'-]+\b", p)) for p in paragraphs) < MIN_OPENING_TOTAL_WORDS:
            fail(f"translation opening lacks standalone context: {path.name}")
        error = math_markup_error(text)
        if error or (contains_math(text) and front_matter_value(text, "math") != "true"):
            fail(f"translation math declaration or delimiters are invalid: {path.name}")
        original_body, translated_body = original.split("---", 2)[2], text.split("---", 2)[2]
        urls = lambda body: set(re.findall(r'https://[^\s<>"\)\]]+', body))
        if not urls(original_body).issubset(urls(translated_body)):
            fail(f"translation dropped a public source link: {path.name}")
        fences = lambda body: re.findall(r"```.*?```", body, re.DOTALL)
        if fences(original_body) != fences(translated_body):
            fail(f"translation changed or omitted a code/output block: {path.name}")


def check_thesis_series() -> None:
    orders: list[int] = []
    forbidden = re.compile(
        r"\b(?:delve(?:s|d)?|game[- ]changing|transformative|pivotal|"
        r"unlock(?:s|ed|ing)?|seamless(?:ly)?|rapidly evolving landscape)\b|"
        r"^## Why this matters\s*$",
        re.IGNORECASE | re.MULTILINE,
    )
    for filename in THESIS_SERIES:
        path = POSTS / filename
        if not path.exists():
            fail(f"thesis-series post missing: {filename}")
        text = path.read_text(encoding="utf-8")
        if front_matter_value(text, "series") != "controlled-synthetic-narratives":
            fail(f"thesis-series metadata missing in {filename}")
        order = front_matter_value(text, "series_order")
        if order is None or not order.isdigit():
            fail(f"thesis-series order is invalid in {filename}")
        orders.append(int(order))
        status = front_matter_value(text, "evidence_status")
        if status not in {"published-analysis", "thesis-analysis", "accepted", "thesis-only"}:
            fail(f"thesis-series evidence status is invalid in {filename}")
        if "{% include thesis-series.html %}" not in text:
            fail(f"thesis-series navigation missing in {filename}")
        if not re.search(r"> \*\*(?:Archive note|Evidence status)\.", text):
            fail(f"visible chronology or evidence note missing in {filename}")
        if forbidden.search(text):
            fail(f"AI-smell phrase in thesis series: {filename}")

        historical = date.fromisoformat(filename[:10]) < date(2026, 8, 27)
        if historical and front_matter_value(text, "published_at") is None:
            fail(f"backdated thesis-series post lacks a publication timestamp: {filename}")

    if sorted(orders) != list(range(1, len(THESIS_SERIES) + 1)) or len(set(orders)) != len(orders):
        fail("thesis-series order must be unique and contiguous")


def check_math_system() -> None:
    include = ROOT / "_includes" / "mathjax.html"
    if not include.exists():
        fail("MathJax include is missing")
    include_text = include.read_text(encoding="utf-8")
    for required in (
        'inlineMath: [["\\\\(", "\\\\)"]]',
        'displayMath: [["\\\\[", "\\\\]"]]',
        'displayOverflow: "scroll"',
        f'<script defer src="{MATHJAX_SOURCE}"></script>',
    ):
        if required not in include_text:
            fail(f"MathJax include lost required configuration: {required}")

    # Root pages can contain equations too; they share the post renderer.
    for source in sorted(ROOT.glob("*.md")):
        text = source.read_text(encoding="utf-8")
        if front_matter_value(text, "layout") is None:
            continue
        error = math_markup_error(text)
        if error:
            fail(f"{error} in {source.name}")
        if contains_math(text) and front_matter_value(text, "math") != "true":
            fail(f"math markup requires 'math: true' in {source.name}")

    head = (ROOT / "_includes" / "head.html").read_text(encoding="utf-8")
    if "{% if page.math %}{% include mathjax.html %}{% endif %}" not in head:
        fail("MathJax is not conditionally loaded from page front matter")


def check_current_work() -> None:
    now = (ROOT / "_data" / "now.yml").read_text(encoding="utf-8")
    try:
        reviewed = date.fromisoformat(front_matter_value(now, "reviewed") or "")
    except ValueError:
        fail("current-work review date must be an ISO date")
    age = (datetime.now(ZoneInfo("Europe/Bucharest")).date() - reviewed).days
    if age < 0:
        fail("current-work review date is in the future")
    if age > 45:
        print(f"::warning::Current-work data was last reviewed {age} days ago; review _data/now.yml.")


def check_repository_hygiene() -> None:
    junk_names = re.compile(r"(?:^\.DS_Store$|^\._|~$|\.(?:bak|orig|rej|swp)$| 2\.[^.]+$)")
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if {".git", "_site", "vendor"}.intersection(relative.parts):
            continue
        if path.is_file() and junk_names.search(path.name):
            fail(f"repository junk file: {relative}")

    public_text_files = [
        ROOT / name
        for name in ("index.md", "about.md", "engineering.md", "research.md", "papers.md", "business.md", "work-with-me.md", "resume.md")
    ]
    public_text_files.extend(sorted(POSTS.glob("*.md")))
    placeholder = re.compile(r"\b(?:TODO|FIXME|XXX)\b|lorem ipsum", re.IGNORECASE)
    for path in public_text_files:
        text = path.read_text(encoding="utf-8")
        if placeholder.search(text):
            fail(f"placeholder text in {path.relative_to(ROOT)}")
        if re.search(r"(?m)[ \t]+$", text):
            fail(f"trailing whitespace in {path.relative_to(ROOT)}")


def check_applied_papers() -> None:
    if not PAPER_MAP.exists():
        fail("applied-papers map is missing")
    text = PAPER_MAP.read_text(encoding="utf-8")
    expected = set(range(551, 641)) - {580, 586}
    groups = json.loads((ROOT / "_data" / "papers.json").read_text(encoding="utf-8"))
    issues = [paper["issue"] for group in groups for paper in group["papers"]]
    if not expected.issubset(issues) or len(issues) != len(set(issues)):
        fail("applied-papers map lost an original issue or contains duplicates")
    if len(groups) != 5 or len({group["id"] for group in groups}) != 5:
        fail("applied-papers map must retain five distinct themes")
    for group in groups:
        for paper in group["papers"]:
            if not all(paper.get(key) for key in ("title", "contribution", "business")):
                fail(f"paper {paper['issue']} is incomplete")
            if not paper["url"].startswith("https://"):
                fail(f"paper {paper['issue']} has an insecure source")
    if "—" in json.dumps(groups, ensure_ascii=False):
        fail("applied-papers data contains an em dash")
    if 'where: "series", "applied-paper-notes"' not in text:
        fail("applied-papers page no longer renders its article series")
    if "—" in text:
        fail("applied-papers map contains an em dash")

    series_posts = []
    for path in sorted(POSTS.glob("*.md")):
        post = path.read_text(encoding="utf-8")
        if front_matter_value(post, "series") == "applied-paper-notes":
            series_posts.append(path)
            if "—" in post:
                fail(f"applied-paper note contains an em dash: {path.name}")
    if not series_posts:
        fail("applied-papers series has no published notes")


def check_engineering_boundary() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in {".html", ".md", ".py", ".svg", ".yml", ".yaml", ".json"}:
            continue
        if {".git", "_site", "vendor"}.intersection(path.relative_to(ROOT).parts):
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"/(?:Users|private/tmp)/", text):
            fail(f"private filesystem path in {path.relative_to(ROOT)}")
        if re.search(r"(?i)github\.com/klusai(?:/|$)", text):
            fail(f"stealth repository link in {path.relative_to(ROOT)}")

    engineering_posts = []
    for path in sorted(POSTS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if re.search(r"(?m)^post_type:\s*engineering note\s*$", text):
            engineering_posts.append(path)

    if len(engineering_posts) < 5:
        fail("engineering record unexpectedly lost posts")

    paths = (*PUBLIC_ENGINEERING_FILES, *engineering_posts)
    for path in dict.fromkeys(paths):
        if not path.exists():
            fail(f"expected engineering file missing: {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        if re.search(
            r"(?i)github\.com/klusai|\bklusai\b|"
            r"huggingface\.co/(?:datasets|models|spaces)/klusai(?:/|$)|"
            r"\b(?:RES|KLU)-\d+\b",
            text,
        ):
            fail(f"private program reference in {path.relative_to(ROOT)}")

    engineering = (ROOT / "engineering.md").read_text(encoding="utf-8")
    if 'where: "post_type", "engineering note"' not in engineering:
        fail("engineering page no longer renders the engineering-note record")
    for required in (
        "https://github.com/86Box/86Box/pull/7772",
        "https://github.com/86Box/86Box/pull/7774",
        "https://github.com/86Box/86Box/pull/7777",
        "https://github.com/86Box/86Box/pull/7787",
        "https://github.com/mihainadas/86box-vm-recipes",
        "https://github.com/mihainadas/retro-hardware-lab",
    ):
        if required not in engineering:
            fail(f"engineering evidence link missing: {required}")


def check_figure_system() -> None:
    figure = ROOT / "_includes" / "figure.html"
    if not figure.exists():
        fail("shared figure include is missing")
    figure_text = figure.read_text(encoding="utf-8")
    for required in (
        'class="content-figure',
        'alt="{{ include.alt | escape }}"',
        'loading="lazy"',
        "<figcaption>",
    ):
        if required not in figure_text:
            fail(f"shared figure include lost required behavior: {required}")

    referenced_assets: set[Path] = set()
    expected_dimensions: dict[Path, tuple[int, int]] = {}
    figure_calls = 0
    for path in ROOT.rglob("*.md"):
        if {".git", "_site", "vendor"}.intersection(path.relative_to(ROOT).parts):
            continue
        if path == ROOT / "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"{%\s*include\s+figure\.html\s+(.*?)%}", text, re.DOTALL):
            figure_calls += 1
            attributes = dict(re.findall(r'(\w+)=["\']([^"\']*)["\']', match.group(1)))
            for required in ("src", "alt", "caption", "width", "height"):
                if not attributes.get(required):
                    fail(f"figure in {path.relative_to(ROOT)} requires {required}")
            for dimension in ("width", "height"):
                if not attributes[dimension].isdigit() or int(attributes[dimension]) <= 0:
                    fail(f"figure in {path.relative_to(ROOT)} has invalid {dimension}")
            source = attributes["src"]
            if not source.startswith("/assets/figures/"):
                fail(f"figure in {path.relative_to(ROOT)} must use a local assets/figures path")
            asset = ROOT / source.lstrip("/")
            if not asset.exists():
                fail(f"figure asset missing for {path.relative_to(ROOT)}: {source}")
            referenced_assets.add(asset.resolve())
            expected_dimensions[asset.resolve()] = (int(attributes["width"]), int(attributes["height"]))
            if path.parent == POSTS:
                slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
                if not source.startswith(f"/assets/figures/{slug}/"):
                    fail(f"figure asset is outside the post directory for {path.name}")
            mobile_source = attributes.get("mobile_src")
            if mobile_source:
                if not mobile_source.startswith("/assets/figures/"):
                    fail(f"mobile figure in {path.relative_to(ROOT)} must be local")
                for dimension in ("mobile_width", "mobile_height"):
                    value = attributes.get(dimension, "")
                    if not value.isdigit() or int(value) <= 0:
                        fail(f"mobile figure in {path.relative_to(ROOT)} requires {dimension}")
                mobile_asset = ROOT / mobile_source.lstrip("/")
                if not mobile_asset.exists():
                    fail(f"mobile figure asset missing for {path.relative_to(ROOT)}: {mobile_source}")
                referenced_assets.add(mobile_asset.resolve())
                expected_dimensions[mobile_asset.resolve()] = (
                    int(attributes["mobile_width"]),
                    int(attributes["mobile_height"]),
                )
            for url_field in ("link", "source_url"):
                value = attributes.get(url_field)
                if value and not value.startswith("https://"):
                    fail(f"{url_field} in {path.relative_to(ROOT)} must use HTTPS")

    if figure_calls < 1:
        fail("shared figure include is not exercised by published content")

    figure_root = ROOT / "assets" / "figures"
    for asset in figure_root.rglob("*"):
        if not asset.is_file():
            continue
        if asset.resolve() not in referenced_assets:
            fail(f"orphaned figure asset: {asset.relative_to(ROOT)}")
        if asset.suffix.lower() != ".svg":
            continue
        text = asset.read_text(encoding="utf-8")
        if re.search(r"(?i)\b(?:klusai|codex|chatgpt)\b|/(?:Users|private/tmp)/", text):
            fail(f"private label or path in SVG: {asset.relative_to(ROOT)}")
        try:
            root = ET.fromstring(text)
        except ET.ParseError as error:
            fail(f"invalid SVG XML in {asset.relative_to(ROOT)}: {error}")
        local_name = lambda value: value.rsplit("}", 1)[-1]
        if local_name(root.tag) != "svg":
            fail(f"figure asset is not SVG: {asset.relative_to(ROOT)}")
        if not root.get("width") or not root.get("height") or not root.get("viewBox"):
            fail(f"SVG lacks explicit dimensions or viewBox: {asset.relative_to(ROOT)}")
        expected = expected_dimensions[asset.resolve()]
        if (root.get("width"), root.get("height")) != tuple(map(str, expected)):
            fail(f"SVG dimensions do not match its figure include: {asset.relative_to(ROOT)}")
        child_names = {local_name(node.tag) for node in root.iter()}
        if not {"title", "desc"}.issubset(child_names):
            fail(f"SVG lacks a title or description: {asset.relative_to(ROOT)}")
        if {"script", "foreignObject"}.intersection(child_names):
            fail(f"active or embedded HTML content in SVG: {asset.relative_to(ROOT)}")
        for node in root.iter():
            for name, value in node.attrib.items():
                if local_name(name) in {"href", "src"} and re.match(r"(?i)https?:", value):
                    fail(f"remote reference in SVG: {asset.relative_to(ROOT)}")
                if re.search(r"(?i)url\(\s*['\"]?https?:", value):
                    fail(f"remote CSS reference in SVG: {asset.relative_to(ROOT)}")

    about = (ROOT / "about.md").read_text(encoding="utf-8")
    if "{% include career-thread.html %}" not in about:
        fail("About page is missing the career-thread diagram")


def main() -> int:
    try:
        validate_media(ROOT)
        validate_professional(ROOT)
    except (ValueError, KeyError, OSError) as error:
        fail(str(error))
    check_books(ROOT, fail)
    check_posts()
    check_localization()
    check_thesis_series()
    check_math_system()
    check_current_work()
    check_applied_papers()
    check_engineering_boundary()
    check_figure_system()
    check_repository_hygiene()
    print("site content checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
