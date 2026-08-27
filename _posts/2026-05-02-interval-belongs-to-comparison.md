---
layout: post
title: "The Interval Belongs to the Comparison"
date: 2026-05-02
published_at: 2026-08-27 09:11:56 +0300
feed_date: "2026-08-27 09:11:56 +0300"
last_modified_at: 2026-08-27 09:11:56 +0300
post_type: research note
description: "Why two model gaps require different bootstrap designs—and why one missing record prevents an interval altogether."
tags: [evaluation, statistics, language-models]
series: controlled-synthetic-narratives
series_order: 3
evidence_status: thesis-analysis
---

A score has no pairing structure. A comparison does.

That difference determines the bootstrap. In TF1, candidate generators were evaluated on disjoint samples, so the model gap was resampled independently. In TF2, several systems translated the same held-out items, so the gap was resampled by item. Calling both procedures “a bootstrap confidence interval” hides the experimental design that makes each one valid.

> **Archive note.** The 2 May date marks [TF1 arXiv v2](https://arxiv.org/abs/2504.20605v2), which introduced the revised panel evaluation. The confidence-interval analysis itself was added later in the August 2026 thesis draft.

{% include figure.html
  src="/assets/figures/interval-belongs-to-comparison/bootstrap.svg"
  mobile_src="/assets/figures/interval-belongs-to-comparison/bootstrap-mobile.svg"
  alt="Two bootstrap paths: independent resampling for model scores measured on different stories, and paired item resampling for systems evaluated on the same translations. A third path stops because per-item outputs were not retained."
  caption="Resample the unit that carries the comparison. Without per-item records, a paired interval cannot be reconstructed."
  width="1200"
  height="650"
  mobile_width="320"
  mobile_height="1110"
  wide=true
%}

## Different stories: resample independently

The TF1 historical-judge comparison between Tulu and Llama has an estimated gap of +0.02 with a 95% bootstrap interval of [−0.13, +0.17]. The open-panel comparison gives +0.12 [+0.07, +0.18]. Each model was scored on its own sampled stories. One model's row 37 is not the counterpart of the other's row 37, so preserving row numbers as pairs would invent dependence.

Independent resampling respects that design: draw with replacement within each model's sample, recompute the two means, then store their difference. The interval is about the difference of two sample means, not a halo around either score.

The two TF1 intervals also make a useful substantive distinction. The historical-judge gap includes zero; the panel gap does not under this analysis. That does not make the panel ground truth. It says the measured separation is more stable under one evaluator construction.

## Same items: keep the pair intact

TF2 systems translated the same items. Their errors can therefore be correlated: a difficult sentence may reduce every system's score. Resampling each system separately would throw away that information and usually misstate the uncertainty of the difference.

The paired procedure samples item indices and carries every system score attached to an index. It produced +0.03 [−0.02, +0.08] for o3 minus GPT-4.1, and +0.31 [+0.23, +0.41] for o3 minus TF2-4B. The first interval does not establish a separation; the second does on this set and evaluator.

## The missing interval

TF2-12B was reported nine hundredths below o3, but its per-item evaluation outputs were not retained. A mean and a sample size cannot recover the covariance between systems. There is no honest paired interval to compute after the fact.

Missing the item rows removed the covariance needed for a paired interval. It also ruled out parity or non-inferiority language. The repair is operational: preserve one row per evaluated item, with the input identifier, system output, judge scores, prompt version, and run metadata.

The choice between paired and independent bootstrap is made before any random resampling begins. It lives in the data lineage of the comparison.

{% include thesis-series.html %}
