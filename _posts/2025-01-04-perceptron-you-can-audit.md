---
layout: post
title: "A Perceptron You Can Audit"
date: 2025-01-04 19:00:00 +0200
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: retrospective
description: "A January 2025 perceptron notebook rebuilt around inspectable updates, deterministic data, and explicit limits."
featured: true
redirect_from: /2025/01/04/simple-perceptron.html
tags: [machine-learning, perceptron, notebooks]
---

> **Retrospective.** The original notebook was written in January 2025. I rebuilt and re-executed it in August 2026 after finding that its prose overstated two results.

The original version did run, but it told a cleaner story than its outputs supported. It said a hand-picked boundary separated the data when it classified only part of the training set, and it claimed convergence one epoch before the mistake table reached zero. Neither error changes the perceptron algorithm. Both weaken trust in the notebook.

The revised version is intentionally smaller.

## The construction

An integer \(x_1\) becomes one of two points:

\[
x_2 = \begin{cases}
x_1 & \text{for even } x_1 \\
2x_1 & \text{for odd } x_1.
\end{cases}
\]

Points on the first line receive class 0; points on the second receive class 1. The classifier predicts class 1 when

\[
w_1x_1 + w_2x_2 + b \ge 0.
\]

This is a toy problem with a known linear separator. That is useful here: the update rule can be inspected without confusing algorithmic behavior with data quality.

## What changed

The repaired notebook now:

- constructs equal-size classes with a local seeded random generator;
- holds out four points, two from each class;
- records one row per epoch—mistakes, weights, and bias—instead of attaching the last sample to the whole epoch;
- asserts the final training and held-out accuracy;
- renders deterministic plots rather than relying on a live widget in static HTML;
- states the decision-line slope and intercept correctly;
- describes the returned separator as _a_ separator, not an optimum.

The implementation remains direct Python. There is no estimator abstraction hiding the update:

```python
for x1, x2, label in data:
    prediction = int(w1 * x1 + w2 * x2 + bias >= 0)
    update = learning_rate * (label - prediction)
    w1 += update * x1
    w2 += update * x2
    bias += update
```

This fence is abbreviated but executable in the context of the notebook. The repository test runs the complete notebook from a clean kernel and fails on cell errors or warnings written to standard error.

## The actual result

On the fixed 20-point construction, the learned boundary classifies all 16 training points and all four held-out points correctly. The four-point hold-out is a consistency check on the same two lines and says little about realistic generalization.

The perceptron convergence theorem gives the right boundary for the conclusion: linearly separable data leads to a finite number of updates. It does not guarantee a unique separator, a maximum margin, or useful behavior when the classes overlap.

- [Rendered notebook](https://mihainadas.github.io/notebooks/perceptron_en.html)
- [Source and execution test](https://github.com/mihainadas/notebooks)

Revisiting the notebook reinforced a simple rule: the prose and saved output must agree, even in a teaching example.
