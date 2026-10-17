/** MyPhatshala: course page (syllabus search + expand/collapse) */
(function () {
  const searchEl = document.getElementById("lesson-search");
  const countEl = document.getElementById("search-count");
  const expandBtn = document.getElementById("expand-all");
  if (!searchEl) return;

  searchEl.addEventListener("input", () => {
    const q = searchEl.value.trim().toLowerCase();
    let shown = 0;
    document.querySelectorAll(".module").forEach(mod => {
      let hits = 0;
      mod.querySelectorAll(".lesson").forEach(li => {
        const hit = !q || li.dataset.search.includes(q);
        li.hidden = !hit;
        if (hit) hits++;
      });
      mod.hidden = hits === 0;
      if (q) mod.open = hits > 0;
      shown += hits;
    });
    countEl.textContent = q ? `${shown} lesson${shown === 1 ? "" : "s"} match “${searchEl.value.trim()}”` : "";
  });

  expandBtn.addEventListener("click", () => {
    const open = expandBtn.dataset.state !== "open";
    document.querySelectorAll(".module").forEach(m => (m.open = open));
    expandBtn.dataset.state = open ? "open" : "closed";
    expandBtn.textContent = open ? "Collapse all" : "Expand all";
  });

  // Open the module named in the URL hash (links from site search use #m3 etc.)
  const target = location.hash && document.querySelector(location.hash);
  if (target && target.tagName === "DETAILS") { target.open = true; target.scrollIntoView({ block: "start" }); }
})();
