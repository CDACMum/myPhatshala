/** MyPhatshala: shared behaviour for every page (watermark, theme toggle, scroll reveal) */
(function () {
  if ((window.MP_CONFIG || {}).watermark !== false) document.body.classList.add("has-watermark");

  /* Opened straight from disk (file://)? Folder links like "../" show a file listing there,
     so point them at the folder's index.html. On the live site nothing changes. */
  if (location.protocol === "file:") {
    const fix = a => {
      const h = a.getAttribute("href");
      if (!h || /^([a-z]+:|#|\/\/)/i.test(h)) return;
      const m = h.match(/^([^?#]*)(.*)$/), path = m[1];
      if (path.endsWith("/")) a.setAttribute("href", path + "index.html" + m[2]);
      else if (path === "." || path === "..") a.setAttribute("href", path + "/index.html" + m[2]);
    };
    const fixAll = () => document.querySelectorAll("a[href]").forEach(fix);
    fixAll();
    document.addEventListener("click", e => { const a = e.target.closest && e.target.closest("a[href]"); if (a) fix(a); }, true);
    new MutationObserver(fixAll).observe(document.body, { childList: true, subtree: true });
  }

  const btn = document.getElementById("theme-btn");
  if (btn) btn.addEventListener("click", () => {
    const root = document.documentElement;
    const dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    root.dataset.theme = dark ? "light" : "dark";
    try { localStorage.setItem("mp-theme", root.dataset.theme); } catch (e) {}
  });

  const els = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window)) { els.forEach(el => el.classList.add("in")); return; }
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
  }), { threshold: 0.12 });
  els.forEach(el => io.observe(el));
})();
