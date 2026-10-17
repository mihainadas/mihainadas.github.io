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

The masthead uses the existing self-hosted Newsreader at weight 550, with restrained negative tracking and Romanian diacritics intact. Manrope provides the smaller localized “Strategy, technology & AI” descriptor. A CSS vermilion dot is decorative and adds no spoken punctuation. The name and descriptor remain selectable text; the full lockup is one link to the current language homepage.

Three code-native treatments were compared in the homepage on 17 October 2026: the editorial signature, an MN badge beside the name, and an architectural Manrope lockup with a vertical accent rule. The editorial signature was selected for its continuity with the display typography, stronger personal-name hierarchy, and simpler small-screen silhouette. The badge crowded the identity and the sans-serif treatment felt more corporate than personal. These are design judgments, not audience-test results.

The small-size `assets/favicon.svg` is an original passive MN line drawing in charcoal, warm ivory and vermilion. It is not a raster asset or an extra font dependency. Keep it separate from the masthead rather than placing a competing symbol beside the name. Header sizing, compact-navigation behavior, light/dark rendering and both language versions must be checked together when this component changes.

## Design references

- [Webflow: web design trends for 2026](https://webflow.com/blog/web-design-trends-2026): expressive typography and a recognizable visual system.
- [web.dev: image performance](https://web.dev/learn/images/performance-issues): responsive sources, dimensions, and loading priority.
- [web.dev: reduced motion](https://web.dev/articles/prefers-reduced-motion): motion is optional; the page contains no automatic animation.

The artworks provide atmosphere only. All navigation, headings, summaries, and research claims remain live HTML text.
