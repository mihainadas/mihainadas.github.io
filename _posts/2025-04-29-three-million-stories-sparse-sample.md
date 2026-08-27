---
layout: post
title: "Three Million Stories Are Still a Sparse Sample"
date: 2025-04-29 13:15:28 +0300
published_at: 2026-08-27 09:11:56 +0300
feed_date: "2026-08-27 09:11:56 +0300"
last_modified_at: 2026-08-27 09:11:56 +0300
post_type: research note
description: "What a three-million-row corpus covers when six slots each have one hundred possible values."
tags: [synthetic-data, experimental-design, language-models]
series: controlled-synthetic-narratives
series_order: 1
evidence_status: thesis-analysis
---

Three million sounds exhaustive until it is divided by a trillion.

TF1 constructs a prompt from six slots—character, trait, setting, challenge, outcome, and teaching—with one hundred values available in each. That makes \(100^6\), or one trillion, possible specifications. The released three-million-story corpus occupies at most 0.0003% of that grid.

> **Archive note.** This is an August 2026 analysis of the [April 2025 TF1 release](https://arxiv.org/abs/2504.20605). The date marks the artifact being examined; the argument was added to this journal later.

{% include figure.html
  src="/assets/figures/three-million-stories-sparse-sample/coverage.svg"
  mobile_src="/assets/figures/three-million-stories-sparse-sample/coverage-mobile.svg"
  alt="A scale comparison showing one trillion possible six-slot specifications, three million generated stories, about thirty thousand appearances per individual value, and about three hundred appearances per cross-slot pair."
  caption="Scale gives strong marginal coverage and useful pairwise coverage; it does not fill the joint design space."
  width="1200"
  height="610"
  mobile_width="320"
  mobile_height="1010"
  wide=true
%}

## What three million buys

If the sampler is balanced, each individual value appears about 30,000 times: a particular character, setting, or teaching is no longer a rare event. A particular value pair across two slots appears about 300 times on average. That is enough to inspect many first-order and pairwise effects with useful replication.

The sixth-order combination is different. Even with no duplicate rows, the corpus leaves 999,997,000,000 possible specifications unseen. A claim that the data “covers the design space” would confuse a large row count with dense joint coverage.

The distinction changes which questions the corpus can answer. It can support statements about marginal balance: whether every setting is represented, for example. It can support planned pairwise checks, such as whether one character is unusually associated with one moral. It cannot show that every plausible interaction among all six fields has been exercised.

## Coverage is a claim with an order

The useful question is not whether the corpus is large. It is: coverage of what?

- **First order:** roughly 30,000 observations for each slot value.
- **Second order:** roughly 300 for each cross-slot value pair.
- **Sixth order:** at most three million occupied combinations; almost all the rest are unseen.

Those averages assume balanced independent sampling. The actual records still need frequency tables, duplicate checks, and conditional counts; an expectation is not an audit. Rare generation failures or filtering can also disturb the intended balance after sampling.

## A better release record

For a controlled synthetic corpus, I would publish three coverage summaries beside the row count: per-value frequencies, cross-slot pair frequencies, and the number of distinct full specifications. They expose different failures. A balanced marginal table can coexist with hidden pairwise coupling; clean pair counts can coexist with duplicated full prompts.

Three million rows make first- and second-order projections measurable. They do not make a trillion-cell space dense.

{% include thesis-series.html %}
