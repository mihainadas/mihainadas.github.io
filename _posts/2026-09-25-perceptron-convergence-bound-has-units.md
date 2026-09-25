---
layout: post
title: "The Perceptron Convergence Bound Has Units"
date: 2026-09-25 09:34:18 +0300
post_type: research note
description: "A linearly separable dataset can require a very different perceptron update path after one feature changes units."
context_reviewed: 2026-09-25
tags: [machine-learning, perceptron, experimental-design]
---

The perceptron is a binary linear classifier that changes its weights only when it misclassifies an example. My earlier [auditable perceptron notebook](/2025/01/04/perceptron-you-can-audit.html) used two numeric features, a bias, and a fixed example order so that every update could be inspected. On its small separable dataset, one complete zero-mistake pass was enough to declare convergence.

The convergence theorem explains why that procedure must eventually stop when a separating hyperplane exists. It does not say that all numeric representations of the same labeled examples take the same route. The bound depends on a radius and a margin measured in the coordinates supplied to the algorithm.

This note isolates that dependence with six points and one controlled change. The labels, example order, update rule, and separating decision boundary stay fixed. Only the unit of the first feature changes. The resulting run needs either 3 updates or 3,049.

## The theorem counts mistakes, not epochs

Write each label as \(y_i \in \{-1, +1\}\) and include the bias by augmenting each point:

\[
z_i = (x_{i1}, x_{i2}, 1).
\]

Starting from \(w=0\), the basic update is

\[
w \leftarrow w + y_i z_i
\]

whenever \(y_i(w^Tz_i) \leq 0\). If a unit vector \(v\) separates every point with margin

\[
\gamma = \min_i y_i(v^Tz_i) > 0
\]

and \(R = \max_i \lVert z_i \rVert\), the algorithm makes at most

\[
\left(\frac{R}{\gamma}\right)^2
\]

updates. Novikoff's [1962 convergence proof](https://cs.uwaterloo.ca/~y328yu/classics/novikoff.pdf) isolates the progress argument behind the finite bound. MIT's [perceptron theory notes](https://openlearninglibrary.mit.edu/courses/course-v1%3AMITx%2B6.036%2B1T2019/jump_to/block-v1%3AMITx%2B6.036%2B1T2019%2Btype%40vertical%2Bblock%40perceptron_theory_of_the_perceptron_vert) state the modern \((R/\gamma)^2\) form directly.

The quantity being bounded is the number of mistaken-example updates. An epoch is only one pass through however many examples the implementation presents. A run can complete many epochs but make few updates, or concentrate several updates in one epoch.

## Six labels under three rulers

Consider these points in this fixed order:

```text
(-3,  3) -> -1
(-2,  0) -> -1
(-4, -3) -> -1
( 3,  0) -> +1
(-1,  1) -> -1
( 0,  2) -> +1
```

The rule

\[
x_1 + 0.3x_2 - 0.2 = 0
\]

separates them. Now replace the first coordinate with \(x'_1=sx_1\). The equivalent boundary is

\[
\frac{1}{s}x'_1 + 0.3x_2 - 0.2 = 0.
\]

The decision for every point is unchanged for any positive \(s\). The perceptron does not receive the symbolic equivalence, though. It receives vectors whose first coordinate may be one hundred times larger or smaller, and its additive update uses those coordinates literally.

This exact loop, evaluated with rational arithmetic, records the effect:

```python
from fractions import Fraction


ROWS = [
    (-3, 3, -1),
    (-2, 0, -1),
    (-4, -3, -1),
    (3, 0, 1),
    (-1, 1, -1),
    (0, 2, 1),
]


def train(scale):
    weights = [Fraction(0), Fraction(0), Fraction(0)]
    updates = 0

    for epoch in range(1, 10_000):
        mistakes = 0
        for x1, x2, label in ROWS:
            point = [scale * x1, Fraction(x2), Fraction(1)]
            score = sum(weight * value for weight, value in zip(weights, point))
            if label * score <= 0:
                weights = [
                    weight + label * value
                    for weight, value in zip(weights, point)
                ]
                updates += 1
                mistakes += 1
        if mistakes == 0:
            return updates, epoch, weights


for scale in (Fraction(100), Fraction(1), Fraction(1, 100)):
    print(scale, train(scale))
```

The three returned results are:

```text
100   -> 3 updates,    3 epochs, weights = (300, 1, 1)
1     -> 3 updates,    3 epochs, weights = (3, 1, 1)
1/100 -> 3,049 updates, 822 epochs, weights = (66.77, 1, -1)
```

All three final weight vectors classify all six transformed points correctly. The slow run is not evidence that the labels became nonseparable. Shrinking the first coordinate made each update in that direction small, while the fixed second coordinate and bias continued to move by whole units.

## The geometry changes with the representation

The same known boundary provides a valid, though not necessarily optimal, margin for each scale. In transformed coordinates its unnormalized weight vector is \((1/s, 0.3, -0.2)\). Normalizing that vector and measuring the largest augmented point gives:

```text
s = 100:  R = 400.0125, gamma = 1.108974, bound = 130,109 updates
s =   1:  R =   5.0990, gamma = 0.376288, bound =     184 updates
s = 0.01: R =   3.1625, gamma = 0.004000, bound = 625,109 updates
```

These are upper bounds derived from one separator, not predictions of the observed counts and not claims that this separator has the maximum possible margin. Their looseness is visible at \(s=100\): the bound grows to 130,109 while the run still needs only three updates.

The useful part is the dependency. Rescaling one coordinate changes both the largest vector norm and the normalized margin. Uniformly multiplying every augmented coordinate by the same positive constant would multiply \(R\) and \(\gamma\) together, leaving their ratio unchanged. Changing one feature's unit changes the Euclidean geometry seen by the update rule.

The theorem also does not promise the same final separator. It promises that some separator will be reached after finitely many mistakes under its assumptions. Example order, feature scaling, tie handling, bias representation, and learning rate can all change the path.

## Scaling is part of the experiment record

For a direct implementation, the input units belong beside the seed and example order. Reporting only that the data were linearly separable omits information needed to reproduce the trace.

For library code, the estimator's stopping rule must also be distinguished from the theorem. Scikit-learn's [`Perceptron`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Perceptron.html) exposes `max_iter`, `tol`, and optional shuffling; its documented iteration count is a count of passes, not the raw mistake bound above.

Standardization is one defensible coordinate choice, not a theorem requirement. Scikit-learn's [`StandardScaler`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html) records the training mean and variance used for each feature. Its [preprocessing guidance](https://scikit-learn.org/stable/common_pitfalls.html) also gives the operational constraint: learn transformations from the training subset, then apply the same transformation to validation, test, and production inputs.

The six-point construction establishes a narrow result. A change of units can leave every label and separating rule intact while changing a deterministic perceptron run by three orders of magnitude. Convergence is a property of separability; the route to convergence belongs to the representation.
