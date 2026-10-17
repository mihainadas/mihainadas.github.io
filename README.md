# mihainadas.github.io

Research and engineering notes published at [mihainadas.github.io](https://mihainadas.github.io/).

## Book selections and reviews

The `/books/` shelf is data-driven from `_data/books.json`, with affiliate programs independently disabled by default in `_data/book_programs.json`. `/library/` groups Books, Applied Papers, and Notebooks without adding another primary navigation item. Book review posts retain the ordinary feed, archive, publication cap, and editorial gates. See [the operations guide](docs/books-operations.md) before drafting a review or activating referral links. It includes application preparation, cover provenance, and safeguards against unsupported personal recommendations.

## Editorial opening contract

Every post must make sense to a reader who arrives without the repository, paper, or previous post open. Before the first level-two heading, use at least two substantive prose paragraphs to identify the project or system, explain its purpose, and state the technical question or minimum setup needed to understand the result. Do not open with an unexplained metric, acronym, incident, benchmark, or artifact. Keep the context specific; generic scene-setting does not satisfy the contract.

After a cold-reader review, add `context_reviewed: YYYY-MM-DD` to the front matter. `scripts/check_site.py` enforces the marker and the minimum opening structure. The check cannot decide whether an explanation is accurate or useful, so the marker records the required editorial judgment rather than replacing it.

## Writing that earns the reader's time

Accuracy is the floor. Before marking `editorial_reviewed: YYYY-MM-DD`, read the complete draft aloud for cadence and check it as a cold reader:

- Identify the system and the practical question in the opening, then give the reader a concrete reason to continue. Preserve the two-paragraph, 60-word opening floor above.
- Explain unfamiliar terms when first needed. Technical notes can retain derivations; applied notes should establish the decision before introducing a sequence of papers.
- Let the evidence provide the tension: an unexpected output, an assumption that failed, a trade-off that changes a decision. Never invent a personal anecdote, motivation, dialogue, or experiment.
- Use first person where the public record supports a choice or interpretation. Distinguish an author's operating proposal from a measured benefit.
- Vary sentence length, section shape, and titles. Do not make every article a correction in the form “X is not Y,” or every section a matching list.
- Keep each limitation next to its claim. Remove repeated qualifications and an ending that merely restates the opening.
- Read code, equations, tables, citations, and prose together. Editing for accessibility must not silently alter a measurement, denominator, uncertainty, version, or scope.
- Remove stock prose, placeholders, and every em dash from the complete reviewed file.

New posts dated 17 October 2026 onward require the editorial marker as well as `context_reviewed`. These markers record judgment; checks cannot certify that readers enjoy an article.

The six initial revisions cover the evidence-budget, LoRA merge, Unicode/diacritics, three-emulator-bugs, three-million-stories, and noisy-text model-comparison articles. Other historical posts retain their existing review status; this is not a claim that the entire archive received a full prose rewrite.

Every article offers a voluntary email feedback link asking where the reader lost the thread. It sends nothing automatically and adds no tracking service. Use actual reader responses, not an automated readability score, to decide the next editorial changes. Do not describe the presence of the link as evidence of engagement.

## Romanian editions

English remains the complete publication archive. `/ro/` is a localized entry point, with complete Romanian editions of selected existing material. The first set covers Research, Unicode/diacritics, and evidence budgets. These live as Pages, not new dated posts, and do not duplicate entries in the English feed, homepage chronology, or weekly new-post count.

Each paired source and edition has the same `translation_key` and explicit `lang: en` or `lang: ro`. Romanian editions also declare `translation_source` (repository-relative), `translation_source_url`, `translation_source_sha256`, `translation_reviewed`, `context_reviewed`, and `editorial_reviewed`. They preserve all public citations and code/output blocks. Prose, terminology, navigation, date labels, feedback, and contents controls are localized. References to untranslated material are marked EN.

The source signature covers the English title, description, evidence-status, math and post-type declarations, and complete body. Obtain it with `scripts.check_site.language_source_signature` after reviewing the edition against the final source. Never refresh the signature merely to silence a stale-translation failure. A changed source blocks publication until its paired edition has been reviewed. Source review-only metadata does not invalidate the signature.

Layouts emit reciprocal `hreflang` for exact pairs, a separate self-canonical URL for each edition, and language-aware article metadata. Do not canonicalize Romanian articles to English or pair a summary with a complete article as equivalent translations. The language switch goes to the exact counterpart when available and otherwise to the language landing page; it never redirects automatically. On narrow screens it lives inside the menu to avoid crowding the header. The Romanian article list derives from published `translated-post` Pages.

Initialize locale data in the content layouts as well as the outer default layout: Jekyll renders inner layouts first. Moving initialization solely to the outer layout can leave article-level controls in English even when the header is Romanian. The generated checks guard against that regression.

Keep Romanian natural and precise, use modern diacritics in prose, retain exact character variants in Unicode examples, and explain technical English terms rather than transliterating them mechanically. Do not imply a Romanian-only original is an edition of an unrelated English article.

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

The default social preview is `assets/social-card.png`. To regenerate it, run `scripts/render_social_card.py --font MANROPE.ttf --display-font NEWSREADER.ttf --italic-font NEWSREADER-ITALIC.ttf` in a Python environment with Pillow, using the official font sources. It uses the local editorial artwork. Posts may supply `social_image` and `social_image_alt` for a specific preview. Keep preview files local and supply descriptive alternative text.

The visual system uses self-hosted Manrope for reading and navigation, Newsreader for display typography, a warm-paper surface, and restrained vermilion accents. New component styles live in `_sass/editorial.scss`. Artwork provenance, the exact generation prompts, responsive encoding, and font-subsetting instructions are in [the editorial asset notes](assets/editorial/README.md). These decorative studies are separate from factual figures in `assets/figures/`; never present them as experimental evidence.

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
