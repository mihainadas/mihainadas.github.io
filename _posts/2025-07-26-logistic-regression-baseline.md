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

The original notebook used scikit-learn's Breast Cancer Wisconsin diagnostic dataset. It also reversed the target description: the dataset defines `0 = malignant` and `1 = benign`, not the other way around. The saved estimator emitted an `lbfgs` convergence warning because features with very different scales were passed directly to logistic regression.

Those are not cosmetic defects. A reversed class description corrupts the interpretation of recall and false negatives. A convergence warning means the displayed coefficients and metrics may come from an unfinished optimization.

## The repaired baseline

The model now uses a pipeline:

```python
model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=2_000, random_state=42),
)
```

The train/test split is stratified and deterministic. Scaling stays inside the pipeline, so cross-validation learns preprocessing from each training fold rather than leaking full-dataset statistics into validation.

The notebook reports a hold-out classification table and a five-fold distribution for accuracy, balanced accuracy, and ROC AUC. In the ROC plot, malignant cases are converted to the explicit positive condition. That keeps the clinical consequence aligned with the curve even though scikit-learn's numeric positive label is normally 1.

## Limits of the score

The dataset is small and curated. Cross-validation estimates variation across partitions of this dataset; it does not test a new hospital, different imaging equipment, changed prevalence, calibration, or performance across demographic groups.

The notebook is a baseline example intended to demonstrate a sequence of defensible defaults: verify labels, stratify, scale inside the pipeline, inspect class-specific errors, and report a distribution rather than one favorable split.

- [Rendered notebook](https://mihainadas.github.io/notebooks/logistic_regression.html)
- [Source](https://github.com/mihainadas/notebooks/blob/main/logistic_regression/logistic_regression.ipynb)
- [Dataset documentation](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_breast_cancer.html)
