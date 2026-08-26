---
layout: post
title: "When BLEU and a Literary Rubric Answer Different Questions"
date: 2025-07-07 10:00:00 +0300
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: research note
description: "Why TF2 keeps a reproducible overlap metric and a five-dimensional literary rubric instead of collapsing quality into one score."
tags: [evaluation, translation, natural-language-processing]
---

[BLEU](https://aclanthology.org/P02-1040/) measures n-gram overlap with one or more references. It is reproducible, cheap, and useful for corpus-level comparison. It also cannot tell whether a low-overlap literary translation made a valid stylistic choice or lost the source meaning.

TF2 therefore reports BLEU and a five-dimensional rubric separately. The two instruments expose different properties.

## The five dimensions

**Accuracy** asks whether meaning, events, and relationships survive translation.

**Fluency** asks whether the target reads as grammatical, natural Romanian.

**Coherence** tracks logical and narrative continuity across sentences.

**Style** examines tone, imagery, rhythm, and genre rather than grammaticality alone.

**Cultural and pragmatic adaptation** covers idiom, politeness, names, and framing whose literal transfer can be wrong in use.

Scoring each dimension from 1 to 5 makes trade-offs visible. A literal translation may score high on accuracy and lower on style; a polished adaptation can reverse that profile.

## The judge is part of the protocol

Model-based scoring adds its own uncertainty. TF2 stores per-dimension justifications and uses several judges rather than one opaque aggregate. Judge identity, prompt, schema, and decoding configuration belong in the experiment record.

Human review remains the reference for disputed or consequential cases; proprietary-model agreement supplies a comparison point.

## Reading the result

A stronger TF2 result is not “model A has the highest quality.” It is a profile: where models trade accuracy for style, where BLEU and rubric scores disagree, how stable judgments are across evaluators, and whether the ranking survives human inspection.

The [TF2 release note](/2025/09/09/tf2-preprint-release.html) describes the artifacts and the bounded near-parity claim. This note describes the measurement boundary underneath it.
