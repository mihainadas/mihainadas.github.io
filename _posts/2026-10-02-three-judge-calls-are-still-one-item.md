---
layout: post
title: "Three Judge Calls Are Still One Item"
date: 2026-10-02 09:34:00 +0300
post_type: research note
description: "Repeated judge calls measure within-item variation. They do not turn one held-out item into several independent test cases."
context_reviewed: 2026-10-02
tags: [evaluation, statistics, language-models, experimental-design]
---

TinyFabulist compares story generators and translation systems on held-out items. A model judge may score the same output more than once to reveal sampling instability, presentation-order effects, or invalid responses. The resulting table can contain several rows for one item, one system, and one judge configuration.

My earlier note on [paired and independent bootstrap designs](/2026/05/02/interval-belongs-to-comparison.html) treated each held-out item as one observation. Repeated judge calls add another level. They measure how the evaluator varies while the text, requested task, and item difficulty remain fixed. They do not add new stories or translations to the test set.

This note isolates the consequence with four items and three calls per item. The example is deliberately small and contains no TinyFabulist result. It shows why resampling twelve score rows can report much less uncertainty than resampling the four item identities that generated them.

## Twelve rows can contain four independent units

Suppose two systems are scored on the same four items. Subtract system B's score from system A's score for each judge call. To make the dependence visible, let all three calls for an item return the same difference:

| Item | Call 1 | Call 2 | Call 3 |
| --- | ---: | ---: | ---: |
| 1 | -1 | -1 | -1 |
| 2 | 0 | 0 | 0 |
| 3 | 1 | 1 | 1 |
| 4 | 4 | 4 | 4 |

The mean difference is 1.0 whether it is computed over four item means or twelve rows. The point estimate does not expose the problem.

A row bootstrap draws twelve values independently from the twelve cells. It can draw the first copy of item 4 without the other two, as if those copies described different sampled texts. An item bootstrap draws four item identities. When item 4 is selected, its three calls travel together because they share the same experimental unit.

Enumerating both empirical bootstrap distributions gives:

| Resampling unit | Units drawn | Bootstrap standard error | 95% discrete percentile interval |
| --- | ---: | ---: | ---: |
| score row | 12 | 0.540 | [0.000, 2.083] |
| item | 4 | 0.935 | [-0.500, 3.000] |

The row analysis reduces the standard error by a factor of about \(\sqrt{3}\), exactly what would happen if three perfect copies had tripled the sample size. They did not. The narrower interval is manufactured by the independence assumption.

This is a compact instance of [pseudoreplication](https://doi.org/10.2307/1942661): repeated measurements are analyzed as independent replicates even though they belong to the same experimental unit. Stochastic judge outputs make the copies less obvious, but they do not remove the shared item.

Four items are not enough for a defensible system comparison, and these percentile bounds are not proposed as a small-sample remedy. The construction only holds the point estimate fixed while exposing what the resampling unit changes.

## Pairing and clustering preserve different relations

Pairing answers the system-comparison question. If systems A and B translated the same source sentence, their scores for that sentence must stay together. A difficult sentence can lower both scores, and the paired difference removes part of that shared item effect.

Clustering answers the repetition question. If one sentence was judged three times, those calls remain attached to that sentence when items are resampled. Flattening the table and preserving only the A/B row alignment keeps the system pair but loses the item cluster.

SciPy's [`bootstrap` documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html) makes the first operation explicit: with `paired=True`, it draws one index array and applies it to every input sample. That is sufficient when each index names one item. It does not infer clusters from repeated item identifiers in a long table.

For balanced repeats, the simplest item-level estimator is:

\[
d_i = \frac{1}{R}\sum_{r=1}^{R}(s_{Air} - s_{Bir}),
\qquad
\hat{\Delta} = \frac{1}{N}\sum_{i=1}^{N} d_i.
\]

Compute one mean difference \(d_i\) per item, then bootstrap the \(N\) item differences. Every item receives equal weight. Three calls refine the estimate for item \(i\); they do not change \(N\).

## The target determines whether calls are resampled

Collapsing to item means treats the observed calls as the measurement used for each item and estimates variation across new items under that fixed procedure. That often matches the question behind a held-out evaluation: how stable is the mean system gap over another sample of comparable items?

If the target also includes fresh stochastic judge calls, a two-level bootstrap can represent both sources. First sample item identities with replacement. Within each selected item, sample its judge calls with replacement. Recompute the per-item mean and then the system gap. The [hierarchical-bootstrap paper by Saravanan, Berman, and Sober](https://pmc.ncbi.nlm.nih.gov/articles/PMC7906290/) describes this resampling pattern for nested measurements and publishes the [simulation code](https://github.com/soberlab/Hierarchical-Bootstrap-Paper) used to study it.

Those procedures answer different questions. The item-only bootstrap conditions on the observed measurement procedure. The two-level bootstrap includes its finite-call variation. Neither procedure turns judge calls into additional item coverage.

The design becomes more complicated when every item is scored by every member of a judge panel. Items and judges are then crossed rather than purely nested. Whether judges should be resampled depends on whether the named checkpoints are fixed instruments or a sample from a wider population of possible judges. A generic hierarchical loop cannot decide that estimand.

## Unequal repeats create an accidental weighting rule

Evaluation tables rarely stay balanced. One item may need a retry after malformed JSON, another may time out, and a third may receive extra calls during an audit. Averaging every surviving row gives more weight to items with more valid responses.

That weighting might be intended, but it should not arise from failure handling. An invalid response followed by a successful retry is one requested measurement with two linked attempts, not two votes. If each held-out item should count equally, aggregate according to a declared retry rule and compute one item contribution before resampling.

The minimum record needs enough structure to reconstruct that choice:

```text
item_id, system_id, judge_id, judge_digest,
prompt_version, run_id, seed, presentation_order,
attempt_id, retry_of, parse_status, score
```

Without `item_id`, cluster membership is gone. Without `attempt_id` and `retry_of`, a transport failure can silently change statistical weight. Without the judge and prompt versions, repeated calls may combine different instruments under one label.

## Spend repetitions on the uncertainty they can reduce

Additional judge calls can estimate within-item instability. They can reveal a position-sensitive comparison, quantify invalid-output rates, or reduce noise in an item's aggregated score. They cannot reveal how the systems behave on an unseen kind of story or translation.

For a fixed evaluation budget, one more call on an existing item and one call on a new item therefore buy different evidence. The first measures the evaluator more precisely at a known point. The second expands item coverage. A confidence interval should preserve that distinction by resampling the identity that was actually sampled.
