# Structure & signal

Two decorative editorial studies created on 17 October 2026 with the built-in image-generation tool. These are invented material compositions, not photographs of research apparatus, evidence of an experiment, or functioning circuit diagrams.

The website uses responsive WebP derivatives at 480, 960, and 1440 pixels wide. The first study is eager-loaded with high priority; the second is lazy-loaded. Both have explicit intrinsic dimensions. Re-encode source artwork with `scripts/prepare_editorial_assets.py SOURCE structure` or `signal` using Pillow.

## Exact generation prompts

### Study 01: Structure & signal

Use case: photorealistic-natural. Asset type: original editorial hero art for a personal research-and-engineering journal. Create a landscape macro studio photograph of a physically hand-built architectural paper sculpture. One continuous wide ribbon of thick, uncoated ivory paper folds into disciplined stepped planes and elegant offset layers, with one very thin vermilion-orange cord passing through a few clean pinholes and following a precise signal-like route. The paper construction is a metaphor for turning abstract structures into working systems, not a scientific diagram. Dark charcoal matte ground and background, subtle warm-white highlights, one controlled burnt-orange accent. Unusual but plausible physical fabrication, asymmetrical composition, tactile paper fibres visible, sharp material edges, generous dark negative space around the silhouette. Single hard raking studio light from upper left produces beautiful credible shadows. Close crop, 70mm product photography, independent architecture journal art direction, restrained fine grain. Object occupies the middle two-thirds. Landscape 3:2 aspect ratio. No words, no symbols, no logos, no watermarks. Avoid floating glossy blobs, glass orbs, iridescence, neon glow, brains, robots, holograms, excessive cables, and decorative UI. It must look like a photographed crafted object, not a generic AI illustration.

### Study 02: Tracing the system

Use case: photorealistic-natural. Asset type: original editorial section art for a personal engineering and AI research journal. Create a landscape close-up still life photograph of an ivory printed-circuit substrate with extremely fine black etched parallel traces, one red-orange copper jumper wire taking an elegant deliberate route across the traces, and a few small uncoated paper tabs standing vertically from precise cuts. No electronics branding, no chips or recognizable commercial board. This is an invented physical editorial object about structure, experiment, and signal, not a functioning scientific circuit diagram. High craft: realistic fibrous white paper edges, tiny machining imperfections, matte copper and graphite texture. Strong asymmetrical crop, shapes run beyond image edges, museum design catalogue photography, raking daylight, muted warm ivory, graphite and vermilion only. Wide landscape 3:2 aspect ratio. No text, no letters, no numbers, no watermarks. Avoid neon, shiny chrome, glass, generic sci-fi, human faces, ornamental floating shapes and busy pseudo-technical clutter.

## Typography

