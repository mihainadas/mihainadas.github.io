---
layout: post
title: "What the Diacritics Study Measured at InnoComp 2025"
date: 2025-10-27 19:00:00 +0200
published_at: 2026-08-27 10:00:00 +0300
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: research note
description: "A bounded account of the Romanian diacritic-restoration comparison presented at InnoComp 2025."
redirect_from: /2025/11/17/innocomp-diacritics.html
tags: [romanian-nlp, evaluation, conference]
---

I presented our comparison of large language models for Romanian diacritic restoration at InnoComp 2025, held in Cluj-Napoca on 22–24 October.

> **Publication update, January 2026.** The paper appears in Springer **Communications in Computer and Information Science**, volume 2794—not LNCS. The [published chapter](https://doi.org/10.1007/978-3-032-12481-4_4) and [arXiv preprint](https://arxiv.org/abs/2511.13182) are now available.

## The comparison

The study evaluates several proprietary and open models under prompt templates ranging from zero-shot instructions to more elaborate multi-shot prompts. It contributes a controlled comparison—the same Romanian corpus, restoration task, and evaluation definitions across model and prompt combinations—rather than a new restoration model.

The strongest proprietary models achieved high restoration accuracy. Open models varied more widely, which makes model choice and prompt sensitivity part of the result rather than implementation noise.

## The error that accuracy hides

Most Romanian characters do not need a diacritic. A model can therefore achieve a high character-level score while still failing on the positions that matter. Restoration evaluation needs to isolate diacritizable words and characters and track unwanted edits to text that should have remained unchanged.

This becomes especially important for generative systems. A restored sentence that silently rewrites a name or non-diacritical character may look fluent while violating the task.

## Scope of the study

The paper establishes comparative baselines under the tested conditions. Production choices still require latency, cost, privacy, and robustness measurements on historical spelling, OCR noise, and informal text.

Those gaps motivate the next phase: compare prompted LLMs with lightweight supervised baselines and fine-tuned small models under explicit noise conditions. Deployment ranking must include the failure modes and constraints of the target application, not only clean-benchmark accuracy.
