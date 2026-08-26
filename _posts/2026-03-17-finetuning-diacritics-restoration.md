---
layout: post
title: "A Three-Way Test for Romanian Diacritic Restoration"
date: 2026-03-17 14:00:00 +0200
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: experiment plan
description: "A comparison of prompted LLMs, lightweight supervised baselines, and fine-tuned small models under clean and noisy Romanian text."
tags: [romanian-nlp, language-models, evaluation]
---

The next diacritic-restoration experiment compares three system classes under the same data splits and noise conditions:

1. prompted large language models, using the InnoComp study as a baseline;
2. lightweight supervised systems, including character-level and sequence-to-sequence models;
3. LoRA or fully fine-tuned decoder models in the 1B–8B range.

This is an experiment plan. The first draft used an unsupported novelty claim and described preliminary direction without publishing the table. Both have been removed.

> **Status, August 2026.** The three-way comparison remains in progress. No performance advantage is claimed here.

## The test is robustness, not clean accuracy

Clean benchmark text is only one condition. The evaluation matrix adds missing diacritics, existing partial diacritics, typos, case changes, OCR-like corruption, and historical â/î variation. Corruption is generated after the split so related versions of the same sentence cannot leak across train and test partitions.

## Metrics and invariants

The suite includes word accuracy, character accuracy, diacritizable-position accuracy, diacritic error rate, per-character precision/recall/F1, and unwanted-edit rate.

The unwanted-edit rate is a contract check: a restoration system should not improve its diacritic score by rewriting unrelated text. Exact preservation outside declared positions is tested separately from fluency.

## Data provenance

The training corpus and any dexonline-derived resources require explicit licensing, extraction date, normalization rules, and deduplication documentation. “Comes from dexonline” is not a sufficient dataset description.

## Decision criterion

A fine-tuned generative model is justified only if its robustness gain survives comparison with the much faster supervised baselines and its unwanted-edit rate remains acceptable. Batch restoration of historical documents and real-time keyboard correction have different latency budgets; the experiment should not collapse them into one winner.

The [prompting baseline](https://arxiv.org/abs/2511.13182) and [prior Romanian recurrent model](https://arxiv.org/abs/2009.02743) provide two anchors. The result will need the full table, model identifiers, data version, hardware, and failure analysis before any advantage is claimed.
