"""Fast, dependency-free checks for posts and code fences."""

from __future__ import annotations

import ast
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"
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


def main() -> int:
    check_posts()
    print("site content checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
