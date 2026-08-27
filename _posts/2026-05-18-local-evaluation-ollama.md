---
layout: post
title: "A Defensive Ollama Client for Local Judge Inference"
date: 2026-05-18 16:00:00 +0300
published_at: 2026-08-27
feed_date: "2026-08-27"
last_modified_at: 2026-08-27
post_type: engineering note
description: "A corrected native Ollama API example with schema-constrained output, non-streaming responses, timeouts, parsing, and validation."
featured: true
redirect_from: /2026/02/03/local-inference-ollama.html
tags: [tools, evaluation, language-models]
---

A local judge can return valid JSON and still be scientifically useless. Before reaching that harder problem, my first client managed two simpler mistakes: it was dated before the named model existed, and it mixed Ollama’s native API with the OpenAI-compatible request shape.

The corrected client uses Ollama’s native `/api/chat` endpoint. Structured output belongs in `format`, not `response_format`. Streaming is off because the caller expects one document. The content inside the response is still a JSON string, so transport success, JSON parsing, and schema validation are separate checks.

## The client

```python
import requests
from examples.ollama_response import SCORE_SCHEMA, parse_scores

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "granite4.1:8b",
        "messages": [
            {"role": "system", "content": "Return a grammar score and brief justification."},
            {"role": "user", "content": "The text to evaluate."},
        ],
        "format": SCORE_SCHEMA,
        "stream": False,
        "options": {"temperature": 0, "seed": 42},
    },
    timeout=(10, 120),
)
response.raise_for_status()
scores = parse_scores(response.json())
```

The request shape follows Ollama’s [structured-output documentation](https://docs.ollama.com/capabilities/structured-outputs). The [parser](/examples/ollama_response.py) declares an object schema with no extra properties. Its build-time tests cover success, a malformed envelope, invalid inner JSON, scalar JSON, and an out-of-range score. `jsonschema` is pinned in the site’s example requirements.

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

The integration test stops at schema validation. Judge validity begins with a human-rated slice and perturbation suite; neither belongs to this client. The digest identifies the model file that produced the document.
