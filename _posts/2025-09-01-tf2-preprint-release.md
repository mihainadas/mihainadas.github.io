---
layout: post
title: "Building Large-Scale EN-RO Translation Resources"
date: 2025-09-01 09:00:00 +0300
tags:
  - translation
  - dataset-release
  - romanian-nlp
  - synthetic-data
---

The TF2 paper is now on arXiv, and both datasets are available on HuggingFace. This post summarizes what we built and why it matters for Romanian NLP.

The preprint is available at [arXiv:2509.07829](https://arxiv.org/abs/2509.07829). The datasets are [klusai/ds-tf2-en-ro-3m](https://huggingface.co/datasets/klusai/ds-tf2-en-ro-3m) (the full 3M parallel corpus) and [klusai/ds-tf2-en-ro-15k](https://huggingface.co/datasets/klusai/ds-tf2-en-ro-15k) (a curated 15K subset).

## What TF2 Contains

The TF2 project produced three main artifacts:

**TF2-12B**: A LoRA-fine-tuned translation model based on a 12B-parameter open-weight model, specialized for English-to-Romanian literary translation.

**DS-TF2-EN-RO-3M**: A parallel corpus of three million English-Romanian fable pairs. Each pair includes the English source (from TF1), the Romanian translation, the model that produced the translation, and five-dimensional quality scores.

**DS-TF2-EN-RO-15K**: A curated subset of 15,000 high-quality translation pairs, selected based on evaluation scores across all five dimensions. This subset is intended for fine-tuning and benchmarking.

## Why Two Datasets

The full 3M corpus is useful for pre-training and large-scale experiments, but not every translation in it is high quality. The 15K curated subset applies quality thresholds on all five evaluation dimensions (accuracy, fluency, coherence, style, cultural/pragmatic adaptation) to provide a clean, high-quality resource.

This two-tier approach is deliberate. Researchers working on data filtering or quality estimation benefit from having the full range of quality levels. Researchers who just need good parallel data can use the 15K subset directly.

## Evaluation Highlights

The paper includes a systematic comparison of zero-shot, few-shot, and LoRA-fine-tuned models across the five-dimensional rubric. Key findings:

- Fine-tuned models consistently outperform zero-shot models on accuracy and fluency
- Style scores show the most variation across models and the least improvement from fine-tuning
- The cultural/pragmatic dimension is where Romanian-language expertise matters most -- models often produce technically correct translations that sound unnatural to native speakers

## Budget-Aware Translation

One practical contribution of TF2 is a cost analysis of large-scale translation with open models. Running translation inference on consumer hardware (Apple Silicon) is feasible but slow. The paper includes timing benchmarks and cost estimates for different hardware configurations, which I hope will be useful for other researchers planning similar projects on a budget.

## What Comes Next

TF2 gives us a large parallel corpus. The natural next question is: can we use this corpus to train a compact Romanian language model from scratch? That is the premise of TF3, which I have already started working on.
