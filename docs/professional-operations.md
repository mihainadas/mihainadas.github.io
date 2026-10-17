# Business writing and professional record

Confirmed direction, 17 October 2026: business drives the site. Research, engineering, applied papers, and books are interwoven evidence for prospective consulting clients, founders, investors, and board nomination teams assessing Mihai's judgment. Commercial positioning must come from the work, not invented authority.

## The operating advantage

This is a working editorial thesis, not a new academic theory or a proven universal law: when software becomes easier to build, investigate the combination of customer access, workflow knowledge, useful lawful data, organizational capability, and execution that could turn it into a durable advantage. Use `_data/strategy.json` for shared public wording and selected, carefully qualified article connections.

The selected research foundation is David Teece’s [Profiting from technological innovation (1986)](https://www.sciencedirect.com/science/article/pii/0048733386900272): innovation does not automatically deliver returns to its inventor, and complementary assets affect who captures value. This fits a cross-industry executive and operating perspective better than treating every company as a platform.

Alternatives considered: Ben Thompson’s [Aggregation Theory](https://stratechery.com/2015/aggregation-theory/) is especially useful for platforms controlling the customer relationship and aggregating commoditized supply; it is too narrow as the whole site's organizing lens. [Modularity Theory](https://www.christenseninstitute.org/theory/modularity/) helps ask where interfaces are predictable enough to buy components, and where interdependencies justify integration. Keep both as supporting lenses, not interchangeable names for the selected framework. [Dynamic capabilities](https://www.davidjteece.com/dynamic-capabilities) can inform adaptation and reconfiguration; do not conflate it with ordinary operating efficiency.

Each commissioned business article should identify a decision, the proposed source of value, the complement that might be scarce, a buy/build/partner alternative, and what evidence could disprove the claim. These are editorial questions, not a compulsory five-part template. Sometimes a standard purchased service is best. Complements that are easy to obtain, irrelevant to customer choice, or too costly to maintain do not establish a moat. Research benchmarks and emulator fixes are evidence of methods, not client ROI.

Publish a full introductory strategy essay through the normal post route when cadence allows. The short landing-page thesis is positioning, not a workaround for the three-post cap. No new original essay is authorized this already-full week. Future runs are business-led, replacing the former GitHub-first priority while retaining public activity review as a valuable source.

## Reader paths

- `/business/`: a decision-led map supported by existing writing. Three lenses: software-led differentiation, AI investment/adoption, and evidence/accountability. `_data/business.json` supplies the lenses, industry questions, and engagement formats.
- `/work-with-me/`: scoping conversations, evidence, responsibility boundaries, and LinkedIn contact. No implied immediate availability, fixed fees, guaranteed savings, independent-director status, or employer representation.
- `/resume/`: selected professional record with role sources and papers. `_data/profile.json` is shared by HTML and PDF. The two-page PDF is selective, not a complete history or a vacancy-specific application.
- Books remains the reading shelf. A selection is not a review; paid links do not determine the editorial choice.

Keep five English primary destinations: Business, Engineering, Research, Library, About. Archive remains in the footer/homepage; résumé belongs under About and engagement enquiries under Business. Do not crowd the header again.

## Career evidence and maintenance

The public LinkedIn profile and its Experience/Education detail views were inspected on 17 October 2026 with the user's authorization. Role descriptions and periods come from that record, N13's management page, and linked research sources. Do not import private analytics, recruiter-only status, sidebar suggestions, messages, or contact overlays.

Mihai confirmed on 17 October that the PhD is still in progress. LinkedIn's October 2023–July 2026 period is stale, not evidence of an awarded doctorate. Do not edit LinkedIn without a separate request. ORCID confirms the undergraduate and master's degrees; LinkedIn supplies study dates and Intelligent Systems as the master's programme. Its Management of Business Development entry is described as graduate study, not a separately verified awarded degree.

The accesa.eu Executive Board role is historical and executive. Do not describe it as a current, independent, non-executive, statutory, or listed-company directorship. Preserve overlapping periods, including the METRO entries and Yonder CTO/business-unit roles. Do not sum overlapping jobs into inflated experience. Microsoft MVP, if added, is an award/community programme, not Microsoft employment.

Review roles, dates, education status, sources, publication status, and contact before changing `profile.reviewed`. Never auto-refresh it. Checks warn after 90 days without inventing new evidence. About/current-work roles must agree with the résumé. Move a paper from preprint to journal only with a verified publication record.

Add commercial metrics, client names, referee contacts, testimonials, or claims of availability only with evidence and authorization for public use. A paper or code link is an evidence reference, not an endorsement by a co-author or employer. Keep private identity, tax, contact, and application material out of the repository.

## Rebuild the résumé

Install the separate pinned `requirements-resume.txt` in an isolated environment. The generator fixes variable-font axes in the retained OFL Manrope source. Run:

```sh
python3 scripts/render_resume.py
python3 scripts/check_professional.py
```

This generates `assets/downloads/mihai-nadas-resume.pdf` and `_data/resume_build.json`. The record covers the profile, renderer, font, and PDF. A changed input without regeneration fails the normal source gate. Ordinary Jekyll/Pages builds publish the committed PDF without installing a PDF toolchain or using a remote service.

Inspect every rendered PDF page after regeneration: layout, Romanian glyphs, selectable text, and links. Keep the concise two-page layout. The server-rendered HTML is the accessible primary version. The current ReportLab PDF is selectable and linked but not tagged; do not claim PDF/UA compliance. Store previews in ignored `vendor/`. Run every normal site check before release.

## Editorial commissioning queue

These are briefs, not completed articles or approved reviews. All original business essays and reviews count toward the weekly limit. Use the normal post route and opening/editorial/evidence checks. A landing page does not create an obligation to publish an essay immediately.

### What remains scarce when implementation gets easier?

Choose one workflow. Separate code production from finding a useful problem, lawful data access, integration, acceptance testing, distribution, maintenance, and ownership. Compare buy, adapt, and build against a declared baseline. Industry examples stay illustrative unless supported by public cases or authorized evidence.

Research starting points: METR's current [research index](https://metr.org/research/), [February 2026 experiment-design update](https://metr.org/blog/2026-02-24-uplift-update/), and [May 2026 technical-worker survey](https://metr.org/blog/2026-05-11-ai-usage-survey/). The older developer study is not a current universal productivity estimate. Distinguish randomized timing, self-reported value, selection effects, tool/date/task setting, and later updates. Read the full original work at drafting time before using numbers.

### Where does an AI pilot's cost move?

Trace one service workflow, including human review, exceptions, recovery, integration, and maintenance. Model inference cost is not total workflow cost. Read the latest original [Generative AI at Work](https://www.nber.org/papers/w31161), not a stale headline percentage. Check population, outcome, and identification method. Do not transfer a support-agent result to an unrelated industry without a new test.

### Oversight and industry applications

Extend the evidence-budget work only with a distinct method or result, for example the minimum evidence package a board should receive for an AI investment. Distinguish investment oversight from legal advice. Research jurisdictional obligations from current official sources if relevant.

Use sector-specific workflow questions: professional-services evidence trails, retail/distribution planning, regulated-service approvals, or industrial exception handling. These are editorial lenses, not a claim of client delivery in every sector. Prefer a narrow source-grounded article over a broad industry roundup.

### Books

Proposed first reviews remain *Thinking in Systems* on recurring backlogs, *Working in Public* on maintenance responsibility, and *Scaling People* on decision ownership. Obtain the lawful reading basis and Mihai's approval first. The shelf and four US referral links work already; do not register Amazon again. Tax/payment completion remains private and unverified. Follow `docs/books-operations.md`.
