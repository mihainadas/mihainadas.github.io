---
layout: post
title: "A Defensive Ollama Client for Local Judge Inference"
date: 2026-05-18 16:00:00 +0300
published_at: 2026-08-27 10:00:00 +0300
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: engineering note
description: "A corrected native Ollama API example with schema-constrained output, non-streaming responses, timeouts, parsing, and validation."
featured: true
redirect_from: /2026/02/03/local-inference-ollama.html
tags: [tools, evaluation, language-models]
---

My first version of this note was dated before one of its named models existed and mixed the OpenAI-compatible API with Ollama's native request shape. This revision starts from the client contract and keeps the research conclusions narrower.

The client contract uses Ollama's native `/api/chat` endpoint. Native structured output belongs in the `format` field, not `response_format`; streaming must be disabled if the caller expects one JSON document; and the returned message content is still a JSON string that needs parsing and validation.

## The client

```python
import json
import requests

schema = {
    "type": "object",
    "properties": {
        "grammar_score": {"type": "integer", "minimum": 1, "maximum": 10},
        "grammar_justification": {"type": "string"},
    },
    "required": ["grammar_score", "grammar_justification"],
}

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "granite4.1:8b",
        "messages": [
            {"role": "system", "content": "Return a grammar score and brief justification."},
            {"role": "user", "content": "The text to evaluate."},
        ],
        "format": schema,
        "stream": False,
        "options": {"temperature": 0, "seed": 42},
    },
    timeout=120,
)
response.raise_for_status()
scores = json.loads(response.json()["message"]["content"])

assert set(schema["required"]) <= scores.keys()
assert 1 <= scores["grammar_score"] <= 10
assert isinstance(scores["grammar_justification"], str)
```

The code fence is syntax-checked in the site build. The request shape follows Ollama's [structured-output documentation](https://docs.ollama.com/capabilities/structured-outputs). A production client should validate the full schema with a library such as `jsonschema` or Pydantic, record the Ollama and model digest, and distinguish transport retries from invalid model output.

## Version the model, not only the family

`granite4.1:8b` is readable, but it is still a moving tag. Ollama exposes model digests; the experiment record should capture the digest and quantization alongside the human-facing tag. The same applies to the server version and prompt template.

Granite 4.1 was released in late April 2026. That date is why this note now appears after the release rather than in February. The earlier chronology was impossible.

## Reproducibility without magical thinking

Temperature zero and a fixed seed reduce sampling variation. They do not guarantee identical output across model files, Ollama versions, kernels, hardware backends, or concurrency conditions. Repeatability must be tested at the system boundary that matters.

For judge panels, I record at least:

- model tag, digest, and quantization;
- Ollama version and host hardware;
- prompt and schema version;
- timeout, retry, and invalid-output counts;
- input identifier and content hash;
- raw response before aggregation.

Local inference improves cost control, access, and inspectability. The client solves transport and parsing; judge validity still depends on agreement with humans, sensitivity to the rubric, and bias under the target task.
