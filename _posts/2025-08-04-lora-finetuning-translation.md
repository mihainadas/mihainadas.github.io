---
layout: post
title: "What LoRA Changes in the TF2 Translation System"
date: 2025-08-04 14:00:00 +0300
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: engineering note
description: "The role of low-rank adaptation, quantization, and the 15K reference set in TF2."
tags: [language-models, translation, fine-tuning]
---

TF2 uses low-rank adaptation to move a general 12B open model toward English–Romanian literary translation without updating every base-model parameter.

For a weight matrix \(W\), LoRA learns a low-rank update \(BA\) and applies \(W + BA\) at inference or after merging. The trainable matrices are much smaller than \(W\), reducing optimizer state and checkpoint size enough to make the experiment feasible on constrained hardware.

## The data boundary

The fine-tuning set is the curated 15K reference corpus, not the full three-million-pair release. Its purpose is to teach the task and narrative style from higher-quality examples. The large corpus is a downstream artifact produced at scale.

Keeping those roles separate prevents a common circular description in which a model appears to be trained on data it later generated.

## Why quantization appears in the system

Quantization reduces the memory footprint of the frozen base model during adaptation and deployment. The adapter remains a small set of higher-precision trainable parameters. The exact memory and speed benefit depends on the base model, quantization method, kernels, sequence length, and batch size.

The first version of this note included an abbreviated code fragment with undefined variables and no executable environment. It has been removed. Configuration belongs in the released training scripts and paper, where model identifiers, target modules, ranks, precision, and data versions can be read together.

## The result to look for

The comparison tracks how adaptation changes the accuracy–style balance relative to the base model, alongside training cost, inference cost, and results from much larger systems.

The [TF2 paper](https://arxiv.org/abs/2509.07829) reports that comparison for the released 12B model. Its near-parity result is bounded by the fable domain, English–Romanian direction, reference set, evaluators, and tested systems.

LoRA is the mechanism that made the adaptation economical. The research claim comes from the controlled before/after evaluation, not from the choice of adapter library.
