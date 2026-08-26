---
layout: post
title: "Why TF2 Chose Translation Before Romanian-Native Generation"
date: 2025-06-09 12:00:00 +0300
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: research note
description: "The decision to use controlled English fables as source material for Romanian literary translation."
tags: [translation, synthetic-data, romanian-nlp]
---

TF2 begins with translation rather than asking a model to generate Romanian fables directly. The decision trades native composition for paired, inspectable source and target text.

TF1 already provided three million English stories with structured specifications and provenance. Translating a selected subset creates a parallel resource: each Romanian output can be compared with a known English source, and multiple systems can be evaluated on the same material.

## Why the paired design matters

A native Romanian story can be judged for grammar and narrative quality, but there is no source whose meaning it must preserve. Translation adds a constraint: accuracy and cultural adaptation can disagree, and the evaluation must show both.

This makes literary text harder than a domain in which terminology and sentence correspondence dominate. A faithful translation can be flat; a fluent adaptation can change the moral or character relationship. BLEU alone cannot resolve that trade-off.

## What the design gives up

Translated fables are not the same as Romanian-native writing. They can carry source-language syntax, narrative conventions, and model-specific translationese. A large translated corpus may therefore be useful for controlled experiments while remaining a poor sample of Romanian literature.

TF3 later adds Romanian-native generation, which lets the two regimes be studied separately instead of conflated.

## The experimental path

TF2 uses a 15K high-quality reference set for instruction tuning and evaluation, then builds a three-million-pair corpus at scale. Open models are compared with larger proprietary systems under corpus metrics and a five-dimensional rubric.

The [TF2 paper](https://arxiv.org/abs/2509.07829) and [research map](/research/) separate the reference set, large corpus, and fine-tuned model. This early design note records why those artifacts exist: pairing gives the project an observable relationship between source, translation, and evaluation that native generation alone cannot provide.
