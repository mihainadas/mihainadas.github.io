---
layout: post
title: "LoRA Fine-Tuning for Literary Translation"
date: 2025-08-04 14:00:00 +0300
tags:
  - language-models
  - translation
  - machine-learning
---

One of the more practical contributions of the TF2 project is demonstrating that lightweight fine-tuning can meaningfully improve literary translation quality with open-weight models. In this post, I want to discuss the approach and some observations from the process.

## The Case for Fine-Tuning

General-purpose language models can translate text out of the box, but literary translation has specific requirements that zero-shot prompting does not always meet. Models tend to produce literal translations that are accurate but stylistically flat, or they take creative liberties that sacrifice accuracy for fluency.

Fine-tuning on a curated set of high-quality literary translations can shift the model's behavior toward the balance we want: faithful to the source meaning while natural and stylistically appropriate in the target language.

The challenge is doing this efficiently. Full fine-tuning of a 7B+ parameter model requires significant compute. LoRA (Low-Rank Adaptation) offers an alternative: freeze the base model weights and train small low-rank adapter matrices that modify the model's behavior. The adapter typically adds less than 1% of the base model's parameters.

## The Training Setup

For TF2, my LoRA fine-tuning setup looks like this:

- **Base models**: Multiple open-weight models in the 7B-12B range
- **Training data**: A curated subset of English-Romanian literary translations, including fables, short stories, and folk tales
- **LoRA configuration**: Rank 16, alpha 32, targeting attention projection layers
- **Training**: 3 epochs, learning rate 2e-4 with cosine schedule, gradient accumulation for effective batch size 32

```python
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    task_type="CAUSAL_LM"
)

model = get_peft_model(base_model, lora_config)
```

The adapter files are small (tens of megabytes) and can be swapped in and out of the base model, which means I can maintain multiple specialized adapters without duplicating the full model weights.

## Quantization for Deployment

Beyond training, I also experimented with quantization to make the fine-tuned models more practical to deploy. Two approaches:

**GGUF quantization** via llama.cpp. This converts the model to a format optimized for CPU inference, making it possible to run translation on consumer hardware. The LoRA adapter is merged into the base model before quantization.

**W8A8 quantization** (8-bit weights, 8-bit activations). This preserves more precision than aggressive 4-bit quantization while still reducing memory requirements substantially. For literary translation, where subtle word choices matter, I found that 8-bit quantization preserves quality better than 4-bit.

## Observations

Some patterns from the fine-tuning experiments:

**LoRA adapters transfer across model sizes.** An adapter trained on a 7B model does not directly transfer to a 12B model, but the training recipe transfers well. The same hyperparameters and data produce good results across model sizes, which simplifies experimentation.

**Small training sets work.** Literary translation fine-tuning benefits from quality over quantity. A few thousand carefully curated translation pairs outperform a larger but noisier dataset. This matters because high-quality literary translations are expensive to produce.

**Style is the hardest dimension to improve.** Fine-tuning consistently improves accuracy and fluency scores, but style improvement is more variable. Some models respond well to style-focused training examples; others seem to have strong stylistic priors that resist adaptation.

**The cost is minimal.** A LoRA fine-tuning run on a single GPU takes hours, not days. This makes iteration fast and accessible to researchers without large compute budgets. For my setup, a single run on a Mac Studio with an M-series chip completes overnight.

## Next Steps

The TF2 paper will include a systematic comparison of zero-shot, few-shot, and LoRA-fine-tuned models across all five evaluation dimensions. The fine-tuned models are also being used to generate the large-scale parallel corpus, so the fine-tuning work feeds directly into the dataset release.
