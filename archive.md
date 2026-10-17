---
layout: page
title: Archive
permalink: /archive/
description: "Find engineering notes, research, experiment reports, and retrospectives by topic or type."
---

Browse the complete record or search for a topic. Entries follow the event or original note date. Reconstructed accounts are labeled “event” and show their actual publication date on the article.

<div data-filter-list>
  <div class="filter-controls" hidden>
    <div><label for="archive-query">Search notes</label><input type="search" id="archive-query" data-query placeholder="Title, topic, or keyword" autocomplete="off"></div>
    <div><label for="archive-type">Type</label><select id="archive-type" data-category><option value="">All types</option>{% assign types = site.posts | map: 'post_type' | uniq | sort %}{% for type in types %}<option value="{{ type }}">{{ type | capitalize }}</option>{% endfor %}</select></div>
    <button type="button" data-reset>Clear filters</button>
    <p class="filter-status" data-status role="status" aria-live="polite" aria-atomic="true"></p>
  </div>
  {% assign months = site.posts | group_by_exp: "post", "post.date | date: '%B %Y'" %}
  {% for month in months %}
  <section data-filter-group class="archive-month" aria-labelledby="month-{{ forloop.index }}">
    <h2 id="month-{{ forloop.index }}">{{ month.name }}</h2>
    <ol class="archive-list">
      {% for post in month.items %}
      <li data-filter-item data-category="{{ post.post_type }}" data-search="{{ post.description | escape }} {{ post.tags | join: ' ' | escape }}">
        <time datetime="{{ post.date | date_to_xmlschema }}">{% if post.published_at %}event {% endif %}{{ post.date | date: '%d %b' }}</time>
        <div><a href="{{ post.url | relative_url }}">{{ post.title }}</a><span class="archive-type">{{ post.post_type }}</span></div>
      </li>
      {% endfor %}
    </ol>
  </section>
  {% endfor %}
</div>
