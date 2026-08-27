---
layout: post
title: "TF3-RO: Training and Compressing a Romanian Model from Scratch"
date: 2026-01-15 16:02:00 +0200
published_at: 2026-08-27
feed_date: "2026-08-27"
last_modified_at: 2026-08-27
post_type: release note
description: "The tokenizer, 51.65M-parameter model, compressed student, and Romanian-native generation pipeline released with TF3-RO."
featured: true
redirect_from: /2026/01/05/tf3-romanian-microfiction.html
tags: [language-models, romanian-nlp, synthetic-data]
---

TF3-RO chose a tokenizer that made sequences longer, trained a 51.65M-parameter teacher from random weights, and compressed it to a 26.45M-parameter student. Those numbers describe three separate decisions; collapsing them into “a small Romanian model” loses the experiment.

- [Paper](https://arxiv.org/abs/2601.10410)

## Two model sizes, two roles

The 51.65M-parameter teacher is a LLaMA-style transformer trained from scratch. Near 27,000 steps it reached reported cross-entropy of about 0.89 and perplexity of about 2.43 on the held-out distribution.

Quantization changes numerical precision without reducing the parameter count. A masking sweep—50% of MLP channels and 30% of attention heads—was used to locate spare capacity and produced roughly a 26–27% validation-loss increase. It was not the final student. The 26.45M-parameter student instead reduces hidden width from 512 to 384, MLP width from 1,365 to 1,024, and attention heads from eight to six, then uses logit-based distillation with tied embeddings.

## The tokenizer decision came earlier

TF3 uses the 32,000-token Unigram tokenizer selected during the design comparison. The [engineering note](/2025/12/08/training-lm-from-scratch.html) keeps the BPE comparison and its qualitative evidence; this release note follows the model and corpus artifacts that came afterward.

Training uses 2,048-token packed blocks over roughly one billion tokens. Starting from random weights makes the documented corpus and procedure more visible than in a fine-tuned multilingual model. It does not erase preprocessing choices or turn attribution into proof.

## From translated data to Romanian-native generation

TF2 supplies model-generated Romanian translations for training. The resulting model then participates in a controlled combinatorial prompting pipeline that generates three million fables directly in Romanian.

“Romanian-native” describes the direction of generation, not human authorship. The translated corpus trains the model; the direct-Romanian corpus is an output of the trained system. Reversing that arrow would turn an evaluation claim into a provenance error.

## Evaluation boundary

The evaluation combines intrinsic language-model measures, Romanian agreement probes, entity coherence, rule-based grammar checks, and model-based assessment. Each detects a different failure class. None alone establishes broad Romanian competence.

The release keeps the teacher, masking sweep, student, and direct-Romanian corpus as separate artifacts, so each measured change remains attached to its stage.
