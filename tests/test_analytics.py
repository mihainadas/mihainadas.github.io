"""Production analytics and disclosure must survive generated-site changes."""
import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from unittest.mock import patch
from scripts import check_build

ROOT = Path(__file__).resolve().parents[1]


class AnalyticsBuildTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.site = Path(temporary.name)
        self.loader = (ROOT / '_includes/analytics.html').read_text().split('\n', 1)[1].rsplit('{% endif %}', 1)[0]
        self.page = '<footer class="site-footer h-card"><a href="/privacy/">Privacy</a></footer>'
        (self.site / 'privacy').mkdir()
        (self.site / 'privacy/index.html').write_text('https://plausible.io/data-policy Do Not Track Global Privacy Control')

    def audit(self, loader=None, origin='https://nadas.ro', footer=None):
        (self.site / 'index.html').write_text((self.loader if loader is None else loader) + (self.page if footer is None else footer))
        with patch.object(check_build, 'SITE', self.site), patch.object(check_build, 'site_origin', return_value=origin), redirect_stderr(StringIO()):
            check_build.audit_analytics()

    def test_complete_loader_and_notice_pass(self):
        self.audit()

    def test_missing_or_duplicate_loader_fails(self):
        for loader in ('', self.loader * 2):
            with self.assertRaises(SystemExit):
                self.audit(loader)

    def test_all_runtime_guards_are_required(self):
        for text in ('window.location.hostname', 'window.location.protocol', 'window.navigator.doNotTrack', 'window.navigator.globalPrivacyControl', 'outboundLinks: false', 'payload.u = window.location.origin', 'new URL(payload.r).origin'):
            with self.assertRaises(SystemExit):
                self.audit(self.loader.replace(text, 'removed'))

    def test_unguarded_external_script_fails(self):
        with self.assertRaises(SystemExit):
            self.audit(self.loader + '<script src="https://plausible.io/js/example.js"></script>')

    def test_footer_disclosure_link_required(self):
        with self.assertRaises(SystemExit):
            self.audit(footer=self.page.replace('/privacy/', '/'))

    def test_alternate_origin_must_omit_loader(self):
        self.audit('', origin='https://preview.example.org')
        with self.assertRaises(SystemExit):
            self.audit(origin='https://preview.example.org')
