"""Regression tests for the reusable media and evidence-linked professional record."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.check_media import validate_media
from scripts.check_professional import validate_professional

ROOT = Path(__file__).resolve().parents[1]


class PlatformTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for folder in ('_data', '_posts', '_layouts', '_includes', 'assets/media', 'assets/editorial', 'assets/media-sources', 'assets/downloads', 'scripts'):
            shutil.copytree(ROOT / folder, self.root / folder)
        shutil.copy(ROOT / '_data/now.yml', self.root / '_data/now.yml')
        shutil.copy(ROOT / '_config.yml', self.root / '_config.yml')
        for path in ROOT.glob('*.md'):
            shutil.copy(path, self.root / path.name)

    def update_data(self, name, transform):
        path = self.root / f'_data/{name}.json'
        data = json.loads(path.read_text(encoding='utf-8'))
        transform(data)
        path.write_text(json.dumps(data), encoding='utf-8')

    def test_current_catalogue_passes(self):
        self.assertEqual(len(validate_media(self.root)), 3)

    def test_missing_display_is_rejected(self):
        (self.root / 'assets/editorial/signal-480.webp').unlink()
        with self.assertRaisesRegex(ValueError, 'missing or unsafe'):
            validate_media(self.root)

    def test_wrong_mobile_dimensions_are_rejected(self):
        self.update_data('media', lambda data: data['decision-loop'].update(mobile_height=99))
        with self.assertRaisesRegex(ValueError, 'dimensions disagree'):
            validate_media(self.root)

    def test_missing_rights_are_rejected(self):
        self.update_data('media', lambda data: data['signal'].pop('rights'))
        with self.assertRaisesRegex(ValueError, 'missing rights'):
            validate_media(self.root)

    def test_retained_master_replacement_is_rejected(self):
        self.update_data('media', lambda data: data['signal'].update(master_sha256='0' * 64))
        with self.assertRaisesRegex(ValueError, 'retained master changed'):
            validate_media(self.root)

    def test_path_traversal_is_rejected(self):
        self.update_data('media', lambda data: data['signal'].update(src='/assets/../_data/profile.json'))
        with self.assertRaisesRegex(ValueError, 'local and bounded'):
            validate_media(self.root)

    def test_active_svg_is_rejected(self):
        path = self.root / 'assets/media/decision-loop.svg'
        path.write_text(path.read_text().replace('</svg>', '<script>alert(1)</script></svg>'))
        with self.assertRaisesRegex(ValueError, 'passive content'):
            validate_media(self.root)

    def test_unknown_component_id_is_rejected(self):
        path = self.root / '_layouts/home.html'
        path.write_text(path.read_text().replace('id="structure"', 'id="not-registered"'))
        with self.assertRaisesRegex(ValueError, 'unknown media ID'):
            validate_media(self.root)

    def test_unregistered_asset_is_rejected(self):
        shutil.copy(self.root / 'assets/media/decision-loop.svg', self.root / 'assets/media/unused.svg')
        with self.assertRaisesRegex(ValueError, 'unregistered reusable'):
            validate_media(self.root)

    def test_current_professional_record_passes(self):
        self.assertEqual(validate_professional(self.root)['name'], 'Mihai Dan Nadăș')

    def test_executive_evidence_does_not_lead_with_pr_counts(self):
        self.update_data('profile', lambda data: data['evidence'][1].update(detail='Three merged 86Box fixes, with distinct regression tests and links to the upstream pull requests.'))
        with self.assertRaisesRegex(ValueError, 'implementation activity counts'):
            validate_professional(self.root)

    def test_strategy_requires_a_primary_source(self):
        self.update_data('strategy', lambda data: data.update(source=''))
        with self.assertRaisesRegex(ValueError, 'primary source'):
            validate_professional(self.root)

    def test_strategy_connections_need_real_evidence(self):
        self.update_data('strategy', lambda data: data['connections'][0].update(slug='not-a-post'))
        with self.assertRaisesRegex(ValueError, 'real article'):
            validate_professional(self.root)

    def test_strategy_connections_preserve_limitations(self):
        self.update_data('strategy', lambda data: data['connections'][0].update(limit=''))
        with self.assertRaisesRegex(ValueError, 'limitation'):
            validate_professional(self.root)

    def test_changed_profile_requires_pdf_regeneration(self):
        self.update_data('profile', lambda data: data.update(headline='A changed headline'))
        with self.assertRaisesRegex(ValueError, 'resume is stale'):
            validate_professional(self.root)

    def test_changed_renderer_requires_pdf_regeneration(self):
        path = self.root / 'scripts/render_resume.py'
        path.write_text(path.read_text() + '\n# changed renderer\n')
        with self.assertRaisesRegex(ValueError, 'resume is stale'):
            validate_professional(self.root)

    def test_corrupt_pdf_is_rejected(self):
        (self.root / 'assets/downloads/mihai-nadas-resume.pdf').write_bytes(b'not a PDF')
        with self.assertRaisesRegex(ValueError, 'PDF is missing, corrupt'):
            validate_professional(self.root)

    def test_domain_change_requires_pdf_regeneration(self):
        path = self.root / '_config.yml'
        path.write_text('url: "https://new-origin.example.org"\n')
        with self.assertRaisesRegex(ValueError, 'changing the site origin'):
            validate_professional(self.root)

    def test_unrelated_config_change_does_not_stale_pdf(self):
        path = self.root / '_config.yml'
        path.write_text(path.read_text() + '\n# unrelated Jekyll setting\n')
        validate_professional(self.root)

    def test_changed_origin_reader_requires_pdf_regeneration(self):
        path = self.root / 'scripts/site_config.py'
        path.write_text(path.read_text() + '\n# changed reader\n')
        with self.assertRaisesRegex(ValueError, 'resume is stale'):
            validate_professional(self.root)

    def test_unresolved_business_evidence_is_rejected(self):
        self.update_data('business', lambda data: data['themes'][0]['posts'].append('nonexistent-note'))
        with self.assertRaisesRegex(ValueError, 'does not resolve'):
            validate_professional(self.root)

    def test_roles_must_agree_with_existing_about_record(self):
        self.update_data('profile', lambda data: data['experience'][0].update(organization='A different employer'))
        with self.assertRaisesRegex(ValueError, 'current roles disagree'):
            validate_professional(self.root)

    def test_ongoing_doctorate_must_remain_explicit(self):
        self.update_data('profile', lambda data: data['education'][0].update(status='Completed'))
        with self.assertRaisesRegex(ValueError, 'ongoing doctorate'):
            validate_professional(self.root)

    def test_missing_professional_evidence_route_is_rejected(self):
        self.update_data('profile', lambda data: data['evidence'][0].update(url='/not-a-public-page/'))
        with self.assertRaisesRegex(ValueError, 'does not resolve to a public source'):
            validate_professional(self.root)


if __name__ == '__main__':
    unittest.main()
