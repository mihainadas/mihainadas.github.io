---
layout: post
title: "Starting a PhD in NLP: Research Directions and Early Decisions"
date: 2024-10-28 18:00:00 +0200
tags:
  - phd-journey
  - natural-language-processing
  - romanian-nlp
---

A few weeks ago, I officially started my PhD at Babes-Bolyai University. After more than a decade in the IT industry, going back to academia felt both exciting and humbling. I want to use this blog to document the journey as it unfolds.

## Why NLP, and Why Now

My research sits at the intersection of natural language processing and language model training. Specifically, I am interested in how we can use structured synthetic data to train and evaluate small language models. The field has exploded in the last two years with the rise of large language models, but I believe there is still enormous untapped potential in smaller, more efficient models, especially for languages that are not English.

Romanian is one of those languages. Despite being spoken by roughly 24 million people, Romanian remains underrepresented in NLP research. There are gaps in available corpora, evaluation benchmarks, and even basic tools like reliable diacritic restoration. These gaps are not just academic curiosities; they have practical consequences for anyone building Romanian-language technology.

## The Thesis Direction

My thesis, tentatively titled *Controlled Synthetic Narratives for Training and Evaluating Small Language Models*, will explore a pipeline approach: generating large-scale synthetic text with controlled properties, using it to train compact models, and developing robust evaluation methods that do not rely solely on expensive proprietary APIs.

The "controlled" aspect is key. Rather than scraping the web for training data, I want to generate text with known structure, known difficulty, and known properties. This lets us study what models actually learn, rather than guessing from opaque internet-scale corpora.

## Early Decisions

I spent the first few weeks reading broadly and making some foundational choices:

- **Domain**: Moral fables and short narratives. They have clear structure (characters, conflict, resolution, moral), manageable length, and are culturally interesting across languages.
- **Languages**: English first (for benchmarking against the wider community), then Romanian (where the contribution is most needed).
- **Evaluation**: I want to move beyond single-number metrics. LLM-based evaluation, rubric scoring, and human validation will all play a role.

These early choices will shape everything that follows. I expect some of them to change as I learn more, and that is fine. The point of a PhD is not to have all the answers on day one, but to ask better questions over time.

I will be sharing more here as the work takes shape. If any of this resonates, or if you are working on similar problems, I would love to hear from you.
