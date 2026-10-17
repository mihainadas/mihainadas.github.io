# The reusable media library

The catalogue is `_data/media.json`; the shared renderer is `_includes/media.html`. The two editorial studies and the responsive decision-loop diagram are reusable assets, not article results. The existing scientific library remains in `assets/figures/`, with 14 editable desktop/mobile SVG sources tied to seven articles. Do not detach those figures from their evidence and reuse them as generic decoration.

Use `{% include media.html id="signal" %}` for a relevant decorative introduction. The homepage sets `class="hero-art" priority=true` for Structure, and uses normal lazy loading for Signal. The component owns dimensions, alternative text, captions, responsive variants, and loading. Do not duplicate image URLs through new layouts.

For actual experimental evidence, continue to use `figure.html` and the article-specific folder. Diagram patterns already available include a pipeline, comparison, intervention, uncertainty interval, robustness comparison, and test-oracle mapping. Read the original article before adapting a pattern; replace its data, captions, and source links, not just its title.

## Retention and rights

All catalogue display files are checked into Git. The decision-loop SVGs are their own editable originals, with a compact mobile composition. The raster studies retain their exact prompts in `assets/editorial/README.md`, but their original generation files were not retained in this checkout. The 1440-pixel WebPs are the best retained masters, not lossless originals. Their hashes prevent accidental replacement. Do not repeatedly re-encode them, claim pixel-identical regeneration from a prompt, or regenerate them each publishing run.

For future raster assets, retain a rights-cleared original in `assets/media-sources/`, excluded from the public build, alongside the optimized display variants and a catalogue entry. Do not put private files, people, client material, book covers, or third-party art there without a suitable permission basis. Every entry needs provenance, usage boundaries, source status, dimensions, alt text, and a meaningful caption. Generated art is decoration, never evidence.

`assets/media-sources/` retains the Google Fonts Manrope and Newsreader regular/italic variable TTF sources with their licenses. The PDF generator fixes Manrope's axes deterministically. The existing WOFF2 files and licenses remain the browser typography source. These retained sources also support `scripts/render_social_card.py`, the reusable social-card template, instead of commissioning a new visual identity per article. Use the editorial guide's optical-size instancing and subsetting commands when rebuilding display fonts.

Open Library book covers remain external edition-identification embeds, credited and backed by the title fallback. They are not locally licensed assets or part of a permanent archive. Do not download Amazon product images into this library. New covers continue through `books.json` and the existing Books workflow.

## Authoring and checks

1. Choose a relevant existing asset or pattern before creating a new one. Do not force the same image into unrelated articles.
2. Put factual claims in live prose; make decorative and conceptual uses explicit. Maintain enough contrast and a mobile layout.
3. Register reusable media in `_data/media.json`. For article evidence, keep the figure include, caption, source, and per-post folder.
4. Run `python3 scripts/check_media.py`, then the normal source, build, test, and link gates. The media checker is also called by `check_site.py` and CI.
5. Inspect the actual pages at desktop and mobile widths, light and dark, with images unavailable where a fallback matters.

“Durable” means versioned and recoverable, not immortal. A remote Git copy is useful redundancy, not an independent backup policy. Keep an independent repository backup; never store private credentials in it. The catalogue can be extended as the writing requires, without a speculative stockpile.
