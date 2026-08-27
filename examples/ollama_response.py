"""Parse the nested response returned by Ollama's native chat endpoint."""

from __future__ import annotations

import json
from typing import Any

from jsonschema import validate


SCORE_SCHEMA = {
    "type": "object",
    "properties": {
        "grammar_score": {"type": "integer", "minimum": 1, "maximum": 10},
        "grammar_justification": {"type": "string", "minLength": 1},
    },
    "required": ["grammar_score", "grammar_justification"],
    "additionalProperties": False,
}


def parse_scores(envelope: dict[str, Any]) -> dict[str, Any]:
    """Return validated scores or raise for a malformed response."""

    try:
        content = envelope["message"]["content"]
    except (KeyError, TypeError) as error:
        raise ValueError("Ollama response lacks message.content") from error
    if not isinstance(content, str):
        raise ValueError("Ollama message.content must be a JSON string")
    try:
        scores = json.loads(content)
    except json.JSONDecodeError as error:
        raise ValueError("Ollama message.content is not valid JSON") from error
    validate(instance=scores, schema=SCORE_SCHEMA)
    return scores
