# Books: editorial and referral workflow

Reviewed 17 October 2026. This file is excluded from the public site. Never add addresses, tax identifiers, bank details, passwords, account tokens, or completed tax forms to this repository.

## Editorial scope

The audience is international English-speaking engineers, AI practitioners, and technology leaders, with Romanian buying options. Start with a decision rather than a bestseller list. Gates Notes is a reference for idea-led essays and personal judgment, not a voice to impersonate or a claim that Mihai shares Bill Gates's opinions.

The initial five selections connect recurring operating problems to systems, management, open-source maintenance, and applied machine learning. The two machine-learning titles preserve the previous shelf; the three additions broaden its range. The public descriptions are explicitly source-based selections. No full review has been published in this change.

`_data/books.json` holds edition-specific metadata, ISBNs, source links, verified Open Library cover IDs, and retailer links. Do not use popularity, star ratings, or commission rate as the selection criterion. A new title must have a specific reader, question, limitation, and verified edition. Check whether a newer edition changes the recommendation.

The cover API expressly supports public embedding: https://openlibrary.org/dev/docs/api/covers. Embed by verified cover ID, retain the whole image with `object-fit: contain`, credit the service, and retain the fallback. Do not describe the artwork as public domain or reuse it outside this identification context. Do not scrape Amazon covers into permanent assets. Recheck correspondence against the stated ISBN when changing an edition.

## A full review

Obtain a lawful full text, or Mihai's substantive reading notes and access to the passages being discussed. Publisher copy, an extract, and another review do not constitute a full-book reading basis. Do not invent a personal anecdote, reading completion, endorsement, quotation, or result.

A promising first review is *Thinking in Systems*: why the same backlog keeps returning after a local fix. Before writing, examine the full treatment of stocks, flows, delays, and feedback. Any software-service example we construct must be labeled illustrative, not reported as an experiment or an example from the book. Follow with *Working in Public* on maintenance responsibility, then *Scaling People* on decision ownership.

For each review, establish the subject and practical question in two substantive opening paragraphs (at least 60 words). Explain the author's argument; closely examine one passage or example; distinguish the book's evidence from our proposed application; identify who should skip it. Finish when the point is complete. Avoid a chapter-by-chapter recap, generic praise, or invented numerical ratings. Have Mihai approve the actual judgment and every attributed personal experience.

Publish through `_posts`, with the normal title, date, description, `context_reviewed`, and `editorial_reviewed` fields. Also set `post_type: book review`, a known `book_id`, `reading_basis` (`Full book` or `Full book and author's reading notes`), `author_reviewed` (the actual approval date), and `material_relationship` (a truthful statement about review copies, sponsorship, or other relationships). The shared post layout supplies the edition, cover, links, and disclosure. The books hub lists these posts automatically, and they enter the ordinary feed and archive. Do not evade the three-original-posts-per-Bucharest-week publishing limit by putting a new review in a Page.

The date markers record real judgment. They are not a machine certification that someone read the book. The source check deliberately rejects publisher-summary reviews and missing author approval; normal opening, math, prose, build, and link checks still apply.

## Recommended referral sequence

1. Start with Amazon US as the provisional English-language channel. This is an audience-fit hypothesis, not evidence that US readers dominate; revisit with actual reader feedback. Enroll as an individual using Mihai's confirmed Romanian residence, subject to Amazon's acceptance. Do not invent an address in another country.
2. After US enrollment, inspect the current OneLink international options inside Associates Central. Add Germany only through an actually assigned, valid program/tracking identity, not by copying a US tag to a German URL. Do not assume every storefront or international purchase earns a commission.
3. For Romanian readers, evaluate the live Cărturești and Libris programs in 2Performant/BusinessLeague. Their directory lists both: https://2performant.com/affiliate-programs/. Merchant acceptance and current terms are separate checks. Do not cite old advertised rates as current.
4. Defer Geniuslink. It can route links but does not remove the need to meet the affiliate programs' requirements. Its own guide recommends choosing country programs based on audience: https://intercom.geni.us/en/articles/1065261-amazon-associates-program-guide. No paid account or subscription is authorized by this implementation.

