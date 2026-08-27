"""Small, inspectable calculations used in the thesis-draft post series."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Coverage:
    full_space: int
    sampled_fraction: float
    expected_per_value: float
    expected_per_cross_slot_pair: float


def coverage_counts(*, slots: int, values_per_slot: int, samples: int) -> Coverage:
    """Return balanced-sampling expectations at joint, marginal, and pair order."""
    if slots < 2 or values_per_slot < 1 or samples < 0:
        raise ValueError("slots >= 2, values_per_slot >= 1, and samples >= 0 are required")
    full_space = values_per_slot**slots
    return Coverage(
        full_space=full_space,
        sampled_fraction=samples / full_space,
        expected_per_value=samples / values_per_slot,
        expected_per_cross_slot_pair=samples / values_per_slot**2,
    )


def relative_drop(clean: float, high_noise: float) -> float:
    """Return the fractional loss relative to the clean score."""
    if clean <= 0:
        raise ValueError("clean score must be positive")
    return (clean - high_noise) / clean


def wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    """Compute a two-sided Wilson score interval for a binomial proportion."""
    if total <= 0 or not 0 <= successes <= total:
        raise ValueError("require 0 <= successes <= total and total > 0")
    proportion = successes / total
    denominator = 1 + z**2 / total
    centre = (proportion + z**2 / (2 * total)) / denominator
    radius = (
        z
        * math.sqrt(proportion * (1 - proportion) / total + z**2 / (4 * total**2))
        / denominator
    )
    return centre - radius, centre + radius


if __name__ == "__main__":
    coverage = coverage_counts(slots=6, values_per_slot=100, samples=3_000_000)
    print(coverage)