Self-hosted Newsreader and Manrope variable fonts come from the official [Google Fonts repository](https://github.com/google/fonts). The SIL Open Font License notices are included in `assets/fonts/`. Subsets retain Latin, extended Latin (including Romanian), punctuation, and common arrows. Font loading uses WOFF2 and `font-display: swap`.

The originals are the Newsreader regular and italic variable TTFs and Manrope regular variable TTF. Newsreader first uses `fontTools.varLib.instancer SOURCE opsz=32 wght=400:650 -o DISPLAY.ttf` to fix the optical size for headings and retain the weight range in use. All derivatives then use fonttools 4.60.1 with `--flavor=woff2 --unicodes=U+0000-024F,U+1E00-1EFF,U+2000-206F,U+20AC,U+2122,U+2190-2199 --layout-features='*'`.

## Personal signature

The masthead uses the existing self-hosted Newsreader at weight 550, with restrained negative tracking and Romanian diacritics intact. Manrope provides the smaller localized “Strategy, technology & AI” descriptor. The name and descriptor remain selectable text; the full lockup is one link to the current language homepage.

Three code-native treatments were compared in the homepage on 17 October 2026: the editorial signature, an MN badge beside the name, and an architectural Manrope lockup with a vertical accent rule. The editorial signature was selected for its continuity with the display typography, stronger personal-name hierarchy, and simpler small-screen silhouette. The badge crowded the identity and the sans-serif treatment felt more corporate than personal. These are design judgments, not audience-test results.

The first refinement added a folded N, replacing the dot and MN favicon. A subsequent user-directed comparison moved the graphic gesture after the name: a trailing forward stroke, a rising underline, and a faint diagonal behind the surname. The forward stroke was selected because it leaves the name dominant and the accent marks unobstructed, while freeing the leading edge. The underline competed with the descriptor and the comma below ș; the background diagonal made the letters busier. These are design judgments, not audience-test results. The folded N remains useful as a standalone monogram and favicon, not in the written signature.

`_includes/brand-stroke.html` is the original editable forward stroke, `M2 28L10 4` in a 12-by-32 viewBox. The final refinement keeps ONE heavier stroke (4 SVG units), tightly spaced after the full name (0.18rem), lifted by 2 CSS pixels, in the existing vermilion. It is not a slash character in the accessible name. Only a 1-pixel horizontal nudge over 160ms responds to hover or keyboard focus. No automatic entrance, loop, pixel assembly or second line is published. Reduced motion disables the movement while retaining the resting placement; print and forced colors use ordinary ink. Do not place it in front of the name, overlap the letters, or add another badge. The geometry suggests forward movement without claiming measured business growth or trademark uniqueness.

A private exploration compared six shapes, thick/thin pairs, close/raised combinations, draw/settle/stagger motion and pixels flying in from the right. The user then requested tighter spacing and simpler animation and delegated the final choice. The single close stroke was retained to avoid punctuation-like clutter and animation competing with the name. Explorations remain outside publication under ignored `vendor/`; they are not approved production alternatives or audience-test evidence.

Only the accent strokes of ă and ș are muted in the masthead. The source retains the two precomposed Unicode letters, not an ASCII name with simulated accents. CSS background clipping paints the upper 24% of ă and lower 22% of ș in `--muted`, leaving the base glyphs in full ink. These boundaries were checked against the retained Newsreader's accent/base separation at weight 550 and reviewed in the actual header. `site.js` activates the calibrated paint only after the Font Loading API confirms that Newsreader loaded; fallback fonts and no-JavaScript readers keep ordinary full-ink text. Change the font only with a fresh visual review. Forced-color and print rules also disable the paint. Copy, accessible text and identity metadata preserve the spelling. Do not extend accent muting to Romanian content.

### Folded N: reusable identity assets

- `_includes/brand-mark.html`: retained inline, theme-aware standalone monogram source; not used in the written header/footer signature.
- `assets/brand/nadas-mark.svg`: transparent charcoal/vermilion master for light surfaces.
- `assets/brand/nadas-mark-inverse.svg`: transparent ivory/vermilion export for dark surfaces.
- `assets/brand/nadas-mark-mono.svg`: single-color export for restrained print and one-ink applications.
- `assets/favicon.svg`: the same geometry on a charcoal rounded square, checked at 16, 32 and 64 pixels.

These are original editable passive SVGs, not generated raster assets, font glyphs or externally licensed logos. The two monogram path geometries must remain identical across the retained inline component and exports; release tests reject drift and active content. The separate forward-stroke component has its own exact-geometry and placement checks. Retain those reproducible sources and the existing palette. No new font, script, image service or tracking is required.

Use the monogram sparingly without the full written signature: favicon or the corner of a future reviewed presentation/social template. Keep its proportions and transparent clearspace; the 32-unit viewBox includes at least 5 units around the strokes. Use at least 24 CSS pixels for the standalone mark in normal content; the favicon is the small-size exception. Do not tile it, use it as a bullet on every section, imply certification, or place it inside scientific diagrams. Written names remain the accessible identity. Header sizing, compact navigation, both themes and both language versions must be reviewed together when the lockup changes.

## Design references

- [Pentagram: Warner Music Group](https://www.pentagram.com/work/warner-music-group): a repeatable diagonal as a wider visual-system ingredient, not a reference to copy its specific angle or artwork.
- [COLLINS: AICP](https://wearecollins.com/story/aicp/): a simple graphic gesture that can adapt. Our signature stays much quieter and does not borrow its mark or animation.
- [Webflow: web design trends for 2026](https://webflow.com/blog/web-design-trends-2026): expressive typography and a recognizable visual system.
- [web.dev: image performance](https://web.dev/learn/images/performance-issues): responsive sources, dimensions, and loading priority.
- [web.dev: reduced motion](https://web.dev/articles/prefers-reduced-motion): motion is optional; the page contains no automatic animation.

The artworks provide atmosphere only. All navigation, headings, summaries, and research claims remain live HTML text.
