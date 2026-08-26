# mihainadas.github.io

Research and engineering notes published at [mihainadas.github.io](https://mihainadas.github.io/).

## Local checks

```sh
bundle install
python3 scripts/check_site.py
bundle exec jekyll build --strict_front_matter
python3 scripts/check_build.py
bundle exec htmlproofer ./_site --disable-external --enforce-https
```

The site uses the GitHub Pages dependency set and the bundled Minima release rather than an unpinned theme branch.

## Figures and diagrams

Keep visual material with the site under `assets/figures/<post-slug>/`. Prefer SVG for diagrams and WebP or PNG for screenshots. Every visual needs useful alternative text and a factual caption; diagrams should still make sense at 320 pixels wide and in print.

Use the shared include from a page or post:

```liquid
{% include figure.html
  src="/assets/figures/example/system-boundary.svg"
  alt="Requests cross an API boundary before entering the evaluation worker."
  caption="The boundary used by the timeout and schema checks."
  width="1200"
  height="720"
  wide=true
%}
```

For a dense diagram, add `mobile_src`, `mobile_width`, and `mobile_height` to provide a portrait composition below 640 pixels. Optional `source_url` and `source_label` fields add a separate attribution line.

Use a diagram when it clarifies a sequence, system boundary, data flow, artifact relationship, or chronology. Do not turn a short list into boxes merely to break up the page.
