---
layout: post
title: "What the Diacritics Study Measured at InnoComp 2025"
date: 2025-10-27 19:00:00 +0200
published_at: 2026-08-27
feed_date: "2026-08-27"
last_modified_at: 2026-08-27
post_type: research note
description: "A bounded account of the Romanian diacritic-restoration comparison presented at InnoComp 2025."
redirect_from: /2025/11/17/innocomp-diacritics.html
tags: [romanian-nlp, evaluation, conference]
---

Romanian diacritic restoration looks easy when most of the characters being counted never needed restoration. In our InnoComp comparison, that innocent denominator helped an echo baseline reach 0.8100.

> **Publication update, January 2026.** The paper appears in Springer **Communications in Computer and Information Science**, volume 2794—not LNCS. The [published chapter](https://doi.org/10.1007/978-3-032-12481-4_4) and [arXiv preprint](https://arxiv.org/abs/2511.13182) are now available.

## Prompting moved the ranking

The study uses eight task evaluators and aggregates them into a total average score (TAS). For each system, the maximum TAS (MTAS) selects its best prompt configuration across zero-shot through three-shot prompting. GPT-4o reached an MTAS of 0.9639, 19% above the echo baseline.

| System | MTAS |
| --- | ---: |
| GPT-4o | 0.9639 |
| GPT-4 | 0.9350 |
| Gemini 1.0 Pro | 0.9108 |
| Llama 3 70B | 0.8735 |
| Echo baseline | 0.8100 |
| Llama 3 8B | 0.7663 |
| RoLlama 2 7B | 0.6463 |

Model size did not determine the outcome, and prompt choice was not a cosmetic detail: GPT-4o improved by 1.66% from the two-shot to the three-shot setup.

## Where the remaining errors collect

Most Romanian characters do not need a diacritic. A system can therefore score well while missing the positions the task exists to restore. In the error analysis, misplaced **â** accounted for 21.3% of all errors. Separately, the authors estimate that rule-aware post-processing could eliminate up to 19% of the remaining mistakes. Sentence-initial capitals and final syllables were also recurring trouble spots.

Generative systems add another failure: they can rewrite text outside the restoration target. A fluent sentence that changes a name or non-diacritical character has still violated the contract.

## What the study is good for

The comparison supplies prompted-model baselines on two 1,000-item datasets. It does not decide which system belongs in a keyboard, an OCR cleanup pipeline, or a private document workflow. Those choices also need latency, cost, privacy, unwanted-edit, and noisy-text measurements.

I presented the work at InnoComp 2025 in Cluj-Napoca on 22–24 October. GPT-4o led at 0.9639. The echo baseline’s 0.8100 changed the next experiment: diacritizable-position accuracy and unwanted-edit rate became primary measures.
