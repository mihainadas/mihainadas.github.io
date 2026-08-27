---
layout: post
title: "Romanian Diacritics: The Errors Hidden by Overall Accuracy"
date: 2025-09-29 17:00:00 +0300
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: research note
description: "Why Romanian diacritic restoration needs context-sensitive examples, task-specific denominators, and a measure of unwanted edits."
tags: [romanian-nlp, evaluation, natural-language-processing]
---

Romanian uses **ă**, **â**, **î**, **ș**, and **ț**. Removing them does more than alter typography: `fata` may correspond to _fata_ (“the girl”) or _fața_ (“the face”), and the surrounding sentence determines which restoration is correct.

That ambiguity makes automatic diacritic restoration a sequence problem rather than a character-replacement table.

## The denominator problem

Most characters in Romanian text are not diacritizable. Overall character accuracy can therefore remain high when a system misses the positions the task exists to restore.

A useful evaluation separates:

- word and character accuracy over all text;
- accuracy restricted to diacritizable words or positions;
- per-character precision, recall, and F1 for ă, â, î, ș, and ț;
- diacritic error rate;
- unwanted changes to characters that should remain untouched.

The last measure is especially important for generative models. A fluent output that silently rewrites a name or fixes unrelated spelling has violated a restoration-only contract.

## Clean text is the easy regime

Prior Romanian work has shown strong supervised restoration on standard corpora; see [Romanian Diacritics Restoration Using Recurrent Neural Networks](https://arxiv.org/abs/2009.02743). The deployment question is broader:

- OCR errors and keyboard typos;
- mixed presence of correct and missing diacritics;
- inconsistent casing;
- historical orthography, including â/î conventions;
- names, code, URLs, and multilingual fragments that must not be rewritten.

A benchmark that strips diacritics from clean text tests only one slice of that problem.

## Why compare model classes

Prompted LLMs require no task-specific training but bring latency, cost, and uncontrolled-edit risks. Character-level and encoder-based systems are faster and easier to constrain. Fine-tuned small generative models may handle noise and joint normalization better, but they must justify their inference cost and demonstrate that they do not hallucinate changes.

The [InnoComp study](https://arxiv.org/abs/2511.13182) establishes prompted-model baselines. The later fine-tuning note defines the comparison needed to move from clean accuracy to application-specific robustness.
