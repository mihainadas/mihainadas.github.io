"""Guard the personal wordmark and its non-scripted navigation fallback."""
from contextlib import redirect_stderr
from io import StringIO
import unittest
from pathlib import Path

from scripts.check_build import audit_brand_header, audit_brand_symbol

ROOT = Path(__file__).resolve().parents[1]


class BrandTests(unittest.TestCase):
    def header(self, lang='en'):
        home, descriptor = ('/ro/', 'Strategie, tehnologie și IA') if lang == 'ro' else ('/', 'Strategy, technology &amp; AI')
        return (
            '<header class="site-header"><a class="site-title" rel="author" '
            f'href="{home}"><span class="brand-signature">' +
            '<span class="brand-name">Mihai Nad<span class="brand-letter brand-letter--breve">ă</span>'
            '<span class="brand-letter brand-letter--comma">ș</span></span>' +
            (ROOT / '_includes/brand-stroke.html').read_text() + '</span>' +
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
        self.rejects(self.header().replace('>ă<', '>a<').replace('>ș<', '>s<'))

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

    def test_real_letters_cannot_be_replaced_by_cosmetic_accents(self):
        self.rejects(self.header().replace('>ă<', '>ă<'))

    def test_decorative_mark_is_not_announced_twice(self):
        self.rejects(self.header().replace('aria-hidden="true"', 'aria-hidden="false"'))

    def test_mark_has_no_separate_keyboard_stop(self):
        self.rejects(self.header().replace('focusable="false"', 'focusable="true"'))

    def test_stroke_must_follow_the_name(self):
        stroke = (ROOT / '_includes/brand-stroke.html').read_text()
        html = self.header().replace(stroke, '').replace('<span class="brand-signature">', stroke + '<span class="brand-signature">')
        self.rejects(html)

    def test_old_monogram_cannot_return_to_the_masthead(self):
        stroke = (ROOT / '_includes/brand-stroke.html').read_text()
        self.rejects(self.header().replace(stroke, (ROOT / '_includes/brand-mark.html').read_text()))

    def test_forward_stroke_has_passive_exact_geometry(self):
        stroke = (ROOT / '_includes/brand-stroke.html').read_text()
        audit_brand_symbol(stroke, ['M2 28L10 4'])
        self.rejects(self.header().replace('M2 28L10 4', 'M2 28L9 4'))

    def test_motion_is_optional_and_never_loops(self):
        css = (ROOT / '_sass/editorial.scss').read_text()
        self.assertIn('@media (prefers-reduced-motion: reduce)', css)
        self.assertIn('.brand-stroke { transition: none; }', css)
        self.assertNotIn('animation:', css[css.index('.brand-stroke {'):css.index('.brand-symbol {')])

    def test_signature_stays_close_single_and_quiet(self):
        css = (ROOT / '_sass/editorial.scss').read_text()
        self.assertIn('align-items: center; gap: 0.18rem;', css)
        self.assertIn('transition: transform 160ms ease-out;', css)
        self.assertIn('transform: translate(1px, -2px);', css)
        stroke = (ROOT / '_includes/brand-stroke.html').read_text()
        self.assertEqual(stroke.count('<path '), 1)
        self.assertNotIn('stroke-pixel', (ROOT / 'assets/site.js').read_text())

    def test_all_exports_share_the_geometry(self):
        for path in [ROOT / '_includes/brand-mark.html', ROOT / 'assets/favicon.svg', *sorted((ROOT / 'assets/brand').glob('*.svg'))]:
            audit_brand_symbol(path.read_text())

    def test_export_geometry_drift_is_rejected(self):
        markup = (ROOT / 'assets/brand/nadas-mark.svg').read_text().replace('M7 7L25 25', 'M7 7L24 24')
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            audit_brand_symbol(markup)

    def test_active_exports_are_rejected(self):
        markup = (ROOT / 'assets/brand/nadas-mark.svg').read_text().replace('</svg>', '<script>alert(1)</script></svg>')
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            audit_brand_symbol(markup)

    def test_accent_paint_has_plain_text_and_high_contrast_fallbacks(self):
        css = (ROOT / '_sass/editorial.scss').read_text()
        self.assertIn('@supports ((background-clip: text)', css)
        self.assertIn('@media (forced-colors: active), print', css)
        self.assertIn('.brand-font-ready .brand-letter { background: none; color: inherit; }', css)
