---
layout: post
title: "When BLEU and a Literary Rubric Answer Different Questions"
date: 2025-07-07 10:00:00 +0300
last_modified_at: 2026-08-27
post_type: research note
description: "Why TF2 reports an overlap metric and a five-dimensional literary rubric instead of collapsing quality into one score."
tags: [evaluation, translation, natural-language-processing]
---

Agreement is easy to summarize. The useful cases are the ones where lexical overlap and literary judgment pull in different directions.

[BLEU](https://aclanthology.org/P02-1040/) measures n-gram overlap with one or more references. It is inexpensive and useful for corpus-level comparison. The TF2 paper does not publish an implementation signature, tokenizer, casing, or smoothing configuration, so its BLEU values should be read as reported overlap results, not as independently reproducible measurements from this post.

TF2 therefore reports BLEU and a five-dimensional rubric separately. The two instruments expose different properties.

## Five questions, kept separate

The rubric asks whether meaning, events, and relationships survive; whether the Romanian reads naturally; whether the narrative remains connected; what happened to tone and rhythm; and whether idiom, politeness, names, and moral framing work in Romanian.

Scoring each dimension from 1 to 5 keeps a polished average from hiding a changed moral or broken character relationship. In the TF2 comparisons, the untuned baseline sometimes corrupted the animal itself—rendering “skunk” as *Fumeg*—while the fine-tuned model preserved *sconcs*. No aggregate overlap score can explain that error as clearly as the text does.

## Disagreement is a diagnostic

A low BLEU score can reflect legitimate rephrasing or a substantive error. A strong style score is equally incomplete when accuracy is weak. When the instruments disagree, the next step is inspection: locate the wording or meaning change, see which rubric dimensions moved, compare judges, and send consequential cases to human review.

TF2 stores per-dimension justifications and the judge, prompt, schema, and decoding configuration behind them. The Romanian references are synthetic silver data, so BLEU measures consistency with a strong machine translation, not distance from a human-authored gold text.

## Reading the profile

A model's result is a profile: where it trades accuracy for style, where BLEU and rubric scores diverge, how stable the judgment is across evaluator families, and whether the ranking survives human inspection.

The [TF2 release note](/2025/09/09/tf2-preprint-release.html) carries the system-level numbers. The error worth remembering here is the animal that changed species: a fluent sentence can still be the wrong translation.
