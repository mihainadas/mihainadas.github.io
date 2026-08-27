---
layout: post
title: "The Panel Was Weak on Items and Useful for Ranking Systems"
date: 2026-08-27 09:11:56 +0300
published_at: 2026-08-27 09:11:56 +0300
feed_date: "2026-08-27 09:11:56 +0300"
last_modified_at: 2026-08-27 09:11:56 +0300
post_type: research note
description: "An open-weight judge panel was weak at item-level agreement yet useful for ranking systems in one fixed protocol."
tags: [evaluation, open-models, language-models]
series: controlled-synthetic-narratives
series_order: 4
evidence_status: accepted
---

The three panel members disagreed on individual scores. After median aggregation, the panel's TF1 system ranking tracked o4-mini at Spearman \(\rho=0.93\) and Kendall \(\tau=0.78\).

Those results concern different units of analysis. The first tests item-level labels; the second tests whether an aggregated instrument orders systems similarly to a proprietary comparator. The fixed panel combined Granite 4.1 30B, EXAONE 3.5 32B, and Granite 3.3 8B. Across three tasks it ran 6,180 evaluations, with another 900 bias reruns. Item-level agreement remained weak: Krippendorff's alpha ranged from −0.34 to +0.12, and mean weighted kappa from −0.02 to +0.15.

> **Evidence status.** The panel study was accepted by the thesis cutoff. The human-arbitration protocol remains proposal-stage and has not run.

{% include figure.html
  src="/assets/figures/judges-rank-systems-not-items/agreement.svg"
  mobile_src="/assets/figures/judges-rank-systems-not-items/agreement-mobile.svg"
  alt="A diagram separating low item-level agreement from high aggregate rank agreement, ending at a human-review gate that remains open."
  caption="The measured evidence supports aggregate system ranking under the tested protocol, not trustworthy labels for individual items."
  width="1200"
  height="630"
  mobile_width="320"
  mobile_height="1030"
  wide=true
%}

## Agreement depends on the object

For individual items, the judges often used the rubric differently. That is not surprising in literary generation and translation: an answer can preserve meaning while losing style, or read fluently while changing an event. A single ordinal score compresses those disagreements.

Aggregation changed the picture. Under the paper protocol, TF1 system rankings from the panel tracked the o4-mini reference at Spearman \(\rho=0.93\) and Kendall \(\tau=0.78\). A later composition analysis using the full panel produced \(\rho=0.952\) and \(\tau=0.822\). These are different protocols, so the two pairs should not be blended into one headline number.

The defensible operating rule is narrow: use the panel for the tested TF1 model-selection protocol and report system-level rank agreement. Do not infer from that result that its item scores are reliable filters.

## Three judges are not three independent views

Panel size alone can overstate diversity. Two members come from the Granite family. Model lineage, training data, and instruction style can create correlated errors even when parameter counts differ. A panel audit therefore needs more than a list of checkpoints: family diversity, order sensitivity, rubric perturbations, and repeated runs belong in the record.

The 900 bias reruns address part of that record. They do not prove independence or eliminate shared blind spots.

## The human gate is still open

The proposed workflow routes model disagreements and other ambiguous cases to human review. The thesis projects a reduction from 3,588 human judgments under a three-rater, per-task protocol to 255 judgments concentrated on 85 disagreement cases. That is a planning estimate, not a completed human study.

Until the arbitration is run, the panel is a ranking instrument with a known weak point. It can reduce the amount of work presented to people; it has not earned the right to stand in for them.

{% include thesis-series.html %}
