---
layout: post
title: "Synthetic Data Generation with LLMs: A Survey Published in IEEE Access"
date: 2025-03-31 11:00:00 +0300
tags:
  - synthetic-data
  - natural-language-processing
  - machine-learning
---

I am happy to share that my survey paper on synthetic data generation using large language models has been published in IEEE Access. The preprint is available on [arXiv (2503.14023)](https://arxiv.org/abs/2503.14023).

## What the Survey Covers

The paper provides a comprehensive overview of how LLMs are being used to generate synthetic data for both text and code. It covers:

- **Generation methods**: From simple prompting and few-shot demonstrations to more sophisticated approaches like self-instruct, evol-instruct, and multi-agent generation pipelines.
- **Quality control**: How researchers filter, validate, and curate synthetic data to ensure it is useful for downstream tasks.
- **Applications**: Instruction tuning, data augmentation for low-resource settings, evaluation benchmark creation, and domain-specific corpus generation.
- **Risks and limitations**: Including model collapse from training on synthetic data, stylistic homogeneity, factual errors, and the challenge of evaluating synthetic data quality at scale.

## Why This Matters for My Thesis

This survey grew directly out of my PhD literature review. When I started reading about synthetic data generation, I found that the field was moving so fast that no single paper captured the full landscape. Existing surveys covered specific sub-areas (instruction tuning, or code generation) but none provided a unified view across text and code, across generation methods, and across application domains.

Writing the survey forced me to organize my understanding of the field systematically. It also helped me identify the specific gap my thesis work addresses: most synthetic data generation targets general-purpose instruction following, while controlled, domain-specific generation (like the structured fable generation in TinyFabulist) remains underexplored.

## Open Access

One aspect I appreciate about IEEE Access is that papers are open access by default. Academic publishing has its frustrations, but making research freely available to anyone is a value I want to uphold throughout my PhD work.

The survey is a snapshot of the field as of early 2025. Given the pace of progress, it will inevitably become dated, but I hope it serves as a useful reference for researchers entering this space.
