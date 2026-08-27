---
layout: post
title: "What Breaks When Fable Generation Reaches Millions"
date: 2025-03-10 10:00:00 +0200
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: engineering note
description: "The public provenance record and the retry design reconstructed after TinyFabulist moved from prompt prototype to corpus pipeline."
tags: [synthetic-data, language-models, infrastructure]
---

At prototype scale, a failed generation is a bad example. At three million items, it is a data-accounting problem.

The prototype could be restarted by hand. The corpus pipeline could not. A combinatorial engine produced story specifications, a prompt builder rendered them, and model workers returned text with inference metadata. Recovery had to preserve the identity of the story across all three steps.

## Identity comes before throughput

Each output needs a stable story identifier and enough provenance to answer four questions later:

- Which specification and rendered prompt produced it?
- Which model and decoding configuration ran?
- Did the first attempt succeed?
- Which validation and evaluation versions touched it?

JSONL was a practical storage format because records remain streamable and can be repartitioned without loading the corpus into memory. The [TF1 paper](https://arxiv.org/abs/2504.20605) documents the resulting provenance fields. In the fuller design, generation output, operational status, and later scores should occupy distinct fields so re-evaluation cannot overwrite generation history.

## The retry design

Sequential requests leave accelerators idle. Batching improves utilization, but a batch should not become the unit of identity. If one response fails validation, the safe design retries that record rather than discarding or silently regenerating its neighbours.

The recommended attempt ledger distinguishes a vanished worker, timeout, out-of-memory event, empty response, malformed output, and failed content check. Those cases should not share a blind retry policy. The public TF1 paper and dataset expose story-level provenance, but they do not expose this attempt ledger; this section records the design rule, not a claim about a released schema.

## Multi-model generation complicates comparison

Several model families receive equivalent specifications so the corpus does not inherit one generator's style and failure modes. Equivalent input does not imply equivalent serving: context templates, quantization, batching limits, and throughput vary across runtimes.

The comparison therefore belongs to versioned experiment records, not model-family folklore. The [TF1 paper](https://arxiv.org/abs/2504.20605) reports the ten-model comparison and its hardware/cost assumptions.

## The number I could not defend

The first draft said “creative reinterpretation” appeared in roughly 5–10% of outputs. I had no recorded sample, annotator, or definition for the category. The percentage had the shape of a result and none of the machinery behind one, so I removed it.

At three million items, the operational requirement is two identities: the requested story and each attempt to produce it. The public release documents the first; a future pipeline release would need to expose the second.
