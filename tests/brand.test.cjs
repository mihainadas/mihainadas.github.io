"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const vm = require("node:vm");
const fs = require("node:fs");

async function setup(faces, rejected = false, supported = true) {
  const classes = [], requests = [];
  const document = {
    documentElement: { classList: { add(value) { classes.push(value); } } },
    querySelector() { return null; }, querySelectorAll() { return []; }
  };
  if (supported) {
    document.fonts = { load(font, text) {
      requests.push({ font, text });
      return rejected ? Promise.reject(Error("Font unavailable")) : Promise.resolve(faces);
    } };
  }
  vm.runInNewContext(fs.readFileSync("assets/site.js", "utf8"), { document });
  await Promise.resolve();
  await Promise.resolve();
  return { classes, requests };
}

test("accent paint activates only after the actual wordmark font loads", async () => {
  const ui = await setup([{ status: "loaded" }]);
  assert.deepEqual(ui.classes, ["brand-font-ready"]);
  assert.deepEqual(ui.requests, [{ font: "550 1em Newsreader", text: "Mihai Nadăș" }]);
});
test("fallback, unloaded and rejected fonts retain ordinary full-ink letters", async () => {
  for (const [faces, rejected] of [[[], false], [[{ status: "unloaded" }], false], [[], true]]) {
    assert.deepEqual((await setup(faces, rejected)).classes, []);
  }
});
test("an unavailable font-loading API never prevents readable navigation", async () => {
  assert.deepEqual((await setup([], false, false)).classes, []);
});
