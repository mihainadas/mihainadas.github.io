---
layout: post
title: "Three Decisions at the Start of the PhD"
date: 2024-10-28 18:00:00 +0200
last_modified_at: 2026-08-27
post_type: retrospective
description: "A reconstruction of the three early research decisions behind TinyFabulist, and which ones survived contact with the work."
tags: [phd, natural-language-processing, romanian-nlp]
---

> **Retrospective.** This note reconstructs the start of the PhD from the later papers and project record. It was revised in August 2026 rather than presented as an untouched 2024 diary entry.

The phrase I would most like to take back from the first year is “low-resource language.” It made Romanian sound like a single shortage. In practice, the constraint changes with the task: literary parallel text, permissive licensing, noisy diacritics, and compact-model training each have a different evidence problem.

That correction came later. At the start, after more than a decade in software engineering, I made three working decisions: use fables as controlled objects, begin generation in English before moving into Romanian, and design evaluation as part of the pipeline. All three are still visible in the work, though not in their original form.

## Fables were a constraint, not a stand-in for language

Moral fables gave the project a compact unit of text with recognizable components. The released prompt renders them as character, trait, setting, challenge, outcome, and teaching. Those fields could be represented before generation and compared with the result afterward.

The choice survived, but the rationale became narrower. Fables are not a proxy for language as a whole. They are a tractable domain for studying control, provenance, narrative coherence, and downstream training under known limitations.

## English was scaffolding; Romanian was the research target

Starting with English made generator comparison easier because model coverage and evaluation resources were stronger. Romanian remained the target that justified the cross-lingual work: parallel literary data, Romanian-specific tokenization, native generation, and diacritic restoration.

That sequence became TF1, TF2, and TF3. The [research map](/research/) now separates their artifacts and claims.

## Evaluation had to move upstream

The initial plan already rejected a single-number evaluation. Grammar, creativity, moral clarity, and adherence measure different properties. Translation later required accuracy, fluency, coherence, style, and cultural adaptation. Romanian model evaluation added tokenization, agreement probes, entity coherence, and rule-based checks.

The part that changed most was my confidence in model judges. They scale, but they bring position, length, self-preference, calibration, and rubric-sensitivity problems. Judge-panel work therefore became a research question in its own right rather than invisible infrastructure.

The original framing also used “low-resource” too loosely. Romanian has substantial linguistic resources and active research; the relevant shortage depends on the task, license, domain, and quality bar. Literary parallel data and openly documented compact-model pipelines can be scarce even when a language appears throughout multilingual pre-training.

In my working notes, “low-resource Romanian” is now crossed out. Its replacement has four blanks: missing resource, license, domain, and task. The [TF1](https://arxiv.org/abs/2504.20605), [TF2](https://arxiv.org/abs/2509.07829v4), and [TF3](https://arxiv.org/abs/2601.10410) papers record the later evidence; this page records the wording I had to retire.
