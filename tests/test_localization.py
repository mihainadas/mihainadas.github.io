"""The bilingual publication gate must detect stale or incomplete editions."""

import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path

from scripts import check_site
from scripts import check_build


class LocalizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "ro").mkdir()
        self.original = self.root / "research.md"
        self.edition = self.root / "ro" / "research.md"
        self.body = (
            "\nThe system repairs Romanian letters in imported text while preserving other characters. "
            "This example asks which changes belong to normalization and which require a language policy.\n\n"
            "A reader needs to distinguish a canonical encoding from a spelling decision before applying the function. "
            "We test the same inputs under both rules and keep the raw source so that later checks remain possible.\n\n"
            "## Evidence\n\n[Source](https://www.unicode.org/reports/tr15/)\n\n"
            "```python\nprint('same example')\n```\n"
        )
        self.source = "---\nlayout: page\ntitle: A test\nlang: en\npermalink: /research/\ntranslation_key: research\n---\n" + self.body
        self.original.write_text(self.source)
        digest = check_site.language_source_signature(self.source)
        self.translated = (
            "---\nlayout: page\ntitle: Un test\nlang: ro\npermalink: /ro/research/\n"
            "translation_key: research\ntranslation_source: research.md\ntranslation_source_url: /research/\n"
            f"translation_source_sha256: {digest}\ntranslation_reviewed: 2025-01-01\n"
            "context_reviewed: 2025-01-01\neditorial_reviewed: 2025-01-01\n---\n" + self.body
        )
        self.edition.write_text(self.translated)

    def rejects(self) -> None:
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            check_site.check_localization(self.root)

    def test_complete_pair_passes(self) -> None:
        check_site.check_localization(self.root)

    def test_changed_source_requires_review(self) -> None:
        self.original.write_text(self.source + "\nA changed conclusion.\n")
        self.rejects()

    def test_review_only_metadata_does_not_invalidate_source(self) -> None:
        revised = self.source.replace("lang: en", "lang: en\neditorial_reviewed: 2025-01-01")
        self.assertEqual(check_site.language_source_signature(self.source), check_site.language_source_signature(revised))

    def test_wrong_original_url_is_rejected(self) -> None:
        self.edition.write_text(self.translated.replace("translation_source_url: /research/", "translation_source_url: /wrong/"))
        self.rejects()

    def test_evidence_status_change_invalidates_signature(self) -> None:
        revised = self.source.replace("lang: en", "lang: en\nevidence_status: thesis-only")
        self.assertNotEqual(check_site.language_source_signature(self.source), check_site.language_source_signature(revised))

    def test_new_post_requires_editorial_review(self) -> None:
        posts = self.root / "_posts"
        posts.mkdir()
        (posts / "2026-10-17-new.md").write_text("---\nlayout: post\ntitle: New note\ndate: 2026-10-17 09:00:00 +0300\n---\n" + self.body)
        self.rejects()

    def test_missing_citation_is_rejected(self) -> None:
        self.edition.write_text(self.translated.replace("[Source](https://www.unicode.org/reports/tr15/)", "No source"))
        self.rejects()

    def test_changed_code_is_rejected(self) -> None:
        self.edition.write_text(self.translated.replace("print('same example')", "print('different example')"))
        self.rejects()

    def test_duplicate_edition_is_rejected(self) -> None:
        (self.root / "ro" / "duplicate.md").write_text(self.translated)
        self.rejects()

    def test_missing_peer_is_rejected(self) -> None:
        self.edition.unlink()
        self.rejects()

    def test_unsafe_source_is_rejected(self) -> None:
        self.edition.write_text(self.translated.replace("translation_source: research.md", "translation_source: ../research.md"))
        self.rejects()

    def test_thin_opening_is_rejected(self) -> None:
        self.edition.write_text(self.translated.replace(self.body, "\nA short opening.\n\n## Evidence\n"))
        self.rejects()


class LanguageMetadataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.alternates = {"en": "https://example.com/a/", "ro": "https://example.com/ro/a/"}
        self.html = (
            '<html lang="ro"><head><link rel="canonical" href="https://example.com/ro/a/">'
            '<link rel="alternate" hreflang="en" href="https://example.com/a/">'
            '<link rel="alternate" hreflang="ro" href="https://example.com/ro/a/"></head></html>'
        )

    def audit(self, text: str) -> None:
        check_build.audit_localized_html(text, "ro", self.alternates["ro"], self.alternates)

    def test_self_canonical_and_reciprocal_pair_pass(self) -> None:
        self.audit(self.html)

    def test_cross_language_canonical_is_rejected(self) -> None:
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            self.audit(self.html.replace('rel="canonical" href="https://example.com/ro/a/"', 'rel="canonical" href="https://example.com/a/"'))

    def test_missing_return_annotation_is_rejected(self) -> None:
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            self.audit(self.html.replace('<link rel="alternate" hreflang="ro" href="https://example.com/ro/a/">', ""))

    def test_wrong_document_language_is_rejected(self) -> None:
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            self.audit(self.html.replace('lang="ro"', 'lang="en"'))


if __name__ == "__main__":
    unittest.main()
