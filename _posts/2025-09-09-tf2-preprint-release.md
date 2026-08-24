---
layout: post
title: "TF2: Open Models for English–Romanian Literary Translation"
date: 2025-09-09 18:07:00 +0300
published_at: 2026-08-27 10:00:00 +0300
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: release note
description: "The model, 15K reference set, and three-million-pair corpus released with the TF2 preprint."
featured: true
redirect_from: /2025/09/01/tf2-preprint-release.html
tags: [translation, dataset-release, romanian-nlp, language-models]
---

The TF2 preprint was submitted on 9 September 2025. The project releases related but distinct artifacts: a 15K high-quality reference set, a three-million-pair English–Romanian corpus, a fine-tuned 12B open model, and the scripts and prompts used to build and evaluate them.

> **Version note.** This retrospective was published here in August 2026 and follows the [v4 preprint](https://arxiv.org/abs/2509.07829v4) and [Frontiers article](https://doi.org/10.3389/frai.2026.1807431), not only the September 2025 submission. The paper's current title is *Building Large-Scale English–Romanian Literary Translation Resources with Open Models*.

- [Journal article](https://doi.org/10.3389/frai.2026.1807431)
- [Versioned preprint](https://arxiv.org/abs/2509.07829v4)
- [Three-million-pair corpus](https://huggingface.co/datasets/klusai/ds-tf2-en-ro-3m)
- [Curated 15K set](https://huggingface.co/datasets/klusai/ds-tf2-en-ro-15k)

## Why the 15K and 3M sets are separate

The smaller set supplies high-quality Romanian references selected from the TF1 pool. It supports instruction tuning and a more controlled evaluation target. The larger corpus is the scale artifact: useful for downstream training and analysis, but not interchangeable with a human-authored literary parallel corpus.

Calling both “the TF2 dataset” hides their different provenance and quality guarantees. The revised site and research map name them separately for that reason.

## Training and evaluation

The 12B model is adapted in two stages: instruction tuning for the narrative task, then adapter compression for deployment. Evaluation combines corpus-level BLEU with a five-dimensional model-based rubric covering accuracy, fluency, coherence, style, and cultural adaptation.

BLEU remains useful as a reproducible overlap measure. It is weak evidence for literary quality on its own because several valid translations can share little surface form. The rubric adds semantic and stylistic judgments, but it introduces judge bias and calibration questions. The two instruments answer different questions; neither should be presented as a complete evaluator.

## Scope of the result

In the reported experiments, the fine-tuned open model narrows the gap to much larger proprietary systems at substantially lower estimated inference cost. The comparison applies to this task, dataset, rubric, and model set.

TF2 provides a reproducible route from controlled English source text to Romanian parallel resources. TF3 then asks whether those resources can support compact Romanian language models trained from scratch.
