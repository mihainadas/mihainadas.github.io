"""Regression tests for the cold-reader opening contract."""

import unittest
import tempfile
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from scripts.check_site import contains_math, math_markup_error, opening_prose_paragraphs
from scripts import check_site


class EditorialContextTests(unittest.TestCase):
    def test_extracts_two_context_paragraphs_before_first_heading(self) -> None:
        post = """---
title: Example
---

The project turns structured requests into short texts so later checks can compare the request with the result.

This note asks whether one field can change without disturbing another field that should remain fixed.

## Result

The result does not belong to the opening.
"""
        self.assertEqual(len(opening_prose_paragraphs(post)), 2)

    def test_ignores_status_notes_lists_and_code(self) -> None:
        post = """---
title: Example
---

> **Status.** This note alone is not an introduction.

- one item
- another item

```python
print("not prose")
```

## Result
"""
        self.assertEqual(opening_prose_paragraphs(post), ())


class MathMarkupTests(unittest.TestCase):
    def test_root_pages_require_the_same_math_contract_as_posts(self) -> None:
        original_root = check_site.ROOT
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "_includes").mkdir()
            for name in ("head.html", "mathjax.html"):
                (root / "_includes" / name).write_text((original_root / "_includes" / name).read_text())
            source = root / "research.md"
            for metadata, markup in (("", r"\\(x\\)"), ("math: true\n", r"\(x\)")):
                source.write_text("---\nlayout: page\n" + metadata + "---\n" + markup)
                with patch.object(check_site, "ROOT", root), redirect_stderr(StringIO()):
                    with self.assertRaises(SystemExit):
                        check_site.check_math_system()
            source.write_text("---\nlayout: page\nmath: true\n---\n" + r"\\(x\\)")
            with patch.object(check_site, "ROOT", root):
                check_site.check_math_system()

    def test_accepts_markdown_safe_inline_and_display_delimiters(self) -> None:
        post = r"""---
title: Example
---

Inline \\(x^2\\) appears before the display.

\\[
y = x^2
\\]
"""
        self.assertTrue(contains_math(post))
        self.assertIsNone(math_markup_error(post))

    def test_rejects_delimiters_markdown_would_strip(self) -> None:
        post = r"""---
title: Example
---

Inline \(x^2\) will not survive Kramdown.
"""
        self.assertEqual(
            math_markup_error(post),
            "TeX punctuation must use two source backslashes so Markdown preserves it",
        )

    def test_rejects_tex_punctuation_markdown_would_strip(self) -> None:
        post = r"Text \\(\#\{i: y_i=1\}\\)"
        self.assertEqual(
            math_markup_error(post),
            "TeX punctuation must use two source backslashes so Markdown preserves it",
        )

    def test_ignores_math_like_text_inside_code(self) -> None:
        post = r"""---
title: Example
---

Use `\(x\)` when documenting a delimiter.

```text
\[not rendered\]
```
"""
        self.assertFalse(contains_math(post))
        self.assertIsNone(math_markup_error(post))

    def test_rejects_unbalanced_delimiters(self) -> None:
        self.assertEqual(
            math_markup_error(r"Text \\(x^2"),
            r"unclosed math delimiter: \\(",
        )


if __name__ == "__main__":
    unittest.main()
