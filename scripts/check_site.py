"""Fast, dependency-free checks for posts and code fences."""

from __future__ import annotations

import ast
import re
import sys
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"
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


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_posts() -> None:
    for path in sorted(POSTS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if "\ufffc" in text:
            fail(f"object-replacement character in {path.name}")
        if "http://mihainadas.github.io" in text:
            fail(f"insecure internal link in {path.name}")
        if re.search(r"(?i)happy (coding|learning)!|excited to share", text):
            fail(f"promotional stock phrase in {path.name}")

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


def check_engineering_boundary() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in {".html", ".md", ".py", ".svg", ".yml", ".yaml"}:
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
    check_posts()
    check_engineering_boundary()
    check_figure_system()
    print("site content checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
