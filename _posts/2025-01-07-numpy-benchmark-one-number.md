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

The 546× speedup was a formatting error wrapped around a benchmarking error. The saved notebook printed “NumPy is 545.88 times faster”; the paragraph underneath said 5.45×. Both came from one call to `time.time()`.

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

## The August 2026 run

Performance ratios change with vector size. At small sizes, call overhead is a larger fraction of the work. At large sizes, memory bandwidth, vectorized instructions, and BLAS threading become more visible. A single headline ratio hides that shape.

The executed notebook produced this table with nine samples per size:

| Items | NumPy median (ms) | NumPy IQR (ms) | loop median (ms) | loop IQR (ms) | median ratio |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1,000 | 0.0007 | 0.0001 | 0.114 | 0.011 | 162.4× |
| 10,000 | 0.0033 | 0.0003 | 1.146 | 0.129 | 347.2× |
| 100,000 | 0.0228 | 0.0007 | 9.918 | 0.337 | 434.1× |
| 1,000,000 | 0.4519 | 0.0263 | 99.622 | 7.790 | 220.4× |

Environment: Python 3.12.13, NumPy 2.5.2, macOS 26.5.2 on Arm64. The notebook requested one BLAS thread, but `threadpoolctl` found no compatible controller, so the backend thread count is explicitly recorded as uncontrolled. That caveat belongs beside the ratios.

- [Rendered notebook](https://mihainadas.github.io/notebooks/numpy_vs_python.html)
- [Source at the executed revision](https://github.com/mihainadas/notebooks/blob/63389f88cf80c901e1ff409477a461261cc0f9ec/numpy/numpy_vs_python.ipynb)
- [Execution test](https://github.com/mihainadas/notebooks/blob/63389f88cf80c901e1ff409477a461261cc0f9ec/scripts/test_notebooks.py)

The repaired notebook no longer owns a universal speedup. It owns a measurement procedure. The ratio belongs to whichever machine runs it next.
