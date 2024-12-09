---
layout: post
title: "Navigating the NLP Literature Landscape"
date: 2024-12-09 14:00:00 +0200
tags:
  - phd-journey
  - natural-language-processing
  - machine-learning
---

Two months into the PhD, and my reading list has grown faster than my ability to process it. Literature review is the unglamorous backbone of research, and I wanted to share some notes on how I have been approaching it.

## The Scale of the Problem

The pace of NLP research is staggering. ArXiv alone sees hundreds of new NLP papers per month, and that does not count workshop papers, technical reports, or blog posts that often contain important results. Staying current while building deep understanding of foundational work is a genuine challenge.

I have been organizing my reading around three main threads that map to my thesis:

1. **Synthetic data generation with LLMs** -- How are researchers using language models to create training data? What quality controls exist? Where does synthetic data outperform or underperform human-written data?
2. **Small language model training** -- What architectures, training recipes, and data strategies work best for models under 1B parameters? How do these models perform on languages other than English?
3. **LLM-based evaluation** -- How are language models being used as judges and evaluators? What are the known biases, and how can multi-judge panels mitigate them?

## Key Patterns I Have Noticed

Several themes keep recurring across the papers I have read so far:

**Data quality matters more than quantity.** Multiple papers demonstrate that carefully curated or filtered synthetic data can outperform larger but noisier datasets. This reinforces my plan to use structured, controlled generation rather than open-ended prompting.

**Evaluation is the bottleneck.** Many papers propose new generation methods but rely on weak evaluation: a single GPT-4 call, or only automated metrics like BLEU or ROUGE. The community is increasingly aware of this gap, with several groups proposing multi-evaluator frameworks and rubric-based assessment.

**Low-resource languages are afterthoughts.** Most synthetic data work targets English, Chinese, or a handful of other high-resource languages. When Romanian appears at all, it is usually as one line in a multilingual benchmark table, not as a first-class research target.

## Tools and Workflow

On the practical side, I have settled on a reading workflow that works for me: Zotero for reference management, Markdown notes for paper summaries, and a simple tagging system that maps papers to thesis threads. Nothing revolutionary, but consistency matters more than sophistication here.

I have also started tracking which papers cite each other, which helps me identify the intellectual lineages and community clusters within each thread. The synthetic data and LLM-evaluation communities overlap more than I initially expected, which is encouraging for my thesis plan.

## What Comes Next

Over the next couple of months, I plan to move from reading to building. The first concrete project will focus on synthetic narrative generation -- taking the theoretical grounding from the literature and turning it into a working pipeline. I will share more about that as it takes shape.
