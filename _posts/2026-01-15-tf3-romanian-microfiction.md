---
layout: post
title: "TF3-RO: Training and Compressing a Romanian Model from Scratch"
date: 2026-01-15 16:02:00 +0200
published_at: 2026-08-27 10:00:00 +0300
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: release note
description: "The tokenizer, 51.65M-parameter model, compressed student, and Romanian-native generation pipeline released with TF3-RO."
featured: true
redirect_from: /2026/01/05/tf3-romanian-microfiction.html
tags: [language-models, romanian-nlp, synthetic-data]
---

TF3-RO was submitted to arXiv on 15 January 2026. It closes the loop opened by TF1 and TF2: build Romanian-specific tokenization, train a compact model from scratch, compress it, evaluate it, and use it for controlled Romanian-native generation.

- [Paper](https://arxiv.org/abs/2601.10410)

## Two model sizes, two roles

The main model is a 51.65M-parameter LLaMA-style transformer trained from scratch. Quantization, structured pruning, and logit-based knowledge distillation then produce a 26.45M-parameter student with tied embeddings.

The larger model establishes the training pipeline; the student tests how much of its behavior survives a deployment-oriented compression path. Their parameter counts refer to separate artifacts.

## Romanian-specific tokenization

Multilingual tokenizers can split morphologically rich Romanian forms inefficiently, increasing sequence length and training cost. TF3 compares Romanian-specific BPE and Unigram tokenizers built from the project corpus. Tokenization is treated as a measured design variable rather than a library default.

The training pipeline uses long-sequence packing to reduce padding waste. Because the model begins from random weights, its behavior can be attributed more directly to the documented corpus and training procedure than in a fine-tuned multilingual model. That improves attribution; it does not make the experiment free of preprocessing and evaluation choices.

## From translated data to Romanian-native generation

TF2 supplies quality-controlled Romanian translations for training. The resulting model then participates in a controlled combinatorial prompting pipeline that generates three million Romanian-native fables.

That sequence matters. The translated corpus supports model training; the native-generation corpus is an output of the trained system. Collapsing both into “the TF3 data” obscures which artifact trained which stage.

## Evaluation boundary

The evaluation combines intrinsic language-model measures, Romanian agreement probes, entity coherence, rule-based grammar checks, and model-based assessment. Each detects a different failure class. None alone establishes broad Romanian competence.

TF3 demonstrates an end-to-end, openly documented pipeline for compact Romanian language modeling on controlled synthetic narratives. It does not claim parity with internet-scale models or prove that synthetic fables are a sufficient corpus for general Romanian.
