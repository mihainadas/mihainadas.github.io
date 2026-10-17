---
layout: post
title: "Perplexity Has a Tokenizer in Its Denominator"
date: 2026-10-07 09:32:43 +0300
post_type: research note
description: "Token-level perplexity changes when the same text is split into a different number of tokens, even if its total likelihood does not."
context_reviewed: 2026-10-07
math: true
tags: [language-models, tokenization, evaluation, experimental-design]
---

TF3-RO trains a compact Romanian language model from random initialization on synthetic moral microfiction. Before training, the project compared two 32,000-entry Romanian tokenizers. BPE produced 304.89 tokens per sentence on average, while the selected Unigram tokenizer produced 340.35. The Unigram choice favored morphological segmentation rather than the shortest sequences.

My earlier [TF3 release note](/2026/01/15/tf3-romanian-microfiction.html) reported that the resulting 51.65M-parameter model reached held-out cross-entropy near 0.89 and perplexity near 2.43. Those values are useful for following checkpoints and compression variants that share the same tokenizer and evaluation pipeline. They do not create a tokenizer-independent scale.

This note isolates the denominator. Perplexity exponentiates average negative log-likelihood per predicted token. If a tokenizer divides the same text into more pieces, it changes that average even when the model assigns the complete text exactly the same probability. A cross-tokenizer comparison therefore needs a unit tied to the text, not only to each model's tokens.

## The average is over tokens

For a token sequence \\(x_1, \ldots, x_T\\), let the total negative log-likelihood be

\\[
L = -\sum_{t=1}^{T}\log p(x_t \mid x_{<t}).
\\]

Token-level cross-entropy is \\(L/T\\), and perplexity is

\\[
\operatorname{PPL} = \exp(L/T).
\\]

The [Hugging Face perplexity guide](https://huggingface.co/docs/transformers/perplexity) gives this definition and states the comparison constraint directly: tokenization affects perplexity. The exponent does not remove that dependence. It only maps average log loss back to the model's token scale.

Consider one text with total negative log-likelihood 12 nats under two deterministic, lossless tokenizations:

| Tokenization | Predicted tokens | Total NLL | Per-token NLL | Perplexity |
| --- | ---: | ---: | ---: | ---: |
| coarse | 6 | 12 | 2 | 7.39 |
| fine | 12 | 12 | 1 | 2.72 |

Both factorizations assign the complete text probability \\(e^{-12}\\), about \\(6.14 \times 10^{-6}\\). The finer tokenization reports much lower perplexity because the same loss is divided by twice as many prediction events.

The comparison can reverse the likelihood ordering. A model with total NLL 10 over five tokens has perplexity 7.39. Another with total NLL 12 over ten tokens has perplexity 3.32. The second perplexity is lower, but its probability for the complete text is also lower: \\(e^{-12}\\) rather than \\(e^{-10}\\). The token scales differ, so the two averages do not rank the texts on a common unit.

## TF3 fixes the tokenizer before reporting perplexity

The [TF3 paper](https://arxiv.org/abs/2601.10410) reports that Romanian BPE averaged 304.89 tokens per sentence and Romanian Unigram averaged 340.35 under the actual preprocessing pipeline. The latter is about 11.6% longer. TF3 then uses the Unigram tokenizer for its Transformer, Mamba, compression, and generation experiments.

That order makes the reported training curve interpretable. A decrease from one checkpoint to another uses the same vocabulary, segmentation, held-out distribution, packing rule, and token denominator. The curve describes improved next-token prediction within that fixed system.

It would be different to train one model with each tokenizer and compare only their token perplexities. Even in the artificial case where both models assigned every sentence the same total likelihood, the 11.6% token-count difference would give them different per-token losses. Lower perplexity could reflect a better model, a finer segmentation, or both.

The tokenizer is more than a list of strings. The original [SentencePiece paper](https://arxiv.org/abs/1808.06226) describes a model file that contains the vocabulary, segmentation parameters, and character-normalization behavior. Changing that file can change the token count and the text presented to the language model. A reproducible perplexity result therefore needs the tokenizer artifact and its normalization policy, not only the vocabulary size.

## Normalize by a shared text unit

When two systems score the same normalized text, total negative log-likelihood remains additive across their token factorizations. It can be divided by a unit outside either tokenizer. For a text containing \\(C\\) declared characters,

\\[
\text{bits per character} = \frac{L}{C\log 2}.
\\]

Bits per byte uses the byte length in the denominator instead. Either can support a cross-tokenizer comparison if both systems score the same underlying sequence and the unit is defined identically. Bytes avoid ambiguity about what counts as a Unicode character, while characters can be easier to interpret for a fixed normalization and encoding contract.

The contract matters for Romanian. Precomposed `ț` and `t` followed by a combining comma can be different code-point counts while representing canonically equivalent text. The evaluation should specify whether \\(C\\) counts raw code points, NFC-normalized code points, grapheme clusters, or UTF-8 bytes. Applying different normalization inside two tokenizers would mean they are no longer scoring the same input object.

This normalization does not make unlike corpora comparable. A restricted synthetic domain can be more predictable than open-domain prose regardless of the denominator. It also does not turn likelihood into a complete generation-quality measure. It only removes the token count as one source of scale mismatch.

## Context policy changes the numerator

The denominator is not the only protocol choice. A finite-context model cannot condition every token on an arbitrarily long prefix. Splitting a corpus into disjoint blocks gives tokens at the start of each block little context and usually increases their loss.

The official perplexity guide recommends a strided sliding window for fixed-length models. Overlapping context is supplied to the model, but only the newly scored targets contribute to the loss. Each target must be counted once. The guide's GPT-2 example changes from perplexity 19.44 with disjoint 1,024-token chunks to 16.44 with a stride of 512. The model and tokenizer are unchanged; the available context changes the numerator.

Packed training data adds a related boundary choice. The evaluation record should say whether prediction continues across document boundaries, whether an end-of-sequence token separates records, and which first token in each segment is unscored because it has no left context in the batch. These choices alter the set of conditional probabilities included in \\(L\\).

Corpus aggregation must retain the same weighting rule. If document \\(i\\) contributes loss \\(L_i\\) over \\(T_i\\) valid targets, token-weighted perplexity is

\\[
\exp\left(\frac{\sum_i L_i}{\sum_i T_i}\right).
\\]

Averaging the per-document losses \\(L_i/T_i\\) instead gives every document equal weight. The two agree only when the documents have equal scored lengths or happen to have the same mean loss. Batch boundaries should not silently choose the estimand.

## Report enough to reconstruct the fraction

A token-level perplexity result should preserve at least:

- the tokenizer artifact and character-normalization policy;
- the held-out text identity and preprocessing revision;
- total negative log-likelihood and the number of valid target tokens;
- treatment of beginning, end, padding, and ignored tokens;
- context length, stride, packing, and document-boundary policy;
- a shared-unit result such as bits per byte for cross-tokenizer comparisons.

The first five fields make the reported token perplexity reproducible. The last separates model likelihood from the tokenizer's choice of how many prediction steps represent the text.

TF3's perplexity near 2.43 is a result on its Romanian Unigram scale. It can compare checkpoints and variants that keep that scale fixed. The BPE and Unigram token counts answer a different question about segmentation. Combining the two requires returning to the fraction underneath perplexity: total loss in the numerator, and an explicitly chosen unit in the denominator.
