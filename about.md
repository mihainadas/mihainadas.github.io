---
layout: page
title: About
permalink: /about/
description: "Mihai Nadăș is a technology executive, engineer, and PhD researcher working on small language models, reproducible systems, and PC emulation."
---

I am Mihai Dan Nadăș. My papers and open-source work usually appear under the shorter form, Mihai Nadăș.

{% for role in site.data.now.roles %}{{ role.title }}, {{ role.organization }}{% unless forloop.last %}. {% endunless %}{% endfor %}. Alongside these roles, I pursue doctoral research and contribute to open source. The chronology below shows how that operating work grew out of engineering.

<p class="review-date">Roles reviewed {{ site.data.now.reviewed | date: "%d %B %Y" }}.</p>

{% include career-thread.html %}

Research and open source are how I stay close to implementation and test ideas in public. My doctoral work follows controlled narratives from English generation through English–Romanian translation to compact Romanian models trained from scratch. A parallel line examines Romanian diacritic restoration and open-weight models as evaluators. The [Research page]({{ '/research/' | relative_url }}) maps the papers and released artifacts.

Outside NLP, I contribute fixes to PC emulation software and maintain experiments around reproducible virtual machines. The public record includes merged upstream changes, focused regression tests, versioned machine definitions, and short experiment reports.

Running software organizations changed what I expect from technical work: another person should be able to see what failed, reproduce it, and decide whether the result is sufficient. The projects here are built around that standard.

This site contains the technical record that does not fit cleanly into a CV, paper, or patch. Only released results are described as results; reconstructed notes are marked as retrospectives. It is a personal site and does not speak for either organization. [LinkedIn](https://www.linkedin.com/in/mihainadas) carries the fuller operating history.

## Elsewhere

For a concise, evidence-linked view of my background, see the [professional record and downloadable résumé]({{ '/resume/' | relative_url }}). For consulting, advisory, or board-role discussions, [start with the decision or remit]({{ '/work-with-me/' | relative_url }}).

- [GitHub](https://github.com/mihainadas)
- [ORCID](https://orcid.org/0009-0003-3467-3262)
- [DBLP bibliography](https://dblp.org/pid/402/3758.html)
- [Google Scholar results for “Mihai Nadas”](https://scholar.google.com/scholar?q=author%3A%22Mihai+Nadas%22)
- [LinkedIn](https://www.linkedin.com/in/mihainadas)
- [arXiv author search](https://arxiv.org/search/?query=Mihai+Nadas&searchtype=author)
