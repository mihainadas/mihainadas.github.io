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

## Volume needs a downstream consequence

[Self-Instruct](https://arxiv.org/abs/2212.10560) was the first paper in this review that changed a field in the TinyFabulist schema. It showed that a model could expand a small seed collection into instruction data; retaining the seed and generation path therefore mattered as much as retaining the final text. [Textbooks Are All You Need](https://arxiv.org/abs/2306.11644) made the quality-over-volume case in code generation. Neither paper gave us permission to call a large collection useful merely because it was readable.

TinyFabulist changed in response. Each story retained its specification and generation history, and TF3 became a downstream test: train compact Romanian models and inspect what they learn from the resulting resources.

## Generator count is only a starting point

Several model families reduce reliance on one generator's recurring style and errors. They do not demonstrate diverse output. The public corpus therefore keeps generator identity and the rendered prompt that embeds the specification; its prompt hash can join later readability, diversity, or judge records. A later analysis can change the metric without losing the generation record.

## A score needs an audit trail

[MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) made model judging operational at scale. [Large Language Models are not Fair Evaluators](https://arxiv.org/abs/2305.17926) showed that presentation order could alter comparative judgments.

That evidence changed the evaluation record. Scores remained attached to the judge, prompt, rubric, justification, and input order that produced them. Multi-dimensional rubrics replaced a single quality number, and generator–judge family overlap became something to disclose and test. More judges help only when their errors provide different information.

## Romanian needed a narrower question

Romanian has substantial corpora, tools, and an active research community. The constraints differ by task: licensed literary parallel text, restoration under noisy diacritics, and openly documented compact-model pipelines present different shortages.

That distinction narrowed TF2 to English–Romanian literary translation and turned diacritic restoration into its own research line. The papers mattered because they changed fields, metrics, and experiments—not because they made the bibliography longer.

The margin note beside Wang et al. is shorter than the summary: “store order; run A/B and B/A; decide the rejection threshold before seeing reversals.” A paper stays in my working notes when it changes a field, metric, experiment, or explicit rejection.
