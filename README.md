# Legacy website redirect

Redirects known mihainadas.github.io website pages to their explicit https://nadas.ro destinations. JavaScript preserves query strings and fragments; immediate meta refresh and ordinary links also work without JavaScript. Unknown deep links retain the original custom 404 fallback.

GitHub Pages publishes the main branch root. Do not add a CNAME: nadas.ro is served by klusai/nadas-pages-site.

## Explicit HTML routes

`redirect-map.json` is the reviewed map of 81 current HTML pages and eight historical aliases. Generate their small redirect pages with `python3 scripts/build_redirects.py`; validate with `python3 scripts/build_redirects.py --check`, `python3 -m unittest discover -s tests` and `node --test tests/*.test.cjs` before pushing.

Known routes return HTTP 200 with an immediate meta refresh in the head, the matching destination canonical, an ordinary link, and a JavaScript enhancement preserving query strings and fragments. The refresh works without JavaScript. Google documents zero-second meta refresh as a permanent redirect signal when server-side redirection is unavailable: https://developers.google.com/search/docs/crawling-indexing/301-redirects . These are not HTTP 301/308 responses: GitHub Pages does not expose custom server redirect rules on this hostname.

The existing custom 404 remains a JavaScript convenience for unknown paths, not the SEO mechanism for known routes. No redirects take over `/notebooks/`, which belongs to a separate project. XML feeds and PDF/binary URLs are outside this HTML redirect mechanism. Do not duplicate private website source, change the primary domain binding, or add a CNAME.
