"""Primary contract metrics for aligned Romanian diacritic restoration."""

from __future__ import annotations

from typing import Optional


_BASE = str.maketrans(
    {
        "ă": "a", "â": "a", "î": "i", "ș": "s", "ş": "s", "ț": "t", "ţ": "t",
        "Ă": "a", "Â": "a", "Î": "i", "Ș": "s", "Ş": "s", "Ț": "t", "Ţ": "t",
    }
)
_CANDIDATE_BASES = frozenset("aist")


def _candidate(character: str) -> bool:
    return character.translate(_BASE).casefold() in _CANDIDATE_BASES


def restoration_metrics(
    source: str, prediction: str, reference: str
) -> dict[str, Optional[float]]:
    """Score equal-length text; return None when a denominator is empty."""

    if len({len(source), len(prediction), len(reference)}) != 1:
        raise ValueError("source, prediction, and reference must be character-aligned")

    candidate_positions = [index for index, char in enumerate(source) if _candidate(char)]
    untouched_positions = [index for index, char in enumerate(source) if not _candidate(char)]

    position_accuracy = None
    if candidate_positions:
        position_accuracy = sum(
            prediction[index] == reference[index] for index in candidate_positions
        ) / len(candidate_positions)

    unwanted_edit_rate = None
    if untouched_positions:
        unwanted_edit_rate = sum(
            prediction[index] != source[index] for index in untouched_positions
        ) / len(untouched_positions)

    return {
        "diacritizable_position_accuracy": position_accuracy,
        "unwanted_edit_rate": unwanted_edit_rate,
    }
