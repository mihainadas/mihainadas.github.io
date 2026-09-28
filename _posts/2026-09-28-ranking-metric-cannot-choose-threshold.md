---
layout: post
title: "A Ranking Metric Cannot Choose a Threshold"
date: 2026-09-28 09:35:13 +0300
post_type: research note
description: "ROC AUC can stay fixed while calibration and the operating decision change. A classifier report needs all three."
context_reviewed: 2026-09-28
tags: [machine-learning, evaluation, experimental-design]
---

A binary classifier performs two separable jobs. It assigns each case a score, which orders cases by evidence for the positive class, and an operating rule converts that score into an action. My earlier [logistic-regression baseline](/2025/07/26/logistic-regression-baseline.html) used the Breast Cancer Wisconsin diagnostic dataset, treated malignant cases as the positive class, and reported ROC AUC alongside precision and recall.

Those numbers answer different questions. ROC AUC evaluates how well scores rank malignant cases above benign cases across possible cutoffs. Recall and precision describe the labels produced at one cutoff. A model can keep exactly the same ranking while a changed score scale moves many cases across the default cutoff.

This note isolates that distinction with six labeled cases. No medical claim follows from the toy sample. Its purpose is to show what a ranking metric preserves, what it discards, and why threshold selection belongs in the experimental protocol rather than in a default call to `predict`.

## AUC keeps the order

Consider three negative and three positive cases with these scores:

```python
import numpy as np
from sklearn.metrics import confusion_matrix, roc_auc_score


labels = np.array([0, 0, 0, 1, 1, 1])
scores = np.array([0.10, 0.40, 0.60, 0.55, 0.70, 0.90])
shifted = scores**3

print(roc_auc_score(labels, scores))
print(roc_auc_score(labels, shifted))
```

Both calls return (8/9), or approximately 0.889. There are nine positive-negative pairs. The positive case scored at 0.55 ranks above two negatives, while the positive cases at 0.70 and 0.90 each rank above all three. Eight pairs are ordered correctly.

Cubing every score is strictly increasing on this interval, so it preserves every pairwise order. The [`roc_auc_score` documentation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html) accepts either probability estimates or non-thresholded decision values because AUC concerns this ordering rather than one class cutoff.

The labels at a cutoff of 0.5 do not survive the transformation:

```python
for name, values in (("original", scores), ("cubed", shifted)):
    predicted = (values >= 0.5).astype(int)
    tn, fp, fn, tp = confusion_matrix(labels, predicted).ravel()
    print(name, {"tp": tp, "fp": fp, "fn": fn, "tn": tn})
```

The original scores produce three true positives and one false positive. The cubed scores produce one true positive, no false positives, and two false negatives. Their AUC values are identical. AUC does not contain a preferred numeric origin or scale from which 0.5 could be recovered.

This is not a criticism of AUC. It is the property that lets AUC compare ranking performance from probability estimates and raw decision scores. The mistake is asking that ranking summary to specify an operating decision.

## A threshold contains a cost judgment

A cutoff determines which errors the system accepts. On the original six scores, three candidate cutoffs give:

```text
cutoff 0.50: TP=3, FP=1, FN=0, TN=2
cutoff 0.65: TP=2, FP=0, FN=1, TN=3
cutoff 0.85: TP=1, FP=0, FN=2, TN=3
```

Suppose, only for arithmetic, that one missed positive costs five units and one false alarm costs one. The three error costs are 1, 5, and 10. Reverse that ratio, so that a false alarm costs five units and a miss costs one, and the costs become 5, 1, and 2. The score order and AUC did not change. The preferred cutoff among these candidates did.

Real decisions require a defensible objective rather than invented unit costs. The relevant quantities might be review capacity, the consequence of a missed case, a minimum recall constraint, or the measured utility of downstream actions. Scikit-learn's [threshold-tuning guide](https://scikit-learn.org/stable/modules/classification_threshold.html) makes the software boundary explicit: `predict_proba` or `decision_function` produces scores, while a threshold converts them to labels. Its usual 0.5 probability cutoff and zero decision-score cutoff are defaults, not application requirements.

Precision and recall must therefore be attached to the selected rule. Moving the cutoff changes both even when the model and every score remain fixed. Reporting “the model has 0.98 recall” without naming the positive class, cutoff, and evaluation set omits part of the classifier being evaluated.

## Calibration is a separate claim

The cubed values above remain useful scores for ranking, but calling them probabilities would require evidence. A calibrated probability has a frequency interpretation: among cases assigned a value near 0.8, roughly 80% should belong to the positive class. Scikit-learn's [calibration guide](https://scikit-learn.org/stable/modules/calibration.html) tests this relation with reliability diagrams that compare mean predicted probability with observed positive frequency in bins.

A strictly increasing transformation can preserve AUC while changing calibration. That gives two independent questions:

- Does the model rank positive cases ahead of negative cases?
- Do its numeric outputs support a probability interpretation?

The second matters when a decision rule uses estimated risk, expected cost, or a probability communicated to a person. It is less necessary when a validated rule simply reviews the highest-scoring fixed number of cases, though that rule still needs evaluation under the deployment distribution.

Logistic regression does not make calibration automatic. The scikit-learn guide notes why logistic regression can be well calibrated when the model is correctly specified and regularization is appropriate. Dataset shift, regularization, feature changes, and a mismatched functional form can still break the frequency interpretation. Calibration has to be measured on data not used to fit the calibrator.

## Do not spend the test set choosing the cutoff

Threshold selection is model selection even when the fitted coefficients never change. Trying many cutoffs on the final test set and keeping the one with the best F1 score adapts the reported result to that test sample.

A clean protocol separates three roles:

1. Fit preprocessing and model parameters on training data.
2. Select or tune the operating rule on validation data or within an explicit cross-validation procedure.
3. Evaluate the fixed model and fixed rule once on a held-out test set.

Scikit-learn's [`TunedThresholdClassifierCV`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TunedThresholdClassifierCV.html) implements the second role by optimizing a specified binary metric over thresholds using cross-validation. Its documentation also warns against fitting the estimator and selecting its cutoff on the same data. Cross-validation handles the mechanics; it does not choose the right objective or positive label for the application.

The evaluation record should preserve the score source, positive-class mapping, calibration method if any, threshold objective, data used for selection, chosen cutoff, and final confusion counts. Those fields make clear which result belongs to ranking and which belongs to the operating rule.

## Report the score and the rule

The earlier Wisconsin baseline's ROC AUC of 0.995 supports a narrow statement about ranking on resamples of that dataset. Its malignant-class recall of 0.98 supports a different statement about one fitted pipeline, label mapping, and cutoff on one holdout split. Neither number determines the other.

A deployable classifier is not just a scoring function. It is a scoring function plus a declared rule for acting on the score. AUC can compare the first part across all cutoffs. Calibration can test whether the score has a probability meaning. The threshold, selected against a stated objective on separate data, completes the decision.
