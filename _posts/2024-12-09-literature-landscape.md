---
layout: post
title: "Papers That Changed the TinyFabulist Design"
date: 2024-12-09 14:00:00 +0200
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: retrospective
description: "A literature note organized around design changes rather than a generic reading workflow."
tags: [synthetic-data, evaluation, language-models]
---

> **Retrospective.** The first version discussed “the literature” without citing any literature. This revision records the papers that changed concrete design decisions.

## Synthetic data needs a downstream test

[Self-Instruct](https://arxiv.org/abs/2212.10560) showed how a model can bootstrap instruction data from a small seed set. [Textbooks Are All You Need](https://arxiv.org/abs/2306.11644) made a stronger quality-over-volume argument in code. Neither implies that generated data is useful merely because it is large.

For TinyFabulist, that moved the target from “generate many stories” to “store enough structure and provenance to test what the stories are useful for.” The later TF3 stage—training compact Romanian models—became the downstream test that the first-generation work lacked.

## Diversity must be designed and measured

Model-generated corpora can inherit narrow phrasing, preferences, and errors from their generators. Using several model families reduces dependence on one generator, but family count is only a proxy for output diversity.

We retained generator identity and specification fields in each record, then added reference-free diversity and readability measures alongside model-based scores. Those records make output diversity open to direct analysis.

## Model judges are measurements with failure modes

[MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) made model-based judging operational at scale. [Large Language Models are not Fair Evaluators](https://arxiv.org/abs/2305.17926) documented order sensitivity in comparative evaluation. Those papers changed how I treated judge output: not as a label, but as a measurement produced by another model and prompt.

The design consequence was multi-dimensional rubrics, stored justifications, model-family separation between generators and judges where possible, and a later validation program for open-weight panels. Human arbitration remains necessary for cases that matter most.

## Romanian is task-specific, not uniformly “low-resource”

Romanian has mature corpora, tools, and research communities. Scarcity appears unevenly: literary parallel text, licensed high-quality corpora, robust diacritic restoration under noise, and openly documented compact-model pipelines pose different constraints.

That observation narrowed TF2 from generic machine translation to English–Romanian literary translation, and it turned diacritics from a side note into its own evaluation line.

## The reading workflow that survived

I still use Zotero and Markdown notes, but the durable unit is a decision record:

- claim made by the paper;
- evidence and experimental boundary;
- assumption relevant to my system;
- design change, rejected change, or unresolved question.

I kept literature notes that led to a design change, a rejected change, or a question for the next experiment.
