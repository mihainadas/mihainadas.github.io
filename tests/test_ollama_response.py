"""Contract tests for the Ollama response parser used in the journal."""

import unittest

from jsonschema import ValidationError

from examples.ollama_response import parse_scores


class OllamaResponseTests(unittest.TestCase):
    def test_accepts_valid_scores(self) -> None:
        scores = parse_scores(
            {
                "message": {
                    "content": '{"grammar_score": 8, "grammar_justification": "Clear."}'
                }
            }
        )
        self.assertEqual(scores["grammar_score"], 8)

    def test_rejects_malformed_envelope(self) -> None:
        with self.assertRaisesRegex(ValueError, "message.content"):
            parse_scores({})

    def test_rejects_invalid_inner_json(self) -> None:
        with self.assertRaisesRegex(ValueError, "not valid JSON"):
            parse_scores({"message": {"content": "{"}})

    def test_rejects_scalar_json(self) -> None:
        with self.assertRaises(ValidationError):
            parse_scores({"message": {"content": "7"}})

    def test_rejects_schema_violation(self) -> None:
        with self.assertRaises(ValidationError):
            parse_scores(
                {
                    "message": {
                        "content": '{"grammar_score": 11, "grammar_justification": ""}'
                    }
                }
            )


if __name__ == "__main__":
    unittest.main()
