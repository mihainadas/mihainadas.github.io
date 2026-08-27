---
layout: post
title: "Romanian Diacritics: The Errors Hidden by Overall Accuracy"
date: 2025-09-29 17:00:00 +0300
last_modified_at: 2026-08-27
post_type: research note
description: "Why Romanian diacritic restoration needs context-sensitive examples, task-specific denominators, and a measure of unwanted edits."
tags: [romanian-nlp, evaluation, natural-language-processing]
---

`fata` can mean _the girl_ or become `fața`, _the face_. A replacement table cannot decide which one a sentence needs.

Romanian uses **ă**, **â**, **î**, **ș**, and **ț**, but restoration is a sequence problem: context chooses the mark, and the system must leave every unrelated character alone.

## The denominator problem

Most characters in Romanian text are not diacritizable. In a 100-character sentence with five missing marks, returning the input unchanged gives 95% overall character accuracy and 0% restoration accuracy. That is an illustrative denominator, not a benchmark result, but it shows how the headline number can reward doing nothing.

A useful evaluation separates:

- word and character accuracy over all text;
- accuracy restricted to diacritizable words or positions;
- per-character precision, recall, and F1 for ă, â, î, ș, and ț;
- diacritic error rate;
- unwanted changes to characters that should remain untouched.

For the two primary measures, let \(P\) be character positions whose case-normalized, unaccented input is one of `a`, `i`, `s`, or `t`, including uppercase and legacy cedilla forms. Let \(U\) contain every other position. With an aligned clean reference:

\[
A_P = \frac{\#\{i \in P : \hat{y}_i = y_i\}}{|P|}, \qquad
E_U = \frac{\#\{i \in U : \hat{y}_i \ne x_i\}}{|U|}.
\]

The first score tests every place where a mark may be needed, including candidates that should remain plain. The second counts edits outside that candidate set. Insertions and deletions fail the aligned scorer. An empty \(P\) or \(U\) returns no score for that denominator instead of dividing by zero. The [executable implementation](/examples/diacritics_metrics.py) is covered by uppercase, empty-set, correct-restoration, and alignment tests in the site build.

The last measure is especially important for generative models. A fluent output that silently rewrites a surname, normalizes a URL, or fixes unrelated spelling has violated a restoration-only contract.

## Clean text is the easy regime

Prior Romanian work has shown strong supervised restoration on standard corpora; see [Romanian Diacritics Restoration Using Recurrent Neural Networks](https://arxiv.org/abs/2009.02743). The deployment question is broader:

- OCR errors and keyboard typos;
- mixed presence of correct and missing diacritics;
- inconsistent casing;
- historical orthography, including â/î conventions;
- names, code, URLs, and multilingual fragments that must not be rewritten.

A benchmark that strips diacritics from clean text tests only one slice of that problem.

## Why compare model classes

Prompted LLMs require no task-specific training but bring latency, cost, and uncontrolled-edit risks. Character-level and encoder-based systems offer simpler constrained decoding and are expected to have lower latency; the deployment benchmark must measure that assumption on the target hardware. Fine-tuned small generative models may handle noise and joint normalization better, but they must justify their inference cost and unwanted edits.

The [InnoComp study](https://arxiv.org/abs/2511.13182) supplies prompted-model baselines. The later fine-tuning study must test whether robustness repays the latency and unwanted edits. Its two primary denominators are accuracy at diacritizable positions and changes outside them.
