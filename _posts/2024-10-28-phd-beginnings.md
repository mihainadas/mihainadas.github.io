---
layout: post
title: "Three Decisions at the Start of the PhD"
date: 2024-10-28 18:00:00 +0200
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: retrospective
description: "A reconstruction of the three early research decisions behind TinyFabulist, and which ones survived contact with the work."
tags: [phd, natural-language-processing, romanian-nlp]
---

> **Retrospective.** This note reconstructs the start of the PhD from the later papers and project record. It was revised in August 2026 rather than presented as an untouched 2024 diary entry.

I entered the PhD after more than a decade in software engineering with a tentative thesis direction: controlled synthetic narratives for training and evaluating small language models. Three early decisions shaped the work that followed.

## Use narratives with inspectable structure

Moral fables gave the project a compact unit of text with recognizable components: character, trait, setting, conflict, resolution, and moral. Those fields could be represented before generation and compared with the result afterward.

The choice survived, but the rationale became narrower. Fables are not a proxy for language as a whole. They are a tractable domain for studying control, provenance, narrative coherence, and downstream training under known limitations.

## Build English first, then make Romanian central

Starting with English made generator comparison easier because model coverage and evaluation resources were stronger. Romanian remained the target that justified the cross-lingual work: parallel literary data, Romanian-specific tokenization, native generation, and diacritic restoration.

That sequence became TF1, TF2, and TF3. The [research map](/research/) now separates their artifacts and claims.

## Treat evaluation as a system, not a final metric

The initial plan already rejected a single-number evaluation. Grammar, creativity, moral clarity, and adherence measure different properties. Translation later required accuracy, fluency, coherence, style, and cultural adaptation. Romanian model evaluation added tokenization, agreement probes, entity coherence, and rule-based checks.

The part that changed most was my confidence in model judges. They scale, but they bring position, length, self-preference, calibration, and rubric-sensitivity problems. Judge-panel work therefore became a research question in its own right rather than invisible infrastructure.

## What I would state differently now

The original framing used “low-resource” too loosely. Romanian has substantial linguistic resources and active research; the relevant shortage depends on the task, license, domain, and quality bar. Literary parallel data and openly documented compact-model pipelines can be scarce even when a language is not absent from multilingual pre-training.

The thesis idea became more conditional: controlled specifications, traceable generation, task-specific evaluation, and compact models form a system whose trade-offs can be measured. The later papers test individual pieces of that system rather than offering a universal recipe.
