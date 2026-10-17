# mihainadas.github.io

Research and engineering notes published at [mihainadas.github.io](https://mihainadas.github.io/).

## Editorial opening contract

Every post must make sense to a reader who arrives without the repository, paper, or previous post open. Before the first level-two heading, use at least two substantive prose paragraphs to identify the project or system, explain its purpose, and state the technical question or minimum setup needed to understand the result. Do not open with an unexplained metric, acronym, incident, benchmark, or artifact. Keep the context specific; generic scene-setting does not satisfy the contract.

After a cold-reader review, add `context_reviewed: YYYY-MM-DD` to the front matter. `scripts/check_site.py` enforces the marker and the minimum opening structure. The check cannot decide whether an explanation is accurate or useful, so the marker records the required editorial judgment rather than replacing it.

## Mathematics

Add `math: true` to any post or page that contains TeX. The site then loads MathJax 4 only for that page. Use Markdown-safe delimiters with two source backslashes:

```text
Inline: \\(x^2 + y^2\\)

\\[
z = \sqrt{x^2 + y^2}
\\]
```

Kramdown consumes a backslash before punctuation such as `#`, `{`, `}`, `!`, and `|`. Double that source backslash inside TeX as well, for example `\\#`, `\\{`, `\\}`, `\\!`, or `\\|`. The source and generated-site checks enforce the renderer flag, delimiter balance, Markdown-safe punctuation, and intact display blocks.

## Homepage and discovery

The homepage derives its latest note, recent cards, chronology, and field-note count from published posts. `_data/threads.yml` maps the three homepage threads to existing `post_type` values. Optional `home_summary` overrides a post's `description`; publishing does not require duplicate homepage metadata. `featured: true` retains curated entry points independently of recent work.

`_data/now.yml` is the source for the homepage focus and About-page operating roles. Review its contents before changing `reviewed`; that date records a human content review rather than a deployment. CI warns after 45 days without preventing unrelated publication. `_data/papers.json` supplies the five-theme paper map and paper count. `_data/notebooks.json` supplies the notebook collection and count. Keep new paper IDs unique and retain the original 88 records.

The notebook collection lives at `/lab-notebooks/` because `/notebooks/` is served by a separate GitHub Pages project. Rendered notebooks keep their original project URLs. Update internal collection links to the new route, without changing rendered notebook URLs.

Papers and Archive render their complete contents at build time. `assets/site.js` progressively adds local search, category filters, shareable query URLs, mobile menu behavior, and a contents disclosure for long articles. These features make no third-party API calls. With JavaScript unavailable, all records and navigation remain accessible.

The RSS feed orders every eligible post by `feed_date`, then `published_at`, then `date`, using the first available value. `feed_date` is an optional historical override, not an inclusion requirement. Generated-site checks compare recent publications with the feed and homepage and retain checks for navigation, paper integrity, mathematics on pages and posts, and social metadata.

The default social preview is `assets/social-card.png`. To regenerate it, run `scripts/render_social_card.py --font <installed-sans-serif-font>` in a Python environment with Pillow. Posts may supply `social_image` and `social_image_alt` for a specific preview. Keep preview files local and supply descriptive alternative text.

## Running checks

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

For a notebook-derived chart, keep the notebook as the source of truth. Execute it cleanly with fixed seeds and a non-interactive plotting backend, export a deterministic SVG, strip timestamps and local-path metadata, and record the notebook commit in `source_url`/`source_label`. State the principal result in the alternative text; use the caption for the population, runs, units, and interpretation. Keep important numerical conclusions in the prose as well.

The checks require local assets, explicit dimensions, a factual caption, per-post storage, safe SVG content, and a real generated figure. They reject orphaned assets, private filesystem paths, active SVG content, and remote SVG dependencies.
