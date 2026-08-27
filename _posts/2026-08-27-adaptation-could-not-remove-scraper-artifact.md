---
layout: post
title: "Ten Thousand Adaptation Steps Could Not Remove One Scraper Artifact"
date: 2026-08-27 09:11:56 +0300
feed_date: "2026-08-27 09:11:56 +0300"
last_modified_at: 2026-08-27 09:11:56 +0300
post_type: research note
description: "One Romanian checkpoint kept emitting a web-page token after supervised adaptation, turning contamination into a model-selection failure."
tags: [romanian-nlp, data-quality, language-models]
series: controlled-synthetic-narratives
series_order: 6
evidence_status: thesis-only
---

The model was asked to restore Romanian diacritics. It answered with `autoResizeIframe`.

That token is not a plausible restoration error. It is a web-page artifact, probably learned from scraped training text. In one experiment, it appeared in outputs from the LLMic_v2 3B checkpoint before adaptation and remained after rank-16 LoRA, a doubled schedule, and 10,000 training steps.

> **Evidence status.** This is a thesis-draft case study of one checkpoint, one task corpus, and one adaptation setup. It does not show that LoRA generally cannot remove contamination, or that the artifact is irreversible.

{% include figure.html
  src="/assets/figures/adaptation-could-not-remove-scraper-artifact/artifact-path.svg"
  mobile_src="/assets/figures/adaptation-could-not-remove-scraper-artifact/artifact-path-mobile.svg"
  alt="A provenance path from scraped web text to a pretrained checkpoint, through LoRA adaptation, ending with the same autoResizeIframe artifact in a Romanian diacritic-restoration output."
  caption="Task adaptation improved the checkpoint slightly but did not suppress the observed artifact in this run."
  width="1200"
  height="600"
  mobile_width="320"
  mobile_height="990"
  wide=true
%}

## The adapter learned around the failure

The base checkpoint scored 0.00% word accuracy on the clean restoration test. After adaptation it reached 1.45%. The task score moved, but remained unusable, and the distinctive artifact survived.

A separate multilingual Qwen checkpoint adapted on the same task did not show that exact output pattern. That contrast narrows the diagnosis to this checkpoint and run; it does not identify the original document or prove a single causal path through pretraining.

The important operational signal came before aggregate evaluation. A model that emits templating code into ordinary Romanian text has failed the output contract, even if later tuning raises an average score. More epochs are a poor default response when the base model's failure is both severe and out of distribution for the task.

## Contamination is also a selection problem

Dataset cleaning is usually discussed upstream, where the pretraining corpus may be inaccessible to a downstream user. Checkpoint selection is the available downstream control. A small diagnostic set can probe for markup, navigation fragments, templating identifiers, instruction leakage, and non-language tokens before adaptation consumes compute.

That screen should preserve raw generations. Normalizing or post-processing them too early can erase the best clue about provenance.

For this task, the observed artifact should be a stop condition: reject or quarantine the checkpoint, compare another base model, and only then tune hyperparameters. If the model must be studied further, treat the artifact rate as its own metric rather than burying it inside word accuracy.

## The checkpoint was disqualified before the causal story was complete

The experiment did not identify the original pretraining document or test full-parameter tuning. It did settle the model-selection decision: after 10,000 adaptation steps, this checkpoint still emitted scraper debris into Romanian output. That was enough to quarantine it before another sweep.

{% include thesis-series.html %}
