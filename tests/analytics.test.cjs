"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const vm = require("node:vm");
const fs = require("node:fs");
const template = fs.readFileSync("_includes/analytics.html", "utf8");
const source = template.match(/<script id="analytics-bootstrap">([\s\S]*?)<\/script>/)[1];

function setup(hostname = "nadas.ro", protocol = "https:", navigator = {}) {
  const scripts = [];
  const window = {location: {hostname, protocol, origin: protocol + "//" + hostname, pathname: "/archive/"}, navigator};
  const document = {
    getElementById: id => scripts.find(script => script.id === id),
    createElement: tag => { assert.equal(tag, "script"); return {}; },
    head: {appendChild: script => scripts.push(script)}
  };
  const run = () => vm.runInNewContext(source, {window, document, URL});
  run();
  return {scripts, window, run};
}

test("build gate requires production and the exact canonical origin", () => {
  assert.match(template, /jekyll.environment == 'production' and site.url == 'https:\/\/nadas.ro'/);
  assert.match(fs.readFileSync("_includes/head.html", "utf8"), /include analytics.html/);
});
test("HTTPS production loads the registered asynchronous script once", () => {
  const page = setup();
  assert.equal(page.scripts.length, 1);
  assert.equal(page.scripts[0].src, "https://plausible.io/js/pa-gSE5BAIvwmxkbBbrt7gz3.js");
  assert.equal(page.scripts[0].async, true);
  page.run();
  assert.equal(page.scripts.length, 1);
});
test("enhanced measurements are explicitly disabled before loading", () => {
  const {window} = setup();
  assert.deepEqual(JSON.parse(JSON.stringify(window.plausible.o)), {
    outboundLinks: false, fileDownloads: false, formSubmissions: false
  });
});
test("local, alternate, subdomain and deceptive hosts never load analytics", () => {
  for (const host of ["localhost", "127.0.0.1", "::1", "mihainadas.github.io", "www.nadas.ro", "preview.nadas.ro", "nadas.ro.example.org"]) {
    const page = setup(host);
    assert.equal(page.scripts.length, 0, host);
    assert.equal(page.window.plausible, undefined, host);
  }
});
test("HTTP and local file previews do not load analytics", () => {
  for (const protocol of ["http:", "file:"]) assert.equal(setup("nadas.ro", protocol).scripts.length, 0);
});
test("search queries, campaign tags, fragments and referrer paths are redacted before transmission", () => {
  const {window} = setup();
  const transform = window.plausible.o.transformRequest;
  const payload = transform({n: "pageview", u: "https://nadas.ro/archive/?q=private&utm_source=mail#fragment", r: "https://example.org/private?q=secret"});
  assert.equal(payload.u, "https://nadas.ro/archive/");
  assert.equal(payload.r, "https://example.org");
  assert.equal(transform({r: "not a URL"}).r, null);
  assert.equal(transform({r: null}).r, null);
});
test("Do Not Track and Global Privacy Control prevent all tracker loading", () => {
  for (const navigator of [{doNotTrack: "1"}, {globalPrivacyControl: true}]) {
    const page = setup("nadas.ro", "https:", navigator);
    assert.equal(page.scripts.length, 0);
    assert.equal(page.window.plausible, undefined);
  }
});
