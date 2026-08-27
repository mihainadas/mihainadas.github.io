---
layout: post
title: "Decision Gates for an Open-Weight Judge Panel"
date: 2026-02-24 13:00:00 +0200
last_modified_at: 2026-08-27
post_type: method note
description: "The locked tests and unresolved decisions that stand between an open-weight judge panel and research use."
tags: [evaluation, language-models, methodology]
---

A panel is not safer because it has more model names in it. If three related judges share the same preference, averaging them turns correlated error into a confident decimal.

> **Status, 27 August 2026.** This note preserves the gate before execution. The later study fixed the panel, ran the cross-stage benchmark and bias audit, and left human anchoring explicitly undone. [The results note separates the model-ranking evidence from the missing human-validation step]({{ '/2026/08/27/judges-rank-systems-not-items.html' | relative_url }}).

The current decision record separates what is already locked from what still blocks execution:

| Decision | Locked | Unresolved |
| --- | --- | --- |
| Tasks | TF1 adherence/grammar; TF2 translation; TF3 Romanian generation | sampling weight per task |
| Order test | every pair scored as A/B and B/A; both raw records retained | acceptable reversal rate |
| Human slice | stratify clear successes, clear failures, and judge disagreements | sample size, rater count, adjudication |
| Family test | repeat the conclusion after replacing one judge family | candidate checkpoints and tolerance |
| Aggregation | expose per-judge distributions before any panel statistic | rule, interval, decision threshold |

The right-hand column records what still blocked execution when this gate was written. The subsequent study resolved the model, sample, and aggregation choices; the human-arbitration gate remains open.

## The first test is literal

Take one TF2 source and two candidate translations. Score them as A/B, then send the same pair as B/A. Keep both raw responses. A reversal is an observed failure, not noise to hide inside a mean. [Wang et al.](https://arxiv.org/abs/2305.17926) is why this swap sits at the entrance to the protocol.

The next run replaces one judge family and repeats the conclusion. Every checkpoint carries its family, quantization, prompt template, digest, and relationship to the generator. Agreement on TF1 grammar does not grant that checkpoint a vote on TF2 translation or TF3 Romanian generation.

## What would stop publication

The result stops if order swaps, harmless formatting changes, or family replacement move the substantive ranking beyond the threshold still missing from the table. Human ratings cover clear successes, clear failures, and model disagreements; their own disagreement stays visible. Per-judge distributions, pairwise agreement, weighted kappa, rank correlation, confidence intervals, and invalid outputs appear before the aggregate.

[MT-Bench](https://arxiv.org/abs/2306.05685) supplies continuity with earlier judge work. The remaining blockers are mundane and decisive: named checkpoints, sample size, raters, aggregation rule, and numerical thresholds.
