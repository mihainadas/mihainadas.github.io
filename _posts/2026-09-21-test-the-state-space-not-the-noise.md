---
layout: post
title: "Test the State Space, Not the Noise"
date: 2026-09-21 09:42:25 +0300
post_type: engineering note
description: "An emulator's pseudorandom sound path needs a recurrence, period, seed, and mixer test before listening becomes useful."
context_reviewed: 2026-09-21
tags: [systems, emulation, testing, audio]
---

86Box emulates historical PC hardware, including the Creative Music System and Game Blaster sound cards. Each card uses two Philips SAA1099 chips. An SAA1099 combines six tone channels, two noise generators, stereo amplitude control, and envelope control, which lets old software build effects from digital tones and coloured noise.

The programming interface exposes four clock choices for each noise generator. The [Philips description of the chip](https://www.worldradiohistory.com/Archive-Company-Publications/Philips-Technical-Review/Electronic-Compoinents/Electronic-Components-%26-Apps-Vol-8-No-1.pdf) specifies three fixed rates and one rate controlled by a tone generator. It does not give an emulator author a bit-for-bit reference sequence. The implementation still needs a precise state transition, or the right register writes can produce the wrong sound.

That distinction mattered in an [86Box report about static sound effects](https://github.com/86Box/86Box/issues/6557). The old noise path used a 16-bit state and the wrong feedback taps. The merged correction changed it to the SAA1099's 18-bit recurrence. Listening found the symptom; a state-space test made the correction reviewable.

## Write the recurrence as a contract

The corrected implementation shifts the state left and inserts the XNOR of stages 18 and 11. In zero-based C bit positions, those taps are 17 and 10:

```python
MASK = (1 << 18) - 1


def step(state):
    feedback = 1 ^ ((state >> 17) & 1) ^ ((state >> 10) & 1)
    return ((state << 1) | feedback) & MASK
```

This short form fixes four choices that prose such as "use an 18-bit LFSR" leaves open: shift direction, tap numbering, XOR versus XNOR, and the retained width. A test should fix the seed as well.

86Box starts its allocated device state at zero, so XNOR feedback is convenient. The all-zero state immediately advances; the all-ones state is the excluded lock-up state. AMD's [LFSR application note](https://docs.amd.com/v/u/en-US/xapp052) describes the general rule: a maximum-length `n`-bit recurrence visits `2^n - 1` states, and changing XOR to XNOR changes which uniform state locks up.

MAME's [SAA1099 implementation](https://github.com/mamedev/mame/blob/d0f1c15a0f6df2dd51a754cb46e6175b7079c8f2/src/devices/sound/saa1099.cpp#L282-L294) uses the complementary convention: XOR feedback with an all-ones initial state. Comparing its literal state words with 86Box would therefore reject a valid complement. The useful comparison is the tap relation, update direction, period, and declared output polarity.

## Count every state once

For 18 stages, the maximum non-locking period is

\[
2^{18} - 1 = 262{,}143.
\]

The period test is small enough to run directly:

```python
state = 0

for period in range(1, 1 << 18):
    state = step(state)
    if state == 0:
        break

assert period == 262_143
```

This checks more than the integer width. A mistyped tap can remain inside 18 bits and still enter a shorter cycle. A correct recurrence reaches its starting state after 262,143 updates and not before.

Running the same audit on the replaced 86Box recurrence gives a different structure. Starting from zero, it first advances to one, then enters a cycle of 32,767 states. The declared storage was 16 bits, but the feedback relation behaved as a shorter maximal sequence. This explains why changing only the C type would not have repaired the generator.

The [merged 86Box code](https://github.com/86Box/86Box/blob/e76d467e3563d12cf25ccb725e75940d84eaa187/src/sound/snd_cms.c#L98-L104) stores the running history in a 32-bit integer. Only the low 18 bits participate in the recurrence and output. Those low bits complete the 262,143-step cycle; the extra high bits are storage headroom, not additional generator stages.

## Separate sequence from clocking

The SAA1099 register interface controls how quickly the recurrence advances. It does not select a different feedback polynomial. The Philips programming description gives fixed noise clocks of 31.25 kHz, 15.6 kHz, and 7.8 kHz, plus a tone-controlled option from roughly 61 Hz to 15.6 kHz.

A state-space test should therefore call the transition directly. If it renders audio samples instead, a clock-divider error can masquerade as a sequence error, and the test may pass or fail depending on buffer size. Timing needs its own assertions: each register choice should produce the intended number of generator updates over a known sample interval.

This separation also makes failures easier to name. Wrong taps alter the bit order and period. A wrong divider preserves the order but plays it at the wrong rate. Both can sound like bad noise, but they are not the same defect.

## Test stereo with unequal values

The same [86Box change](https://github.com/86Box/86Box/pull/7772) fixed a separate mixer error. In the noise-only path, the right output used the left amplitude. A listening test with equal channel levels could never expose it.

The smallest useful mixer test sets deliberately unequal values, enables noise without a tone, forces a known high noise bit, and checks the two accumulators independently. In the 86Box mixer's integer scale, left and right amplitudes of 3 and 11 should contribute 270 and 990 respectively. Swapping, duplicating, or averaging them must fail.

That is a different invariant from the LFSR period. Keeping the tests separate prevents a stereo regression from being hidden inside a long expected audio buffer.

## State what the test establishes

The period test establishes that the implemented recurrence has the intended maximum-length cycle under its declared seed convention. The tap and prefix checks establish deterministic bit order. The asymmetric mixer test establishes independent digital channel gains at the implementation boundary.

None of them proves that the recurrence is a transistor-level description of every SAA1099 revision. The public Philips material documents the programming surface and noise clock choices, while the exact recurrence is corroborated by an independent emulator implementation and by the repaired game paths. Direct hardware capture would be stronger evidence for silicon fidelity.

That boundary is useful rather than embarrassing. The tests turn an audible complaint into three narrow claims about sequence, timing, and stereo routing. A later hardware trace can challenge one claim without making the others vague.
