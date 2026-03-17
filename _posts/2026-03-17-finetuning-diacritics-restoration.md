---
layout: post
title: "Fine-Tuning Small Models for Diacritic Restoration"
date: 2026-03-17 14:00:00 +0200
tags:
  - romanian-nlp
  - language-models
  - machine-learning
---

Building on my InnoComp paper, which evaluated LLMs for Romanian diacritics through prompting, I am now investigating the opposite end of the spectrum: can small, fine-tuned models match or exceed the performance of much larger prompted models?

## The Three-Way Comparison

My experimental design compares three approaches to Romanian diacritic restoration:

**Prompting large models** (the baseline from my InnoComp paper). Give a capable LLM the text and ask it to restore diacritics. Simple, no training required, but expensive at scale and limited by the model's existing Romanian knowledge.

**Lightweight supervised baselines.** Character-level BiLSTM networks, CharCNN combined with BERT-based token classification, and sequence-to-sequence models (ByT5, mT5). These are purpose-built for the task and do not require LLM-scale compute.

**Fine-tuned small LLMs.** LoRA and full fine-tuning on models in the 1B-8B parameter range. This is the novel contribution -- no peer-reviewed paper has systematically explored fine-tuning decoder-only LLMs for Romanian diacritics.

## Why Fine-Tuning Is Interesting Here

Diacritic restoration sits in an unusual position in the NLP task landscape. On clean benchmarks, it is nearly solved -- supervised models achieve above 99% word accuracy. But the interesting question is not peak performance on clean data; it is robustness across conditions:

**Noisy input.** Real-world Romanian text has typos, inconsistent casing, and mixed diacritics. Can a fine-tuned LLM handle this noise better than a character-level model that has never seen it?

**Orthographic variation.** Pre-1993 and post-1993 Romanian orthography differ in the usage of â and î. A model that handles both conventions correctly demonstrates deeper linguistic understanding.

**Model unification.** A fine-tuned LLM could potentially handle diacritic restoration, typo correction, and orthographic normalization in a single pass, while traditional approaches require separate models for each task.

## The Training Setup

For the LoRA experiments, the setup is similar to what I used for literary translation in TF2:

```python
from peft import LoraConfig

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    task_type="CAUSAL_LM"
)
```

The training data comes from [dexonline](https://dexonline.ro), the comprehensive Romanian dictionary and language resource. I construct training pairs by taking correctly diacritized text and generating degraded versions with varying levels of noise (removed diacritics, introduced typos, casing changes).

The noise injection is configurable, which lets me train models that are robust to specific types of degradation and evaluate how robustness transfers across noise types.

## Evaluation Metrics

The evaluation suite is more comprehensive than what most diacritics papers report. For every model, I compute:

| Metric | What It Measures |
|--------|-----------------|
| Word Accuracy (WA) | Fraction of words with all diacritics correct |
| Character Accuracy (CA) | Fraction of characters correct |
| Diacritizable WA | WA restricted to words that could have diacritics |
| Diacritizable CA | CA restricted to diacritizable characters |
| Diacritic Error Rate (DER) | Error rate specifically on diacritizable positions |
| Hallucination Rate | How often the model changes non-diacritizable characters |
| Per-character F-scores | Precision/recall/F1 for each of ă, â, î, ș, ț |

The hallucination rate is particularly important for generative models. A model that achieves 99% diacritizable accuracy but also changes 2% of non-diacritizable characters is not practically useful.

## Preliminary Direction

Without presenting final results (the paper is still in preparation), I can share the general direction: fine-tuned small models show promising robustness on noisy input, which is where traditional supervised baselines tend to struggle. The trade-off is inference speed -- a BiLSTM processes text orders of magnitude faster than even a small LLM.

Whether the robustness advantage justifies the inference cost depends on the application. For batch processing of historical documents, speed matters less. For real-time input correction, it matters a lot.

I will share the full results and analysis when the paper is ready.
