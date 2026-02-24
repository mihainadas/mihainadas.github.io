---
layout: post
title: "Designing Open-Weight Judge Panels for Text Evaluation"
date: 2026-02-24 13:00:00 +0200
tags:
  - evaluation
  - language-models
  - natural-language-processing
---

One of the questions I have been exploring this year is whether a carefully designed panel of open-weight language models can serve as a reliable, reusable evaluation system across different text generation tasks. This post describes the methodology and rationale behind this work, which is still in progress.

## The Problem with Single-Model Evaluation

The most common approach to LLM-based evaluation is to use a single powerful model -- typically GPT-4 or a comparable proprietary system -- as the sole judge. This works well enough for many purposes, but it has limitations:

- **Single point of failure.** If the judge model has a systematic bias, every evaluation inherits that bias.
- **Cost and access.** Proprietary API calls add up, especially at scale. Access terms can change without notice.
- **Reproducibility.** Proprietary models are versioned opaquely. Results from GPT-4 in January may not match GPT-4 in June.

The alternative I am exploring is a **panel of diverse open-weight judges**: multiple models from different families that evaluate independently, with scores aggregated through majority vote or averaging.

## Design Principles

Three principles guide the panel design:

### Family Diversity

The judges must come from different model families. If all three judges are Llama variants, their biases are likely correlated and the panel adds little value over a single model. By drawing from distinct families (e.g., Granite, EXAONE), the biases are less likely to align, and aggregated scores are more robust.

### Independence from Generators

The judge models must not come from the same family as the models that generated the text being evaluated. This prevents self-preference bias -- the well-documented tendency for models to rate outputs from similar architectures more favorably.

### Task Transferability

The panel should work across different evaluation tasks without redesigning it from scratch. My thesis involves three distinct tasks:

1. **TF1**: Evaluating English fable generation (grammar, creativity, moral clarity, adherence)
2. **TF2**: Evaluating EN-RO literary translation (accuracy, fluency, coherence, style, cultural adaptation)
3. **TF3**: Evaluating Romanian native generation (the same TF1 dimensions, applied to Romanian text)

A panel that requires different judges for each task would be impractical. The hypothesis is that a single diverse panel, given appropriate rubrics, can handle all three.

## What "Works" Means

Evaluating an evaluation system is inherently circular, so the validation approach matters. I am using several complementary methods:

**Inter-judge agreement.** How often do the panel members agree? High agreement on clear cases and meaningful disagreement on ambiguous cases is the desired pattern.

**Correlation with proprietary baselines.** Do panel scores correlate with scores from GPT-4? This is not the gold standard (GPT-4 has its own biases), but large discrepancies warrant investigation.

**Human arbitration.** For a subset of cases where the panel disagrees with the proprietary baseline, human evaluators adjudicate. This is the most expensive validation step but the most informative.

## What I Am Not Claiming

This work is in progress, and I want to be clear about its scope. I am not claiming that open-weight panels are universally better than proprietary judges. The question is more nuanced: under what conditions can a reusable open-weight panel provide evaluation quality that is sufficient for research purposes?

The answer likely depends on the task, the rubric quality, and the specific models in the panel. I will share results when the investigation is complete and the paper is ready.
