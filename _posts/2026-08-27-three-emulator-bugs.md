---
layout: post
title: "Three Emulator Bugs, Three Different Tests"
date: 2026-08-27 00:00:00 +0300
post_type: engineering note
description: "Printer output, audio hardware, and memory bookkeeping needed different tests—and the same discipline about what each fix established."
featured: true
tags: [systems, emulation, testing]
---

Three merged 86Box fixes touched unrelated subsystems: printer raster output, audio generation, and dynamic-recompiler page bookkeeping. The difficult part in each case was choosing an oracle specific enough to justify the change.

{% include figure.html
  src="/assets/figures/three-emulator-bugs/test-oracles.svg"
  mobile_src="/assets/figures/three-emulator-bugs/test-oracles-mobile.svg"
  alt="Three parallel test paths: a printer failure checked by a completed page, audio faults checked by a deterministic harness, and a restart abort checked by repeated guest restarts."
  caption="Each regression test supports a different, deliberately narrow claim."
  width="1200"
  height="560"
  mobile_width="320"
  mobile_height="1110"
  wide=true
%}

## A printer failure needs a completed page

The ESC/P 2 interpreter treated the `ESC .` Print Raster Graphics command as fatal. A Windows 95 Epson LQ-2500 test page reached that command, produced seven malformed PNG pages, and terminated the emulator.

[The merged change](https://github.com/86Box/86Box/pull/7774) parses the six-byte command header, handles uncompressed and run-length encoded row data, renders at the requested densities, and advances the print position by the raster width. The PR records a local replay of the same job: one complete page with the raster logo and text, without terminating 86Box.

The acceptance test covers one Windows 95 driver path. It supports a narrow claim: the previously fatal command is consumed and rendered correctly for the reproduced job.

## Audio hardware needs an invariant

The CMS implementation used a 16-bit noise state and feedback taps that did not match the SAA1099. Its noise-only path also sent the left amplitude to both output channels. Listening can reveal that something is wrong, but it is a weak oracle for a pseudorandom sequence and an easy way to miss channel coupling.

[The fix](https://github.com/86Box/86Box/pull/7772) uses the device's 18-bit feedback polynomial and the independent right-channel amplitude. The PR records a focused local harness for the sequence, its 262,143-state period, and separate stereo levels. It fails against the old implementation and passes with the change; the full macOS Arm64 build also completes.

The harness establishes digital behavior at the implementation boundary. Analog fidelity would need measurements against original hardware; listening alone cannot replace the sequence and channel assertions.

## A two-line deletion needs a causal account

A Windows 95 soft restart on a VIA VT82C496G machine could abort inside the new dynamic recompiler. During conventional-memory remapping, the code changed page backing pointers and masks, then marked each page as absent from the eviction list without unlinking it. A page could remain the list head while its membership marker denied that it belonged to the list.

[The merged correction](https://github.com/86Box/86Box/pull/7787) removes those two assignments. The page table establishes eviction membership when it is allocated; remapping the backing memory should not rewrite the live list topology. The PR records the unmodified debug build aborting during the first guest-initiated restart and the corrected build returning to the Windows network logon dialog after three consecutive restarts.

Because the correction deletes only two assignments, the state transition and regression path carry most of the explanatory weight. Three successful restarts exercise the path that motivated the change; other remapping paths require their own tests.

## What carries across subsystems

These fixes used different oracles: a rendered page, a deterministic harness, and a repeated guest lifecycle. The reviewable unit was the same in each case:

1. describe the observed failure;
2. identify the violated invariant;
3. make the smallest change that restores it;
4. rerun the original path;
5. record the boundary of the test.

Together, the reproduced failure and regression test define the claim supported by each change.
