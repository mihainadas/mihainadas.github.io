"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const vm = require("node:vm");
const fs = require("node:fs");
const source = fs.readFileSync("assets/theme.js", "utf8");

function setup(saved = null, blocked = false) {
  const events = {}, attrs = {};
  let stored = saved, focused = null;
  function element(id) {
    return { id, hidden: true, textContent: id, attrs: {},
      setAttribute(k, v) { this.attrs[k] = v; },
      addEventListener(k, fn) { events[id + ":" + k] = fn; },
      contains(target) { return target === this || (id === "panel" && radios.includes(target)); },
      focus() { focused = this; }
    };
  }
  const radios = ["system", "light", "dark"].map(value => Object.assign(element(value), {
    value, checked: false, matches: () => true,
    closest: () => ({ querySelector: () => ({ textContent: value }) })
  }));
  const selector = element("selector"), trigger = element("trigger"), panel = element("panel"), color = element("color");
  selector.querySelectorAll = () => radios;
  selector.querySelector = query => query === "legend" ? { textContent: "Appearance" } : radios.find(r => r.checked);
  const system = { matches: false, addEventListener: (k, fn) => { events["system:" + k] = fn; } };
  const root = { setAttribute: (k, v) => { attrs[k] = v; }, removeAttribute: k => { delete attrs[k]; } };
  const document = { documentElement: root,
    getElementById: id => ({ "theme-preference": selector, "theme-trigger": trigger, "theme-panel": panel, "theme-color": color })[id],
    addEventListener: (k, fn) => { events["document:" + k] = fn; }
  };
  const window = { matchMedia: () => system,
    localStorage: { getItem() { if (blocked) { throw Error(); } return stored; },
      setItem(k, v) { if (blocked) { throw Error(); } stored = v; }, removeItem() { if (blocked) { throw Error(); } stored = null; } },
    addEventListener: (k, fn) => { events["window:" + k] = fn; }
  };
  vm.runInNewContext(source, { document, window });
  return { events, attrs, radios, trigger, panel, color, system,
    choose: value => events["selector:change"]({ target: radios.find(r => r.value === value) }),
    stored: () => stored, focused: () => focused, setStored: v => { stored = v; } };
}

test("saved explicit mode, native checked radio and accessible trigger agree", () => {
  const ui = setup("dark");
  assert.equal(ui.attrs["data-theme"], "dark");
  assert.equal(ui.radios[2].checked, true);
  assert.equal(ui.trigger.attrs["aria-label"], "Appearance: dark");
});
test("all modes persist correctly and system follows device changes", () => {
  const ui = setup();
  for (const mode of ["light", "dark"]) {
    ui.choose(mode);
    assert.equal(ui.attrs["data-theme"], mode);
    assert.equal(ui.stored(), mode);
  }
  ui.choose("system");
  assert.equal(ui.attrs["data-theme"], undefined);
  assert.equal(ui.stored(), null);
  ui.system.matches = true;
  ui.events["system:change"]();
  assert.equal(ui.color.attrs.content, "#0b0f10");
});
test("storage denial does not stop theme selection", () => {
  const ui = setup(null, true);
  ui.choose("dark");
  assert.equal(ui.attrs["data-theme"], "dark");
});
test("open focuses selected radio; Escape closes and restores focus", () => {
  const ui = setup();
  ui.events["trigger:click"]();
  assert.equal(ui.panel.hidden, false);
  assert.equal(ui.focused(), ui.radios[0]);
  ui.events["document:keydown"]({ key: "Escape" });
  assert.equal(ui.panel.hidden, true);
  assert.equal(ui.focused(), ui.trigger);
});
test("outside click and focus departure dismiss without stealing focus", () => {
  const ui = setup();
  for (const event of ["pointerdown", "focusin"]) {
    ui.events["trigger:click"]();
    ui.events["document:" + event]({ target: {} });
    assert.equal(ui.panel.hidden, true);
    assert.equal(ui.trigger.attrs["aria-expanded"], "false");
    assert.notEqual(ui.focused(), ui.trigger);
  }
});
test("cross-tab changes and clearing storage update the current page", () => {
  const ui = setup();
  ui.setStored("dark");
  ui.events["window:storage"]({ key: "mihainadas-theme" });
  assert.equal(ui.attrs["data-theme"], "dark");
  ui.setStored(null);
  ui.events["window:storage"]({ key: null });
  assert.equal(ui.attrs["data-theme"], undefined);
});
