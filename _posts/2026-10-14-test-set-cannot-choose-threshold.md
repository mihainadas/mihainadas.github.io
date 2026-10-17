---
layout: post
title: "A Test Set Cannot Choose Its Own Threshold"
date: 2026-10-14 09:33:01 +0300
post_type: research note
description: "Choosing a classifier cutoff on the final test labels turns evaluation noise into an optimistic result, even when the score order contains no signal."
context_reviewed: 2026-10-14
math: true
tags: [machine-learning, evaluation, model-selection, experimental-design]
---

A binary classifier produces a score for each case, then a threshold converts that score into a positive or negative decision. My earlier note on [ranking and thresholds](/2026/09/28/ranking-metric-cannot-choose-threshold.html) separated those two operations: ROC AUC evaluates the score order, while recall, precision, and error cost depend on the chosen cutoff.

Selecting the cutoff does not change the fitted coefficients, but it still uses labels to choose one rule from several candidates. If the same final test labels choose the threshold and measure its performance, the reported score includes the noise that made this threshold win. The test set has become part of model selection.

This note makes that bias exact with ten fixed scores that contain no label information. Across every balanced assignment of five positive labels, the best same-sample threshold averages 65.3% accuracy. Apply the selected threshold to an independent balanced assignment and its expected accuracy is 50%. The apparent improvement comes entirely from reusing the labels.

## Eleven cutoffs search one random ordering

Number ten cases from lowest score to highest score. The score order is fixed before any labels are assigned. Exactly five cases are positive, but every one of the \\(\binom{10}{5}=252\\) balanced labelings is equally likely. Under this construction, the scores carry no information about the labels.

A threshold between adjacent scores can predict the highest \\(k\\) cases as positive, for \\(k=0,1,\ldots,10\\). These are eleven distinct decision rules. For each labeling, choose the value of \\(k\\) with the largest accuracy on those same ten cases.

Exact enumeration gives this distribution:

| Best correct predictions | Labelings | Fraction of all labelings |
| ---: | ---: | ---: |
| 5 of 10 | 42 | 1/6 |
| 6 of 10 | 90 | 5/14 |
| 7 of 10 | 75 | 25/84 |
| 8 of 10 | 35 | 5/36 |
| 9 of 10 | 9 | 1/28 |
| 10 of 10 | 1 | 1/252 |

The mean of the selected accuracies is

\\[
\frac{823}{1260} \approx 0.6532.
\\]

One of the 252 random labelings can even be separated perfectly by a threshold: all five negatives happen to receive the lower scores and all five positives the higher scores. That event is rare, but every labeling lets the selection procedure keep its most favorable cutoff.

The enumeration needs no machine-learning library:

```python
from itertools import combinations
from statistics import mean


n = 10
all_cases = set(range(n))
best_accuracies = []

for positive_tuple in combinations(range(n), n // 2):
    positive = set(positive_tuple)
    accuracies = []

    for k in range(n + 1):
        predicted_positive = set(range(n - k, n))
        true_positive = len(positive & predicted_positive)
        true_negative = len(
            (all_cases - positive) - predicted_positive
        )
        accuracies.append((true_positive + true_negative) / n)

    best_accuracies.append(max(accuracies))

print(mean(best_accuracies))  # 0.6531746031746032
```

This value is not a universal correction for threshold tuning. It belongs to ten cases, balanced labels, accuracy, and this set of eleven nested rules. Its role is to show the mechanism without simulation error.

## A fixed cutoff has no advantage here

For any fixed \\(k\\), the highest-scored group contains \\(k/2\\) positives on average. The remaining \\(10-k\\) cases contain \\((10-k)/2\\) negatives on average. The expected number of correct predictions is therefore

\\[
\frac{k}{2} + \frac{10-k}{2} = 5,
\\]

so the expected accuracy is 50% for every cutoff chosen without seeing the evaluated labels.

