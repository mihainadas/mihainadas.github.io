---
layout: post
title: "What Breaks When Fable Generation Reaches Millions"
date: 2025-03-10 10:00:00 +0200
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: engineering note
description: "The batching, retry, provenance, and storage decisions required to turn TinyFabulist from a prompt prototype into a corpus pipeline."
tags: [synthetic-data, language-models, infrastructure]
---

At prototype scale, a failed generation is a bad example. At three million items, it is a data-accounting problem.

The TinyFabulist generation path has three boundaries: a combinatorial engine produces structured story specifications; a prompt builder renders those fields into model input; model workers return text plus inference metadata.

## Keep the record before optimizing the worker

Each output needs a stable story identifier and enough provenance to answer four questions later:

- Which specification and rendered prompt produced it?
- Which model and decoding configuration ran?
- Did the first attempt succeed?
- Which validation and evaluation versions touched it?

JSONL was a practical storage format because records remain streamable and can be repartitioned without loading the corpus into memory. The schema matters more than the file extension: generation output, operational status, and later scores must not overwrite one another.

## Batch for utilization, isolate for recovery

Sequential requests leave accelerators idle. Batching improves utilization, but a batch must not become the unit of identity. If one response fails validation, the pipeline retries that record rather than discarding or silently regenerating its neighbours.

The pipeline distinguishes six operational failure classes:

- transport or worker failure;
- timeout;
- out-of-memory condition;
- empty or truncated response;
- structurally invalid output;
- completed output that fails content checks.

Those categories have different remedies. An out-of-memory failure, for example, usually requires a smaller batch, a smaller model, or a different quantization before retrying.

## Multi-model generation complicates comparison

Several model families receive equivalent specifications so the corpus does not inherit one generator's style and failure modes. Equivalent input does not imply equivalent serving: context templates, quantization, batching limits, and throughput vary across runtimes.

The comparison therefore belongs to versioned experiment records, not model-family folklore. The [TF1 paper](https://arxiv.org/abs/2504.20605) reports the ten-model comparison and its hardware/cost assumptions.

## Claims removed from the first draft

The original note estimated that “creative reinterpretation” occurred in roughly 5–10% of outputs without defining the sample, annotator, or criterion. That number is gone. An observation becomes a result only when its denominator and measurement procedure are recorded.

The engineering outcome of the scaling work was less glamorous and more useful: every story could be traced from specification through generation and later evaluation, and failures could be resumed without making successful records ambiguous.
