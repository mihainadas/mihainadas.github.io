---
layout: page
title: Archive
permalink: /archive/
description: "All engineering notes, experiment reports, release notes, and retrospectives."
---

Entries are ordered by the event or original note date. Reconstructed entries are labeled “event” here and show their actual publication date on the post.

{% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}
{% for year in posts_by_year %}
## {{ year.name }}

{% for post in year.items %}
- {% if post.published_at %}event {% endif %}{{ post.date | date: "%d %b" }} — [{{ post.title }}]({{ post.url | relative_url }}){% if post.post_type %} · _{{ post.post_type }}_{% endif %}
{% endfor %}
{% endfor %}
