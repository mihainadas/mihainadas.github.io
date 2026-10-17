# Standing publishing policy

Confirmed by Mihai on 17 October 2026. This is the canonical agreement for future manual and scheduled blog updates. The scheduler prompt and `AGENTS.md` must direct each run here. Detailed syntax and component contracts remain in `README.md`, `docs/books-operations.md`, and `assets/editorial/README.md`.

## Scope and repository safety

- The publishing checkout is this repository only. Do not edit sibling projects, inspect private employer programs, use private mailbox material, or broaden a post-writing run into a redesign, financial setup, or general maintenance project.
- Before any network operation at the start of a run, inspect the complete working tree, including staged and untracked files. Do not overwrite, stash, clean, reset, commit, or include pre-existing changes.
- The sole collision-copy exception is an untracked regular file whose basename has ` 2` immediately before its final extension, with an existing Git-tracked regular counterpart in the same directory after removing that ` 2`. Verify every candidate byte for byte. Only if all are identical, move those untracked candidates, preserving repository-relative paths, into the task's recovery directory under `recovery/publish-github-blog/<UTC timestamp>/` in the surrounding workspace. Never delete or overwrite a recovery file.
- A differing copy, a missing or unverifiable counterpart, an archive failure, or any other tracked, staged, or untracked change stops the run. Report exact paths and the conflict. Recheck cleanliness after recovery.
- Once clean, fetch origin and update `main` by fast-forward-only pull. Preserve stable article URLs. Stage only the intended new post and strictly necessary accompanying files.
- The scheduler may read its own configuration and memory and record dated run outcomes there. This does not authorize unrelated writes outside the publishing checkout and its narrowly scoped recovery directory.

## Cadence and topic selection

- At most one new original post per run, and at most three posts with front-matter dates in the current Europe/Bucharest Monday-to-Sunday week. Count book reviews and applied-paper essays too. If the week already has three, make no repository changes. Do not evade the cap through Pages, date manipulation, or a second publishing route.
- With capacity, publish one fully evidenced, gated post. If required evidence, authorization, or checks are missing, do not publish a substitute that pretends to pass; explain the blocker. A draft is not a publication.
- Business drives topic selection: choose a narrow decision about AI, software-led differentiation, investment, operating capability, or oversight. Use “The operating advantage” as the working editorial thread described in `docs/professional-operations.md`, not as a proven proprietary theory. Engineering, research, applied papers, and books provide distinct evidence and perspectives, not separate content silos.
- Review meaningful public `mihainadas` GitHub activity since the previous post, broadening to seven days if needed, as an evidence source rather than a mandatory topic priority. Exclude this blog's maintenance, branch creation, formatting-only work, dependency noise, private work, and sensitive details.
- Prefer completed owned work: merged changes, shipped features, resolved bugs, reproducible experiments, and useful notebooks. Cite the public commits, pull requests, issues, repositories, documentation, or original papers that support the claims.
- Choose one narrow question, not a weekly roundup. Compare subjects across the archive. Public owned work, an earlier note, or current primary research may supply the evidence. A technical article must remain technically useful; do not append a generic business moral or force every research finding into a commercial claim.
- Books and applied-paper essays are eligible only when they meet their own evidence and approval gates and have a distinct useful angle. Do not switch the scheduler into automatic book-review production or expand its scope merely because those sections exist.

## Voice and editorial judgment

