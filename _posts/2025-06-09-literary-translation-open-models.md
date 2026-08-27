---
layout: post
title: "Why TF2 Chose Translation Before Romanian-Native Generation"
date: 2025-06-09 12:00:00 +0300
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: research note
description: "The decision to use controlled English fables as source material for Romanian literary translation."
tags: [translation, synthetic-data, romanian-nlp]
---

TF2 takes an apparent detour: it translates controlled English fables before asking a model to generate directly in Romanian. The detour buys a paired object. Every Romanian text has a source whose events, relationships, and moral can be checked.

TF1 already provided three million English stories with structured specifications and provenance. Translating a selected subset creates a parallel resource: each Romanian output can be compared with a known English source, and multiple systems can be evaluated on the same material.

## Why the paired design matters

A native Romanian story can be judged for grammar and narrative quality, but there is no source whose meaning it must preserve. Translation adds a constraint: accuracy and cultural adaptation can disagree, and the evaluation must show both.

The paper’s inspected example is blunt: the untuned model turns “skunk” into the invented *Fumeg*, while the tuned translation preserves *sconcs*. The sentence can remain fluent while the animal changes species.

## What the design gives up

Translated fables are not the same as Romanian-native writing. They can carry source-language syntax, narrative conventions, and model-specific translationese. A large translated corpus may therefore be useful for controlled experiments while remaining a poor sample of Romanian literature.

TF3 later adds Romanian-native generation, which lets the two regimes be studied separately instead of conflated.

## The experimental path

TF2 uses a [15K silver-reference set](https://huggingface.co/datasets/klusai/ds-tf2-en-ro-15k) for instruction tuning and evaluation, then builds a [three-million-pair corpus](https://huggingface.co/datasets/klusai/ds-tf2-en-ro-3m) at scale. Open models are compared with larger proprietary systems under corpus metrics and a five-dimensional rubric.

The [TF2 paper](https://arxiv.org/abs/2509.07829) separates the 15K set, the large corpus, and the fine-tuned model. The 15K Romanian references are model-generated silver data, not human literary translations. Pairing makes their relationship to the English source inspectable; it does not remove translationese or turn synthetic references into a human standard.
