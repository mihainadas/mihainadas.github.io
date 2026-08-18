---
layout: page
title: Notebooks
permalink: /notebooks/
description: "Tested notebooks accompanying Mihai Nadăș's engineering notes."
---

The public notebook repository now separates three executable notes from the exploratory scratchpad. CI validates every notebook file and runs the curated set from top to bottom.

## A perceptron you can audit

A two-weight implementation of the binary perceptron, with a deterministic balanced dataset, an epoch-level update trace, a held-out check, and an explicit statement of what the example does not establish.

- [Rendered notebook](https://mihainadas.github.io/notebooks/perceptron_en.html)
- [Source](https://github.com/mihainadas/notebooks/blob/main/perceptron/perceptron.ipynb)

## NumPy versus a Python loop

A repaired microbenchmark using warm-up, repeated trials, medians and IQRs across four vector sizes, result-equivalence assertions, and environment disclosure. It replaces an earlier one-shot timing whose saved output and prose disagreed by two orders of magnitude.

- [Rendered notebook](https://mihainadas.github.io/notebooks/numpy_vs_python.html)
- [Source](https://github.com/mihainadas/notebooks/blob/main/numpy/numpy_vs_python.ipynb)

## A logistic-regression baseline

A scaled, stratified baseline on scikit-learn's breast-cancer dataset. The notebook fixes the class mapping, removes the convergence warning, treats malignant cases explicitly in the ROC plot, and reports variation across five folds.

- [Rendered notebook](https://mihainadas.github.io/notebooks/logistic_regression.html)
- [Source](https://github.com/mihainadas/notebooks/blob/main/logistic_regression/logistic_regression.ipynb)

The survey notebook is retained as historical analysis but is marked under review until its population, skip logic, ordinal bins, and subgroup denominators are rebuilt.