- Read at least six existing posts before drafting, including recent work and at least two older posts. Match Mihai's direct, restrained research-and-engineering voice: short paragraphs, informative headings, concrete nouns, supported numbers, and calibrated uncertainty.
- Establish the subject, purpose, practical question, and minimum setup in the first two to four short paragraphs. Require at least two substantive prose paragraphs and 60 words before the first H2. A search-result visitor should understand the problem before meeting its result, metric, acronym, or implementation detail.
- Give the reader a concrete reason to continue. Explain unfamiliar terms when needed. Use evidence-based tension and trade-offs, not manufactured drama or an invented first-person anecdote. Keep limitations next to claims; distinguish proposed applications from measured outcomes.
- Vary sentence length, headings, and section shape. Avoid repetitive correction titles, canned transitions, stock introductions, matching three-item lists, generic conclusions, fake quotations, and promotional claims. Do not use “delve,” “game-changer,” “key takeaways,” “it is worth noting,” “in conclusion,” or “leverage” as a verb.
- Never use U+2014 (the em dash) in new or revised publication content, including its front matter and accompanying figure text. Scan the complete new file before commit. Do not mention assistance or the publishing automation in articles.
- Review the complete draft aloud for cadence and remove sentences that could fit any technical blog. Verify dates, names, versions, links, arithmetic, quotations, and claims against the cited evidence. Do not copy substantial source passages.
- Add `context_reviewed` only after the cold-reader opening review, and `editorial_reviewed` only after reviewing the complete prose. New posts dated 17 October 2026 onward require both. Never stamp or refresh dates, signatures, or approval markers just to satisfy a checker.
- Preserve the evidence when editing: equations, measurements, denominators, code, outputs, citations, chronology, and uncertainty. Readability scores and a feedback link do not prove reader enjoyment; use actual reader feedback without adding undisclosed tracking.

## Research and applied papers

- Disseminate Mihai's research through a plain-language question, the actual method and evidence, an explicit limitation, and useful links to the original paper, code, data, and notebook where public. Explain how the work relates to the broader research question without inventing access to an unpublished thesis or private documents.
- Applied Papers turns a focused set of original papers into an inspectable operating or business question. A newsletter explanation identifies a paper; it is not a substitute for reading the original source. Separate reported results, interpretation, and the proposed domain application.
- Use the public Papers Explained archive and feeds for newsletter-derived research. Private emails were only an explicitly authorized discovery aid, not a recurring source to mine or publish.
- Retain the existing paper records and unique identifiers. Do not silently rewrite their claims, lose entries, or advertise an unreviewed collection expansion. Topic-map counts must derive from the real data.

## Business purpose and professional record

- The site's organizing purpose is to demonstrate useful strategic judgment for consulting, advisory, and board-role enquiries. Connect research and engineering to software-led differentiation, AI investment economics, operating models, threats, opportunities, and oversight. Use `docs/professional-operations.md` for reader paths, evidence boundaries, and commissioning briefs. Demonstrate cross-functional judgment through evidence, not “rare executive” self-praise.
- On executive-facing entry points and the résumé, lead with judgment and capability rather than PR counts, merge status, bug-fix inventories, or unexplained project detail. Preserve the concrete evidence in the linked technical work. Abstract the relevance without inventing business scale, outcomes, or authority.
- A business essay develops a distinct decision question supported by public owned work, earlier notes, or current primary research. It counts as an original post, uses `post_type: business note`, and must pass the same cadence, evidence, opening, and editorial gates. Do not substitute generic industry predictions for evidence.
- Explain the business decision in plain English before technical detail. Separate reported study findings, their applicability limits, and proposed business tests. Software becoming easier to produce does not itself prove a productivity gain, return on investment, competitive advantage, or a measured client result. Sector lenses are questions, not fabricated industry case studies.
- Keep engagement invitations distinct from promises of availability, employer representation, guaranteed outcomes, independence, or appointments. Use the approved LinkedIn contact route unless Mihai supplies another public channel. No automated outreach or job/board applications are authorized.
- The résumé uses `_data/profile.json` for HTML and a generated PDF, with evidence links and a genuine factual-review date. Read the professional operations guide before changing career facts. Do not invent credentials, completed degrees, responsibilities, impact numbers, endorsements, or referee permission. Preserve the confirmed ongoing PhD status and historical executive-board distinction.
- Maintain the professional record when new verified facts justify it, not on every article run. Never refresh dates simply to appear active. Regenerate and visually inspect the PDF after covered inputs change; source checks reject a stale download. This does not authorize unrelated résumé maintenance during a capped or dirty-tree scheduled run.

