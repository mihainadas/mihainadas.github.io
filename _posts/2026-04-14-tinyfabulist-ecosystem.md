---
layout: post
title: "The TinyFabulist Ecosystem: Connecting Generation, Translation, and Evaluation"
date: 2026-04-14 11:00:00 +0300
tags:
  - synthetic-data
  - language-models
  - evaluation
  - phd-journey
---

As I approach the final stretch of my PhD, I want to step back and describe how the different pieces of my research connect into a coherent whole. The TinyFabulist ecosystem spans three major tasks, multiple papers, and several open-source tools and datasets. Here is how they fit together.

## The Pipeline

The TinyFabulist ecosystem is fundamentally a pipeline with three stages:

**TF1: Generation.** The pipeline starts with structured YAML story specifications that are expanded into natural language prompts and fed to multiple open-weight language models. The result is [TF1-EN-3M](https://huggingface.co/datasets/klusai/ds-tf1-en-3m), a dataset of three million English moral fables with full provenance and multi-dimensional quality scores. ([Paper](https://arxiv.org/abs/2504.20605))

**TF2: Translation.** The English fables are translated to Romanian using open-weight models, including LoRA-fine-tuned variants specialized for literary translation. The result is a parallel corpus ([DS-TF2-EN-RO-3M](https://huggingface.co/datasets/klusai/ds-tf2-en-ro-3m)) and a curated subset ([DS-TF2-EN-RO-15K](https://huggingface.co/datasets/klusai/ds-tf2-en-ro-15k)), each with five-dimensional translation quality scores. ([Paper](https://arxiv.org/abs/2509.07829))

**TF3: Training.** The high-quality Romanian translations serve as training data for a compact (51M parameter) Romanian language model trained from scratch. TF3 demonstrates that synthetic literary text can bootstrap a functional language model for a low-resource language. ([Paper](https://arxiv.org/abs/2601.10410))

## The Evaluation Thread

Running parallel to the pipeline is an evaluation thread that has become a significant research contribution in its own right.

The [synthetic data survey](https://arxiv.org/abs/2503.14023) (IEEE Access) established the broader context for the work. The LLM judges survey (under review at Springer Artificial Intelligence Review) maps the landscape of LLM-based evaluation approaches. And the ongoing work on open-weight judge panels explores whether a single diverse evaluation panel can assess text quality across all three TinyFabulist tasks.

## The Romanian NLP Thread

A third thread focuses specifically on Romanian: the challenges of diacritic restoration, the limitations of existing tools, and the potential for fine-tuned small models to address practical needs. The InnoComp/Springer LNCS paper ([arXiv](https://arxiv.org/abs/2511.13182)) established prompting baselines, and ongoing work extends this to fine-tuning.

## What Ties It Together

The thesis title -- *Controlled Synthetic Narratives for Training and Evaluating Small Language Models* -- captures the unifying idea. Every component addresses some aspect of this:

- **Controlled**: The structured YAML specifications give precise control over what text is generated
- **Synthetic**: The entire pipeline produces and uses synthetic data, with known provenance at every stage
- **Narratives**: The fable domain provides natural structure that enables meaningful evaluation
- **Training**: TF3 demonstrates that synthetic narratives can train a functional language model
- **Evaluating**: The multi-dimensional rubrics and judge panels provide evaluation that goes beyond surface metrics
- **Small Language Models**: The focus throughout is on efficient, accessible models rather than scale

## Open Science

Everything in the TinyFabulist ecosystem is publicly available: the papers on arXiv, the datasets on HuggingFace, and the code on GitHub. This was a deliberate choice from the beginning. Reproducibility is a core value of the project, and making all artifacts public is how I put that value into practice.

## Looking Forward

The pipeline I have described works end to end, but there are many directions to extend it. Other languages beyond Romanian. Other narrative domains beyond fables. Other model architectures beyond transformers. Other evaluation approaches beyond judge panels.

I am particularly interested in whether this controlled-synthetic-data approach could help other low-resource languages bootstrap their NLP ecosystems. If you can generate structured text in a high-resource language, translate it with quality control, and train a compact model on the result, you have a reproducible recipe that does not require large natural corpora.

This is the kind of work I hope to continue beyond the PhD. The specific fables will be left behind, but the methodology and the tools will, I hope, prove useful to others working on similar problems.