The selected cutoff is also fixed before an independent second labeling is revealed. Conditional on any \\(k\\) chosen from the first sample, its expected accuracy on that second balanced sample is still 50%. Averaging over the threshold-selection procedure does not change the result.

The gap between 65.3% and 50% is selection bias. Each individual accuracy is an unbiased estimate for its fixed rule under this construction. The maximum of the eleven noisy estimates is not an unbiased estimate of the selected rule's future accuracy.

The thresholds are strongly dependent, so the example is not equivalent to taking the maximum of eleven independent measurements. Dependence reduces the search space, but it does not remove selection. A run of positives near one end of the random score order can still make one cutoff look useful on the sample that exposed the run.

## Threshold tuning is part of fitting

The same boundary applies to a real classifier. Choosing a cutoff to maximize F1, balanced accuracy, recall under a precision constraint, or measured utility adapts a decision rule to labeled data. The operation may leave the score function unchanged, but the deployed predictor now contains a learned threshold.

Scikit-learn's [`TunedThresholdClassifierCV`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TunedThresholdClassifierCV.html) represents that threshold as fitted state. Its documentation describes cross-validated cutoff selection and explicitly warns that using `cv="prefit"` with the same data for estimator fitting and threshold tuning is subject to overfitting.

That warning covers one reuse boundary. A second boundary appears at evaluation time. If cross-validation chooses the cutoff and the same cross-validation score is then presented as the final performance estimate, the selection criterion is being used to assess its own winner. Cawley and Talbot's paper on [over-fitting in model selection](https://www.jmlr.org/papers/volume11/cawley10a/cawley10a.pdf) treats model selection as part of fitting and shows why performance evaluation must include that complete procedure.

A clean single-split experiment assigns three roles:

1. Fit preprocessing and score-model parameters on training data.
2. Choose the threshold and its objective on separate validation data.
3. Freeze both, then evaluate once on the test data.

The [scikit-learn cross-validation guide](https://scikit-learn.org/stable/modules/cross_validation.html) gives the same separation for hyperparameter selection: settings chosen to optimize test performance leak test information into the model, so the final test set remains held out after validation or cross-validation.

Thresholds deserve the same treatment as regularization strengths, feature choices, and calibration methods. They are all decisions informed by labels.

## The outer split evaluates the procedure

When one validation split would waste too much data or make the result depend heavily on one partition, nested cross-validation can estimate the complete procedure. In each outer fold:

1. Use only the outer training portion to fit preprocessing and the score model.
2. Use an inner split or inner cross-validation to choose the threshold.
3. Apply the resulting model and fixed threshold to the untouched outer test portion.

The outer predictions can then be collected for an overall confusion matrix or scored within folds according to a declared aggregation rule. Threshold selection must restart inside every outer fold. Choosing one global threshold from all out-of-fold labels before scoring those same labels would recreate the original reuse in a less visible form.

After evaluation, a final deployment model may be refit on all available development data and receive a threshold selected by the declared inner procedure. The outer-fold score estimates that procedure's performance; it does not certify that one final numeric threshold is invariant across samples.

Threshold variability is itself useful evidence. If small changes to the validation set move the selected cutoff widely while the objective barely changes, reporting only one threshold hides an unstable choice. The metric curve around the optimum, fold-level thresholds, and confusion counts can distinguish a broad plateau from a sharp, sample-specific maximum.

## Preserve the selection path

A reproducible threshold result needs more than the final number. I would retain:

- the score source, positive-class mapping, and fitted preprocessing;
- the candidate threshold rule, including ties and endpoint cutoffs;
- the selection objective and any constraints or error costs;
- the sample or inner folds used to choose the threshold;
- the independent sample or outer folds used for evaluation;
- the chosen threshold, objective curve, and final confusion counts.

Those fields separate the rule that was searched from the data that judged the search. A threshold can be tuned aggressively when the application requires it. The final test labels must remain unavailable until that tuning is finished.
