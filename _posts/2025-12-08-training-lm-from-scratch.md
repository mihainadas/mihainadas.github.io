---
layout: post
title: "Designing a 51M-Parameter Romanian Model from Scratch"
date: 2025-12-08 11:00:00 +0200
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: engineering note
description: "The tokenizer, architecture, packing, checkpoint, and attribution decisions that preceded TF3-RO."
tags: [language-models, romanian-nlp, training]
---

TF3 trains a compact Romanian language model from random initialization. The point is attribution: when the corpus and training path are documented, later behavior can be related to those inputs more directly than after fine-tuning an internet-scale multilingual model.

Tokenization, filtering, sequence packing, architecture, schedule, precision, and checkpoint selection still shape a model trained from scratch.

## Tokenization is a measured decision

Romanian morphology and diacritics can create token inflation under a tokenizer trained mainly on other languages. TF3 therefore trains Romanian-specific BPE and Unigram candidates and compares their vocabulary coverage and sequence-length behavior.

A lower fertility is useful only if the vocabulary does not simply memorize the corpus or damage rare forms. The tokenizer is versioned with its training data and normalization rules.

## The architecture is intentionally small

The main TF3 model is a 51.65M-parameter LLaMA-style decoder. That size permits repeated training and ablation within the project budget while remaining large enough to test whether narrative and Romanian agreement signals emerge.

The later 26.45M-parameter student is a separate compression result, not the original model rounded down.

## Pack sequences, preserve document boundaries

Naive padding wastes a large fraction of compute on short stories. Packing improves utilization by concatenating examples into fixed-length training sequences. The implementation must still mark boundaries so the model is not trained to treat the end of one fable and the start of another as ordinary continuation.

## Checkpoint selection

Training loss alone cannot select the final model. TF3 records intrinsic validation loss alongside Romanian agreement probes, generation samples, entity coherence, and grammar checks. Checkpoints support learning-curve analysis and make regressions visible.

The first draft of this note described “early observations” without publishing a curve or checkpoint table. Those claims have been removed. The [TF3 paper](https://arxiv.org/abs/2601.10410) is the result record; this post is the design record that preceded it.

The experiment asks which Romanian structures a compact model learns from controlled synthetic narrative data. General-purpose capability is outside its scope.
