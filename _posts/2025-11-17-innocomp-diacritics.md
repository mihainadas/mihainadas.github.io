---
layout: post
title: "Presenting at InnoComp 2025: LLMs for Romanian Diacritics"
date: 2025-11-17 19:00:00 +0200
tags:
  - romanian-nlp
  - natural-language-processing
  - phd-journey
---

Last week I presented my paper on Romanian diacritic restoration at InnoComp 2025. The paper, *Evaluating Large Language Models for Diacritic Restoration in Romanian Texts: A Comparative Study*, is published in Springer LNCS and the preprint is available on [arXiv (2511.13182)](https://arxiv.org/abs/2511.13182).

## The Paper

The study evaluates how well current LLMs handle Romanian diacritic restoration across different text genres. Rather than proposing a new model, the contribution is a systematic comparison of existing LLMs on this task, with analysis of where and why they fail.

Key findings:

- **Large proprietary models** (GPT-4 class) achieve high accuracy on clean benchmark text, but the gap narrows on noisy, real-world input
- **Open-weight models** in the 7B-70B range show wide variation -- some handle diacritics competently, others make systematic errors that suggest limited Romanian training data
- **Genre matters**: Models perform best on formal text (news, Wikipedia) and worst on informal text (social media, forum posts) where diacritics are inconsistently used even in the ground truth
- **Error analysis** reveals that models struggle most with genuinely ambiguous words and with the pre-1993 vs. post-1993 orthographic distinction (â vs. î in word-internal positions)

## The Conference Experience

InnoComp is a smaller conference, which has its advantages. The audience during my talk included researchers working on other low-resource European languages, and the questions after the presentation surfaced connections I had not considered. A researcher working on Slovak asked about handling háčeks and čárkas -- the diacritic problem is structurally similar across many Central and Eastern European languages, even though the specific characters differ.

The poster session was equally valuable. I had a long conversation with someone working on OCR post-correction for digitized Romanian texts, where diacritic restoration is a critical processing step. Their use case is exactly the kind of noisy, real-world scenario where current models underperform.

## What Publishing in LNCS Is Like

This was my first experience with Springer LNCS, and the process was more structured than arXiv self-publishing. The formatting requirements are strict (12-page limit, specific LaTeX template, detailed author metadata), and the review process added several months to the timeline. But the result is a peer-reviewed publication, which carries different weight in the academic world.

The paper benefited from reviewer feedback. One reviewer pushed me to strengthen the error analysis section, which ended up being the most interesting part of the final paper. Another suggested comparing against a character-level baseline, which provided a useful lower bound.

## Connection to Ongoing Work

This paper establishes a baseline: here is how well current LLMs handle Romanian diacritics through prompting alone. The natural follow-up question is whether fine-tuning can do better. Can a small, fine-tuned model outperform a large model that relies on prompting? That investigation is already underway, and it connects to the broader thesis theme of what small, specialized models can achieve.

I am grateful for the opportunity to present this work and for the feedback from the community. Conferences remind me that research is a conversation, not a monologue.
