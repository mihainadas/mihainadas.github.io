---
layout: post
title: "What Must Be Fixed Before the Diacritics Comparison"
date: 2026-03-17 14:00:00 +0200
last_modified_at: 2026-08-27
post_type: method note
description: "The locked measures and unresolved design choices for comparing Romanian diacritic-restoration systems."
tags: [romanian-nlp, language-models, evaluation]
---

> **Status, 27 August 2026.** The comparison described here has now run. [The results separate the clean-text winner from the model that survives corrupted input]({{ '/2026/08/27/small-model-diacritics-noise.html' | relative_url }}); [a second note records the single-checkpoint contamination failure]({{ '/2026/08/27/adaptation-could-not-remove-scraper-artifact.html' | relative_url }}).

A 7B decoder has no place behind a keyboard if a constrained character model restores the same marks faster and with fewer unwanted edits. The generative system has to earn its latency.

The first draft used an unsupported novelty claim and hinted at a result without publishing the table. I removed both.

> **Original status, March 2026.** The comparison was not ready to run. Candidate checkpoints, dataset versions, split sizes, corruption rates, latency budgets, and acceptance thresholds remained open.

The parts already fixed are narrower. Prompted InnoComp baselines, constrained character or sequence models, and fine-tuned 1B–8B decoders will use identical splits. Corruption happens after the split. Each result carries the corpus license, extraction date, normalization, and deduplication record.

The empty fields are just as important: exact checkpoints, training recipes, corpus version, split sizes, corruption rates, sample counts, two latency budgets, and acceptance thresholds. They stay written here because filling them after the run would turn design choices into result-dependent choices.

## Two denominators

The primary measures are accuracy at diacritizable positions and unwanted-edit rate outside them. Word accuracy, overall character accuracy, diacritic error rate, and per-character precision/recall/F1 remain diagnostics. This ordering prevents the many characters that require no action from dominating the result.

The unwanted-edit rate is a contract check: a restoration system should not improve its diacritic score by rewriting unrelated text. Exact preservation outside declared positions is tested separately from fluency.

## A keyboard and an archive

Clean sentences are only the first slice. The test also adds partial diacritics, typos, case changes, OCR-like corruption, and historical â/î variation. A fine-tuned decoder advances when its robustness gain survives comparison with faster baselines and unwanted edits stay inside the threshold still to be set.

The [prompting baseline](https://arxiv.org/abs/2511.13182) and [prior Romanian recurrent model](https://arxiv.org/abs/2009.02743) provide two anchors. A keyboard path optimizes latency and exact preservation. An archive path may spend more time on OCR damage and historical spelling. The experiment will report two selections if those jobs disagree.
