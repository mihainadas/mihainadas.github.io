"""Fast, dependency-free checks for posts and code fences."""

from __future__ import annotations

import ast
import re
import sys
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
        if not path.is_file() or path.suffix not in {".html", ".md", ".py", ".yml", ".yaml"}:
            continue
        if {".git", "_site", "vendor"}.intersection(path.relative_to(ROOT).parts):
            continue
        text = path.read_text(encoding="utf-8")
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

    for path in ROOT.rglob("*.md"):
        if {".git", "_site", "vendor"}.intersection(path.relative_to(ROOT).parts):
            continue
        if path == ROOT / "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"{%\s*include\s+figure\.html\s+(.*?)%}", text, re.DOTALL):
            attributes = dict(re.findall(r'(\w+)=["\']([^"\']*)["\']', match.group(1)))
            if not attributes.get("src") or not attributes.get("alt"):
                fail(f"figure in {path.relative_to(ROOT)} requires src and alt")
            source = attributes["src"]
            if source.startswith("/") and not (ROOT / source.lstrip("/")).exists():
                fail(f"figure asset missing for {path.relative_to(ROOT)}: {source}")
            mobile_source = attributes.get("mobile_src")
            if mobile_source and mobile_source.startswith("/"):
                if not (ROOT / mobile_source.lstrip("/")).exists():
                    fail(f"mobile figure asset missing for {path.relative_to(ROOT)}: {mobile_source}")

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
