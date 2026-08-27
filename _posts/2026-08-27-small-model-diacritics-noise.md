---
layout: post
title: "The 2.4M-Parameter Model Won—Until the Text Got Noisy"
date: 2026-08-27 09:11:56 +0300
feed_date: "2026-08-27 09:11:56 +0300"
last_modified_at: 2026-08-27 09:11:56 +0300
post_type: research note
description: "Romanian diacritic restoration changes winners when clean benchmark text gives way to typos and OCR-like corruption."
featured: true
tags: [romanian-nlp, evaluation, small-models]
series: controlled-synthetic-narratives
series_order: 5
evidence_status: thesis-only
---

On clean Romanian, a 2.4M-parameter BiLSTM reached 96.23% word accuracy. Under heavy corruption it fell to 36.76%. The dictionary baseline finished at 70.31%.

The input distribution, not the parameter count, chose the winner. “Best model” changed when the test text began to resemble a noisy keyboard or OCR pipeline rather than an edited corpus.

> **Evidence status.** This comparison is preliminary thesis work and a manuscript in preparation. It has not been peer reviewed. ByT5 used 50,000 training pairs, so its result is not a budget-matched architecture comparison.

{% include figure.html
  src="/assets/figures/small-model-diacritics-noise/robustness.svg"
  mobile_src="/assets/figures/small-model-diacritics-noise/robustness-mobile.svg"
  alt="Word accuracy from clean to heavily corrupted Romanian text for four restoration systems: the BiLSTM starts highest and falls fastest, the dictionary baseline starts second and finishes highest, and ByT5 remains between them under heavy noise."
  caption="Clean-text accuracy and robustness answer different deployment questions. Values are from the preliminary CRAWLER-1000 experiment."
  width="1200"
  height="680"
  mobile_width="320"
  mobile_height="1110"
  wide=true
%}

## The clean table rewards constraint

On the clean CRAWLER-1000 test, the dictionary system reached 93.72% word accuracy with a 0.045 diacritic error rate. The 2.4M-parameter BiLSTM led at 96.23% and 0.033. ByT5 reached 92.00% and 0.081. A 1.7B-parameter Qwen3 model adapted with LoRA reached 48.99% and 0.545; prompted Qwen2.5 and Llama baselines were both near 70.5% word accuracy.

Parameter count did not predict the result. The constrained systems have the right inductive bias for a mostly character-preserving transformation. The decoder has far more capacity, but capacity is not the same as control.

## Noise reverses the operational choice

From clean to high corruption, word accuracy changed as follows:

| System | Clean | Low | Medium | High | Relative drop |
| --- | ---: | ---: | ---: | ---: | ---: |
| Dictionary | 93.72 | 92.26 | 81.31 | 70.31 | 25.0% |
| BiLSTM, 2.4M | 96.23 | 49.17 | 43.66 | 36.76 | 61.8% |
| ByT5 | 92.00 | 76.59 | 69.03 | 60.71 | 34.0% |
| Qwen3 LoRA, 1.7B | 48.99 | 53.15 | 45.72 | 37.60 | 23.2% |

The Qwen model's low-noise uptick should be treated as sampling variation until replicated. Its smaller relative drop is not a robustness victory because it starts from a much lower clean ceiling.

The practical selection is therefore conditional. For clean text, the BiLSTM leads this benchmark. For corrupted input, the dictionary is the strongest of these four by the high-noise endpoint. ByT5 loses some clean accuracy but degrades more gradually; a budget-matched training run is needed before attributing that behavior to architecture.

## Put the corruption model in the contract

A diacritic-restoration benchmark should state which non-diacritic edits are present, when corruption is applied, and whether the system may alter other characters. It should report accuracy at diacritizable positions together with unwanted edits elsewhere. Otherwise, a fluent rewrite can score as restoration while changing the source.

The next experiment needs repeated corruption draws across additional declared seeds, confidence intervals for model differences, latency on the target hardware, and an exact-preservation measure. Until then, this table chooses candidates for deployment tests; it does not crown a universal Romanian restoration model.

{% include thesis-series.html %}
