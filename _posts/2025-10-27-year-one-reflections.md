---
layout: post
title: "One Year In: The Decisions Behind the Output"
date: 2025-10-27 20:00:00 +0200
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: retrospective
description: "A first-year PhD retrospective focused on the decisions, delays, and failures behind the papers and datasets."
tags: [phd, research-practice]
---

The visible first-year output was straightforward to list: the synthetic-data survey, TF1 and TF2 preprints, public datasets, and an LLM-judge survey in progress. The useful lessons came from decisions that do not appear in that list.

## I delayed evaluation too long

Generation was concrete and rewarding: prompts produced stories, logs filled, the corpus grew. Evaluation felt like the stage that could be designed afterward. That was backwards.

Once millions of items exist, changing the rubric, judge protocol, or stored provenance becomes expensive. The second half of the year moved evaluation requirements closer to schema design: every output needed the fields required for later attribution and re-scoring.

## Scale amplified vague definitions

Words such as “quality,” “diversity,” and “adherence” were harmless in early discussion and dangerous in a paper. Each needed an operational definition, denominator, and failure analysis.

The TF1 experience changed how I write experiment plans. If I cannot state what would falsify a claim or how a measurement could mislead, the experiment is not ready to scale.

## Engineering habits transferred; production assumptions did not

Interfaces, resumability, idempotent processing, versioned configuration, and structured logs transferred directly from industry. They made the research pipeline easier to audit.

The production instinct to optimize for delivery could work against research. A pipeline that completes quickly but cannot explain a surprising result has failed its main customer. I had to make room for slower comparisons, preserved intermediate artifacts, and experiments whose outcome was “this design does not support the claim.”

## Public artifacts forced useful precision

Releasing data through Hugging Face and papers through arXiv exposed naming, licensing, schema, and documentation decisions to readers outside the project. That pressure improved the work. It also made chronology important: a release note must not predate the thing it says is available.

## The next-year constraint

The work did not need more parallel threads. It needed a closed loop: TF2 resources into TF3 training, and a validation protocol for the evaluators used across all three stages.

The strongest change after year one was therefore editorial as much as technical: plans, observations, measurements, and validated findings had to stop sharing the same voice.
