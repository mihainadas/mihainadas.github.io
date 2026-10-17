"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const vm = require("node:vm");
const fs = require("node:fs");

function setup(narrow) {
  const events = {}, queries = [];
  let focused = false;
  const summary = { focus() { focused = true; } };
  const link = { addEventListener(type, callback) { events["link:" + type] = callback; } };
  const menu = {
    open: true,
    addEventListener(type, callback) { events[type] = callback; },
    querySelector() { return summary; },
    querySelectorAll() { return [link]; }
  };
  const media = { matches: narrow, addEventListener(type, callback) { events["media:" + type] = callback; } };
  vm.runInNewContext(fs.readFileSync("assets/site.js", "utf8"), {
    document: { querySelector(selector) { return selector === ".navigation" ? menu : null; }, querySelectorAll() { return []; } },
    window: { matchMedia(query) { queries.push(query); return media; } }
  });
  return { menu, media, events, queries, focused: () => focused };
}

test("compact navigation starts closed at the shared 880px breakpoint", () => {
  const ui = setup(true);
  assert.deepEqual(ui.queries, ["(max-width: 880px)"]);
  assert.match(fs.readFileSync("assets/main.scss", "utf8"), /@media \(max-width: 880px\)/);
  assert.equal(ui.menu.open, false);
});
test("resizing between compact and full navigation resets native details", () => {
  const ui = setup(false);
  assert.equal(ui.menu.open, true);
  ui.media.matches = true;
  ui.events["media:change"]();
  assert.equal(ui.menu.open, false);
  ui.media.matches = false;
  ui.events["media:change"]();
  assert.equal(ui.menu.open, true);
});
test("Escape closes compact navigation and returns keyboard focus", () => {
  const ui = setup(true);
  ui.menu.open = true;
  ui.events.keydown({ key: "Escape" });
  assert.equal(ui.menu.open, false);
  assert.equal(ui.focused(), true);
});
test("following a compact link closes navigation without closing the desktop nav", () => {
  for (const narrow of [true, false]) {
    const ui = setup(narrow);
    ui.menu.open = true;
    ui.events["link:click"]();
    assert.equal(ui.menu.open, !narrow);
  }
});
