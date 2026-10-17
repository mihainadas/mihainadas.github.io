# nadas.ro cutover

Requested and activated by Mihai on 17 October 2026. The public configuration now uses `https://nadas.ro`, with the same GitHub repository and article paths. Domain ownership is verified, Pages is bound to the domain, and the four apex A records and `www` CNAME are saved. HTTPS provisioning and final new-host checks are still pending; do not describe the migration as fully verified until they pass.

## Confirmed starting state

Before activation, the clean checkout was fast-forwarded. Public DNS showed Namecheap FreeDNS nameservers, Google mail exchange records, and a Google SPF TXT record. The apex had no A/AAAA answer; `www` returned NXDOMAIN. No CAA or GitHub account-verification TXT answer was found. These describe the starting state, not the current web records.

GitHub uses legacy publishing from `main` at the repository root. The original site had no custom domain and enforced HTTPS on the default hostname. Signed-in Namecheap inspection confirmed control of the FreeDNS zone. The complete expanded host list contained the Google calendar/docs/mail aliases, SPF, DMARC, and Google DKIM record; its snapshot is retained in ignored local `vendor/` storage with the original Google MX values. All six original host records, five MX records, and nameservers matched that snapshot after the web records were added. Authentication and two-factor entry belong in the provider interface, not chat or repository files. Do not search unrelated secrets or password-manager vaults.

## Rehearsal and domain consistency

The generated-site checks read the expected HTTPS origin from Jekyll configuration rather than hard-coding the old hostname. They reject stale canonicals, sitemap URLs, robots sitemap declarations, feed links, multilingual alternates, and professional identity links. Ordinary outbound citations and project notebook links are not globally rewritten or banned. Atom feed and post identifiers deliberately retain `feed_identity_url` while discovery and article links move to the new origin, following [RFC 4287 section 4.2.6](https://www.rfc-editor.org/rfc/rfc4287#section-4.2.6). Do not change those stable identifiers or cause every existing item to appear as a new publication during the move.

Use an ignored URL-only override to rehearse the future deployment:

```yaml
url: "https://nadas.ro"
```

```sh
JEKYLL_ENV=production BUNDLE_PATH=vendor/bundle bundle exec jekyll build --strict_front_matter --config _config.yml,vendor/domain-migration.yml --destination vendor/domain-preview
python3 scripts/check_build.py --site-dir vendor/domain-preview --config vendor/domain-migration.yml
BUNDLE_PATH=vendor/bundle bundle exec htmlproofer vendor/domain-preview --disable-external --enforce-https
```

This is only a metadata and site-build rehearsal. It does not verify public DNS, a certificate, notebook redirects, or account registration. For a future migration, keep production configuration and DNS unchanged until coordinated cutover. The résumé and social-card generators derive their hostname from `_config.yml`; the résumé integrity gate rejects a stale public origin without treating unrelated configuration edits as career changes. Regenerate and visually inspect both assets after switching the origin. Normal production checks also require the source and generated `CNAME` to match the configured custom hostname, preventing an accidental loss of the Pages binding. A URL-only preview override does not modify that live binding.

## Cutover sequence

1. Authenticate to the Namecheap account that actually controls this zone. Inspect and preserve the complete current zone in an ignored local backup or provider export. Keep MX, SPF, DKIM, DMARC, other TXT records, nameservers, and DNSSEC unchanged. Verify ownership under the GitHub personal account with its generated DNS TXT challenge; keep that record afterward. Stop if the zone or domain belongs to a different account or an unexpected active site appears.
2. Finish and verify the repository migration before activation: production `url`, source CNAME for legacy publishing, URL-dependent checks, résumé renderer/footer/links and its build integrity record, social-card renderer and generated artwork, README and operating links. Use current skills and render/inspect the PDF and social image. Career facts and factual-review dates must not change just because the hostname changes. Inspect existing article links before deciding whether to replace them; never alter evidence URLs or translation signatures just to suppress a failure.
3. Stage the exact provider records and review their effects. With ownership verified and rollback ready, bind `nadas.ro` to this Pages repository before activating the GitHub web records, following GitHub's recommended order. Use the current documented A records for the apex and CNAME `www` directly to `mihainadas.github.io`; optionally add the documented AAAA records as well. Do not create a CNAME at the mail-bearing apex, wildcard records, a registrar transfer, or a paid hosting subscription. Do not change account access or submit provider UI changes without required action-time approval.
4. Publish only the migration files through the full existing release gate. Avoid a race with any CNAME commit generated by GitHub settings: inspect/fetch it before committing local work. Allow for DNS propagation and certificate issuance; do not promise an instantaneous or zero-downtime cutover. Enforce HTTPS once GitHub reports the custom-domain certificate ready.
5. Verify apex, `www`, the old homepage and deep article URLs, redirects without loops, certificate names, no mixed content, RSS and sitemap URLs, canonical/identity/hreflang metadata, social preview, PDF links, mobile layout, and mathematics. GitHub user-site domains also affect project sites, so test all three rendered notebooks explicitly. Keep `/lab-notebooks/` as the collection and do not replace it with the colliding `/notebooks/` route.
6. Update the existing affiliate website list and any actual podcast/discovery profiles only with the required authorization. No new affiliate enrollment or show registration is needed solely for a hostname change. Update scheduler guidance and record the actual deployed state, revision, checks, and unresolved items. The checkout path, schedule, model, publication cap, and clean-tree gate remain unchanged.

## Rollback

Keep the old configuration and exact DNS snapshot available. If the new host cannot serve the site securely, restore the previous Pages binding/configuration and the original web records without touching mail or unrelated records. Rebuild, verify the old public URLs, and report the actual state. Do not leave unbound DNS pointing at Pages or silently advertise a failed domain as canonical.

Primary references: [GitHub custom-domain setup and current DNS targets](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site), [domain verification](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages), [project-site inheritance](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages), and [Namecheap DNS-provider identification](https://www.namecheap.com/support/knowledgebase/article.aspx/10837/93/how-to-find-your-domains-dns-provider/).
