---
layout: post
title: "Change One Slot, Watch What Else Moves"
date: 2026-08-27 09:11:56 +0300
feed_date: "2026-08-27 09:11:56 +0300"
last_modified_at: 2026-08-27 09:11:56 +0300
post_type: research note
description: "A paired intervention test separates response to a requested field from leakage into a field that should stay fixed."
featured: true
tags: [synthetic-data, evaluation, experimental-design]
series: controlled-synthetic-narratives
series_order: 2
evidence_status: thesis-only
---

Changing only the protagonist disturbed the unchanged moral in 4.0% to 18.5% of matched pairs, depending on the semantic verifier. Changing the moral almost never displaced the protagonist: specified-character realization changed in 0.5% of pairs [0.1%, 2.8%].

Those directions occupy different cells of the response–leakage matrix. I generated 200 matched pairs per intervention, holding every other slot and the decoding setup fixed and using a common seed within each pair.

> **Evidence status.** These are thesis-draft experiments, not a peer-reviewed result. They cover two of the six slots, one generator, 4-bit local inference, and 200 matched pairs per intervention.

{% include figure.html
  src="/assets/figures/change-one-slot-watch-what-else-moves/intervention.svg"
  mobile_src="/assets/figures/change-one-slot-watch-what-else-moves/intervention-mobile.svg"
  alt="A paired intervention matrix showing complete character response with verifier-sensitive moral leakage, while moral changes respond semantically, exact moral wording is less stable, and measured character leakage is low."
  caption="Response and leakage are separate measurements. Semantic and verbatim verifiers also answer different questions."
  width="1200"
  height="650"
  mobile_width="320"
  mobile_height="1110"
  wide=true
%}

## Characters responded; morals sometimes followed

When the character slot changed, the new character appeared in 100% of pairs, with a 95% Wilson interval of [98.1%, 100%]. The unchanged moral's realization also moved in 4.0% to 18.5% of pairs, depending on the semantic verifier.

The direct response is surface-checkable. The leakage estimate depends on a learned verifier deciding whether two stories still realize the same moral. Every tested verifier detected the direction, but they did not identify one defensible magnitude. The common seed removes one source of variation; it does not prove that every remaining difference was caused by the intervention.

## Moral changes rarely displaced the protagonist

Changing the moral produced an 87.5–98.0% response rate under semantic verification. Exact wording was much less stable: the requested moral appeared verbatim in 33.5% of pairs [27.3%, 40.3%].

The specified character was disturbed in only 0.5% of these interventions [0.1%, 2.8%]. The asymmetry is the result; its mechanism is not identified. Character interventions sometimes altered the moral-realization verdict, while moral interventions almost never disturbed the protagonist.

A story can express the requested lesson without repeating the specification literally. Semantic response measures meaning as interpreted by a verifier; verbatim response measures surface realization. Neither should be renamed ground truth.

## The asymmetric result

Both tested controls responded strongly. Their leakage did not run equally in both directions. Character changes sometimes disturbed the unchanged moral; moral changes almost never disturbed the character.

Because the moral cells depend on automated semantic verifiers, this establishes a direction that survived every tested instrument, not a human-perceived leakage rate. The remaining four slots, other generators, and human adjudication still belong to the next measurement round.

{% include thesis-series.html %}
