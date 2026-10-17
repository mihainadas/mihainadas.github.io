"""Reject accidental commissions, invented full reviews, and edition drift."""

import copy
import json
import subprocess
from pathlib import Path
import unittest

from scripts.check_books import isbn_valid, review_errors, validate_books

ROOT = Path(__file__).resolve().parents[1]


class BooksTests(unittest.TestCase):
    def setUp(self):
        self.actual_books = json.loads((ROOT / "_data/books.json").read_text())
        self.actual_programs = json.loads((ROOT / "_data/book_programs.json").read_text())
        self.books = copy.deepcopy(self.actual_books)
        self.programs = copy.deepcopy(self.actual_programs)
        for program in self.programs.values():
            program.update(active=False, tracking_id="")
        for book in self.books:
            for shop in book["shops"]:
                shop["affiliate_url"] = ""

    def test_current_shelf_is_valid(self):
        self.assertEqual(validate_books(self.actual_books, self.actual_programs), [])

    def test_isbn_checksum(self):
        self.assertTrue(isbn_valid("9781603580557"))
        self.assertFalse(isbn_valid("9781603580558"))

    def test_unknown_program_fails(self):
        self.books[0]["shops"][0]["program"] = "unknown"
        self.assertTrue(validate_books(self.books, self.programs))

    def test_unenrolled_affiliate_link_fails(self):
        self.programs["amazon_us"]["active"] = False
        self.books[0]["shops"][0]["affiliate_url"] = "https://www.amazon.com/dp/1603580557?tag=test-20"
        self.assertTrue(validate_books(self.books, self.programs))

    def test_active_program_requires_real_id(self):
        self.programs["amazon_us"].update(active=True, tracking_id="")
        self.assertTrue(validate_books(self.books, self.programs))

    def test_wrong_store_or_tag_fails(self):
        self.programs["amazon_us"].update(active=True, tracking_id="test-20")
        self.books[0]["shops"][0]["affiliate_url"] = "https://www.amazon.de/dp/1603580557?tag=test-20"
        self.assertTrue(validate_books(self.books, self.programs))

    def test_valid_active_tag_passes(self):
        self.programs["amazon_us"].update(active=True, tracking_id="test-20")
        self.books[0]["shops"][0]["affiliate_url"] = "https://www.amazon.com/dp/1603580557?tag=test-20"
        self.assertEqual(validate_books(self.books, self.programs), [])

    def test_unverified_asin_fails(self):
        self.programs["amazon_us"].update(active=True, tracking_id="test-20")
        self.books[0]["shops"][0]["affiliate_url"] = "https://www.amazon.com/dp/B000000000?tag=test-20"
        self.assertTrue(validate_books(self.books, self.programs))

    def test_hidden_ordinary_referral_fails(self):
        self.books[0]["shops"][0]["url"] += "&tag=test-20"
        self.assertTrue(validate_books(self.books, self.programs))

    def test_null_affiliate_and_wrong_ordinary_store_fail(self):
        self.books[0]["shops"][0]["affiliate_url"] = None
        self.books[0]["shops"][0]["url"] = "https://www.amazon.de/s?k=9781603580557"
        self.assertEqual(len(validate_books(self.books, self.programs)), 2)

    def test_duplicate_id_and_unverified_cover_fail(self):
        self.books.append(copy.deepcopy(self.books[0]))
        self.books[1]["cover_checked"] = ""
        self.assertTrue(validate_books(self.books, self.programs))

    def test_publisher_summary_is_not_full_review(self):
        text = "---\npost_type: book review\nbook_id: thinking-in-systems\nreading_basis: Publisher summary\n---\n"
        self.assertTrue(review_errors(text, self.books))

    def test_review_requires_author_and_relationship(self):
        text = "---\npost_type: book review\nbook_id: thinking-in-systems\nreading_basis: Full book\nauthor_reviewed: 2026-10-17\ncontext_reviewed: 2026-10-17\neditorial_reviewed: 2026-10-17\nmaterial_relationship: Purchased independently; no review copy\n---\n"
        self.assertEqual(review_errors(text, self.books), [])
        self.assertTrue(review_errors(text.replace("author_reviewed: 2026-10-17\n", ""), self.books))

    def render(self, filename, active):
        program = {"active": active, "tracking_id": "test-20" if active else ""}
        book = {"title": "Fixture", "shops": [{"label": "Amazon US", "program": "amazon_us", "url": "https://www.amazon.com/s?k=9781603580557", "affiliate_url": "https://www.amazon.com/dp/1603580557?tag=test-20" if active else ""}]}
        context = {"site": {"data": {"books": [book], "book_programs": {"amazon_us": program}}}, "include": {"book": book}}
        code = 'print Liquid::Template.parse(File.read(ARGV[0])).render!(JSON.parse(STDIN.read))'
        result = subprocess.run(["bundle", "exec", "ruby", "-rliquid", "-rjson", "-e", code, str(ROOT / "_includes" / filename)], input=json.dumps(context), text=True, capture_output=True, cwd=ROOT, check=True)
        return result.stdout

    def test_active_include_discloses_and_marks_paid_links(self):
        shop = self.render("book-shops.html", True)
        self.assertIn('rel="sponsored nofollow"', shop)
        self.assertIn('(paid link)', shop)
        self.assertIn('tag=test-20', shop)
        self.assertIn('As an Amazon Associate I earn from qualifying purchases.', self.render("book-disclosure.html", True))

    def test_inactive_include_does_not_claim_membership(self):
        shop = self.render("book-shops.html", False)
        self.assertNotIn('sponsored', shop)
        self.assertNotIn('(paid link)', shop)
        self.assertNotIn('tag=', shop)
        disclosure = self.render("book-disclosure.html", False)
        self.assertNotIn('As an Amazon Associate', disclosure)
        self.assertIn('No affiliate links are active', disclosure)


if __name__ == "__main__":
    unittest.main()
