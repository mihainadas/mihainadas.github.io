---
layout: post
title: "Treating LLM Judges as Measurement Instruments"
date: 2025-05-12 15:00:00 +0300
last_modified_at: 2026-08-27
post_type: research note
description: "The A/B swap test and evaluation record required before model-judge scores reach the corpus."
tags: [evaluation, language-models, research]
---

The first acceptance test for a pairwise judge uses the same two answers twice. One request presents A/B; the other presents B/A. Both raw records survive. If the preferred answer changes, that judge–task combination has failed before aggregation.

TinyFabulist needs automated evaluation because human review cannot cover three million stories. Human-rated samples have a different job: determine whether those annotations are usable for grammar, adherence, translation, or Romanian-native text.

## One pair, two records

Pointwise scoring fits grammar or adherence; pairwise comparison fits the question “which translation is better?” The latter always creates two records here. The candidate IDs stay fixed while `presentation_order` changes from `A/B` to `B/A`. A consistency field records whether the preference survived.

Generated critiques are kept as explanations, never as proof that a score is grounded. A fluent justification can rationalize a preference that disappears when the candidates swap.

[MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) helped make model judging practical at scale and reports position, verbosity, and self-enhancement biases. [Large Language Models are not Fair Evaluators](https://arxiv.org/abs/2305.17926) isolates position bias and motivates the A/B swap. Average agreement on another benchmark cannot tell us where a method fails on this one.

## The failure can happen before aggregation

Presentation order can reverse a pairwise preference, and elaborate answers can benefit from verbosity bias. Self-enhancement makes generator–judge overlap a variable to record. Generated justifications add another trap: detailed prose can make a weak judgment look well grounded.

A panel only helps when its errors differ. Several related checkpoints may share training data, style preferences, and failure patterns, so family and generator overlap travel with every score.

## The row that reaches the corpus

The surviving row contains the judge digest, prompt and rubric versions, input and candidate IDs, presentation order, score, justification, parse status, retry count, and swap-consistency result. Aggregates can then be rebuilt after a prompt or threshold changes.

The sample size and rejection threshold are still unresolved. The storage contract is settled: both orders and both raw responses must exist before one TF2 pair contributes to a ranking.
