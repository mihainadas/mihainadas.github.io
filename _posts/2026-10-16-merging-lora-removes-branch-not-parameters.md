---
layout: post
title: "Merging LoRA Removes a Branch, Not Parameters"
date: 2026-10-16 09:32:53 +0300
post_type: research note
description: "A merged LoRA checkpoint removes adapter computation at inference, but it stores a full dense model and preserves only the low-rank origin of the update."
context_reviewed: 2026-10-16
tags: [language-models, lora, deployment, reproducibility]
---

TF2 adapts open-weight language models for English-Romanian literary translation. Instead of changing every backbone parameter during training, it learns rank-32 LoRA updates for selected attention and feed-forward projections. The released system then serves merged weights, so an inference runtime can load an ordinary model without a separate adapter path.

My earlier note on [the TF2 adapter](/2025/08/04/lora-finetuning-translation.html) described the update as `W′ = W + (α/r)BA` and separated that adaptation from later quantization. One phrase still needs a sharper boundary: merging does not turn the full model into a low-rank model, and it does not make the deployed checkpoint contain only the adapter parameters.

This note follows one adapted matrix from training to deployment. In exact arithmetic, the merged and unmerged forms compute the same linear map. They differ in storage, serving flexibility, and numerical behavior once finite precision or quantization enters the path. Keeping those properties separate prevents "parameter-efficient" from becoming an ambiguous claim about training, checkpoints, and inference at once.

## The update is low-rank, not the resulting layer

Let the frozen matrix be `W₀ ∈ ℝ^(d × k)`. LoRA trains

<p class="equation"><code>A ∈ ℝ^(r × k) &nbsp;&nbsp; B ∈ ℝ^(d × r)</code></p>

with `r ≪ min(d, k)`. With scale `s = α/r`, the adapted matrix is

<p class="equation"><code>W′ = W₀ + sBA</code></p>

