"""Keep the requested rounded controls consistent without replacing semantics."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ControlShapeTests(unittest.TestCase):
    def test_shared_non_capsule_shape_tokens(self):
        css = (ROOT / 'assets/main.scss').read_text()
        for declaration in ('--action-radius: 18px 8px 18px 8px;', '--control-radius: 12px 8px 12px 8px;', '--field-radius: 12px;'):
            self.assertIn(declaration, css)

    def test_primary_actions_share_the_shape(self):
        css = (ROOT / 'assets/main.scss').read_text()
        hero = re.search(r'\.hero-links \.button-primary \{([^}]+)', css)[1]
        self.assertIn('border-radius: var(--action-radius)', hero)
        professional = (ROOT / '_sass/professional.scss').read_text()
        self.assertIn('border-radius: var(--action-radius)', professional)
        editorial = (ROOT / '_sass/editorial.scss').read_text()
        self.assertNotRegex(editorial, r'\.button-primary\s*\{[^}]*border-radius:\s*0')

    def test_filters_and_icon_control_keep_their_roles(self):
        css = (ROOT / 'assets/main.scss').read_text()
        reset = re.search(r'^\.filter-controls button \{([^}]+)', css, re.MULTILINE)[1]
        self.assertIn('border-radius: var(--action-radius)', reset)
        icon = re.search(r'\.theme-trigger \{([^}]+)', css)[1]
        self.assertIn('border-radius: 50%', icon)
        self.assertIn('min-height: 44px', css)
        for page in ('papers.md', 'archive.md'):
            self.assertIn('<button type="button" data-reset>', (ROOT / page).read_text())