## Amazon application companion

Official entry: https://affiliate-program.amazon.com/. Sign in and proceed to the Associates application, not an Amazon seller account or a paid advertising product.

Mihai must verify the payee address and contact, choose the actual legal/tax status, complete the tax interview and bank details inside Amazon, review the agreements, and authorize any final application submission. Do not submit on his behalf without action-time confirmation. Never infer the correct tax form or Romanian reporting obligations from the site's language or bank country; use Amazon's interview and qualified local advice where needed.

Website: `https://mihainadas.github.io/`

Suggested profile wording, to adapt to the actual question and character limit:

> I publish original engineering and AI research notes for software practitioners and technology leaders. The site covers small language models, evaluation, reproducible experiments, PC emulation, and research applications to business decisions. Its Books section curates relevant technical and management books and will publish independent, evidence-based reviews. Book links help readers find the stated edition at a retailer.

Describe it as a content/blog site if the form offers that category. Do not claim newsletter reach, traffic figures, social distribution, reviews already published, or paid acquisition that does not exist. A proposed store ID such as `mihainadas` is only a request; use the identity Amazon actually assigns, including its market suffix. Answer discovery questions truthfully. Do not answer child-directed-content or policy attestations automatically.

Amazon's application review FAQ requires three qualifying sales in the first 180 days, and excludes personal orders: https://affiliate-program.amazon.com/help/node/topic/G8TW5AE9XL2VX9VM. Do not manufacture qualifying purchases, buy through personal links, or make approval promises. Romania appears in its international bank-transfer support list, which is not an eligibility guarantee: https://affiliate-program.amazon.com/help/node/topic/G8VUMS6GTBCR9RGV.

## Activate only after enrollment

Record the assigned public tracking ID in `_data/book_programs.json` and set only that program's `active` flag. Enrollment is not the same as final application approval; describe the actual status accurately. Generate each final edition-specific Special Link through Amazon's current tools, or its documented simple-text-link format (https://affiliate-program.amazon.com/help/node/topic/GP38PJ6EUR6PFBEC), then copy the full HTTPS URL into the matching `affiliate_url`. Verify the selected product ASIN and displayed ISBN against the exact edition; record `asin`, `product_url`, and the actual `product_checked` date. Do not derive an ASIN solely from an ISBN, or invent prices, ratings, commission rates, or stock. Do not put account credentials in these public data files.

The initial US activation uses four verified edition-specific product destinations. The Amazon product page for the transformer book's candidate ASIN displayed ISBN-13 9789355420329 instead of the selected 9781098103248 on 17 October 2026. That book therefore retains an ordinary ISBN search and no affiliate URL. Do not bypass the mismatch by copying an affiliate tag onto the unverified candidate or silently changing the book's edition. Germany and Romanian retailer programs remain inactive until separately enrolled and verified.

Inactive programs cannot have affiliate URLs. Ordinary links cannot contain referral tags. Active Amazon links must match both the storefront and the assigned tracking ID. The includes add `rel="sponsored nofollow"`, a visible `(paid link)` label, a nearby commission disclosure, and Amazon's required statement only when Amazon links actually appear. Required wording: https://affiliate-program.amazon.com/help/node/topic/GHQNZAU6669EZS98. Current operating policies: https://affiliate-program.amazon.com/help/operating/policies.

Retain independent source and ordinary retailer alternatives. Check the disclosure in the actual rendered page and feed, not just source data. Verify link destination, edition, language, and market after activation. A retailer's destination may set cookies or process purchase data; the blog does not add automatic redirects, affiliate JavaScript, a click tracker, or a paid link aggregator.

## Verification

Run source checks, strict production Jekyll build, generated-site checks, the full unit suite, JavaScript syntax checking, and HTMLProofer. Inspect desktop, mobile, dark mode, keyboard navigation, source/edition disclosures, and unavailable-cover behavior. Verify ordinary and active affiliate rendering with fixtures before accepting a change. Confirm the deployed URL before calling it live.
