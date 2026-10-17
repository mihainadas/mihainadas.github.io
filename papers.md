---
layout: page
title: Applied Papers
nav_title: Papers
permalink: /papers/
description: "Research on agents, evaluation, efficient models, and data, explained through practical business questions."
wide: true
---

What could a research result change in the way a business makes decisions, tests a system, or runs a process? These notes start with that question, return to the original papers, and distinguish what was measured from what might transfer to practice.

The reading map draws on Ritvik Rastogi's [Papers Explained archive](https://ritvik19.github.io/papers-explained/). Each entry pairs a contribution with a question worth testing in an organization. The linked explanations introduce the work; the articles below cite the primary research.

## Published notes

<div class="applied-notes">
{% assign applied_posts = site.posts | where: "series", "applied-paper-notes" %}
{% for post in applied_posts %}
{% include post-card.html post=post %}
{% endfor %}
</div>

## Reading map

<nav class="theme-jumps" aria-label="Paper themes">
{% for theme in site.data.papers %}
<a href="#{{ theme.id }}">{{ theme.label }} <span>{{ theme.papers.size }}</span></a>
{% endfor %}
</nav>

<div data-filter-list>
  <div class="filter-controls" hidden>
    <div><label for="paper-query">Find a paper or business question</label><input type="search" id="paper-query" data-query placeholder="Try retrieval, procurement, or LoRA" autocomplete="off"></div>
    <div><label for="paper-theme">Theme</label><select id="paper-theme" data-category><option value="">All themes</option>{% for theme in site.data.papers %}<option value="{{ theme.id }}">{{ theme.label }}</option>{% endfor %}</select></div>
    <button type="button" data-reset>Clear filters</button>
    <p class="filter-status" data-status role="status" aria-live="polite" aria-atomic="true"></p>
  </div>
  {% for theme in site.data.papers %}
  <section class="paper-theme" data-filter-group aria-labelledby="{{ theme.id }}">
    <h2 id="{{ theme.id }}">{{ theme.title }}</h2>
    <p class="theme-intro">{{ theme.intro }}</p>
    <div class="paper-records">
      {% for paper in theme.papers %}
      <article class="paper-record" data-filter-item data-category="{{ theme.id }}" data-issue="{{ paper.issue }}" aria-labelledby="paper-{{ paper.issue }}">
        <div><p class="paper-number">Paper {{ paper.issue }}</p><h3 id="paper-{{ paper.issue }}"><a href="{{ paper.url }}">{{ paper.title }}</a></h3></div>
        <dl><div><dt>Research contribution</dt><dd>{{ paper.contribution }}</dd></div><div><dt>Business test</dt><dd>{{ paper.business }}</dd></div></dl>
      </article>
      {% endfor %}
    </div>
  </section>
  {% endfor %}
</div>

## How to read these notes

Every applied note identifies the system and question before presenting a result. It cites the original paper, states what the experiment measured, names a plausible business use, and explains where the result may fail to transfer. A benchmark result alone does not establish production reliability or business value.
