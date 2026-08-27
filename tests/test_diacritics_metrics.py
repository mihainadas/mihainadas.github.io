"""Tests for the Romanian diacritics metrics published with the journal."""

import unittest

from examples.diacritics_metrics import restoration_metrics


class DiacriticsMetricsTests(unittest.TestCase):
    def test_scores_correct_restoration(self) -> None:
        result = restoration_metrics("fata", "fața", "fața")
        self.assertEqual(result["diacritizable_position_accuracy"], 1.0)
        self.assertEqual(result["unwanted_edit_rate"], 0.0)

    def test_uppercase_candidates_are_included(self) -> None:
        result = restoration_metrics("ANA", "ĂNA", "ANA")
        self.assertEqual(result["diacritizable_position_accuracy"], 0.5)

    def test_returns_none_for_empty_candidate_denominator(self) -> None:
        result = restoration_metrics("xyz", "xyz", "xyz")
        self.assertIsNone(result["diacritizable_position_accuracy"])

    def test_returns_none_for_empty_untouched_denominator(self) -> None:
        result = restoration_metrics("asit", "așit", "așit")
        self.assertIsNone(result["unwanted_edit_rate"])

    def test_rejects_unaligned_text(self) -> None:
        with self.assertRaisesRegex(ValueError, "character-aligned"):
            restoration_metrics("fata", "fața!", "fața")


if __name__ == "__main__":
    unittest.main()
