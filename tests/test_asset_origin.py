"""Asset origins must follow configuration without accepting unsafe URLs."""

from pathlib import Path
import tempfile
import unittest

from scripts.site_config import canonical_origin


class AssetOriginTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def test_supported_origins(self):
        for value in ('https://mihainadas.github.io', 'https://nadas.ro', 'https://nadas.ro/'):
            with self.subTest(value=value):
                (self.root / '_config.yml').write_text(f'url: "{value}"\n')
                self.assertEqual(canonical_origin(self.root), value.rstrip('/'))

    def test_invalid_origins(self):
        for value in ('', 'http://nadas.ro', 'https://nadas.ro/path', 'https://user@nadas.ro',
                      'https://nadas.ro?x=1', 'https://nadas.ro#fragment', 'https://nadas.ro:443',
                      'https://nadas.ro:invalid', 'https://nadas.ro foo'):
            with self.subTest(value=value):
                (self.root / '_config.yml').write_text(f'url: "{value}"\n')
                with self.assertRaises(ValueError):
                    canonical_origin(self.root)

    def test_missing_or_duplicate_origin(self):
        for text in ('title: Test\n', 'url: https://nadas.ro\nurl: https://example.org\n'):
            (self.root / '_config.yml').write_text(text)
            with self.assertRaises(ValueError):
                canonical_origin(self.root)


if __name__ == '__main__':
    unittest.main()
