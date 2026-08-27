---
layout: post
title: "Treating LLM Judges as Measurement Instruments"
date: 2025-05-12 15:00:00 +0300
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: research note
description: "A taxonomy of model-based evaluation and the biases that must be measured before judge scores are trusted."
tags: [evaluation, language-models, research]
---

An LLM judge does not produce ground truth. It produces a measurement conditioned on a model, prompt, rubric, presentation order, and decoding setup.

That framing changed how I designed evaluation for TinyFabulist. Human review cannot cover three million stories, so model judges provide corpus-scale annotations while human-rated samples test whether those annotations are usable.

## Four evaluation modes

**Pointwise scoring** assigns dimensions such as grammar or adherence to one output. It is easy to aggregate and sensitive to scale calibration.

**Pairwise comparison** asks which of two outputs is better. It avoids some absolute-scale problems but is vulnerable to order effects. [Large Language Models are not Fair Evaluators](https://arxiv.org/abs/2305.17926) documents this failure.

**Critique generation** returns reasons rather than only scores. Reasons help audit rubric interpretation, although plausible prose is not proof that the score is grounded.

**Preference modeling** learns from human comparisons and connects evaluation to reward modeling. It moves the question to the coverage and consistency of the preference data.

[MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) helped establish model judges as a practical evaluation tool. The important follow-up question is not whether they correlate with people on average; it is where that correlation breaks for the target task.

## Biases that enter the experiment

- **Position bias:** presentation order changes pairwise preference.
- **Length bias:** elaboration is mistaken for quality.
- **Self-preference:** a judge favors outputs related to its own family or style.
- **Verbosity in justification:** longer explanations look more rigorous without being more accurate.
- **Rubric drift:** a model silently substitutes its own definition for the supplied criterion.

Panels can reduce dependence on one judge only when their errors are not strongly correlated. Three variants from one family are not automatically three independent measurements.

## What gets stored

For each score, the evaluation record should retain the judge identifier and digest, prompt/rubric version, input identifier, score, justification, parse status, and retry count. Keeping those fields allows aggregates to be recomputed when the protocol changes.

The survey work and open-weight panel experiments remain in progress. Until human validation and disagreement analysis are complete, panel scores are useful annotations—not substitutes for a gold standard.