## English and Romanian

- English remains the default original-post language and complete archive. Romanian originals are appropriate when the work and audience justify them. Selected complete Romanian editions are supported; translating every update automatically is not required or authorized.
- Follow the README's exact pairing, source signature, language metadata, canonical, `hreflang`, localized controls, and review-field mechanics. Never repair a stale-translation failure by changing only its hash or date.
- Use natural Romanian with proper diacritics. Preserve code, math, numerical meaning, source citations, and deliberate Unicode variants. Mark links to untranslated English material clearly. A short summary is not a complete translated counterpart.
- Do not miscount a new original article as a translation to bypass cadence. Preserve the established treatment of genuinely paired translation Pages and the English feed.

## Visual identity, usability, and discovery

- Keep the editorial-journal identity: warm paper and charcoal surfaces, restrained vermilion accents, self-hosted Manrope for reading/navigation, and Newsreader for display. Preserve font licenses and Romanian glyph coverage. Extend shared components rather than introducing unrelated styles for each article.
- Keep the compact navigation and group Books, Applied Papers, and Notebooks under Library. Do not add a new primary item for every collection. Preserve the accessible mobile Menu, Escape/focus behavior, theme and language controls, keyboard access, print, and reduced-motion behavior.
- The homepage stays alive through real published posts and collection data. Preserve latest notes, thread mappings, recent work, curated starting points, counts, and chronology. No fake activity, randomized recency, fabricated counters, or dates refreshed by deployment alone.
- Preserve full server-rendered content, stable URLs, the feed, sitemap, canonical URLs, accurate language metadata, social previews, author identity, and public source links. Structured data must describe actual content. Do not invent ratings or reviews, promise inclusion in ChatGPT/search results, or weaken crawl/access settings for cosmetic reasons.
- Keep the notebook collection at `/lab-notebooks/`; `/notebooks/` is a separate project route. Preserve its actual rendered notebook destinations.

## Media: durable foundation, article-specific evidence

- Use a hybrid approach: reuse the existing visual system, editorial studies, shared figure include, chart/diagram patterns, book-cover treatment, and social-card tooling. Produce bespoke figures when the article's actual result or explanation needs one. Do not regenerate decoration, fonts, or a site identity on every writing run.
- “Durable” means recoverable and maintainable, not guaranteed permanent. Use `_data/media.json`, the shared `media.html` include, and `assets/media/README.md` for the implemented reusable catalogue. Preserve originals or reproducible source where rights and storage permit, plus optimized derivatives, provenance, permitted usage, dimensions, and descriptive text. The retained raster masters are WebPs, not original lossless generation files. Do not create a speculative stockpile or promise perpetual external availability.
- Separate decorative illustrations from evidence. Invented or generated artwork must never masquerade as a measurement, apparatus photograph, real screenshot, book cover, or functioning technical diagram. Avoid generic glossy sci-fi, decorative clutter, and visually plausible but false charts.
- Prefer code-native/SVG diagrams and deterministic notebook-derived charts for factual material. Use the shared figure component, per-post storage, factual captions, useful alternative text, source links, explicit dimensions, and a mobile composition where necessary. Keep important numerical conclusions in prose too.
- Keep remote images exceptional and explicit. Book covers currently use Open Library's documented embed service, credits, edition-specific verification, no page referrer, and a title fallback. This is not a local archive or a guarantee of perpetual availability. Do not permanently copy Amazon imagery or fabricate/repaint covers; establish a suitable permission basis before local hosting.
- Preserve responsive image variants, eager loading only where appropriate, lazy loading elsewhere, and existing size budgets. Check narrow screens, dark mode, print, missing images, clipping, and reading measure. Reuse assets for relevant concepts, not to force unrelated articles into the same illustration.

## Books and affiliate independence

