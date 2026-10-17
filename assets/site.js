(function () {
  "use strict";

  var menu = document.querySelector(".navigation");
  if (menu) {
    var mobileMenu = window.matchMedia("(max-width: 640px)");
    function setMenuMode() { menu.open = !mobileMenu.matches; }
    setMenuMode();
    mobileMenu.addEventListener("change", setMenuMode);
    menu.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && mobileMenu.matches && menu.open) {
        menu.open = false;
        menu.querySelector("summary").focus();
      }
    });
    menu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () { if (mobileMenu.matches) { menu.open = false; } });
    });
  }

  function normalize(value) {
    return value.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  }

  document.querySelectorAll("[data-filter-list]").forEach(function (list) {
    var controls = list.querySelector(".filter-controls");
    var query = controls.querySelector("[data-query]");
    var category = controls.querySelector("[data-category]");
    var status = controls.querySelector("[data-status]");
    var items = Array.from(list.querySelectorAll("[data-filter-item]")).map(function (element) {
      return { element: element, text: normalize(element.textContent + " " + (element.dataset.search || "")), category: element.dataset.category };
    });
    var params = new URLSearchParams(window.location.search);
    query.value = params.get("q") || "";
    var initialCategory = params.get("type") || "";
    if (Array.from(category.options).some(function (option) { return option.value === initialCategory; })) {
      category.value = initialCategory;
    }

    function filter(updateUrl) {
      var words = normalize(query.value.trim()).split(/\s+/).filter(Boolean);
      var count = 0;
      items.forEach(function (item) {
        var visible = (!category.value || category.value === item.category) && words.every(function (word) { return item.text.includes(word); });
        item.element.hidden = !visible;
        if (visible) { count += 1; }
      });
      list.querySelectorAll("[data-filter-group]").forEach(function (group) {
        group.hidden = !Array.from(group.querySelectorAll("[data-filter-item]")).some(function (item) { return !item.hidden; });
      });
      status.textContent = count ? count + " of " + items.length + " entries" : "No matches. Try fewer words or clear the filters.";
      if (updateUrl) {
        var url = new URL(window.location.href);
        if (query.value.trim()) { url.searchParams.set("q", query.value.trim()); } else { url.searchParams.delete("q"); }
        if (category.value) { url.searchParams.set("type", category.value); } else { url.searchParams.delete("type"); }
        window.history.replaceState(null, "", url);
      }
    }
    controls.hidden = false;
    filter(false);
    query.addEventListener("input", function () { filter(true); });
    category.addEventListener("change", function () { filter(true); });
    controls.querySelector("[data-reset]").addEventListener("click", function () {
      query.value = "";
      category.value = "";
      filter(true);
      query.focus();
    });
    document.querySelectorAll(".theme-jumps a").forEach(function (link) {
      link.addEventListener("click", function () {
        query.value = "";
        category.value = "";
        filter(true);
      });
    });
  });

  var article = document.querySelector(".post-content");
  if (article) {
    var headings = Array.from(article.querySelectorAll("h2[id]"));
    if (headings.length >= 4) {
      var contents = document.createElement("details");
      contents.className = "article-contents";
      var summary = document.createElement("summary");
      summary.textContent = document.documentElement.lang === "ro" ? "În acest articol" : "On this page";
      contents.appendChild(summary);
      var links = document.createElement("ul");
      headings.forEach(function (heading) {
        var item = document.createElement("li");
        var link = document.createElement("a");
        link.href = "#" + heading.id;
        link.textContent = heading.textContent;
        item.appendChild(link);
        links.appendChild(item);
      });
      contents.appendChild(links);
      article.before(contents);
    }
  }
}());
