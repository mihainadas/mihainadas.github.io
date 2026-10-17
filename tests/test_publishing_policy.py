"""Keep durable instructions discoverable but out of the public website."""

from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import check_build

ROOT = Path(__file__).resolve().parents[1]


class PublishingPolicyTests(unittest.TestCase):
    def test_both_instruction_loaders_reference_canonical_policy(self):
        for relative in ("AGENTS.md", ".cursor/rules/blog-consistency.mdc"):
            source = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("docs/publishing-policy.md", source)
            self.assertLess(len(source.splitlines()), 50)
        rule = (ROOT / ".cursor/rules/blog-consistency.mdc").read_text(encoding="utf-8")
        self.assertTrue(rule.startswith("---\n"))
        self.assertIn("alwaysApply: true", rule.split("---", 2)[1])

    def test_required_operating_guides_exist(self):
        for relative in ("docs/publishing-policy.md", "README.md", "docs/books-operations.md", "assets/editorial/README.md"):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_jekyll_excludes_guidance(self):
        config = (ROOT / "_config.yml").read_text(encoding="utf-8").split("exclude:\n", 1)[1]
        for relative in ("AGENTS.md", ".cursor", "docs"):
            self.assertIn(f"  - {relative}\n", config)

    def test_empty_generated_site_has_no_guidance_leak(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(check_build, "SITE", Path(folder)):
            check_build.audit_unpublished_guidance()

    def test_published_agent_instructions_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(check_build, "SITE", Path(folder)):
            (Path(folder) / "AGENTS.md").write_text("private instruction fixture", encoding="utf-8")
            with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
                check_build.audit_unpublished_guidance()

    def test_published_operating_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(check_build, "SITE", Path(folder)):
            (Path(folder) / "docs").mkdir()
            with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
                check_build.audit_unpublished_guidance()


if __name__ == "__main__":
    unittest.main()
