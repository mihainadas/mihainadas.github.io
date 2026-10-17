"""Guard the personal wordmark and its non-scripted navigation fallback."""
from contextlib import redirect_stderr
from io import StringIO
import unittest

from scripts.check_build import audit_brand_header


class BrandTests(unittest.TestCase):
    def header(self, lang='en'):
        home, descriptor = ('/ro/', 'Strategie, tehnologie și IA') if lang == 'ro' else ('/', 'Strategy, technology &amp; AI')
        return (
            '<header class="site-header"><a class="site-title" rel="author" '
            f'href="{home}"><span class="brand-name">Mihai Nadăș</span>'
            f'<span class="brand-descriptor">{descriptor}</span></a>'
            '<details class="navigation" open><summary>Menu</summary></details></header>'
        )

    def rejects(self, html, lang='en'):
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            audit_brand_header(html, lang)

    def test_both_locales_pass(self):
        for lang in ('en', 'ro'):
            audit_brand_header(self.header(lang), lang)

    def test_name_preserves_diacritics(self):
        self.rejects(self.header().replace('Mihai Nadăș', 'Mihai Nadas'))

    def test_descriptor_is_localized(self):
        self.rejects(self.header('ro').replace('Strategie, tehnologie și IA', 'Strategy, technology &amp; AI'), 'ro')

    def test_romanian_home_link_is_not_english(self):
        self.rejects(self.header('ro').replace('href="/ro/"', 'href="/"'), 'ro')

    def test_decorative_badge_does_not_replace_live_identity(self):
        self.rejects(self.header().replace('</a>', '<svg></svg></a>'))

    def test_old_suffix_does_not_return(self):
        self.rejects(self.header().replace('</a>', '<span class="site-mark">/ field notes</span></a>'))

    def test_navigation_without_javascript_stays_available(self):
        self.rejects(self.header().replace('navigation" open', 'navigation"'))
