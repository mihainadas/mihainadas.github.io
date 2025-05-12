---
layout: post
title: "LLMs as Judges: Surveying the Evaluation Landscape"
date: 2025-05-12 15:00:00 +0300
tags:
  - evaluation
  - natural-language-processing
  - machine-learning
---

Alongside my work on synthetic data generation, I have been developing a survey on a topic that is becoming increasingly central to NLP research: using large language models as evaluators, critics, and judges.

## The Evaluation Problem

As language models get better at generating text, evaluating that text becomes harder. Traditional metrics like BLEU, ROUGE, and perplexity capture surface-level properties but miss deeper qualities like coherence, creativity, and factual accuracy. Human evaluation is the gold standard but does not scale -- you cannot have humans read and score three million fables.

This is where LLM-based evaluation comes in. The idea is straightforward: use a capable language model to assess the output of another model, following a rubric or set of criteria. The approach has been shown to correlate well with human judgments in many settings, but it also introduces new challenges.

## What the Survey Covers

The survey I am writing spans several strands of this rapidly growing field:

**Pointwise evaluation**: Models score individual outputs on absolute scales (e.g., "rate this translation from 1 to 5 on fluency"). This is the approach I use in TinyFabulist, and it works well when you have clear, dimensional rubrics.

**Pairwise comparison**: Models choose which of two outputs is better. This avoids the calibration problem of absolute scores but introduces position bias -- the output presented first tends to be preferred.

**Critique and feedback**: Models provide natural language explanations of strengths and weaknesses. This is useful for iterative refinement but harder to aggregate quantitatively.

**Preference modeling**: Using human preference data to train models that predict which outputs humans would prefer. This connects to RLHF and constitutional AI, but the survey focuses on the evaluation applications.

## Known Biases and Mitigations

One theme that runs through the literature is that LLM judges are not neutral. They have systematic biases:

- **Position bias**: Preferring the first or last option in a comparison
- **Length bias**: Favoring longer outputs regardless of quality
- **Self-preference**: Models tend to rate their own outputs more favorably
- **Family preference**: Models may prefer outputs from architecturally similar models

The most promising mitigation strategies involve using panels of diverse judges rather than a single model. If the judges come from different model families, their biases are less likely to be correlated, and aggregation (majority vote or mean score) reduces individual bias.

## Connection to My Work

This survey is not purely academic for me. The evaluation framework in TinyFabulist relies directly on LLM-based judging, and I am actively experimenting with multi-judge panels. Understanding the strengths and limitations of these approaches is essential for the credibility of my evaluation results.

The survey is still in progress -- I am targeting a journal submission once the coverage is comprehensive enough. I will share more when there is a public version available.
