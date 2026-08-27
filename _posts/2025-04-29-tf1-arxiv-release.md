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

Six structured fields became three million English fables at a reported generation cost of $405.76. That number—about $0.1353 per thousand stories—is useful only together with the model choice, evaluation trade-off, and April 2025 endpoint prices behind it.

> **Version note.** This retrospective was published here in August 2026. Cost and evaluation details below follow [arXiv v2](https://arxiv.org/abs/2504.20605v2), submitted in May 2026, rather than the shorter 2025 submission.

- [Paper](https://arxiv.org/abs/2504.20605)
- [Dataset](https://huggingface.co/datasets/klusai/ds-tf1-en-3m)

TF1-EN-3M was first submitted to arXiv on 29 April 2025. The release combines the dataset, generation and evaluation code, and the paper describing the pipeline.

## Six slots, not an open-ended prompt

Each story begins as a six-slot specification: character, trait, setting, challenge, outcome, and teaching. The generator receives a natural-language prompt derived from those fields. In the public dataset, that rendered prompt embeds the specification; separate columns retain the prompt hash, model identifier, token counts, timing, host, pipeline version, and generated text. Decoding settings are documented at pipeline level in the paper and code, not repeated per row.

That separation was the central design decision. It allows an evaluator to ask whether the output followed a known request instead of inferring intent after generation. It also makes it possible to regenerate or re-score a subset without losing its origin.

## The highest score did not make the final choice

The paper compares ten instruction-tuned, open-weight models no larger than 8B parameters on 100 sampled prompts each. Every component is min–max normalized across those ten candidates; Self-BLEU is inverted because lower is better. The composite weights are adherence 0.35; grammar and moral clarity 0.20 each; creativity 0.10; and Self-BLEU, Distinct-1, and Flesch Reading Ease 0.05 each. The resulting values are sample-relative composites, not absolute quality scores.

Llama-3.1-Tulu-3-8B led at 0.957. The production choice, Llama-3.1-8B-Instruct, scored 0.839, but the judge placed 92% of its sampled stories in the intended 4–7 age bracket, compared with 71% for the Tulu variant.

That audience fit changed the decision. The reported cost uses Llama-3.1-8B-Instruct and the endpoint rates available during the run; it is a record of one production calculation, not a current cloud quote.

## Evaluation is part of the dataset design

Stories are evaluated along grammar, creativity, moral clarity, and adherence to the specification. Readability and diversity measures add signals that are not produced by the same judge. No single score is treated as “story quality.”

The judge scores are annotations rather than human gold labels. The paper reports strong rank-level agreement among judges but low item-level kappa, from 0.00 to 0.21. That combination supports model-level comparison more comfortably than confident labels on individual stories.

## What can be rerun

The public artifacts expose the inputs, code, prompts, model identifiers, generation settings, and dataset records needed to inspect or repeat the pipeline. Exact byte-for-byte regeneration can still depend on model revisions, inference libraries, kernels, and hardware behavior. Open artifacts improve auditability; they do not suspend the execution environment.

The production model was selected for audience fit after the composite and intended-reader checks disagreed.
