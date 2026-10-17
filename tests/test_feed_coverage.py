"""Posts without feed_date must still appear in the recent publication feed."""

import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from scripts import check_build


class FeedCoverageTests(unittest.TestCase):
    def test_omitting_a_recent_post_without_an_override_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            posts = root / "_posts"
            posts.mkdir()
            (root / "_config.yml").write_text("feed:\n  posts_limit: 2\n")
            for day, title in ((14, "Older note"), (16, "Latest note")):
                (posts / f"2026-10-{day}-note.md").write_text(f"---\ntitle: {title}\ndate: 2026-10-{day} 09:00:00 +0300\n---\nBody\n")

            def feed(titles: list[tuple[int, str]]) -> str:
                entries = "".join(f"<entry><title>{title}</title><published>2026-10-{day}T09:00:00+03:00</published><updated>2026-10-{day}T09:00:00+03:00</updated></entry>" for day, title in titles)
                return '<feed xmlns="http://www.w3.org/2005/Atom"><updated>2026-10-17T10:00:00+03:00</updated>' + entries + "</feed>"

            with patch.object(check_build, "ROOT", root), patch.object(check_build, "POSTS", posts):
                with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
                    check_build.audit_feed_chronology(feed([(14, "Older note")]))
                check_build.audit_feed_chronology(feed([(16, "Latest note"), (14, "Older note")]))


if __name__ == "__main__":
    unittest.main()
