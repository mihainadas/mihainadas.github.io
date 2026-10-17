---
layout: page
title: Notebooks
permalink: /lab-notebooks/
description: "Three tested, executable notebooks with rendered outputs and public source."
---

These executable notes work through small machine-learning and performance questions. The public repository validates every notebook file and runs the curated set from top to bottom in CI.

The rendered notebooks are hosted by the separate [notebooks project](https://github.com/mihainadas/notebooks). Each link below opens its output; this page keeps the collection connected to the [engineering record]({{ '/engineering/' | relative_url }}).

{% for notebook in site.data.notebooks %}
## {{ notebook.title }}

{{ notebook.description }}

- [Read the rendered notebook]({{ notebook.rendered }})
- [View the source]({{ notebook.source }})
{% endfor %}

The survey notebook remains historical analysis and is under review while its population, skip logic, ordinal bins, and subgroup denominators are rebuilt.
