---
layout: post
title: "Literary Translation with Open Models: The TF2 Project"
date: 2025-06-09 12:00:00 +0300
tags:
  - translation
  - synthetic-data
  - romanian-nlp
  - language-models
---

With TF1 complete, I am now working on the second major component of my thesis: translating the English fable corpus into Romanian using open-weight models. I am calling this TF2, and it brings together several threads I have been thinking about since the start of my PhD.

## Why Translation

The original motivation for TinyFabulist was to create controlled synthetic data for training small language models. TF1 demonstrated this for English, but my thesis is ultimately about Romanian. Romania has roughly 24 million speakers and a rich literary tradition, yet the NLP resources available for Romanian remain limited compared to major European languages.

Rather than starting from scratch with Romanian generation, I decided to leverage the three million English fables from TF1 as a source for parallel translation. This creates two things at once: a large-scale English-Romanian parallel corpus and a benchmark for studying literary translation quality with open models.

## The Romanian NLP Connection

Working with Romanian text surfaces challenges that English NLP researchers rarely encounter. One of the most fundamental is **diacritics** -- the characters ă, â, î, ș, and ț that are essential to correct Romanian but frequently missing or mangled in digital text. Much of the Romanian text on the internet uses incorrect or inconsistent diacritics, which means models trained on web-scraped data inherit these inconsistencies.

This problem is not just a Romanian curiosity. Diacritic restoration is a real NLP task with practical importance, and it connects to broader questions about how language models handle orthographic variation. I have been keeping notes on this topic and plan to investigate it more formally later in my PhD.

## Literary vs. Technical Translation

Most machine translation research focuses on news, web content, or technical documents. Literary translation is different in important ways:

- **Style matters.** A fable translated with perfect accuracy but flat prose has lost something essential.
- **Cultural adaptation is necessary.** Idiomatic expressions, character names, and moral framings may need adjustment for the target audience.
- **There is no single correct translation.** Multiple valid translations can exist for the same source text, which makes evaluation harder.

These properties make literary translation a more demanding test of model capabilities than standard MT benchmarks, which is exactly what makes it interesting for research.

## The TF2 Approach

The TF2 pipeline translates fables using multiple open models, similar to how TF1 used multiple models for generation. I am also experimenting with LoRA fine-tuning to adapt general-purpose models for literary translation specifically. The hypothesis is that a LoRA adapter trained on a small set of high-quality literary translations can significantly improve output quality compared to zero-shot translation.

The evaluation framework extends the TF1 rubric to include translation-specific dimensions: accuracy, fluency, coherence, style, and cultural/pragmatic adaptation. Each dimension is scored on a 1-5 scale.

More details on the evaluation methodology in a future post.
