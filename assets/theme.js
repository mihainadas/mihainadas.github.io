(function () {
  "use strict";

  var storageKey = "mihainadas-theme";
  var root = document.documentElement;
  var selector = document.getElementById("theme-preference");
  var themeColor = document.getElementById("theme-color");
  var systemTheme = window.matchMedia("(prefers-color-scheme: dark)");

  if (!selector) {
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
    selector.value = preference;
    updateThemeColor(preference);
  }

  var preference = readPreference();
  applyPreference(preference);

  selector.addEventListener("change", function () {
    preference = selector.value;
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
