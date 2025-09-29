---
layout: post
title: "The Romanian Diacritics Challenge: Why It Still Matters"
date: 2025-09-29 17:00:00 +0300
tags:
  - romanian-nlp
  - natural-language-processing
---

While working on TF2, I kept encountering a problem that every Romanian NLP researcher knows well: diacritics. In this post, I want to explain why automatic diacritic restoration (ADR) remains an important and surprisingly tricky problem.

## The Five Characters

Romanian uses five diacritical characters: **ă**, **â**, **î**, **ș**, and **ț**. These are not decorative -- they change meaning. The word "fata" means "the girl," but "fața" means "the face." "Tara" is not a word, but "țara" means "the country." Omitting diacritics creates genuine ambiguity.

Despite this, much of the Romanian text on the internet lacks correct diacritics. There are several reasons:

- Many Romanian keyboards historically did not have convenient diacritic input
- The 1993 orthographic reform changed the standard forms (replacing î with â in some positions), creating a period of inconsistency
- Social media and informal writing culture normalize diacritic-free text
- OCR and digitization of older documents often drops or mangles diacritics

The result is a large body of Romanian digital text with missing, incorrect, or inconsistent diacritics.

## Why ADR Is Not Solved

On clean benchmark datasets, automatic diacritic restoration can reach very high accuracy -- above 99% word accuracy with models like RoBERT (a Romanian BERT variant). This might suggest the problem is solved.

But benchmarks are misleading. They typically evaluate on clean text where diacritics have been artificially stripped. Real-world text has additional noise: typos, inconsistent casing, mixed orthographic conventions (pre-1993 and post-1993 forms in the same document), and foreign words. On noisy text, performance drops significantly.

There is also the problem of what "accuracy" means. A model that restores 99% of words correctly still makes errors on 1% of words. In a 1,000-word document, that is 10 errors -- enough to be noticeable and annoying to a native speaker. And the errors are not random; they tend to cluster around ambiguous words and uncommon proper nouns.

## Connection to Language Modeling

Diacritic restoration is interesting from a language modeling perspective because it requires understanding context. The correct diacritization of an ambiguous word depends on the sentence around it. This makes ADR a useful probe for how well a model understands Romanian syntax and semantics.

It also connects to my broader thesis work. If I am training a Romanian language model on translated fables (TF2) or generating Romanian text from scratch (TF3), the model needs to handle diacritics correctly. Evaluating diacritics is part of evaluating the model.

## What I Plan to Do

I have been investigating how current LLMs handle Romanian diacritics -- both as a standalone restoration task and as an implicit capability within generation and translation. The initial results are mixed: larger models handle diacritics well in clean contexts but struggle with the noisy, real-world cases that matter most.

I plan to write up these findings more formally. The goal is not to claim a new state of the art on the clean benchmark, but to understand when and why LLMs fail at diacritics and what that tells us about their Romanian language understanding.

More on this in a future post.
