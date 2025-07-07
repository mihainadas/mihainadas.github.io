---
layout: post
title: "Evaluating Translation Quality Beyond BLEU"
date: 2025-07-07 10:00:00 +0300
tags:
  - evaluation
  - translation
  - natural-language-processing
---

One of the most important design decisions in the TF2 project has been the evaluation framework. Machine translation has a long history of automated metrics, but most of them are poorly suited for literary text. Here is how I am approaching the problem.

## The Limits of Standard MT Metrics

**BLEU** (Bilingual Evaluation Understudy) is the most widely used MT metric. It measures n-gram overlap between a machine translation and one or more reference translations. BLEU works reasonably well for news and technical text, where there is relatively little variation in how a sentence can be correctly translated.

For literary translation, BLEU is insufficient. Consider a fable that uses a creative metaphor in the source text. A translator might find an equally creative but entirely different metaphor in the target language -- a valid and arguably superior choice that BLEU would penalize because the n-grams do not match the reference.

Other standard metrics like **METEOR**, **chrF**, and **COMET** improve on BLEU in various ways (paraphrase matching, character-level overlap, learned representations), but they still fundamentally measure similarity to a reference rather than quality in its own right.

## The TF2 Rubric

For TF2, I developed a five-dimensional evaluation rubric designed specifically for literary translation:

### Accuracy (1-5)
Does the translation preserve the meaning of the source text? Are characters, events, and the moral correctly conveyed? This is the most straightforward dimension, closest to what traditional metrics try to capture.

### Fluency (1-5)
Does the translation read naturally in Romanian? Is the grammar correct? Would a native speaker find the prose smooth and well-formed? Fluency is independent of the source -- a perfectly accurate translation can still be disfluent.

### Coherence (1-5)
Does the translation maintain internal consistency? Do characters behave consistently? Does the narrative flow logically from beginning to end? This captures document-level quality that sentence-level metrics miss entirely.

### Style (1-5)
Does the translation preserve the literary qualities of the source? Is the register appropriate? Does it capture the tone -- whimsical, solemn, humorous -- of the original fable? Style is the dimension most likely to differ across valid translations.

### Cultural and Pragmatic Adaptation (1-5)
Has the translator made appropriate choices for the target audience? Are idiomatic expressions adapted rather than literally translated? Are cultural references handled appropriately?

## Implementation with LLM Judges

Each dimension is evaluated by LLM-based judges using detailed rubric descriptions and anchor examples. The judges receive the source fable, the translation, and the rubric, then produce a score and brief justification for each dimension.

Using multiple judges from different model families helps mitigate individual model biases. I aggregate scores across judges and flag cases where judges disagree significantly -- these are often the most interesting translations to examine manually.

```python
rubric_dimensions = [
    "accuracy",
    "fluency",
    "coherence",
    "style",
    "cultural_pragmatic"
]

for dimension in rubric_dimensions:
    scores = [judge.evaluate(source, translation, dimension)
              for judge in panel]
    final_score = aggregate(scores)
```

## Why Multi-Dimensional Evaluation Matters

A single translation quality score hides important information. A translation might score 5/5 on accuracy but 2/5 on style -- it conveys the right meaning in clumsy prose. Another might score 4/5 on style but 3/5 on accuracy -- beautiful Romanian that drifts from the source. These are fundamentally different failure modes that require different interventions.

The multi-dimensional approach also lets me study which models excel at which aspects of translation. Early results suggest that larger models tend to produce more fluent translations, while fine-tuned models show better accuracy. But I will save the detailed results for the paper.

## Correlation with Human Judgments

The critical question is whether LLM-based rubric scores correlate with how human readers assess translation quality. I am building a human evaluation subset to validate this. The preliminary signal is encouraging, but the formal analysis will appear in the TF2 paper.
