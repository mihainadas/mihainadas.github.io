"""Generated commercial paths must retain their scope and evidence boundaries."""

import json
import tempfile
import unittest
from contextlib import redirect_stderr
from html import escape
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from scripts import check_build

ROOT = Path(__file__).resolve().parents[1]


class AdvisoryPathTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.site = Path(temporary.name)
        self.business = json.loads((ROOT / '_data/business.json').read_text())
        review = self.business['review']
        self.offer_url = '/work-with-me/#' + review['id']
        self.home = self.offer_url + '/board-advisory/' + ''.join(
            f'<section id="{buyer["id"]}">{escape(buyer["question"])}</section>'
            for buyer in self.business['buyers'])
        self.engagement = f'<section id="{review["id"]}">' + escape(review['title'])
        self.engagement += ''.join(escape(text) for text in (review['fit'], review['not_fit'], review['boundary'], *review['inputs']))
        self.engagement += ''.join(escape(item[key]) for item in review['outputs'] + review['steps'] for key in ('title', 'detail'))
        self.engagement += ''.join(escape(self.business['delivery'][key]) for key in ('relationship', 'boundary', 'source', 'url'))
        evidence = ''.join(escape(item) for item in self.business['leadership_evidence'])
        self.engagement += evidence + '</section>'
        self.board = '<p data-board-boundary></p><aside id="board-conflicts-heading"></aside>' + self.offer_url + evidence
        for route, value in (('work-with-me', self.engagement), ('board-advisory', self.board)):
            folder = self.site / route
            folder.mkdir()
            (folder / 'index.html').write_text(value)

    def audit(self, home=None):
        with patch.object(check_build, 'SITE', self.site), redirect_stderr(StringIO()):
            check_build.audit_advisory_paths(self.home if home is None else home)

    def test_complete_paths_pass(self):
        self.audit()

    def test_home_must_expose_board_route(self):
        with self.assertRaises(SystemExit):
            self.audit(self.home.replace('/board-advisory/', ''))

    def test_review_outputs_must_render(self):
        text = escape(self.business['review']['outputs'][0]['detail'])
        (self.site / 'work-with-me/index.html').write_text(self.engagement.replace(text, ''))
        with self.assertRaises(SystemExit):
            self.audit()

    def test_delivery_disclosure_must_render(self):
        text = escape(self.business['delivery']['relationship'])
        (self.site / 'work-with-me/index.html').write_text(self.engagement.replace(text, ''))
        with self.assertRaises(SystemExit):
            self.audit()

    def test_board_responsibility_boundary_must_render(self):
        (self.site / 'board-advisory/index.html').write_text(self.board.replace('data-board-boundary', ''))
        with self.assertRaises(SystemExit):
            self.audit()

    def test_operating_evidence_must_render(self):
        (self.site / 'board-advisory/index.html').write_text(self.board.replace(escape(self.business['leadership_evidence'][0]), ''))
        with self.assertRaises(SystemExit):
            self.audit()

    def test_public_relationship_is_permitted_only_on_approved_pages(self):
        (self.site / 'work-with-me/index.html').write_text('<p>KlusAI</p><a href="https://klusai.com/">Delivery</a>')
        with patch.object(check_build, 'SITE', self.site):
            check_build.audit_private_program_references()

    def test_private_repository_is_blocked_even_on_disclosure_page(self):
        # Construct the synthetic forbidden URL without storing a repository
        # link in source; the repository-wide source hygiene gate stays intact.
        forbidden = '/'.join(('https:', '', 'github.com', 'klusai', 'private-project'))
        (self.site / 'board-advisory/index.html').write_text(f'<a href="{forbidden}">KlusAI</a>')
        with patch.object(check_build, 'SITE', self.site), redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            check_build.audit_private_program_references()

    def test_private_project_identifier_remains_blocked(self):
        (self.site / 'work-with-me/index.html').write_text('<p>KLU-123</p>')
        with patch.object(check_build, 'SITE', self.site), redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            check_build.audit_private_program_references()

    def test_public_relationship_does_not_allow_brand_references_elsewhere(self):
        (self.site / 'index.html').write_text('<p>KlusAI</p>')
        with patch.object(check_build, 'SITE', self.site), redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            check_build.audit_private_program_references()

    def test_other_vendor_destinations_remain_blocked(self):
        (self.site / 'work-with-me/index.html').write_text('<a href="https://private.klusai.com/project">KlusAI</a>')
        with patch.object(check_build, 'SITE', self.site), redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            check_build.audit_private_program_references()


if __name__ == '__main__':
    unittest.main()
