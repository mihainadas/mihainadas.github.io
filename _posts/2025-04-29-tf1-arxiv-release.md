---
layout: post
title: "TF1-EN-3M: From Six Slots to Three Million Fables"
date: 2025-04-29 10:15:00 +0300
published_at: 2026-08-27 10:00:00 +0300
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: release note
description: "What TF1-EN-3M released, what the ten-model comparison measured, and where reproducibility still has boundaries."
featured: true
redirect_from: /2025/04/21/tf1-arxiv-release.html
tags: [synthetic-data, dataset-release, language-models]
---

TF1-EN-3M was submitted to arXiv on 29 April 2025. The release joins three artifacts: a three-million-story English dataset, the generation and evaluation code, and the paper describing how the system was built.

> **Version note.** This retrospective was published here in August 2026. Cost and evaluation details below follow [arXiv v2](https://arxiv.org/abs/2504.20605v2), submitted in May 2026, rather than the shorter 2025 submission.

- [Paper](https://arxiv.org/abs/2504.20605)
- [Dataset](https://huggingface.co/datasets/klusai/ds-tf1-en-3m)

## Six slots, not an open-ended prompt

Each story begins as a six-slot specification: character, trait, setting, conflict, resolution, and moral. The generator receives a natural-language prompt derived from those fields. The output record retains the specification, prompt, model identifier, decoding configuration, and generated text.

That separation was the central design decision. It allows an evaluator to ask whether the output followed a known request instead of inferring intent after generation. It also makes it possible to regenerate or re-score a subset without losing its origin.

## Ten generators and one practical trade-off

The paper compares ten instruction-tuned, open-weight models no larger than 8B parameters. The best model was not selected by prose quality alone. We considered quality, throughput, memory requirements, and generation cost together.

In the reported setup, an 8B Llama 3 variant provided the best quality–speed trade-off on a single consumer GPU with less than 24 GB of VRAM, at an estimated cost of about 13.5 US cents per thousand fables. That number belongs to the paper's hardware, software, and accounting assumptions; it is not a cloud-pricing constant.

## Evaluation is part of the dataset design

Stories are evaluated along grammar, creativity, moral clarity, and adherence to the specification. Readability and diversity measures add signals that are not produced by the same judge. No single score is treated as “story quality.”

The judge scores are annotations rather than human gold labels. Bias, rubric interpretation, and generator–judge relationships remain threats to validity, while stored provenance allows later re-evaluation under a revised protocol.

## What “reproducible” means here

The public artifacts expose the inputs, code, prompts, model identifiers, generation settings, and dataset records needed to inspect or repeat the pipeline. Exact byte-for-byte regeneration can still depend on model revisions, inference libraries, kernels, and hardware behavior. Open artifacts improve auditability; they do not suspend the execution environment.

TF1 established the generation stage. The next engineering problem was translation: how to turn controlled English narratives into useful Romanian parallel data without reducing literary quality to token overlap.
