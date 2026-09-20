---
layout: post
title: "A Holdout Is a Set of Equivalence Classes"
date: 2026-09-20 10:42:00 +0300
post_type: research note
description: "An arithmetic benchmark can be string-disjoint and still repeat a training fact. Sampling semantic groups makes the exclusion rule explicit."
tags: [evaluation, arithmetic, reproducibility, experimental-design]
---

An exact-overlap check admitted two of 300 benchmark additions whose operand-swapped twins were present in training. The strings differed. The arithmetic tasks did not.

For addition, training on `12+34` and testing on `34+12` does not support the same generalization claim as testing an unseen operand pair. The [CalcGPT reproducibility branch](https://github.com/mihainadas/calcgpt/pull/2) now treats a holdout as a sample of semantic groups rather than a sample of formatted equations.

That change is small in code. Its useful part is deciding what counts as the same task, then carrying that decision through splitting, benchmark sampling, and artifact records.

## Define sameness before shuffling

The group key parses each equation into integer operands and an operator. It ignores answer formatting and removes leading-zero differences before applying the operation rule:

```python
def semantic_key(left, operator, right):
    if operator == "+":
        low, high = sorted((left, right))
        return ("+", low, high)
    return ("-", left, right)
```

Addition uses an unordered operand pair because it is commutative. Subtraction keeps the operands ordered. `12-7` and `7-12` are different tasks, even before restricting this experiment to nonnegative results.

Parsing before grouping also separates task identity from representation. `012+034=...` and `12+34=...` receive the same key. A reversed answer and a normal answer do too. That is required for the planned representation ablation: changing the serialization must not silently change which arithmetic facts enter the holdout.

The implementation lives in [`lib/data.py`](https://github.com/mihainadas/calcgpt/blob/codex/cleanup-vnext/lib/data.py). It groups examples first, sorts the groups for a stable starting order, shuffles them with a declared seed, and assigns complete groups to training or validation. The regression test compares the sets of group keys across both partitions, not only their equation strings.

This is the arithmetic version of grouped splitting. Scikit-learn's [`GroupShuffleSplit`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html) accepts domain-specific group labels for the same reason: the unit that must stay together is not always one row.

## A requested fraction becomes approximate

Grouping changes the meaning of a 20% validation split. Individual examples are no longer independently movable.

If both addition orders exist, an off-diagonal group can contain two strings. A diagonal group such as `7+7` contains one. The splitter adds whole groups until it reaches its target example count, so the final fraction may cross the requested value by one group.

That is not a defect to hide with another random move. Moving one member would violate the exclusion invariant. The artifact should record the requested fraction, the realized example counts, and the realized group counts. A reproducible split owns its actual denominator, not only its seed and nominal ratio.

## Sample from the group space directly

The benchmark sampler in [`lib/benchmark.py`](https://github.com/mihainadas/calcgpt/blob/codex/cleanup-vnext/lib/benchmark.py) goes further than generating ordered tasks and rejecting leaks afterward. It indexes the semantic group space itself.

For a magnitude bucket containing `n` possible operand values, unordered addition has

\[
\frac{n(n+1)}{2}
\]

groups. Canonical nonnegative subtraction has the same count, because each task satisfies `left >= right`. The combined bucket therefore has `n(n + 1)` semantic groups.

This gives 110 groups for one-digit operands, 8,190 for two-digit operands, and 810,900 for three-digit operands. Each training task is encoded into one of those group identifiers. The sampler removes the blocked identifiers, samples ranks uniformly from the remaining space without replacement, and maps each compressed rank back to its original identifier with a binary search.

Only after an addition group is selected does the sampler choose an operand order. This avoids giving an off-diagonal addition group twice the sampling weight of a diagonal group merely because it has two printable strings.

Rejection sampling could also avoid overlap, but it makes runtime depend on how much of the bucket is blocked and invites an unnoticed retry limit. Sampling the allowed group ranks states the capacity in advance. If 100 tasks are requested and only 99 groups remain, generation fails with that fact instead of returning a smaller benchmark.

## Put the relation in the manifest

The holdout manifest records the exclusion policy, seed, operand width, sample count, task-roster hash, excluded-roster hash, and each task's semantic key. Rendering the same roster into four text representations preserves the manifest identity.

A later report can therefore check two separate claims:

- the evaluated tasks belong to the declared benchmark roster;
- the benchmark roster is disjoint from training under the declared equivalence relation.

A dataset hash alone establishes neither. It identifies bytes, not the task relation used to decide whether those bytes leak information.

## The equivalence relation is part of the claim

This rule does not make every arithmetic notion of similarity disappear. `1+4` and `2+3` share a result but remain different groups. Tasks with similar carry patterns also remain distinct. If the research question concerns unseen results, unseen carries, or extrapolation to wider operands, each needs a different holdout contract.

The present relation supports one narrow statement: no evaluated addition repeats a training operand pair in the opposite order, and no evaluated subtraction repeats the same ordered operands. The [grouping and benchmark tests](https://github.com/mihainadas/calcgpt/tree/codex/cleanup-vnext/tests) establish that software invariant. They do not establish that a model has learned arithmetic.

That result still requires completed runs. The split only makes clear which facts those runs are allowed to call unseen.
