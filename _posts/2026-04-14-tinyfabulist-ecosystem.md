---
layout: post
title: "The Artifact Chain Behind TinyFabulist"
date: 2026-04-14 11:00:00 +0300
last_modified_at: 2026-08-27
post_type: research note
description: "How TF1 generation, TF2 translation, and TF3 training connect—and where the evidence stops at each handoff."
tags: [synthetic-data, language-models, evaluation]
---

The three-million-item Romanian corpus is TF3 output, not TF3 training input. Reversing that arrow is the provenance mistake this map is meant to prevent.

| Stage | Starts with | Produces | Strongest reported evidence |
| --- | --- | --- | --- |
| TF1 | six-slot fable specifications | three million English fables | ten-model comparison; 100 prompts per model |
| TF2 | TF1 English fables and 15K GPT-o3 Romanian silver references | 15K tuning set, three-million-pair corpus, 1B/4B/12B adapters | 12B rubric score 4.43 → 4.83; BLEU 0.0214 → 0.0926 |
| TF3 | translated Romanian training text | 51.65M teacher, 26.45M student, three million direct-Romanian fables | teacher cross-entropy ≈0.89 and perplexity ≈2.43; agreement, entity, and grammar probes |

## Follow one record through the chain

A TF1 record begins with a structured request, becomes an English fable, and keeps its prompt, model, decoding setup, and generation metadata. The [TF1 paper and release record](https://arxiv.org/abs/2504.20605) describes three million such records and compares ten generators on 100 prompts each.

TF2 takes the English text as source material. GPT-o3 supplies 15,000 Romanian silver references, of which 12,000 train the adapters. The tuned models then support the three-million-pair release. That order explains why the 15K set, scale corpus, and model checkpoints need different names. The [TF2 paper](https://arxiv.org/abs/2509.07829v4) records the artifacts, the 4.43-to-4.83 rubric change, and the BLEU comparison.

TF3 consumes translated Romanian training text and starts a 51.65M-parameter model from random weights. Compression yields a separate 26.45M student. Only after training does the pipeline generate three million new fables directly in Romanian. The [TF3 paper](https://arxiv.org/abs/2601.10410) carries the tokenizer, training, compression, and probe results.

## The breakpoints

A good TF1 judge score says little about translation fidelity. A strong TF2 translation score does not validate the TF3 student. Low TF3 validation loss does not certify the generated corpus as natural Romanian. The synthetic-data survey ([arXiv](https://arxiv.org/abs/2503.14023)) and current judge work exist because every arrow introduces a new measurement problem.

The maintained map lives at [/research/](/research/); this snapshot preserves the provenance order that readers most often reverse.
