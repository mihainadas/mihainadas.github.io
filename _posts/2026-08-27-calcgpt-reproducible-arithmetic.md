---
layout: post
title: "Defining a Reproducible Arithmetic Experiment in CalcGPT"
date: 2026-08-27 12:00:00 +0300
post_type: engineering note
description: "What semantic holdouts, versioned artifacts, and a predeclared representation ablation can establish—and what they cannot."
tags: [language-models, arithmetic, reproducibility, testing]
---

CalcGPT began as a small GPT-2-style model trained to complete arithmetic
expressions. The current [pull request](https://github.com/mihainadas/calcgpt/pull/2)
does not make the model larger or publish a new score. It narrows the experiment:
record which arithmetic tasks enter each split, define what counts as an unseen
task, and bind later results to versioned data and model artifacts.

## Exact overlap was not enough

The first held-out check excluded exact operand/operator tuples from the training
data. That misses an equivalence specific to addition. If `12+34` is in training,
testing `34+12` does not provide the same evidence as testing an unseen operand
pair.

Under the intended canonical benchmark seed 42, an audit of the 300-task sample
found two addition tasks whose operand-swapped twins were present in the committed
training data. This does not show that an earlier model memorized either pair. It
shows that exact disjointness could not support the stronger claim of semantic
disjointness.

The proposed sampler assigns addition to a group keyed by its sorted operands;
excluding either ordering excludes both. Subtraction remains directional. A
regression test checks the semantic groups as well as exact task overlap. The
lesson is narrower than “remove duplicates”: the split invariant must match the
symmetry of the task.

## Artifacts record evidence; they do not create it

A saved model needs more than weights. The proposed training path writes a
tokenizer, a task-format specification, and a manifest containing the source
dataset hash, grouped-split hashes, configuration, Git state, dependency versions,
and training losses. Proposed evaluation reports record their own dataset, model,
configuration, and artifact hashes.

Those records matter only when their relationships are checked. The proposed
ablation plan constructs one semantic holdout manifest from the declared source
roster, renders that roster for all four representations, and assigns the same
manifest hash to every cell. Evaluation rejects a supplied manifest whose roster
does not match the evaluated tasks; the summary contract checks that run
provenance against the plan. A shared seed or row count alone is not accepted as
that binding.

Identity checks are necessary but not sufficient. An adversarial review found
that an aggregator could recognize the canonical benchmark hashes while accepting
metrics over only 100 examples from a 300-task manifest, or a completed record
that omitted EOS, arithmetic-stratum, throughput, and supervised-target evidence.
A hash establishes which roster was intended; it does not establish that the
entire roster was scored or that the required measurements were recorded. The
summary validation now requires both provenance and completeness: the canonical
300-task denominator; versioned train and validation target-token counts that
match the training manifest; EOS evidence; all seven declared arithmetic-stratum
partitions reconciled to the primary counts; and finite, internally consistent
throughput under its declared successful-completions scope. Regression tests cover
the missing and inconsistent cases. This establishes a reporting contract, not a
model-quality result.

The repository changes also separate fast contract checks from a real-ML smoke test.
The pull-request matrix stays dependency-light across Python 3.11–3.13 and tests
the extracted source distribution on Python 3.11. A scheduled or manually
dispatched workflow installs the ML runtime, trains an intentionally tiny model,
and checks that the tokenizer, task specification, training manifest, model
configuration, and weights survive the round trip.

That smoke test establishes packaging and artifact plumbing. It is not a model
quality benchmark.

## Low accuracy is a result, not a crashed process

The previous evaluation command returned a failing process status when arithmetic
accuracy fell below 50 percent. That is useful only when a threshold has been
declared as a gate. For an ablation, a small model that scores poorly has still
produced a valid outcome if loading, generation, validation, and report writing
completed correctly.

The proposed command therefore separates operational failure from scientific
outcome. A caller can request a `--fail-under` threshold explicitly; without one,
weak runs remain in the experiment record instead of disappearing behind a
nonzero exit status.

The proposed evaluator restricts its primary arithmetic metrics to prompts with a
determined answer. Given only the first operand, many continuations are valid;
scoring one arbitrary continuation as the unique target makes aggregate accuracy
difficult to interpret. Those cases remain diagnostics rather than headline
accuracy.

## Four representations, one task roster

The planned experiment crosses fixed-width layout with answer order. Fixed-width
means that both operands and the answer occupy declared-width fields:

| Condition | Fixed-width fields | Reversed answer |
|---|---:|---:|
| Plain | no | no |
| Reverse only | no | yes |
| Fixed-width only | yes | no |
| Combined | yes | yes |

The plan renders all four datasets from one ordered roster of normalized
`(left, operator, right)` tasks. It declares model seeds 41, 42, and 43 in advance,
with split seed 42 and benchmark seed 42 fixed across conditions. The current
script validates the configuration and expands the four-by-three matrix into
distinct dataset, model, and report paths; it does not launch training.

This is a whole-representation comparison, not a token-budget-matched test of
operand padding. Under answer-only loss, minimal answers have variable length;
fixed-width answers always contain `operand_width + 1` digits, and EOS is a target
in both cases. Those target counts belong in each run record. Any narrower claim
about padding would require a separate matched-budget experiment.

If the runs proceed, every planned cell—including failures and low scores—belongs
in the record. A completed run binds its normalized train, validation, and
evaluation rosters to the declared benchmark-manifest hash. It reports exact,
numerical, strict-format, EOS, throughput, and arithmetic-stratum measurements
with denominators. A failed run retains its failed stage, error or exit status,
configuration, Git revision, and available diagnostics rather than disappearing.
Model weights can remain release assets; plans, manifests, hashes, and summaries
can remain reviewable files.

## Reinforcement learning is a separate experiment

Reinforcement learning is not part of the current baseline, implementation, or
result. It may become a post-baseline study only after the supervised four-way
matrix is complete.

The smallest useful study is a three-arm continuation from the frozen
padded-reversed checkpoints at seeds 41, 42, and 43: no continuation, an
equal-compute supervised continuation, and a verifier-reward policy-optimization
continuation. Naming the representation before seeing the baseline avoids choosing
the apparent winner after the fact. The supervised control distinguishes an RL
effect from the simpler effect of giving the model more optimization.

The continuation data would use a separate roster with no canonical benchmark
semantic groups. Reward would be 1 only for an exact canonical answer followed by
EOS and 0 otherwise; the KL coefficient, schedule, compute budget, and stopping
rules would be fixed before running. The existing 300-task benchmark would remain
untouched until final evaluation. Verifier mismatch, reward exploitation, and
output collapse would be recorded as failed runs rather than repaired mid-study.

This is an outcome-reward experiment because CalcGPT emits only final answers.
Adding process reward would first require an intermediate-reasoning representation
and would answer a different question. [DeepSeekMath](https://arxiv.org/abs/2402.03300)
introduced Group Relative Policy Optimization for mathematical reasoning, while
[DeepSeek-R1](https://arxiv.org/abs/2501.12948) studied verifier-based reinforcement
learning on reasoning tasks. [Let's Verify Step by
Step](https://arxiv.org/abs/2305.20050) is useful precisely because it separates
process supervision from final-answer outcome supervision. Those results motivate
the protocol; they do not establish that the same behavior will transfer to this
small model.

Without the completed supervised matrix, executable protocol, and recorded runs,
RL remains a deferred question rather than a capability claim.

## What this work establishes

The pull request under review defines stronger software and reporting contracts
for a controlled representation ablation. It does not establish that CalcGPT has
learned a general arithmetic algorithm, generalizes to wider operands, or reaches
a particular canonical accuracy. No model-quality result has been produced by
this work.

Those claims require completed runs and published evidence. The
[pull request](https://github.com/mihainadas/calcgpt/pull/2) is the review boundary,
and the branch's [research log](https://github.com/mihainadas/calcgpt/blob/codex/cleanup-vnext/docs/research-log.md)
records implementation status separately from empirical results.
