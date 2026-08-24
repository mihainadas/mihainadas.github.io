---
layout: post
title: "A Map of LLM-Generated Synthetic Data"
date: 2025-03-18 14:00:00 +0200
published_at: 2026-08-27 10:00:00 +0300
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: release note
description: "The research map behind our survey of LLM-generated synthetic text and code, released as an arXiv preprint on 18 March 2025."
redirect_from: /2025/03/31/synthetic-data-survey.html
tags: [synthetic-data, natural-language-processing, research]
---

Our survey of synthetic text and code generation appeared on arXiv on 18 March 2025. The paper was later published in IEEE Access; this note uses the preprint date rather than backdating the journal publication.

- [Preprint](https://arxiv.org/abs/2503.14023)
- [IEEE record](https://doi.org/10.1109/ACCESS.2025.3589503)

## The organizing problem

“Synthetic data” was already too broad to be a useful category on its own. A generated instruction, an automatically repaired program, and an augmented low-resource classification example have different failure modes and different verification options.

We organized the literature along three operational questions:

1. **How is the data produced?** Prompting, retrieval-augmented generation, iterative refinement, and feedback-driven pipelines make different assumptions about source material and validation.
2. **How is quality controlled?** Text often relies on model or human judgments; code can add execution, tests, and static analysis.
3. **What happens downstream?** More synthetic examples do not automatically improve a model. Utility depends on diversity, correctness, task fit, and the relationship between generator and learner.

The paper's useful boundary is the failure section: factual error, stylistic homogenization, bias amplification, weak evaluation, and recursive training on generated material. These are not footnotes. They determine whether a pipeline creates signal or scales noise.

## What changed in my work

The survey pushed TinyFabulist toward explicit provenance and multi-dimensional evaluation. A generated story is stored with the specification, prompt, generator, and decoding configuration that produced it, supporting failure tracing and alternative filters.

It also made one gap clearer: controlled, domain-specific generation was less developed than general instruction synthesis. Moral narratives gave us a bounded structure in which requested characters, conflict, resolution, and moral could be compared with the output.

The survey covers work available in early 2025, so its model and method inventory will age. The organizing questions—generation, verification, downstream utility, and provenance—should remain useful for longer.
