---
layout: post
title: "The TinyFabulist Idea: Structured Synthetic Narratives"
date: 2025-02-03 16:00:00 +0200
tags:
  - synthetic-data
  - language-models
  - natural-language-processing
---

After months of reading and planning, I have started building the first major component of my thesis work. I am calling it **TinyFabulist** -- a pipeline for generating large-scale synthetic moral fables using open language models.

## Why Fables

The choice of domain is deliberate. Moral fables have several properties that make them ideal for studying synthetic text generation:

- **Clear structure**: Every fable has characters, a setting, a conflict, a resolution, and a moral. This structure can be specified in advance and verified afterward.
- **Bounded length**: Fables are naturally short (200-500 words), which makes them tractable for smaller language models to both generate and learn from.
- **Cultural universality**: The fable tradition spans cultures and languages, which matters for my later goal of extending this work to Romanian.
- **Evaluability**: You can assess a fable along multiple meaningful dimensions -- grammatical correctness, creativity, moral clarity, and adherence to the given prompt.

## The YAML Approach

The core idea behind TinyFabulist is to separate **story specification** from **story generation**. Instead of prompting a model with a vague instruction like "write a fable," I define story elements in structured YAML files:

```yaml
characters:
  - name: a clever fox
    role: protagonist
  - name: a proud eagle
    role: antagonist
setting: a dense mountain forest
conflict: competition for the same territory
moral: wisdom prevails over strength
```

These YAML elements are then composed into structured prompts that give the language model clear constraints. The result is text that is synthetic but controlled -- I know exactly what the model was asked to produce, which makes evaluation meaningful.

## Why Open Models

A deliberate choice in TinyFabulist is to use only open-weight language models for generation. This is partly about reproducibility -- anyone should be able to regenerate the dataset -- but also about studying how different model families handle the same structured prompts. Do Llama and Qwen produce fables with different stylistic tendencies? Does Mistral follow moral constraints more faithfully than Phi? These are empirically testable questions when you have structured inputs.

## The Road to Scale

My initial experiments have been small -- a few hundred fables, testing different prompt templates and models. But the pipeline is designed for scale. The YAML-based approach means I can combinatorially generate thousands of unique story specifications, and the Docker-based infrastructure means I can distribute generation across multiple machines.

The target is ambitious: three million fables. That number is not arbitrary. It is large enough to serve as a meaningful pre-training or fine-tuning corpus, while still being fully reproducible from the structured specifications.

I will write more about the technical details of the pipeline and early results in upcoming posts. For now, I am excited to have moved from planning to building.
