---
layout: post
title: "A Logistic-Regression Baseline Worth Keeping"
date: 2025-07-26 10:00:00 +0300
published_at: 2026-08-27 10:00:00 +0300
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: retrospective
description: "A July 2025 notebook repaired to make scaling, class semantics, stratification, and uncertainty explicit."
tags: [machine-learning, scikit-learn, notebooks]
---

> **Retrospective.** The first notebook was committed on 26 July 2025. The August 2026 revision corrects the target mapping and removes a convergence warning.

The original notebook used scikit-learn's Breast Cancer Wisconsin diagnostic dataset and described its target backwards. The dataset defines `0 = malignant` and `1 = benign`. The saved estimator also emitted an `lbfgs` convergence warning because features with very different scales went directly into logistic regression.

The two defects compound. Reverse the class meaning and recall answers the wrong clinical question; ignore the warning and the displayed coefficients may come from unfinished optimization.

## The repaired baseline

The model now uses a pipeline:

```python
model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=2_000, random_state=42),
)
```

The train/test split is stratified and deterministic. Scaling stays inside the pipeline, so cross-validation learns preprocessing from each training fold rather than leaking full-dataset statistics into validation.

The stratified split contains 455 training and 114 hold-out samples. On the hold-out set, the malignant class has precision 0.98, recall 0.98, and F1 0.98 across 42 cases; overall accuracy is 0.982.

Five-fold stratified cross-validation gives:

| Metric | Mean | Standard deviation |
| --- | ---: | ---: |
| Accuracy | 0.974 | 0.019 |
| Balanced accuracy | 0.968 | 0.026 |
| ROC AUC, malignant positive | 0.995 | 0.006 |

## Limits of the score

The dataset is small and curated. Cross-validation only resamples this collection; it says nothing about a new hospital or a changed prevalence. ROC AUC also leaves calibration and the operating threshold unresolved, which is where a clinical decision would actually be made.

The ROC calculation makes the class conversion explicit:

```python
malignant = (target == 0).astype(int)
probability = estimator.predict_proba(features)[:, 0]
```

Without those two lines, a high AUC could be attached to the opposite clinical event while the plot still looked convincing.

- [Rendered notebook](https://mihainadas.github.io/notebooks/logistic_regression.html)
- [Source at the executed revision](https://github.com/mihainadas/notebooks/blob/63389f88cf80c901e1ff409477a461261cc0f9ec/logistic_regression/logistic_regression.ipynb)
- [Dataset documentation](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_breast_cancer.html)
