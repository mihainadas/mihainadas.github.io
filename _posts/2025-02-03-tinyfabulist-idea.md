---
layout: post
title: "Why TinyFabulist Starts with a Specification"
date: 2025-02-03 16:00:00 +0200
last_modified_at: 2026-08-27
post_type: research note
description: "The six-slot story specification behind TinyFabulist and the control it provides over generation and evaluation."
tags: [synthetic-data, language-models, system-design]
---

Before TinyFabulist asks a model to write, it records what the story must contain. The first public TF1 row was rendered from these values:

```yaml
character: firefly
trait: persuasive
setting: canyon
challenge: betrayal by a friend
outcome: a lesson is documented for future generations
teaching: timely help earns lasting loyalty
```

The rendered prompt separately asks for age group B, ages 4–7. The released row described in the [TF1 paper](https://arxiv.org/abs/2504.20605) records the prompt text, prompt hash, model, token counts, 38.98-second inference time, host, generation time, and pipeline version.

An earlier design used prompts close to “write a moral fable about _x_.” They produced readable stories and almost no defensible way to say whether a story followed the request. The six fields separate the requested story from the generated one.

## What becomes observable

The design ideal stores a story beside its structured request and execution settings. The public TF1 row takes a narrower form: the rendered prompt embeds the request, while model and generation metadata sit in separate columns. An evaluator can still check whether the firefly remains persuasive, whether the rabbit’s absence counts as betrayal, and whether the ending supports lasting loyalty.

The stored input also makes controlled variation and regeneration possible. Change the outcome while keeping the other five fields fixed; or rerun a disputed output from its original request instead of reconstructing that request from prose.

## Why YAML

YAML was chosen because it is readable in code review and maps cleanly to the dictionaries used by the prompt builder. Its role is mundane: keep combinatorial specification separate from natural-language realization.

The cost is rigidity. A finite slot system can over-represent the designer's ontology, generate formulaic combinations, and miss narrative forms that do not fit its fields. Increasing the combination count does not remove that bias.

## The scale target

Three million stories became the project target for corpus analysis and later training experiments; it was not a quality threshold. Reaching the count still left evaluation and downstream utility to be tested separately.

The generated story exposes the value and the limit. It keeps the firefly, canyon, and timely-help moral, but softens “betrayal by a friend” into a rabbit stranded in a cave. The specification makes that drift inspectable. It also reveals the ontology we chose: another set of fields would ask different questions of the same story.
