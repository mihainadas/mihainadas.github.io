---
layout: post
title: "A Validation Plan for Open-Weight Judge Panels"
date: 2026-02-24 13:00:00 +0200
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: experiment plan
description: "How an open-weight judge panel should be validated before its aggregate scores are treated as research evidence."
tags: [evaluation, language-models, methodology]
---

This design asks under what conditions a panel of open-weight models can provide useful evaluation across generation, translation, and Romanian-native text.

> **Status, August 2026.** Validation remains in progress. This note records the planned comparisons and does not report a panel-level result.

Single-judge evaluation concentrates bias, version risk, and access cost. A panel can reduce that dependence only if its members make meaningfully different errors and the aggregation rule is defined before results are inspected.

## Constraints on panel composition

**Family diversity.** Closely related checkpoints may share training data, preferences, and failure modes. Model count is not independence.

**Separation from generators.** A judge from the same family as the generator can introduce self-preference. Where full separation is impossible, the overlap must be reported and tested.

**Task coverage.** TF1 grammar/adherence, TF2 literary translation, and TF3 Romanian generation use different rubrics. A reusable panel must demonstrate transfer rather than assume it.

## Define disagreement before aggregation

Mean scores can hide a judge that systematically uses a different scale. Majority vote discards distance. An arbiter introduces another model and another bias source.

The validation record therefore needs per-judge distributions, pairwise agreement, rank correlations, disagreement thresholds, and the exact rule that maps individual outputs to a panel decision.

## Reference comparisons

Three comparisons serve different purposes:

1. **Human ratings** on stratified samples, including easy cases and known disagreements.
2. **Proprietary-model baselines** for continuity with earlier work—not as ground truth.
3. **Perturbation tests** for order, length, style, and family cues that should not change the substantive judgment.

Work such as [MT-Bench](https://arxiv.org/abs/2306.05685) and [Large Language Models are not Fair Evaluators](https://arxiv.org/abs/2305.17926) motivates these checks. The target result is not “open panels are better.” It is a map of tasks and conditions under which their error is acceptable for a stated use.

Until that validation is complete, panel scores remain experimental annotations.
