---
layout: post
title: "What Each TinyFabulist Stage Establishes"
date: 2026-04-14 11:00:00 +0300
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: research note
description: "A snapshot of the TF1 generation, TF2 translation, TF3 training, and evaluation threads—and the claims that do not transfer between them."
tags: [synthetic-data, language-models, evaluation]
---

TinyFabulist is easier to understand as three experiments connected by artifacts, not as one model or one dataset.

## TF1 establishes controlled generation at scale

Six-slot specifications become English fables through several open-weight generators. The released [TF1-EN-3M dataset](https://huggingface.co/datasets/klusai/ds-tf1-en-3m) retains generation provenance and evaluation signals. The [paper](https://arxiv.org/abs/2504.20605) compares ten models and reports the quality–cost trade-off under its hardware assumptions.

TF1 leaves two questions open for later stages: whether the corpus supports Romanian training and how closely model-judge scores track human ratings.

## TF2 establishes a translation pipeline and cost comparison

TF2 creates a [15K reference set](https://huggingface.co/datasets/klusai/ds-tf2-en-ro-15k), a [three-million-pair corpus](https://huggingface.co/datasets/klusai/ds-tf2-en-ro-3m), and a fine-tuned 12B model. The [paper](https://arxiv.org/abs/2509.07829) evaluates literary translation with BLEU and a five-dimensional rubric.

TF2's evidence covers translated fables and the tested systems; native Romanian literature and other translation domains remain outside its scope.

## TF3 establishes from-scratch training and compression

TF3 trains a 51.65M-parameter Romanian model, compresses it to a 26.45M-parameter student, and uses the pipeline for Romanian-native generation. The [paper](https://arxiv.org/abs/2601.10410) documents tokenization, packing, training, compression, and evaluation.

TF3 evaluates synthetic narratives within a compact, domain-specific pipeline, leaving general-purpose Romanian and broad natural corpora outside the experiment.

## Evaluation remains the cross-cutting uncertainty

Every stage depends on measurements that have their own failure modes. The synthetic-data survey ([arXiv](https://arxiv.org/abs/2503.14023)), judge-panel design, and Romanian diacritics work make those assumptions explicit rather than hiding evaluation behind one number.

The maintained version of this map lives at [/research/](/research/). This dated snapshot remains in the archive because it records the point at which the three stages first formed a complete pipeline.
