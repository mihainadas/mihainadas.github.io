"""Regression tests for quantities printed in the thesis-draft series."""

from __future__ import annotations

import unittest
from pathlib import Path

from examples.thesis_series_calculations import coverage_counts, relative_drop, wilson_interval


class ThesisSeriesCalculationsTest(unittest.TestCase):
    def test_six_slot_coverage_orders(self) -> None:
        result = coverage_counts(slots=6, values_per_slot=100, samples=3_000_000)
        self.assertEqual(result.full_space, 1_000_000_000_000)
        self.assertEqual(result.sampled_fraction, 0.000003)
        self.assertEqual(result.expected_per_value, 30_000)
        self.assertEqual(result.expected_per_cross_slot_pair, 300)

    def test_reported_noise_drops_round_to_table(self) -> None:
        cases = {
            "dictionary": (93.72, 70.31, 25.0),
            "bilstm": (96.23, 36.76, 61.8),
            "byt5": (92.00, 60.71, 34.0),
            "qwen": (48.99, 37.60, 23.2),
        }
        for name, (clean, noisy, expected_percent) in cases.items():
            with self.subTest(name=name):
                self.assertEqual(round(relative_drop(clean, noisy) * 100, 1), expected_percent)

    def test_wilson_intervals_match_paired_intervention_report(self) -> None:
        complete = wilson_interval(200, 200)
        leakage = wilson_interval(1, 200)
        verbatim = wilson_interval(67, 200)
        self.assertEqual(tuple(round(value * 100, 1) for value in complete), (98.1, 100.0))
        self.assertEqual(tuple(round(value * 100, 1) for value in leakage), (0.1, 2.8))
        self.assertEqual(tuple(round(value * 100, 1) for value in verbatim), (27.3, 40.3))

    def test_intervention_directions_are_not_reversed_in_public_copy(self) -> None:
        root = Path(__file__).resolve().parents[1]
        post = (root / "_posts/2026-08-27-change-one-slot-watch-what-else-moves.md").read_text()
        desktop = (
            root / "assets/figures/change-one-slot-watch-what-else-moves/intervention.svg"
        ).read_text()
        mobile = (
            root / "assets/figures/change-one-slot-watch-what-else-moves/intervention-mobile.svg"
        ).read_text()
        self.assertRegex(post, r"(?s)Characters responded.*4\.0% to 18\.5%")
        self.assertRegex(post, r"(?s)Moral changes rarely.*0\.5%")
        self.assertIn("verifier-sensitive moral leakage", post)
        self.assertIn("measured character leakage is low", post)
        for figure in (desktop, mobile):
            self.assertRegex(figure, r"(?s)Character A → B.*4\.0–18\.5%")
            self.assertRegex(figure, r"(?s)Moral A → B.*0\.5%")
            self.assertRegex(
                figure,
                r"(?s)<desc>.*verifier-sensitive moral leakage.*"
                r"(?:little|low) character leakage.*</desc>",
            )
            self.assertNotIn("little moral leakage", figure)
            self.assertNotIn("verifier-sensitive character leakage", figure)


if __name__ == "__main__":
    unittest.main()
