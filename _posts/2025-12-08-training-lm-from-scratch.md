---
layout: post
title: "Training a Small Language Model from Scratch"
date: 2025-12-08 11:00:00 +0200
tags:
  - language-models
  - romanian-nlp
  - machine-learning
---

I have started working on TF3, the third component of my thesis: training a compact Romanian language model from scratch on synthetic literary text. This is the most technically demanding part of the project so far, and I want to walk through the key design decisions.

## Why From Scratch

An obvious question: why train from scratch when you can fine-tune an existing multilingual model? There are several reasons:

**Scientific clarity.** When you fine-tune a model that was pre-trained on trillions of tokens, any downstream performance reflects both the pre-training data and the fine-tuning data. By training from scratch, I know exactly what the model has seen. If TF3 can generate coherent Romanian fables, that capability comes entirely from the synthetic training corpus.

**Size constraints.** My target is a model under 50 million parameters -- small enough to run on a mobile phone or embedded device. Most open multilingual models start at 1B+ parameters. Training from scratch lets me design an architecture for the target size.

**Tokenizer control.** Multilingual tokenizers allocate vocabulary budget across many languages, which means Romanian gets a small fraction of the vocabulary. A Romanian-specific tokenizer can represent the language more efficiently, reducing sequence lengths and improving the model's effective context.

## Tokenizer Design

The tokenizer is the foundation. I am using SentencePiece with a vocabulary size of 16,000 tokens, trained exclusively on the Romanian translations from the TF2 corpus. This gives:

- Full coverage of Romanian characters including all diacritics (ă, â, î, ș, ț)
- Efficient encoding of common Romanian morphological patterns
- Reasonable handling of the literary vocabulary present in the fable corpus

```python
import sentencepiece as spm

spm.SentencePieceTrainer.train(
    input="tf2_romanian_corpus.txt",
    model_prefix="tf3_tokenizer",
    vocab_size=16000,
    model_type="bpe",
    character_coverage=1.0,
    pad_id=0,
    unk_id=1,
    bos_id=2,
    eos_id=3
)
```

A 16K vocabulary is small compared to the 32K-128K vocabularies in modern LLMs, but for a domain-specific model on a single language, it provides adequate coverage. The average tokens-per-word ratio on the training corpus is around 1.4, which is reasonable for Romanian.

## Architecture Choices

TF3 uses a standard decoder-only transformer architecture. The key parameters:

| Parameter | Value |
|-----------|-------|
| Layers | 12 |
| Hidden dim | 512 |
| Attention heads | 8 |
| FFN dim | 2048 |
| Context length | 2048 tokens |
| Total parameters | ~51M |

This is deliberately minimal. The goal is not to compete with larger models on general-purpose benchmarks but to study what a small model can learn from a controlled synthetic corpus.

I considered alternative architectures (state space models, hybrid attention-SSM designs) but decided that the scientific value of TF3 comes from the training data, not the architecture. Using a standard transformer makes the results more directly comparable to other work.

## Data Preprocessing

The training data comes from the TF2 Romanian translations, preprocessed into 2048-token chunks. Each chunk contains one or more complete fables -- I avoid splitting mid-sentence to preserve coherence. The total training corpus is approximately 2GB of text after tokenization.

Data quality filtering is minimal by design. The TF2 dataset already has quality scores, and I use only translations that scored above threshold on all five evaluation dimensions. This means the model trains on the best available synthetic literary Romanian.

## Training Infrastructure

Training a 51M-parameter model is surprisingly tractable. A single machine with a modern GPU can complete the training run in a reasonable timeframe. I am training on a Mac Studio, which keeps iteration cycles fast -- I can test architectural changes and hyperparameter modifications without waiting for cloud GPU allocations.

The training pipeline logs loss curves, checkpoint metrics, and sample generations at regular intervals. I generate sample fable completions from fixed prompts at each checkpoint, which gives a qualitative sense of how the model's Romanian is developing over training.

## Early Observations

Training is still in progress, but early checkpoints show that the model learns Romanian orthography (including correct diacritic usage) within the first few thousand steps. Coherent sentence structure emerges next, followed by narrative structure. Whether the model will learn to produce fables with meaningful morals is the open question -- that requires capturing higher-level narrative reasoning, which is a lot to ask of a 51M-parameter model.

I will share detailed results when the training is complete and the paper is ready.
