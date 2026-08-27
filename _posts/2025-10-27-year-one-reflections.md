---
layout: post
title: "One Year In: The Decisions Behind the Output"
date: 2025-10-27 20:00:00 +0200
last_modified_at: 2026-08-27
post_type: retrospective
description: "A first-year PhD retrospective focused on the decisions, delays, and failures behind the papers and datasets."
tags: [phd, research-practice]
---

The public record of my first PhD year is tidy: the [synthetic-data survey](https://arxiv.org/abs/2503.14023), [TF1](https://arxiv.org/abs/2504.20605), [TF2](https://arxiv.org/abs/2509.07829v4), released datasets, and an LLM-judge survey in progress. The year itself was not tidy. The expensive lessons arrived while generation logs were filling and the evaluation rubric was still moving.

## I delayed evaluation too long

Generation was concrete and rewarding: prompts produced stories, logs filled, the corpus grew. Evaluation felt like a stage I could design afterward. I was wrong.

Once millions of items exist, changing the rubric, judge protocol, or stored provenance becomes expensive. The second half of the year moved evaluation requirements closer to schema design: every output needed the fields required for later attribution and re-scoring.

## Scale amplified vague definitions

Words such as “quality,” “diversity,” and “adherence” were harmless in early discussion and dangerous in a paper. Each needed an operational definition, denominator, and failure analysis.

TF1 changed how I write experiment plans. I removed an early diversity claim based on a guessed percentage because the pipeline did not yet measure the thing the sentence asserted. If I cannot state what would falsify a claim or how a measurement could mislead, the experiment is not ready to scale.

## Engineering habits transferred; production assumptions did not

Interfaces, resumability, idempotent processing, versioned configuration, and structured logs transferred directly from industry. They made the research pipeline easier to audit.

The production instinct to optimize for delivery could work against research. A pipeline that completes quickly but cannot explain a surprising result has failed its main customer. I had to make room for slower comparisons, preserved intermediate artifacts, and experiments whose outcome was “this design does not support the claim.”

## Public artifacts forced useful precision

Releasing data through Hugging Face and papers through arXiv exposed naming, licensing, schema, and documentation decisions to readers outside the project. That pressure improved the work. It also made chronology important: a release note must not predate the thing it says is available.

## The next-year constraint

The work did not need more parallel threads. It needed a closed loop: TF2 resources into TF3 training, and a validation protocol for the evaluators used across all three stages.

For the next run, I propose a preflight check that fails unless the rubric version, provenance record, and invalid-output status are present.
