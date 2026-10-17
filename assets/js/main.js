/**
 * MyPhatshala: home page
 * Reads window.MP_CATALOG (data/catalog.js, built by tools/build-manifest.js)
 * and draws: track filter, course grid per track, career paths, site search.
 */
(function () {
  const C = window.MP_CATALOG;
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const $ = id => document.getElementById(id);

  if (!C || !C.tracks) {
    $("tracks-list").innerHTML = `<p class="empty">Course list not built yet. Double-click <code>build.bat</code> (or run <code>node tools/build-manifest.js</code>).</p>`;
    return;
  }

  // ---------------- stats
  document.querySelectorAll("[data-stat]").forEach(el => { el.textContent = (C.totals[el.dataset.stat] ?? 0).toLocaleString("en-IN"); });

  // ---------------- icons
  const ICONS = {
    code: '<path d="M9 8l-5 4 5 4M15 8l5 4-5 4M13.5 5l-3 14"/>',
    globe: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    cpu: '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    db: '<ellipse cx="12" cy="5.5" rx="7.5" ry="3"/><path d="M4.5 5.5v13c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3v-13M4.5 12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3"/>',
    chart: '<path d="M4 20V4M4 20h16"/><path d="M8 16v-4M12 16V8M16 16v-6M20 16V6"/>',
    cluster: '<circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="18" r="2.5"/><circle cx="19" cy="18" r="2.5"/><circle cx="12" cy="13" r="2.5"/><path d="M12 7.5v3M10 14.5l-3 2M14 14.5l3 2"/>',
    brain: '<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 6 1V5a2 2 0 0 0-3-1zM15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-6 1"/>',
    cloud: '<path d="M7 18h10a4.5 4.5 0 0 0 .5-9A6 6 0 0 0 6 10.5 4 4 0 0 0 7 18z"/>',
    infinity: '<path d="M6.5 8.5c-2 0-3.5 1.6-3.5 3.5s1.5 3.5 3.5 3.5c3.5 0 7.5-7 11-7 2 0 3.5 1.6 3.5 3.5s-1.5 3.5-3.5 3.5c-3.5 0-7.5-7-11-7z"/>',
    shield: '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
  };
  const icon = name => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[name] || ICONS.code}</svg>`;

  // ---------------- track filter chips
  const chips = $("track-chips");
  chips.innerHTML = `<button class="chip is-active" data-track="all">All tracks <span>${C.totals.courses}</span></button>` +
    C.tracks.map(t => `<button class="chip" data-track="${esc(t.id)}" style="--c:${esc(t.color)}">${icon(t.icon)}${esc(t.title)} <span>${t.courses.length}</span></button>`).join("");

  // ---------------- tracks + course grid
  $("tracks-list").innerHTML = C.tracks.map(t => {
    const lessons = t.courses.reduce((a, c) => a + c.stats.lessons, 0);
    return `
    <section class="track" id="track-${esc(t.id)}" data-track="${esc(t.id)}" style="--c:${esc(t.color)}">
      <header class="track__head">
        <div class="track__icon">${icon(t.icon)}</div>
        <div>
          <h3>${esc(t.title)}</h3>
          <p>${esc(t.description)}</p>
        </div>
        <span class="track__count">${t.courses.length} courses · ${lessons} lessons</span>
      </header>
      <div class="course-grid">
        ${t.courses.map(c => {
          const pct = c.stats.lessons ? Math.round(c.stats.live / c.stats.lessons * 100) : 0;
          return `
          <a class="ccard" href="${esc(c.url)}">
            <h4>${esc(c.title)}</h4>
            <p>${esc(c.tagline)}</p>
            <div class="ccard__meta"><span>${esc(c.level)}</span><span>${c.stats.modules} modules</span><span>${c.stats.lessons} lessons</span></div>
            <div class="progress" aria-hidden="true"><span style="width:${Math.max(pct, 2)}%"></span></div>
            <small>${c.stats.live ? `${c.stats.live} lesson${c.stats.live > 1 ? "s" : ""} live` : "Syllabus ready · lessons coming"}</small>
          </a>`;
        }).join("")}
      </div>
    </section>`;
  }).join("");

  chips.addEventListener("click", e => {
    const b = e.target.closest(".chip");
    if (!b) return;
    chips.querySelectorAll(".chip").forEach(x => x.classList.toggle("is-active", x === b));
    const id = b.dataset.track;
    document.querySelectorAll(".track").forEach(s => { s.hidden = id !== "all" && s.dataset.track !== id; });
  });

  // ---------------- career paths
  $("paths-list").innerHTML = C.paths.map(p => `
    <article class="path reveal">
      <header><h3>${esc(p.title)}</h3><span>${esc(p.months)} months · ${p.courses.length} courses</span></header>
      <ol>${p.courses.map(c => `<li><a href="${esc(c.url)}">${esc(c.title)}</a></li>`).join("")}</ol>
    </article>`).join("");

  // ---------------- site-wide search (index loaded only when needed)
  const input = $("site-search"), box = $("search-results");
  let index = null, loading = null;
  function loadIndex() {
    if (index) return Promise.resolve(index);
    if (loading) return loading;
    loading = new Promise(res => {
      const s = document.createElement("script");
      s.src = "data/search-index.js";
      s.onload = () => { index = window.MP_SEARCH || []; res(index); };
      s.onerror = () => { index = []; res(index); };
      document.head.appendChild(s);
    });
    return loading;
  }
  input.addEventListener("focus", loadIndex, { once: true });

  const hl = (text, q) => {
    const i = text.toLowerCase().indexOf(q);
    return i < 0 ? esc(text) : esc(text.slice(0, i)) + "<mark>" + esc(text.slice(i, i + q.length)) + "</mark>" + esc(text.slice(i + q.length));
  };
  let timer;
  input.addEventListener("input", () => {
    clearTimeout(timer);
    timer = setTimeout(async () => {
      const q = input.value.trim().toLowerCase();
      if (q.length < 2) { box.hidden = true; return; }
      const data = await loadIndex();
      const words = q.split(/\s+/);
      const hits = data.filter(r => { const hay = (r[0] + " " + r[1]).toLowerCase(); return words.every(w => hay.includes(w)); })
        .sort((a, b) => (b[3] === "course") - (a[3] === "course") || (b[3] === "live") - (a[3] === "live"))
        .slice(0, 40);
      box.hidden = false;
      box.innerHTML = hits.length
        ? `<p class="sr-count">${hits.length === 40 ? "Top 40" : hits.length} result${hits.length === 1 ? "" : "s"}</p>` + hits.map(r => `
          <a class="sr" href="${esc(r[2])}">
            <span class="sr__title">${hl(r[0], words[0])}</span>
            <span class="sr__course">${r[3] === "course" ? "Course · " + esc(r[1]) : esc(r[1])}</span>
            <span class="badge ${r[3] === "live" ? "badge--live" : ""}">${r[3] === "course" ? "Course" : r[3] === "live" ? "Live" : "Soon"}</span>
          </a>`).join("")
        : `<p class="sr-empty">No lessons match “${esc(input.value.trim())}” yet.</p>`;
    }, 120);
  });
  document.addEventListener("click", e => { if (!e.target.closest(".site-search")) box.hidden = true; });
  input.addEventListener("keydown", e => { if (e.key === "Escape") { box.hidden = true; input.blur(); } });
})();

// ---------------- hero: rotating topic + counting stats
(function () {
  const rot = document.getElementById("hero-rot");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (rot && !reduce) {
    const words = ["Java", "SQL", "Python", "HashMap", "Spark", "Docker", "Pandas", "Kafka", "React", "Git"];
    let i = 0;
    setInterval(() => {
      i = (i + 1) % words.length;
      rot.classList.remove("is-swap"); void rot.offsetWidth;
      rot.textContent = words[i]; rot.classList.add("is-swap");
    }, 2200);
  }
  if (!reduce && "IntersectionObserver" in window) {
    document.querySelectorAll(".hero-stats [data-stat]").forEach(el => {
      const target = parseInt(el.textContent.replace(/\D/g, ""), 10);
      if (!target) return;
      const t0 = performance.now(), dur = 1200;
      el.textContent = "0";
      const tick = now => {
        const p = Math.min(1, (now - t0) / dur), v = Math.round(target * (1 - Math.pow(1 - p, 3)));
        el.textContent = v.toLocaleString("en-IN");
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  }
})();
