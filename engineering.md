---
layout: page
title: Engineering
permalink: /engineering/
description: "Selected systems work: emulator correctness, reproducible virtual machines, and bounded model experiments."
---

My engineering work spans language-model infrastructure and PC emulation. Across both, I define the failure, preserve the evidence, build a test that can fail, and keep the claim no larger than the result.

Only public, independently checkable work appears here. Working forks are not listed as projects, and changes under review are not presented as shipped.

## Upstream emulator work

I contribute fixes to [86Box](https://github.com/86Box/86Box), usually after reducing a guest-visible failure to a smaller implementation invariant. Selected merged changes include:

- [SAA1099 noise generation and stereo output](https://github.com/86Box/86Box/pull/7772): replaced the incorrect noise state and feedback taps and corrected the right-channel amplitude path. The PR records a focused local harness for the sequence, period, and independent channel levels.
- [ESC/P 2 raster graphics](https://github.com/86Box/86Box/pull/7774): implemented uncompressed and run-length encoded raster rows. The PR records a replay of the Windows 95 Epson test page that had previously terminated the emulator.
- [macOS process-activity lifetime](https://github.com/86Box/86Box/pull/7777): reproduced an Objective-C ownership failure under Zombies. The PR records 1,000 local pause/unpause cycles with the production object linked into a focused harness.
- [RAM-remapping eviction links](https://github.com/86Box/86Box/pull/7787): preserved live list metadata during conventional-memory remapping. The PR records repeated guest-initiated restarts through the path that had triggered the abort.

The [merged contribution record](https://github.com/search?q=author%3Amihainadas+repo%3A86Box%2F86Box+is%3Apr+is%3Amerged&type=pullrequests) is the source of truth for changes that entered the upstream project.

## Reproducible machines

[86Box VM Recipes](https://github.com/mihainadas/86box-vm-recipes) stores versioned, media-free machine definitions rather than redistributing installed systems. Each recipe separates public configuration from operating-system media, keys, ROMs, firmware, proprietary drivers, and disk images. The checks cover the public-tree boundary as well as the scripts: a reproducible recipe that accidentally publishes private media has failed its more important test.

[Retro Hardware Lab](https://github.com/mihainadas/retro-hardware-lab) is a set of later-PC emulation experiments. Each experiment starts with a question, a test, and a stop condition. Results become short reports; platform choices become decision records. One early result deferred the 86Box path for the first probe phase and moved the primary probe to QEMU because CPU timing alone would not resolve the chipset, interrupt, PCIe, and graphics-model gaps.

## Model pipelines

Model work appears here when it yields a public method rather than a project announcement. The notes below cover corpus-scale batching and provenance, low-rank adaptation, model design, and defensive local inference. Teaching material and smaller experiments live in the [notebook collection]({{ '/notebooks/' | relative_url }}); I keep them separate from research claims unless a notebook reproduces the relevant measurement.

## Reading the record

Posts distinguish merged fixes, experiments, release notes, plans, and retrospectives. A merge date establishes when a change entered an upstream project. A post date establishes when I wrote the account. Neither proves a broader history than the linked evidence supports.

## Engineering notes

{% assign engineering_posts = site.posts | where: "post_type", "engineering note" %}
{% for post in engineering_posts %}
- {{ post.date | date: "%d %b %Y" }} — [{{ post.title }}]({{ post.url | relative_url }}) — {{ post.description }}
{% endfor %}
