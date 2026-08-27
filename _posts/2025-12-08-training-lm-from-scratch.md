---
layout: post
title: "Designing a 51M-Parameter Romanian Model from Scratch"
date: 2025-12-08 11:00:00 +0200
last_modified_at: 2026-08-27
post_type: engineering note
description: "The tokenizer, architecture, packing, checkpoint, and attribution decisions that preceded TF3-RO."
tags: [language-models, romanian-nlp, training]
---

Unigram produced sequences 11% longer than BPE and still won the tokenizer decision. That result overturned the easy efficiency argument and forced the TF3 design to say what it valued: Romanian morphological behavior, not the shortest sequence at any cost.

TF3 trains a compact Romanian model from random initialization. A documented corpus and training path improve attribution, but tokenization, filtering, packing, architecture, schedule, and checkpoint selection still determine what the experiment means.

## Tokenization is a measured decision

TF3 trained 32,000-token BPE and Unigram candidates on the project corpus. BPE averaged 304.89 tokens per sentence and Unigram 340.35. The paper chose Unigram after manual segmentation inspection and downstream Romanian diagnostics; the length table alone favored BPE. It publishes neither a paired segmentation example nor a standalone morphology score, so that part of the decision remains qualitative.

That is a research trade-off, not evidence that Unigram is universally better for Romanian. The tokenizer, training text, and normalization rules are versioned together so the choice can be inspected later.

## The architecture is intentionally small

The main model is a 51.65M-parameter LLaMA-style decoder trained on roughly one billion tokens in 2,048-token blocks. The size keeps repeated training and ablation within budget while leaving enough capacity to test narrative and Romanian agreement signals.

The later 26.45M-parameter student is a separate compression result, not the original model rounded down.

## Packing buys compute, not evidence

Naive padding spends compute on empty positions. Packing the short narratives into fixed-length blocks improves utilization, but it also changes the stream seen by the model. The block size and separator tokens therefore belong in the experiment record, not in an invisible data-loader default.

## Checkpoint selection

Near 27,000 training steps, the reported teacher reached cross-entropy around 0.89 and perplexity around 2.43. Those numbers describe prediction on the held-out distribution; they do not establish fluency, agreement, or useful generation by themselves. TF3 records them alongside Romanian agreement probes, samples, entity coherence, and grammar checks.

The first draft of this note described “early observations” without a curve or checkpoint table. I removed them. The [TF3 paper](https://arxiv.org/abs/2601.10410) is the result record; this is the design record.

The later model results carry a measured sequence penalty and a qualitative tokenizer rationale. Both belong in the record.
