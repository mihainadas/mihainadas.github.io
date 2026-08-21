---
layout: post
title: "The 546× Speedup That Wasn't One Number"
date: 2025-01-07 10:00:00 +0200
last_modified_at: 2026-08-27 10:00:00 +0300
post_type: retrospective
description: "Why a one-shot NumPy benchmark was not publishable, and the small protocol that replaced it."
redirect_from: /2025/01/07/numpy-vs-python.html
tags: [python, numpy, performance, notebooks]
---

> **Retrospective.** The benchmark first appeared in January 2025. It was rebuilt and re-executed in August 2026.

The saved notebook printed “NumPy is 545.88 times faster.” The paragraph underneath said 5.45×. The larger problem was not the misplaced digits: both numbers came from a single run using `time.time()`.

The original single timing could not support a general speedup claim. Library initialization, CPU scheduling, power state, thread-pool startup, and cache effects can dominate a short operation. The notebook also offered no correctness assertion, no warm-up, no spread, and no runtime description.

## A minimum viable benchmark

The repaired notebook uses the following protocol:

1. Generate deterministic `float64` inputs with a local NumPy generator.
2. Run both code paths once before measuring them.
3. Assert numerical equivalence with `numpy.testing.assert_allclose`.
4. Measure four input sizes over nine repetitions with `time.perf_counter()`.
5. Report medians and interquartile ranges, not only the fastest sample.
6. Record the Python, platform, and NumPy versions next to the result.

The compared loop is explicit:

```python
def python_dot(left, right):
    return sum(float(x) * float(y) for x, y in zip(left, right))
```

That definition matters. It iterates over NumPy scalar values, so the result measures Python interpreter overhead on top of NumPy-backed storage. `numpy.dot` dispatches the complete operation to compiled numerical code and may use a threaded BLAS implementation. This is not “Python versus C” in the abstract; it is these two implementations, on this environment, for these array sizes.

## Why the result is a table

Performance ratios change with vector size. At small sizes, call overhead is a larger fraction of the work. At large sizes, memory bandwidth, vectorized instructions, and BLAS threading become more visible. A single headline ratio hides that shape.

The notebook therefore does not hard-code “NumPy is _n_ times faster” in prose. It produces a table whose medians and IQRs belong to that run. Re-running the notebook is expected to change the values while preserving three invariants: both implementations agree numerically, timings are positive and finite, and the measurement method is disclosed.

- [Rendered notebook](https://mihainadas.github.io/notebooks/numpy_vs_python.html)
- [Source and execution test](https://github.com/mihainadas/notebooks)

The durable result is the protocol. The speedup is an observation attached to a machine and a run.