The [original LoRA paper](https://arxiv.org/html/2106.09685v2#S4.SS1) freezes `W₀`, optimizes `A` and `B`, and identifies `BA` as the constrained update. Because

<p class="equation"><code>rank(BA) ≤ r</code></p>

the difference `W′ - W₀` is low-rank. No corresponding statement says that `W′` is low-rank. If `W₀` has full rank, adding a rank-32 update will normally leave the resulting dense matrix full-rank.

That distinction controls the parameter count. A dense `d`-by-`k` matrix contains `dk` values. Its LoRA pair contains `r(k + d)` trainable values. For a square 4096-by-4096 projection with rank 32:

| Artifact | Values | FP16 storage |
| --- | ---: | ---: |
| Frozen dense matrix `W₀` | 16,777,216 | 32 MiB |
| LoRA matrices `A` and `B` | 262,144 | 0.5 MiB |
| Merged dense matrix `W′` | 16,777,216 | 32 MiB |

The adapter has 1.5625% as many values as this base matrix. That is a real reduction in trainable, optimizer-managed, and task-specific parameters. It is not a 64-fold reduction in the size of the model required for inference. The base weights remain necessary either as a shared artifact or inside each merged checkpoint.

## Merging changes the evaluation graph

Without merging, an evaluation-mode forward pass applies two branches:

<p class="equation"><code>h = W₀x + sB(Ax)</code></p>

The low-rank order matters computationally. Forming `BA` on every forward pass would create a dense matrix and discard the main benefit of keeping an adapter separate. Computing `Ax` and then `B(Ax)` adds roughly `rk + dr` multiply-accumulate operations per input vector, compared with `dk` for the base projection.

After merging, deployment first computes

<p class="equation"><code>W′ ← W₀ + sBA</code></p>

once, then uses

<p class="equation"><code>h = W′x</code></p>

Distributivity makes the two expressions equal in exact arithmetic. Adapter dropout does not contradict this equivalence because dropout is disabled in evaluation mode. The [LoRA paper's deployment construction](https://arxiv.org/html/2106.09685v2#S4.SS1) explicitly stores the sum to avoid additional inference latency, and the current [PEFT LoRA guide](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora#merge-lora-weights-into-the-base-model) exposes the same operation through `merge_and_unload()`.

The practical gain is not the small arithmetic ratio alone. A separate adapter can add kernel launches, wrapper logic, extra memory reads, and synchronization around the base projection. Their effect depends on the runtime, batch size, hardware, and whether it has fused adapter kernels. A merge removes that branch entirely and returns the original dense architecture to the serving system.

The cost is flexibility. A shared base plus several small adapters can switch tasks without storing several full models. A merged checkpoint is one task-specific copy of the full backbone. PEFT's [checkpoint documentation](https://huggingface.co/docs/peft/main/en/developer_guides/checkpoint#merge-the-weights) also notes that `merge_and_unload()` removes PEFT-specific behavior: the result cannot disable, replace, or unmerge the adapter through those APIs.

Merging is therefore deployment repackaging. It trades adapter identity and switching for a simpler inference graph. Compression would require a separate operation such as quantization, pruning, or a smaller architecture.

## Floating point weakens the word identical

The algebra does not promise bitwise equality on a computer. The unmerged path evaluates `W₀x + sB(Ax)`; the merged path first rounds the entries of `W₀ + sBA`, then multiplies the rounded matrix by `x`. Floating-point addition and multiplication can round at different points even when both paths use the same nominal dtype.

For an ordinary FP16 or BF16 merge, the resulting differences should be judged against a declared tolerance and task-level output checks. A useful pre-deployment test compares logits from the adapter path and the merged path on fixed inputs before any generation sampling. Greedy decoded text alone is too coarse: two logit tensors can differ while producing the same tokens, or a tiny difference near a tie can change one token and everything after it.

The test also needs the model in evaluation mode. Otherwise adapter dropout can make repeated unmerged calls differ from each other, which says nothing about whether merging was implemented correctly.

Modules outside the LoRA matrices deserve explicit accounting. Biases or task heads may be trained and stored through configuration such as PEFT's `bias` or `modules_to_save`. A checkpoint that preserves only `A` and `B` while omitting those trained values is not the same adapted model, and merging the LoRA layers cannot reconstruct them.

## Quantized merging is a new approximation

Quantization makes the boundary more visible. If the base weights are already stored in a quantized format, a merge cannot generally add a floating-point `BA` directly to their integer codes. The implementation must reconstruct approximate real values, add the adapter update, and quantize the sum again.

PEFT's current [quantization guide](https://huggingface.co/docs/peft/main/en/developer_guides/quantization#merging-adapters-into-quantized-weights) describes exactly that sequence for supported methods: dequantize, add, then requantize. It also warns that unmerging performs another round trip and does not restore the original quantized weights. Repeated merge and unmerge cycles can accumulate rounding error.

This produces three distinct objects:

1. the quantized approximation of the frozen base, `Q(W₀)`;
2. the runtime combination of that approximation with an unmerged adapter;
3. the quantized approximation of the merged matrix, `Q(W₀ + sBA)`.

There is no general identity that makes the second and third objects numerically equal. Quantization is nonlinear because scales, zero points, groups, clipping, and rounding can change when the update is included. Some quantization methods do not support merging at all, and support can depend on the layer type and configuration.

For a release like TF2, the reproducible statement is not merely "LoRA was merged and the model was quantized." The order matters. Merging into a higher-precision base and then calibrating or quantizing the result is a different export path from loading a previously quantized base and asking an adapter library to merge into it.

## Preserve both the recipe and the product

A small adapter is attractive because the base can remain shared. That benefit depends on recording which base it modifies. Adapter provenance should include the exact backbone revision, tokenizer, target modules, per-layer ranks, scaling convention, trained biases or saved modules, and adapter weights.

A merged artifact needs a different record:

- the base and adapter revisions used to create it;
- the merge library and version, dtype, device, and selected adapters;
- whether the saved result still contains adapter wrappers;
- the quantization method, order, calibration data, group settings, and output dtype;
- a fixed-input logit comparison before and after merge;
- checksums for the adapter and final checkpoint.

The adapter recipe explains how the task-specific difference was encoded. The merged checkpoint records the exact dense product that was deployed. One cannot substitute for the other after quantization or when the original base revision disappears.

LoRA saves training state and task-specific storage because it represents the update with two small matrices. Merging spends that separability to recover the base model's ordinary inference graph. The deployed matrix still has `dk` values; only its difference from the frozen base came through a rank-`r` path.
