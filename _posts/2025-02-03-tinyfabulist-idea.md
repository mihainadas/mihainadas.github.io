---
layout: post
title: "Why TinyFabulist Starts with a Specification"
date: 2025-02-03 16:00:00 +0200
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: research note
description: "The six-slot story specification behind TinyFabulist and the control it provides over generation and evaluation."
tags: [synthetic-data, language-models, system-design]
---

TinyFabulist separates the story requested from the story generated. That boundary is the core of the system.

An early design used open-ended prompts—effectively “write a moral fable about _x_.” The output could be read, but adherence was hard to define because the request contained little structure. I replaced it with a six-slot specification: character, trait, setting, conflict, resolution, and moral.

```yaml
character: fox
trait: clever
setting: mountain forest
conflict: competition for territory
resolution: negotiation
moral: wisdom can outperform strength
```

The exact schema in the released work contains the project fields and controlled vocabularies; this compact example shows the interface, not a verbatim dataset record.

## What the specification buys

**Traceability.** A generated story can be stored with the request, prompt, model, and decoding configuration that produced it.

**Adherence checks.** An evaluator can ask whether the requested elements appear and play the intended roles. Without the specification, the same judgment becomes an impression.

**Controlled variation.** Changing one field while holding the others fixed supports comparisons that unconstrained prompts do not.

**Regeneration.** Failed or disputed outputs can be rerun from their original inputs rather than reverse-engineered from prose.

## Why YAML

YAML was chosen as an authoring format because it is readable in code review and maps cleanly to the dictionaries used by the prompt builder. Its role is mundane but useful: provide a typed boundary between combinatorial specification and natural-language realization.

The cost is rigidity. A finite slot system can over-represent the designer's ontology, generate formulaic combinations, and miss narrative forms that do not fit its fields. Increasing the combination count does not remove that bias.

## The scale target

Three million stories was large enough to support model and corpus analysis and later training experiments. Quality still required a separate evaluation design and, ultimately, a downstream use in TF3.

The later [TF1 release note](/2025/04/29/tf1-arxiv-release.html) records what was actually released and measured. This note preserves the earlier design question: what must be known before generation if the result is meant to be auditable?
