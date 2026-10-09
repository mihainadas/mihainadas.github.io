---
layout: post
title: "A Distillation Weight Needs Its Temperature"
date: 2026-10-09 09:33:16 +0300
post_type: research note
description: "A knowledge-distillation coefficient is not reproducible unless the temperature, reduction, and valid-token denominator are recorded with it."
context_reviewed: 2026-10-09
tags: [language-models, knowledge-distillation, reproducibility, experimental-design]
---

TF3-RO trains a 51.65M-parameter Romanian language model, then compresses it into a 26.45M-parameter student. Both models use the same 32,000-entry Unigram tokenizer and predict the next token over the same vocabulary. This alignment lets the student learn from the teacher's complete probability distribution at each token position, not only from the one token present in the corpus.

The [TF3 paper](https://arxiv.org/html/2601.10410v1#S7.SS2) describes a hybrid objective: teacher-student KL divergence receives weight 1.0, while ordinary next-token cross-entropy receives weight 0.1. Those coefficients look like a complete mixing rule. They are not, because the magnitude and meaning of the KL term also depend on how logits become probabilities and how token losses are reduced.

This note isolates that reproducibility boundary. It does not re-evaluate the TF3 student or show that its reported result is wrong. It shows why a distillation record needs the softmax temperature, any temperature compensation, the KL implementation, and the exact valid-token denominator before `1.0` versus `0.1` can be reconstructed.

## Temperature changes the target

For teacher logits \(v_i\) over a vocabulary and temperature \(T\), the soft target is

\[
p_i^{(T)} = \frac{\exp(v_i/T)}{\sum_j \exp(v_j/T)}.
\]

The student distribution \(q_i^{(T)}\) is computed from student logits with the same temperature. A larger \(T\) moves both distributions toward uniform, exposing relative preferences that may be nearly invisible at \(T=1\).

The original [knowledge-distillation paper](https://arxiv.org/abs/1503.02531) makes this temperature part of the method. It generates teacher targets at a raised temperature, trains the student at that same temperature, then returns the student to \(T=1\) for inference. Temperature is therefore not an inference sampling option pasted onto training. It defines the target distribution being imitated.

Consider teacher logits `[4, 2, 0]` and student logits `[3, 2, 1]` for three possible next tokens:

| \(T\) | Teacher probabilities | Student probabilities | \(\mathrm{KL}(p^{(T)}\|q^{(T)})\) |
| ---: | --- | --- | ---: |
| 1 | [0.8668, 0.1173, 0.0159] | [0.6652, 0.2447, 0.0900] | 0.1156 |
| 2 | [0.6652, 0.2447, 0.0900] | [0.5065, 0.3072, 0.1863] | 0.0603 |
| 4 | [0.5065, 0.3072, 0.1863] | [0.4192, 0.3265, 0.2543] | 0.0191 |

The logits and the coefficient on KL did not change. The numerical loss fell by a factor of six because the probability distributions did. More importantly, the student received a different learning signal about the two lower-ranked tokens.

At \(T=1\), the teacher assigns the third token only 1.6% probability. At \(T=4\), it assigns 18.6%. The higher-temperature target asks the student to preserve more of the teacher's ranking among alternatives. Whether those alternatives contain useful structure or noise is an empirical question, which is why \(T\) belongs in the experiment record.

## The gradient brings a second temperature effect

For soft-target cross-entropy, the derivative with respect to student logit \(z_i\) is

\[
\frac{\partial \mathcal{L}_{\mathrm{soft}}}{\partial z_i}
= \frac{1}{T}\left(q_i^{(T)}-p_i^{(T)}\right).
\]

Raising \(T\) makes the two distributions softer and adds the explicit \(1/T\) factor. At sufficiently high temperature, the gradient magnitude scales approximately as \(1/T^2\). Hinton, Vinyals, and Dean therefore multiply the soft-target term by \(T^2\) when combining it with the hard-target term. The compensation keeps the two gradient contributions on roughly the same scale while \(T\) is varied.

The three-logit example shows the effect. Its unscaled soft-target gradient norm is 0.2497 at \(T=1\), 0.0980 at \(T=2\), and 0.0281 at \(T=4\). Multiplying the loss by \(T^2\) changes those norms to 0.2497, 0.3918, and 0.4490. The compensation is asymptotic, not a promise that finite-temperature norms will be identical.

A complete hybrid objective might therefore be written as

\[
\mathcal{L}
= \alpha T^2\,\mathrm{KL}\!\left(p_T^{(T)}\|p_S^{(T)}\right)
+ \beta\,\mathrm{CE}(y,p_S^{(1)}).
\]

If the implementation uses \(T=1\), the factor is one and can disappear harmlessly. If it uses \(T=4\), omitting the factor makes the soft-target gradient much smaller relative to the hard-target gradient even though \(\alpha\) and \(\beta\) are unchanged. Reporting only those two coefficients does not distinguish the cases.

## Reduction chooses the token denominator

Language-model distillation produces one vocabulary distribution for every scored token. A batch can have shape `[batch, sequence, vocabulary]`, plus a mask for padding or other ignored positions. The KL divergence first sums over vocabulary entries to give one value per token. Only then should the declared token reduction be applied.

This order matters with PyTorch. The current [`KLDivLoss` documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.KLDivLoss.html) says that its input must contain log probabilities and warns that the default `reduction="mean"` does not return the mathematical KL divergence. That reduction averages over every tensor element, including vocabulary entries. `batchmean` sums all elements and divides by `input.size(0)`.

For a classification tensor shaped `[B, V]`, `batchmean` gives a sum over \(V\) followed by a mean over \(B\). For a language-model tensor shaped `[B, L, V]`, it divides only by \(B\), so the result grows with the number of token positions \(L\). Flattening the same valid positions to `[B L, V]` before `batchmean` instead produces a per-token mean. The values can differ by a factor of \(L\) while the logits, temperature, and nominal KL coefficient remain identical.

A masked implementation can make the denominator explicit:

```python
teacher_logp = teacher_logits.log_softmax(dim=-1)
student_logp = student_logits.log_softmax(dim=-1)

per_token_kl = (
    teacher_logp.exp() * (teacher_logp - student_logp)
).sum(dim=-1)

soft_loss = per_token_kl[valid_token_mask].mean()
```

With temperature, both `log_softmax` calls receive logits divided by \(T\), and the final soft loss receives the declared \(T^2\) multiplier if that is the chosen convention. The teacher output should be detached or computed without gradients. The hard-target cross-entropy must use the same valid positions if the coefficient ratio is intended to apply per scored token.

The code also states the direction of the divergence. \(\mathrm{KL}(p_T\|p_S)\) weights each log-ratio by the teacher probability. Reversing the arguments is a different objective. PyTorch's API can make this easy to misread because the student log distribution is the first function argument while the teacher distribution is the target.

## Vocabulary alignment is a real precondition

TF3 satisfies a structural condition that should not be treated as incidental: the teacher and student use the same tokenizer and vocabulary. Token index 17,432 therefore names the same subword on both sides, and both models produce a distribution with the same support at the same source position.

Without that alignment, a pointwise KL over logits is undefined as a transfer of token meaning. Two vocabularies can have the same size while assigning different strings to each index. They can also segment the prefix differently, leaving no one-to-one correspondence between prediction positions. Padding a shorter logit vector or matching indices by number would create a valid tensor operation and an invalid learning objective.

Cross-tokenizer distillation needs another bridge, such as probabilities over a shared byte or character space, sequence-level targets sampled from the teacher, or an explicit mapping between compatible tokens. Each changes the object being transferred. The recent note on [tokenizer-dependent perplexity](/2026/10/07/perplexity-has-a-tokenizer-in-its-denominator.html) concerned an evaluation denominator. Here the shared tokenizer is part of the training objective's domain.

## Record the executable objective

For a language-model student, I would preserve these fields with the checkpoint:

- teacher and student revisions, tokenizer artifact, and vocabulary identity;
- temperature \(T\) for both distributions and inference temperature after training;
- KL direction, log-probability convention, and numerical implementation;
- whether the soft loss is multiplied by \(T^2\);
- hard and soft coefficients after all scaling;
- vocabulary sum, valid-token mask, and final reduction denominator;
- treatment of padding, document boundaries, and any unscored first tokens.

An executable unit test can use fixed teacher and student logits, a mask containing both valid and ignored positions, and a hand-computed loss. It should assert invariance to adding masked padding and to reshaping valid tokens before reduction. A second test can change \(T\) and verify the chosen scaling convention rather than accepting whatever magnitude a library default returns.

TF3 records the main structural facts: a frozen 51.65M teacher, a 26.45M student, a shared tokenizer, KL from the teacher distribution to the student distribution, hard-target cross-entropy, and weights of 1.0 and 0.1. The remaining details determine the executable fraction behind those weights. A distillation coefficient becomes reproducible only when its temperature and denominator travel with it.
