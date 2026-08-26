---
layout: page
title: Research
permalink: /research/
description: "A map of Mihai Nadăș's work on TinyFabulist, Romanian NLP, and open-weight evaluation."
---

## TinyFabulist

TinyFabulist is a three-stage research program built around controlled synthetic narratives.

### TF1 — generation

Structured six-slot specifications are expanded into prompts and passed to open-weight generators no larger than 8B parameters. The released artifact is a three-million-story English corpus with generation metadata and evaluation signals.

- [Paper: TF1-EN-3M](https://arxiv.org/abs/2504.20605)
- [Dataset: DS-TF1-EN-3M](https://huggingface.co/datasets/klusai/ds-tf1-en-3m)

### TF2 — English–Romanian translation

TF2 turns selected TF1 stories into English–Romanian parallel resources and tests how far a fine-tuned open model can narrow the gap to much larger systems at lower inference cost. The project separates the 15K reference set, the three-million-pair corpus, and the released model; they serve different purposes.

- [Journal article: Building Large-Scale English–Romanian Literary Translation Resources with Open Models](https://doi.org/10.3389/frai.2026.1807431)
- [Versioned preprint](https://arxiv.org/abs/2509.07829v4)
- [Full corpus: DS-TF2-EN-RO-3M](https://huggingface.co/datasets/klusai/ds-tf2-en-ro-3m)
- [Curated set: DS-TF2-EN-RO-15K](https://huggingface.co/datasets/klusai/ds-tf2-en-ro-15k)

### TF3 — compact Romanian models

TF3 covers tokenizer construction, from-scratch pre-training, compression, evaluation, and Romanian-native generation. The current paper distinguishes the 51.65M-parameter model from the 26.45M-parameter compressed student; neither number should be reduced to “a 50M model” without context.

- [Paper: TF3-RO-50M](https://arxiv.org/abs/2601.10410)

## Evaluation and Romanian NLP

Two supporting lines of work cut across the pipeline:

- a survey of synthetic text and code generation ([arXiv](https://arxiv.org/abs/2503.14023));
- Romanian diacritic restoration, including the InnoComp 2025 study published in Springer CCIS 2794 ([paper](https://doi.org/10.1007/978-3-032-12481-4_4), [preprint](https://arxiv.org/abs/2511.13182)).

The open-weight judge-panel work remains a research question, not a settled replacement for human or proprietary evaluation. The design notes on this site therefore distinguish validation plans from measured agreement.

## Reproducibility

Public papers, datasets, prompts, and code improve auditability. They do not make hardware behavior, third-party model serving, or stochastic execution automatically identical. Each technical note records the boundary it actually tested.
