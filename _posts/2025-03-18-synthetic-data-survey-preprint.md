---
layout: post
title: "A Map of LLM-Generated Synthetic Data"
date: 2025-03-18 14:00:00 +0200
published_at: 2026-08-27
feed_date: "2026-08-27"
last_modified_at: 2026-08-27
post_type: release note
description: "The research map behind our survey of LLM-generated synthetic text and code, released as an arXiv preprint on 18 March 2025."
redirect_from: /2025/03/31/synthetic-data-survey.html
tags: [synthetic-data, natural-language-processing, research]
---

An instruction generated from a seed example, an automatically repaired program, and an augmented classification record can all be called synthetic data. They cannot be accepted by the same test.

That was the organizing problem behind our survey of LLM-generated synthetic text and code, first released on arXiv on 18 March 2025 and later published in *IEEE Access*.

- [Preprint](https://arxiv.org/abs/2503.14023)
- [IEEE record](https://doi.org/10.1109/ACCESS.2025.3589503)

## Two items, incompatible tests

[Self-Instruct](https://arxiv.org/abs/2212.10560) grows instruction data from seed tasks, then filters generated instructions for validity and similarity. Its output still needs semantic review: a plausible instruction–answer pair can be self-consistent and wrong.

[WizardCoder](https://arxiv.org/abs/2306.08568) evolves code instructions to increase complexity. Code offers an extra gate: parsing, execution, unit tests, and static analysis can reject failures that fluent explanations would miss. Passing tests is still evidence about the tested behavior, not proof that the program matches every intended requirement.

Both pipelines generate new training material. Their acceptable evidence differs because one artifact is primarily interpreted and the other can also be executed.

The survey is a narrative synthesis of 64 references available by early 2025, not a systematic review with exhaustive retrieval guarantees. We used three questions across that literature: how an item was produced, how it was checked, and what downstream result justified producing it.

## What changed in TinyFabulist

The survey moved generation history into the TinyFabulist record. In the public TF1 schema, the rendered prompt embeds the story specification; separate columns retain the generator, token counts, timing, host, pipeline version, and raw output. The paper and code describe the global decoding setup. The prompt hash provides the join point for later filters and evaluator versions.

It also clarified why moral narratives were useful for this work. Character, trait, setting, challenge, outcome, and teaching provide requested elements that can be compared with the generated text. The domain is deliberately narrow; that structure makes control and adherence inspectable.

The concrete change was a public record with rendered prompt, prompt hash, generator, generation metadata, pipeline version, and raw output. The survey’s categories will age; the hash lets future checks attach new evaluation records without rewriting the generation row.