- Curate for international English-speaking engineers, AI practitioners, and technology leaders, with Romanian shopping alternatives. Selection follows reader value, not commission or popularity. Treat Gates Notes as a reference for idea-led essays, not a voice to impersonate.
- Reading selections based on publisher material must be labeled as such. A full review requires a lawfully accessible full book, or substantive reading notes with the passages needed to check the argument, and Mihai's approval of the judgment. Never invent reading completion, endorsement, personal experience, a quote, or a numerical rating.
- A full review should closely examine an argument or example, explain a practical application, show where the idea stops helping, and identify who should skip the book. Follow the existing `book review`, `book_id`, reading-basis, author/context/editorial review, and material-relationship gates.
- Follow `docs/books-operations.md` and the current checked data for exact editions, cover provenance, retailer destinations, and program activation. Verify product ASIN and displayed ISBN, not only a title or an ISBN-derived guess. A mismatch stays an ordinary search link until resolved; do not silently change editions to obtain commission.
- Only verified, enrolled programs and matching assigned tracking IDs may produce paid links. Keep nearby clear commission disclosure, visible paid-link labels, `rel="sponsored nofollow"`, and Amazon's required Associate statement when applicable. Ordinary links must not hide referral tags. Do not scrape prices, ratings, or availability.
- Direct Amazon US was chosen first; Germany and Romanian programs require separate verified setup before activation. Do not assume a US tag monetizes another country. Do not buy a routing-service subscription, open another account, accept terms, solve a verification challenge, or submit tax/bank/payment details unattended.
- Keep tax identifiers, addresses, bank details, passwords, tokens, and signed forms out of this public repository and scheduler memory. Enrollment, final program approval, and completed payment/tax setup are separate states. Do not claim one implies another, or manufacture qualifying sales through personal orders.

## Verification and release gate

Article narration follows `docs/audio-operations.md`. Synthetic audio needs a real listening review, exact transcript, source freshness checks, disclosure in speech and metadata, verified hosting, and actual platform links. No inactive player or invented podcast feed is published. A one-off pilot budget is not permission for recurring generation, account creation, terms acceptance, voice cloning, or paid subscriptions. Narration disclosure is required even though articles do not discuss writing assistance.

Use the repository-local bundle. If missing or incomplete, run `BUNDLE_PATH=vendor/bundle bundle install`. Run all of:

```sh
python3 scripts/check_site.py
JEKYLL_ENV=production BUNDLE_PATH=vendor/bundle bundle exec jekyll build --strict_front_matter
python3 scripts/check_build.py
python3 -m unittest discover -s tests
BUNDLE_PATH=vendor/bundle bundle exec htmlproofer ./_site --disable-external --enforce-https
node --check assets/site.js
node --check assets/theme.js
node --test tests/theme.test.cjs
git diff --check
```

- Install only the existing pinned test dependencies if the environment lacks them. An ignored local test-dependency path is acceptable; do not change dependencies just to force a pass.
- For math, use `math: true`, the README's Markdown-safe TeX delimiters and punctuation escaping, and the existing conditional MathJax setup. Inspect actual rendered equations: a green build alone does not prove a reader sees math. Never replace notation with styled code as a routine shortcut.
- For an unattended publishing run, fix failures in the new post and its strictly necessary accompanying files only. If an existing site issue prevents a clean build, report it rather than weakening checks or silently repairing unrelated material.
- Visually inspect the new article and affected entry points on desktop and narrow mobile, in light and dark themes. Exercise affected navigation, image fallbacks, figures, and mathematics. Keep proof of verification outside published content; report limitations if real visual verification is unavailable rather than claiming it happened.
- Commit a new post with `Add post: <title>`, push `main` to origin, verify build/deployment results and the actual public URL where possible, then report what is live, what remains a draft, and any unverified checks. Do not infer deployment success from push success.
- Record the dated outcome and next useful state in scheduler memory. Standing rules belong here, not scattered through historical run entries. Changes to policy, schedules, models, program registrations, or design direction require the user's explicit request.
