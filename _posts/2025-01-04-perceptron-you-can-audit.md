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

I rebuilt the notebook around the disagreement between its prose and saved output.

## The construction

An integer \(x_1\) is sampled without replacement from 1 through 100 and becomes one of two points:

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

## The repair

The data construction now uses equal-size classes and a local seeded generator; four points, two from each class, are held out before training. The training trace and reporting layer were repaired separately:

- one row now represents one epoch, with its mistake count, weights, and bias;
- the notebook asserts both training and held-out accuracy;
- deterministic plots replace the live widget that disappeared from static HTML;
- the text reports the line's slope and intercept correctly and calls it _a_ separator, not an optimum.

The implementation remains direct Python. There is no estimator abstraction hiding the update:

```python
for x1, x2, label in data:
    prediction = int(w1 * x1 + w2 * x2 + bias >= 0)
    update = learning_rate * (label - prediction)
    w1 += update * x1
    w2 += update * x2
    bias += update
```

The repository test runs the complete notebook from a clean kernel and fails on cell errors or warnings written to standard error.

## The actual result

On the fixed 20-point construction, the learned boundary classifies all 16 training points and all four held-out points correctly. The four-point hold-out is a consistency check on the same two lines and says little about realistic generalization.

The perceptron convergence theorem gives the right boundary for the conclusion: linearly separable data leads to a finite number of updates. It does not guarantee a unique separator, a maximum margin, or useful behavior when the classes overlap.

- [Rendered notebook](https://mihainadas.github.io/notebooks/perceptron_en.html)
- [Source at the executed revision](https://github.com/mihainadas/notebooks/blob/63389f88cf80c901e1ff409477a461261cc0f9ec/perceptron/perceptron.ipynb)
- [Execution test](https://github.com/mihainadas/notebooks/blob/63389f88cf80c901e1ff409477a461261cc0f9ec/scripts/test_notebooks.py)

The saved trace makes the correction visible:

| Epoch | Mistakes | \(w_1\) | \(w_2\) | Bias |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 8 | -0.440 | 0.340 | -0.040 |
| 2 | 0 | -0.440 | 0.340 | -0.040 |

The learned parameters stay fixed after epoch 1; convergence is reportable at epoch 2, when the first zero-mistake pass completes.
