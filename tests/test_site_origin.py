"""A domain cutover must not leave metadata on the previous host."""

from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import check_build


class SiteOriginTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.site = self.root / '_site'
        self.site.mkdir()
        for name, value in (('ROOT', self.root), ('SITE', self.site)):
            patcher = patch.object(check_build, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        (self.root / '_config.yml').write_text('url: "https://nadas.ro"\n')
        (self.site / 'index.html').write_text('<html><head><link rel="canonical" href="https://nadas.ro/"></head></html>')
        (self.site / 'sitemap.xml').write_text('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://nadas.ro/</loc></url></urlset>')
        (self.site / 'robots.txt').write_text('Sitemap: https://nadas.ro/sitemap.xml\n')
        (self.site / 'feed.xml').write_text('<feed xmlns="http://www.w3.org/2005/Atom"><id>https://nadas.ro/feed.xml</id><link rel="self" href="https://nadas.ro/feed.xml"/></feed>')

    def test_custom_origin_passes(self):
        self.assertEqual(check_build.site_origin(), 'https://nadas.ro')
        check_build.audit_canonical_origin()

    def test_previous_origin_remains_supported(self):
        (self.root / '_config.yml').write_text('url: "https://mihainadas.github.io"\n')
        self.assertEqual(check_build.site_origin(), 'https://mihainadas.github.io')

    def test_trailing_slash_is_normalized(self):
        (self.root / '_config.yml').write_text("url: 'https://nadas.ro/'\n")
        self.assertEqual(check_build.site_origin(), 'https://nadas.ro')

    def test_invalid_origins_are_rejected(self):
        for value in ('http://nadas.ro', 'https://nadas.ro/path', 'https://user@nadas.ro', 'https://nadas.ro?x=1', ''):
            (self.root / '_config.yml').write_text(f'url: "{value}"\n')
            with self.subTest(value=value), redirect_stderr(StringIO()), self.assertRaises(SystemExit):
                check_build.site_origin()

    def test_stale_canonical_is_rejected(self):
        (self.site / 'index.html').write_text('<link rel="canonical" href="https://mihainadas.github.io/">')
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            check_build.audit_canonical_origin()

    def test_host_prefix_attack_is_rejected(self):
        (self.site / 'index.html').write_text('<link rel="canonical" href="https://nadas.ro.example.org/">')
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            check_build.audit_canonical_origin()

    def test_stale_sitemap_is_rejected(self):
        (self.site / 'sitemap.xml').write_text('<urlset><url><loc>https://mihainadas.github.io/a/</loc></url></urlset>')
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            check_build.audit_canonical_origin()

    def test_stale_robots_is_rejected(self):
        (self.site / 'robots.txt').write_text('Sitemap: https://mihainadas.github.io/sitemap.xml\n')
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            check_build.audit_canonical_origin()

    def test_stale_feed_link_is_rejected(self):
        (self.site / 'feed.xml').write_text('<feed xmlns="http://www.w3.org/2005/Atom"><link rel="self" href="https://mihainadas.github.io/feed.xml"/></feed>')
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            check_build.audit_canonical_origin()

    def test_feed_identity_is_preserved_across_the_move(self):
        (self.root / '_config.yml').write_text('url: "https://nadas.ro"\nfeed_identity_url: "https://mihainadas.github.io"\n')
        (self.site / 'feed.xml').write_text('<feed xmlns="http://www.w3.org/2005/Atom"><id>https://mihainadas.github.io/feed.xml</id><link rel="self" href="https://nadas.ro/feed.xml"/></feed>')
        check_build.audit_canonical_origin()

    def test_changed_feed_identity_is_rejected(self):
        (self.root / '_config.yml').write_text('url: "https://nadas.ro"\nfeed_identity_url: "https://mihainadas.github.io"\n')
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            check_build.audit_canonical_origin()


if __name__ == '__main__':
    unittest.main()
