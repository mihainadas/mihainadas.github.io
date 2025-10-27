---
layout: post
title: "One Year In: PhD Reflections and What Comes Next"
date: 2025-10-27 20:00:00 +0200
tags:
  - phd-journey
---

A year ago I started my PhD. It feels like a good moment to step back and reflect on what has happened, what I have learned, and where things are heading.

## What Got Done

The numbers are easy to list: two arXiv preprints (TF1 and TF2), one published survey in IEEE Access, two HuggingFace dataset releases, and thousands of lines of pipeline code. I started writing a survey on LLM-based evaluation that is still in progress.

But the numbers do not capture the harder-to-measure things. I have gotten much better at reading papers critically, at designing experiments before running them, and at writing technical prose that communicates clearly. I have also gotten comfortable with the uncomfortable truth that research is mostly about dead ends, failed experiments, and ideas that do not pan out.

## What Surprised Me

**The pace of the field.** When I started in October 2024, Llama 3 was the model everyone was talking about. A year later, the landscape has shifted several times. Keeping up with the field while making progress on my own work requires deliberate choices about what to follow and what to ignore.

**How much engineering a PhD involves.** I expected the PhD to be primarily about ideas and analysis. In practice, a significant fraction of my time goes to infrastructure: building pipelines, managing data, debugging distributed systems, and optimizing inference. The engineering is not separate from the research -- it enables the research -- but it was more than I anticipated.

**The value of writing.** Writing papers, blog posts, and notes has been the single most effective tool for clarifying my thinking. Ideas that seem clear in my head often reveal gaps and inconsistencies when I try to write them down. This blog has been part of that process.

## What I Would Do Differently

I would start evaluating earlier. In the TF1 project, I spent a long time building the generation pipeline before seriously thinking about evaluation. When I finally built the evaluation framework, it revealed issues that required changes to the generation approach. In TF2, I developed generation and evaluation in parallel, which worked much better.

I would also be more systematic about tracking experiment configurations from the start. My early experiments used ad hoc parameter tracking that made it hard to reproduce results later. I have since settled on a structured approach with YAML configuration files and timestamped artifact directories.

## What Comes Next

The second year has several concrete goals:

- **TF3**: Training a compact Romanian language model from scratch on synthetic data. The architecture and tokenizer design are already underway.
- **Diacritics paper**: Formalizing my investigation of LLMs for Romanian diacritic restoration. I will be presenting this at InnoComp 2025 in a few weeks.
- **LLM judges survey**: Completing and submitting the evaluation survey.
- **Thesis writing**: Starting the thesis document itself, integrating the papers into a coherent narrative.

A year in, I am more excited about the work than when I started. The questions have gotten sharper, the tools have gotten better, and the path forward is clearer. That feels like progress.
