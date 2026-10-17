(function () {
  "use strict";

  var storageKey = "mihainadas-theme";
  var root = document.documentElement;
  var selector = document.getElementById("theme-preference");
  var trigger = document.getElementById("theme-trigger");
  var panel = document.getElementById("theme-panel");
  var themeColor = document.getElementById("theme-color");
  var systemTheme = window.matchMedia("(prefers-color-scheme: dark)");

  if (!selector || !trigger || !panel) {
    return;
  }

  function readPreference() {
    try {
      var saved = window.localStorage.getItem(storageKey);
      return saved === "light" || saved === "dark" ? saved : "system";
    } catch (error) {
      return "system";
    }
  }

  function updateThemeColor(preference) {
    if (!themeColor) {
      return;
    }
    var dark = preference === "dark" || (preference === "system" && systemTheme.matches);
    themeColor.setAttribute("content", dark ? "#0b0f10" : "#f7f4ec");
  }

  function applyPreference(preference) {
    if (preference === "light" || preference === "dark") {
      root.setAttribute("data-theme", preference);
    } else {
      root.removeAttribute("data-theme");
    }
    selector.querySelectorAll('input[name="theme"]').forEach(function (radio) {
      radio.checked = radio.value === preference;
      if (radio.checked) {
        trigger.setAttribute("aria-label", selector.querySelector("legend").textContent + ": " + radio.closest("label").querySelector("strong").textContent);
      }
    });
    trigger.setAttribute("data-mode", preference);
    updateThemeColor(preference);
  }

  var preference = readPreference();
  applyPreference(preference);

  selector.addEventListener("change", function (event) {
    if (!event.target.matches('input[name="theme"]')) { return; }
    preference = event.target.value;
    if (["system", "light", "dark"].indexOf(preference) < 0) { return; }
    try {
      if (preference === "system") {
        window.localStorage.removeItem(storageKey);
      } else {
        window.localStorage.setItem(storageKey, preference);
      }
    } catch (error) {
      // The selection still applies for this page when storage is unavailable.
    }
    applyPreference(preference);
  });

  function closePanel(restoreFocus) {
    panel.hidden = true;
    trigger.setAttribute("aria-expanded", "false");
    if (restoreFocus) { trigger.focus(); }
  }

  trigger.addEventListener("click", function () {
    var opening = panel.hidden;
    panel.hidden = !opening;
    trigger.setAttribute("aria-expanded", String(opening));
    if (opening) { selector.querySelector("input:checked").focus(); }
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && !panel.hidden) { closePanel(true); }
  });
  document.addEventListener("pointerdown", function (event) {
    if (!panel.hidden && !panel.contains(event.target) && !trigger.contains(event.target)) { closePanel(false); }
  });
  document.addEventListener("focusin", function (event) {
    if (!panel.hidden && !panel.contains(event.target) && !trigger.contains(event.target)) { closePanel(false); }
  });
  window.addEventListener("storage", function (event) {
    if (event.key === storageKey || event.key === null) {
      preference = readPreference();
      applyPreference(preference);
    }
  });

  function followSystemTheme() {
    if (preference === "system") {
      updateThemeColor(preference);
    }
  }

  if (typeof systemTheme.addEventListener === "function") {
    systemTheme.addEventListener("change", followSystemTheme);
  } else if (typeof systemTheme.addListener === "function") {
    systemTheme.addListener(followSystemTheme);
  }
}());
