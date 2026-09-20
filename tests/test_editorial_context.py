"""Regression tests for the cold-reader opening contract."""

import unittest

from scripts.check_site import opening_prose_paragraphs


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


if __name__ == "__main__":
    unittest.main()
