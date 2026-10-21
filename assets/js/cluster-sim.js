/**
 * MyPhatshala: Cluster Playground (a teaching simulator of a small Hadoop cluster)
 * ------------------------------------------------------------------------------
 * Markup:  <div class="csim"><script type="application/json">{ …config… }</script></div>
 * Config (all optional):
 *   racks: 2, nodes: 3 (per rack), replication: 3, blockMB: 128, slots: 2 (containers per node)
 *   features: ["upload","fail","job","locality","scale","ha","chaos","fsck"]
 *   preload:  [{ "name":"upi_txns.csv", "sizeMB":1024 }]
 *   title, intro (html), try: [{ "text":"…", "on":"node-stop" }]   (a "try this" checklist)
 *   sizes: [3,6,9]  (cluster sizes offered by the "scale" feature)
 * Events used by tasks: upload-done, node-stop, node-start, node-dead, rereplicated, block-missing,
 *   job-done, job-failed, job-done-nolocal, nn-stop, nn-failover, resize, fsck
 * Real Hadoop defaults are modelled: 128 MB blocks, replication 3, the default rack-aware
 * placement policy, heartbeats every 3 s, a DataNode declared dead after 10 min 30 s,
 * real-looking block IDs (blk_1073741825 …). Times of transfers and tasks are simplified.
 */
(function () {
  "use strict";
  const NS = "http://www.w3.org/2000/svg";
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const COLORS = ["#E8772E", "#2E5AAC", "#2F7D5B", "#8B5CF6"];
  const HB = 3, DEAD_AFTER = 630;               // seconds: heartbeat interval, dead-node timeout (2 × 5 min + 10 × 3 s)
  const fmtT = s => { s = Math.floor(s); const h = Math.floor(s / 3600), m = Math.floor(s / 60) % 60, x = s % 60; return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(x).padStart(2, "0")}`; };
  const fmtMB = mb => mb >= 1024 ? (mb / 1024).toFixed(mb % 1024 ? 1 : 0) + " GB" : Math.round(mb) + " MB";
  const ago = s => s < 60 ? Math.floor(s) + "s" : Math.floor(s / 60) + "m " + Math.floor(s % 60) + "s";
  const pick = (arr, rnd) => arr[Math.floor(rnd() * arr.length)];
  // like HDFS, prefer nodes that are less full: choose randomly among the emptier half
  const pickRoomy = (arr, rnd) => { const s = arr.slice().sort((a, b) => a.blocks.size - b.blocks.size); return pick(s.slice(0, Math.max(1, Math.ceil(s.length / 2))), rnd); };
  function rng(seed) { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
  const el = (tag, attrs = {}, parent) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };

  function Sim(root, cfg) {
    const F = new Set(cfg.features || ["upload", "fail", "job"]);
    const S = this;
    let rnd = rng(cfg.seed || 7);
    let racks, nodes, files, blocks, nextBlk, now, speed, queue, packets, job, logLines, history, nn, fastTo, lastFrame;
    const repl0 = cfg.replication || 3, slots = cfg.slots || 2;
    let replication = repl0, blockMB = cfg.blockMB || 128, locality = true;
    let nodesPerRack = cfg.nodes || 3, rackCount = cfg.racks || 2;
    const doneTasks = new Set();

    /* ---------------- DOM ---------------- */
    root.classList.add("is-js");
    const sizes = cfg.sizes || [3, 6, 9];
    root.insertAdjacentHTML("beforeend", `
      ${cfg.title ? `<div class="csim__title"><b>${esc(cfg.title)}</b><span>Cluster Playground</span></div>` : ""}
      ${cfg.intro ? `<div class="csim__intro">${cfg.intro}</div>` : ""}
      ${cfg.try ? `<ol class="csim__tasks">${cfg.try.map((t, i) => `<li data-i="${i}">${t.text}</li>`).join("")}</ol>` : ""}
      <div class="csim__bar">
        ${F.has("upload") ? `<div class="csim__grp"><label>File <select data-k="fsize"><option value="300">300 MB</option><option value="1024" selected>1 GB</option><option value="2048">2 GB</option></select></label>
          <label>Block <select data-k="bsize"><option>64</option><option selected>128</option><option>256</option></select> MB</label>
          <label>Replication <select data-k="repl">${[1, 2, 3].map(v => `<option${v === Math.min(3, repl0) ? " selected" : ""}>${v}</option>`).join("")}</select></label>
          <button type="button" class="csim__btn csim__btn--go" data-a="upload">Upload to HDFS</button></div>` : ""}
        ${F.has("job") ? `<div class="csim__grp"><button type="button" class="csim__btn csim__btn--go" data-a="job">Run word count job</button>
          ${F.has("locality") ? `<label class="csim__chk"><input type="checkbox" data-k="loc" checked> Move code to data (data locality)</label>` : ""}</div>` : ""}
        ${F.has("scale") ? `<div class="csim__grp"><span class="csim__lbl">Cluster size</span>${sizes.map(n => `<button type="button" class="csim__btn" data-a="size" data-n="${n}">${n} node${n > 1 ? "s" : ""}</button>`).join("")}</div>` : ""}
        ${F.has("chaos") ? `<div class="csim__grp"><button type="button" class="csim__btn csim__btn--warn" data-a="chaos">Fail a random node</button></div>` : ""}
        ${F.has("ha") ? `<div class="csim__grp"><button type="button" class="csim__btn csim__btn--warn" data-a="nn">Stop active NameNode</button></div>` : ""}
        ${F.has("fsck") ? `<div class="csim__grp"><button type="button" class="csim__btn" data-a="fsck">hdfs fsck /</button></div>` : ""}
        <div class="csim__grp csim__grp--end">
          <span class="csim__clock" title="Cluster time">⏱ <b>00:00:00</b></span>
          <label>Speed <select data-k="speed"><option value="0.5">½×</option><option value="1" selected>1×</option><option value="4">4×</option><option value="30">30×</option><option value="120">120×</option></select></label>
          <button type="button" class="csim__btn" data-a="ff" hidden>⏩ Skip to timeout</button>
          <button type="button" class="csim__btn" data-a="reset">Reset</button>
        </div>
      </div>
      ${F.has("fail") ? `<p class="csim__hint">Tip: <b>click any DataNode</b> to stop it, and click again to start it.</p>` : ""}
      <div class="csim__main">
        <div class="csim__stage"><svg class="csim__svg" role="img" aria-label="Simulated Hadoop cluster"></svg></div>
        <div class="csim__side">
          <div class="csim__tabs"><button type="button" data-tab="meta" class="on">NameNode metadata</button><button type="button" data-tab="log">Event log</button>${F.has("job") || F.has("scale") ? `<button type="button" data-tab="runs">Job runs</button>` : ""}</div>
          <div class="csim__pane" data-pane="meta"></div>
          <div class="csim__pane" data-pane="log" hidden><ol class="csim__log"></ol></div>
          <div class="csim__pane" data-pane="runs" hidden></div>
        </div>
      </div>
      <p class="csim__foot">A teaching simulator. Defaults match real Hadoop (128 MB blocks, 3 replicas, rack-aware placement, heartbeat every 3 s, dead after 10 min 30 s). Transfer and task times are simplified. <span class="s-wm-text">myphatshala.in</span></p>`);
    const svg = root.querySelector(".csim__svg"), stage = root.querySelector(".csim__stage");
    const q = s => root.querySelector(s);
    const gStatic = el("g", {}, svg), gPk = el("g", {}, svg);

    /* ---------------- model ---------------- */
    function build() {
      rnd = rng(cfg.seed || 7);
      racks = []; nodes = [];
      let id = 1;
      for (let r = 1; r <= rackCount; r++) {
        const rack = { id: r, name: `/rack${r}`, nodes: [] };
        for (let k = 0; k < nodesPerRack; k++) {
          const n = { id: id, name: `DN${id}`, rack: r, alive: true, dead: false, stoppedAt: 0, lastHb: 0, blocks: new Set(), run: [], diskGB: 4096 };
          id++; rack.nodes.push(n); nodes.push(n);
        }
        racks.push(rack);
      }
      files = []; blocks = new Map(); nextBlk = 1073741825; now = 0; queue = []; packets = []; job = null; logLines = [];
      nn = { active: "nn1", up: { nn1: true, nn2: !!F.has("ha") }, down: false };
      fastTo = null;
      log(`Cluster started: ${nodes.length} DataNode${nodes.length > 1 ? "s" : ""} on ${racks.length} rack${racks.length > 1 ? "s" : ""}. NameNode is waiting for heartbeats.`, "info");
      nodes.forEach(n => n.lastHb = 0);
    }
    function log(msg, kind = "") {
      logLines.push({ t: now, msg, kind });
      const ol = q(".csim__log"); if (!ol) return;
      ol.insertAdjacentHTML("afterbegin", `<li class="${kind}"><time>${fmtT(now)}</time>${msg}</li>`);
      while (ol.children.length > 120) ol.lastChild.remove();
    }
    function emit(evt) {
      // tick only the first open task waiting for this event, so a list can use the same event twice
      const i = (cfg.try || []).findIndex((t, k) => t.on === evt && !doneTasks.has(k));
      if (i >= 0) { doneTasks.add(i); const li = q(`.csim__tasks li[data-i="${i}"]`); if (li) li.classList.add("done"); }
    }
    const at = (t, fn) => { queue.push({ t, fn }); queue.sort((a, b) => a.t - b.t); };
    const after = (d, fn) => at(now + d, fn);
    const aliveNodes = () => nodes.filter(n => n.alive);
    const liveNodes = () => nodes.filter(n => !n.dead);          // as the NameNode sees them
    const nnUp = () => !nn.down;

    /* rack-aware placement (BlockPlacementPolicyDefault, simplified) */
    function place(count, writer, exclude = new Set()) {
      const cand = n => n.alive && !n.dead && !exclude.has(n.id);
      const out = [];
      const add = n => { out.push(n); exclude.add(n.id); };
      const pool = () => nodes.filter(cand);
      if (!pool().length) return out;
      add(writer && cand(writer) ? writer : pickRoomy(pool(), rnd));
      if (out.length < count) {
        const other = pool().filter(n => n.rack !== out[0].rack);
        add(other.length ? pickRoomy(other, rnd) : pickRoomy(pool(), rnd));
      }
      if (out.length < count && pool().length) {
        const same = pool().filter(n => n.rack === out[1].rack);
        add(same.length ? pickRoomy(same, rnd) : pickRoomy(pool(), rnd));
      }
      while (out.length < count && pool().length) add(pickRoomy(pool(), rnd));
      return out;
    }

    /* ---------------- layout ---------------- */
    let L = null;
    function layout() {
      const W = Math.max(300, stage.clientWidth || 700);
      const narrow = W < 640;
      const pad = 10, topH = narrow ? 64 : 74;
      const masters = [{ key: "client", label: "Client", sub: "edge node" }, { key: "nn1", label: F.has("ha") ? "NameNode 1" : "NameNode", sub: "master · metadata" }];
      if (F.has("ha")) masters.push({ key: "nn2", label: "NameNode 2", sub: "standby" });
      if (F.has("job") || F.has("scale")) masters.push({ key: "rm", label: "ResourceManager", sub: "master · jobs" });
      const cols = narrow && masters.length > 3 ? 2 : masters.length, mrows = Math.ceil(masters.length / cols);
      const mw = (W - pad * 2 - (cols - 1) * 8) / cols, mh = topH - 18;
      const M = {};
      masters.forEach((m, i) => { M[m.key] = { ...m, x: pad + (i % cols) * (mw + 8), y: pad + Math.floor(i / cols) * (mh + 8), w: mw, h: mh }; });
      const coreY = pad + mrows * (mh + 8) + 12;
      const pos = {}, rackBoxes = [];
      if (!narrow) {
        const rw = (W - pad * 2 - (racks.length - 1) * 10) / racks.length;
        const nh = 84, top = coreY + 34;
        racks.forEach((r, i) => {
          const x = pad + i * (rw + 10);
          const box = { x, y: top, w: rw, h: 30 + r.nodes.length * (nh + 8) + 4, tor: { x: x + rw - 44, y: top + 13 } };
          box.bus = { v: true, x: x + 10, y1: top + 13, y2: top + 30 + (r.nodes.length - 1) * (nh + 8) + nh / 2 };
          rackBoxes.push(box);
          r.nodes.forEach((n, k) => { pos[n.id] = { x: x + 20, y: top + 30 + k * (nh + 8), w: rw - 28, h: nh }; });
        });
      } else {
        const nh = 92;
        let y = coreY + 30;
        racks.forEach(r => {
          const per = Math.min(3, r.nodes.length), rows = Math.ceil(r.nodes.length / per);
          const nw = (W - pad * 2 - 16 - (per - 1) * 6) / per;
          const box = { x: pad, y, w: W - pad * 2, h: 34 + rows * (nh + 6) + 4, tor: { x: W - pad - 46, y: y + 13 } };
          box.bus = { v: false, y: y + 27, x1: pad + 8 + nw / 2, x2: W - pad - 44 };
          rackBoxes.push(box);
          r.nodes.forEach((n, k) => { pos[n.id] = { x: pad + 8 + (k % per) * (nw + 6), y: y + 34 + Math.floor(k / per) * (nh + 6), w: nw, h: nh }; });
          y += box.h + 10;
        });
      }
      const H = rackBoxes.reduce((m, b) => Math.max(m, b.y + b.h), 0) + 12;
      L = { W, H, M, pos, rackBoxes, coreY, narrow, coreX: W - 4 };
      svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
      svg.setAttribute("width", W); svg.setAttribute("height", H);
    }
    const center = key => {
      if (L.M[key]) { const m = L.M[key]; return { x: m.x + m.w / 2, y: m.y + m.h }; }
      const p = L.pos[key]; return { x: p.x + p.w / 2, y: p.y + p.h / 2 };
    };
    function busPts(id) {   // from a node to its rack's ToR switch
      const n = nodes.find(x => x.id === id), p = L.pos[id], box = L.rackBoxes[n.rack - 1], bus = box.bus;
      if (bus.v) { const my = p.y + p.h / 2; return [{ x: p.x, y: my }, { x: bus.x, y: my }, { x: bus.x, y: bus.y1 }, { x: box.tor.x - 34, y: box.tor.y }, { x: box.tor.x, y: box.tor.y }]; }
      const mx = p.x + p.w / 2; return [{ x: mx, y: p.y }, { x: mx, y: bus.y }, { x: bus.x2, y: bus.y }, { x: box.tor.x, y: box.tor.y }];
    }
    function route(a, b) {
      const pa = center(a), pb = center(b);
      const ra = L.M[a] ? 0 : nodes.find(n => n.id === a).rack, rb = L.M[b] ? 0 : nodes.find(n => n.id === b).rack;
      const side = (key, r, p) => {               // from a box up to the core switch
        if (!r) return L.narrow ? [p, { x: p.x, y: L.coreY }, { x: L.coreX, y: L.coreY }] : [p, { x: p.x, y: L.coreY }];
        const t = L.rackBoxes[r - 1].tor;
        return [p].concat(busPts(key), L.narrow ? [{ x: L.coreX, y: t.y }] : [{ x: t.x, y: L.coreY }]);
      };
      if (ra && rb && ra === rb) return [pa].concat(busPts(a), busPts(b).reverse(), [pb]);
      return side(a, ra, pa).concat(side(b, rb, pb).reverse());
    }
    function sendPacket(a, b, dur, color, onDone, label) {
      const pts = route(a, b);
      packets.push({ pts, t0: now, dur, color, onDone, label });
    }

    /* ---------------- drawing ---------------- */
    function draw() {
      if (!L) layout();
      gStatic.innerHTML = "";
      const g = gStatic;
      // core switch line
      if (L.narrow) {
        const lastT = L.rackBoxes[L.rackBoxes.length - 1].tor;
        el("polyline", { points: `10,${L.coreY} ${L.coreX},${L.coreY} ${L.coreX},${lastT.y}`, class: "cs-wire cs-core" }, g);
      } else el("line", { x1: 10, y1: L.coreY, x2: L.W - 10, y2: L.coreY, class: "cs-wire cs-core" }, g);
      el("text", { x: L.W - 12, y: L.coreY - 5, "text-anchor": "end", class: "cs-small" }, g).textContent = "core switch";
      Object.values(L.M).forEach(m => {
        const c = center(m.key);
        el("line", { x1: c.x, y1: c.y, x2: c.x, y2: L.coreY, class: "cs-wire" }, g);
        const up = m.key === "client" || m.key === "rm" || nn.up[m.key];
        const active = m.key === nn.active && nnUp();
        const mg = el("g", { class: m.key === "client" ? "cs-m cs-m--client" : "cs-m cs-m--master" + (up ? "" : " cs-down") }, g);
        el("rect", { x: m.x, y: m.y, width: m.w, height: m.h, rx: 8, class: "cs-mbox" }, mg);
        el("text", { x: m.x + m.w / 2, y: m.y + 18, "text-anchor": "middle", class: "cs-mlabel" }, mg).textContent = m.label;
        let sub = m.sub;
        if (m.key.startsWith("nn") && F.has("ha")) sub = !nn.up[m.key] ? "stopped" : (active ? "ACTIVE" : "standby");
        else if (m.key === "nn1" && nn.down) sub = "stopped";
        el("text", { x: m.x + m.w / 2, y: m.y + 33, "text-anchor": "middle", class: "cs-msub" + (active && F.has("ha") ? " cs-ok" : "") }, mg).textContent = sub;
        let third = "";
        if (m.key === "rm" && job) third = "job: " + job.phase;
        if (m.key.startsWith("nn") && nn.up[m.key] && (!F.has("ha") || active)) third = `${files.length} file${files.length === 1 ? "" : "s"} · ${blocks.size} blocks`;
        if (third && m.h > 40) el("text", { x: m.x + m.w / 2, y: m.y + 47, "text-anchor": "middle", class: "cs-msub cs-acc" }, mg).textContent = third;
      });
      racks.forEach((r, i) => {
        const b = L.rackBoxes[i];
        el("rect", { x: b.x, y: b.y, width: b.w, height: b.h, rx: 10, class: "cs-rack" }, g);
        if (L.narrow) el("line", { x1: b.tor.x, y1: b.tor.y, x2: L.coreX, y2: b.tor.y, class: "cs-wire" }, g);
        else el("line", { x1: b.tor.x, y1: L.coreY, x2: b.tor.x, y2: b.tor.y, class: "cs-wire" }, g);
        if (b.bus.v) {
          el("polyline", { fill: "none", points: `${b.tor.x - 34},${b.tor.y} ${b.bus.x},${b.bus.y1} ${b.bus.x},${b.bus.y2}`, class: "cs-wire cs-bus" }, g);
          r.nodes.forEach(n => { const p = L.pos[n.id]; el("line", { x1: b.bus.x, y1: p.y + p.h / 2, x2: p.x, y2: p.y + p.h / 2, class: "cs-wire cs-bus" }, g); });
        } else {
          el("polyline", { fill: "none", points: `${b.bus.x1},${b.bus.y} ${b.bus.x2},${b.bus.y} ${b.tor.x},${b.tor.y}`, class: "cs-wire cs-bus" }, g);
          r.nodes.forEach(n => { const p = L.pos[n.id]; el("line", { x1: p.x + p.w / 2, y1: b.bus.y, x2: p.x + p.w / 2, y2: p.y, class: "cs-wire cs-bus" }, g); });
        }
        el("rect", { x: b.tor.x - 34, y: b.tor.y - 7, width: 68, height: 14, rx: 4, class: "cs-tor" }, g);
        el("text", { x: b.tor.x, y: b.tor.y + 3.5, "text-anchor": "middle", class: "cs-tiny cs-onboard" }, g).textContent = "ToR switch";
        el("text", { x: b.x + 8, y: b.y + 16, class: "cs-small cs-b" }, g).textContent = `Rack ${r.id} (${r.name})`;
        r.nodes.forEach(n => drawNode(g, n));
      });
    }
    function drawNode(g, n) {
      const p = L.pos[n.id];
      const ng = el("g", { class: "cs-node" + (n.alive ? "" : " is-off") + (n.dead ? " is-dead" : ""), "data-node": n.id, tabindex: F.has("fail") ? 0 : -1, role: F.has("fail") ? "button" : "img", "aria-label": `${n.name} on rack ${n.rack}: ${n.alive ? "running" : "stopped"}` }, g);
      el("rect", { x: p.x, y: p.y, width: p.w, height: p.h, rx: 7, class: "cs-nbox" }, ng);
      el("circle", { cx: p.x + 10, cy: p.y + 11, r: 4, class: n.dead ? "cs-dot-dead" : n.alive ? "cs-dot-ok" : "cs-dot-warn" }, ng);
      el("text", { x: p.x + 18, y: p.y + 15, class: "cs-nlabel" }, ng).textContent = n.name;
      const tight = p.w < 150;
      const st = n.dead ? "DEAD" : !n.alive ? (tight ? `✕ ${ago(now - n.lastHb)}` : `no heartbeat ${ago(now - n.lastHb)}`) : (tight ? `♥ ${ago(Math.max(0, now - n.lastHb))}` : `♥ ${ago(Math.max(0, now - n.lastHb))} ago`);
      el("text", { x: p.x + p.w - 6, y: p.y + 15, "text-anchor": "end", class: "cs-tiny " + (n.dead ? "cs-bad" : !n.alive ? "cs-warn" : "cs-muted") }, ng).textContent = st;
      // block chips
      const cs = L.narrow ? 13 : 15, gap = 3, per = Math.max(1, Math.floor((p.w - 12) / (cs + gap)));
      const list = [...n.blocks].map(id => blocks.get(id)).filter(Boolean).sort((a, b) => a.fileIdx - b.fileIdx || a.idx - b.idx);
      const maxChips = per * 2;
      list.slice(0, maxChips).forEach((b, k) => {
        const x = p.x + 6 + (k % per) * (cs + gap), y = p.y + 22 + Math.floor(k / per) * (cs + gap);
        el("rect", { x, y, width: cs, height: cs, rx: 3, fill: COLORS[b.fileIdx % 4], class: "cs-chip" }, ng);
        el("text", { x: x + cs / 2, y: y + cs / 2 + 3.2, "text-anchor": "middle", class: "cs-chiptxt" }, ng).textContent = b.idx + 1;
      });
      if (list.length > maxChips) el("text", { x: p.x + p.w - 6, y: p.y + 22 + 2 * (cs + gap) - 4, "text-anchor": "end", class: "cs-tiny cs-muted" }, ng).textContent = `+${list.length - maxChips}`;
      // containers / tasks
      const ty = p.y + p.h - 16;
      for (let s = 0; s < slots; s++) {
        const w = (p.w - 12 - (slots - 1) * 4) / slots, x = p.x + 6 + s * (w + 4);
        const t = n.run[s];
        el("rect", { x, y: ty, width: w, height: 11, rx: 3, class: "cs-slot" }, ng);
        if (t) {
          const frac = Math.min(1, Math.max(0, (now - t.start) / t.dur));
          el("rect", { x, y: ty, width: w * frac, height: 11, rx: 3, class: t.kind === "reduce" ? "cs-fill-r" : t.loc === "node" ? "cs-fill-m" : t.loc === "rack" ? "cs-fill-rk" : "cs-fill-off" }, ng);
          el("text", { x: x + 3, y: ty + 8.5, class: "cs-tiny cs-ontask" }, ng).textContent = t.label;
        }
      }
      if (!n.blocks.size && !n.run.some(Boolean)) el("text", { x: p.x + 6, y: p.y + 34, class: "cs-tiny cs-muted" }, ng).textContent = "empty disk";
    }
    function drawPackets() {
      gPk.innerHTML = "";
      packets.forEach(pk => {
        const f = Math.min(1, (now - pk.t0) / pk.dur);
        const segs = []; let tot = 0;
        for (let i = 1; i < pk.pts.length; i++) { const d = Math.hypot(pk.pts[i].x - pk.pts[i - 1].x, pk.pts[i].y - pk.pts[i - 1].y); segs.push(d); tot += d; }
        let d = f * tot, i = 0;
        while (i < segs.length - 1 && d > segs[i]) { d -= segs[i]; i++; }
        const a = pk.pts[i], b = pk.pts[i + 1], r = segs[i] ? d / segs[i] : 1;
        const x = a.x + (b.x - a.x) * r, y = a.y + (b.y - a.y) * r;
        el("circle", { cx: x, cy: y, r: pk.small ? 3 : 5.5, fill: pk.color, class: "cs-packet" }, gPk);
        if (pk.label) el("text", { x: x + 7, y: y - 6, class: "cs-tiny cs-pklabel" }, gPk).textContent = pk.label;
      });
    }
    function drawMeta() {
      const pane = q('[data-pane="meta"]');
      if (!nnUp()) { pane.innerHTML = `<p class="csim__down">NameNode is not running. Clients cannot list, read or write files: the metadata lives only on the NameNode.</p>`; return; }
      if (!files.length) { pane.innerHTML = `<p class="csim__empty">No files yet. ${F.has("upload") ? "Upload one to see how HDFS splits it into blocks and stores copies on different racks." : ""}</p>`; return; }
      const live = liveNodes().length;
      let h = `<p class="csim__sum">Live DataNodes: <b>${live}</b> / ${nodes.length} · Dead: <b class="${live < nodes.length ? "cs-bad-t" : ""}">${nodes.length - live}</b></p>`;
      files.forEach(f => {
        h += `<div class="csim__file"><b style="color:${COLORS[f.idx % 4]}">■</b> <code>/data/${esc(f.name)}</code> <small>${fmtMB(f.sizeMB)} · ${f.blocks.length} blocks · repl ${f.repl}</small><table><tr><th>#</th><th>Block ID</th><th>Locations</th></tr>`;
        f.blocks.forEach(id => {
          const b = blocks.get(id);
          const locs = [...b.locs].map(nid => nodes.find(n => n.id === nid));
          const good = locs.filter(n => !n.dead);
          const st = good.length === 0 ? `<span class="cs-bad-t">MISSING</span>` : good.length < f.repl ? `<span class="cs-warn-t">under-replicated ${good.length}/${f.repl}</span>` : "";
          h += `<tr><td>${b.idx + 1}</td><td><code>blk_${b.id}</code></td><td>${good.map(n => `${n.name}<small>/r${n.rack}</small>`).join(", ") || "none"} ${st}</td></tr>`;
        });
        h += `</table></div>`;
      });
      pane.innerHTML = h;
    }
    function drawRuns() {
      const pane = q('[data-pane="runs"]'); if (!pane) return;
      if (!history.length) { pane.innerHTML = `<p class="csim__empty">No jobs yet. Run the word count job and the result appears here, so you can compare runs.</p>`; return; }
      pane.innerHTML = `<table class="csim__runs"><tr><th>Run</th><th>Nodes</th><th>Maps (local / rack / off)</th><th>Network</th><th>Time</th><th>Result</th></tr>${history.map((r, i) => `<tr><td>${i + 1}</td><td>${r.nodes}</td><td>${r.local} / ${r.rack} / ${r.off}</td><td>${fmtMB(r.net)}</td><td>${r.time ? Math.round(r.time) + " s" : "-"}</td><td>${r.ok ? "✓" : "<span class='cs-bad-t'>failed</span>"}</td></tr>`).join("")}</table>`;
    }
    function drawClock() {
      q(".csim__clock b").textContent = fmtT(now);
      const ff = q('[data-a="ff"]');
      const waiting = nodes.some(n => !n.alive && !n.dead);
      ff.hidden = !waiting;
    }
    let dirty = true;
    const refresh = () => { dirty = true; };

    /* ---------------- HDFS: upload ---------------- */
    function upload(name, sizeMB, preload) {
      if (!nnUp()) { log("Upload failed: the NameNode is down, so no one can allocate blocks.", "bad"); return; }
      const fidx = files.length;
      const nb = Math.ceil(sizeMB / blockMB);
      const f = { idx: fidx, name, sizeMB, repl: replication, blocks: [], complete: !!preload };
      files.push(f);
      log(`Client: <code>hdfs dfs -put ${esc(name)} /data/</code> → ${fmtMB(sizeMB)} in ${nb} blocks of ${blockMB} MB (last block ${fmtMB(sizeMB - (nb - 1) * blockMB)}).`, "info");
      if (preload) {
        for (let i = 0; i < nb; i++) {
          const targets = place(replication, null);
          const b = { id: nextBlk++, fileIdx: fidx, idx: i, sizeMB: Math.min(blockMB, sizeMB - i * blockMB), locs: new Set(targets.map(n => n.id)), repl: replication };
          blocks.set(b.id, b); f.blocks.push(b.id); targets.forEach(n => n.blocks.add(b.id));
        }
        log(`${name} is already stored: ${nb} block${nb > 1 ? "s" : ""} × ${replication} replica${replication > 1 ? "s" : ""}.`);
        refresh(); return;
      }
      let i = 0;
      const one = () => {
        if (i >= nb) { f.complete = true; log(`Upload of ${esc(name)} complete. The NameNode now knows where every block lives.`, "ok"); emit("upload-done"); refresh(); return; }
        if (!nnUp()) { log("Upload stopped: NameNode went down.", "bad"); return; }
        const size = Math.min(blockMB, sizeMB - i * blockMB);
        const targets = place(replication, null);
        if (!targets.length) { log("No live DataNodes: cannot write.", "bad"); return; }
        const b = { id: nextBlk++, fileIdx: fidx, idx: i, sizeMB: size, locs: new Set(), repl: replication };
        blocks.set(b.id, b); f.blocks.push(b.id);
        log(`NameNode: block ${i + 1} → <code>blk_${b.id}</code> on ${targets.map(n => `${n.name} (rack ${n.rack})`).join(" → ")}.${i === 0 && replication > 1 ? (racks.length > 1 ? " The client is not a DataNode, so replica 1 goes to any node; replica 2 to another rack; replica 3 to the same rack as replica 2." : " With only one rack, each replica simply goes to a different node.") : ""}${i === 0 && replication === 1 ? " Replication 1: a single copy, on one node only." : ""}`);
        const hop = (k, from) => {
          const n = targets[k];
          const dur = 0.25 + size / 256 * (from === "client" || nodes.find(x => x.id === from).rack !== n.rack ? 1.3 : 1);
          sendPacket(from, n.id, dur, COLORS[fidx % 4], () => {
            if (n.alive) { n.blocks.add(b.id); b.locs.add(n.id); }
            if (k + 1 < targets.length) hop(k + 1, n.id); else { i++; one(); }
            refresh();
          }, `B${i + 1}`);
        };
        hop(0, "client");
      };
      one();
    }

    /* ---------------- failures & re-replication ---------------- */
    function stopNode(n) {
      if (!n.alive) return;
      n.alive = false; n.stoppedAt = now;
      log(`${n.name} stopped (power cut / crash). It stops sending heartbeats. The NameNode will wait 10 min 30 s before declaring it dead.`, "bad");
      // running tasks on it fail
      n.run.forEach((t, s) => { if (t) { failTask(t, n); n.run[s] = null; } });
      lostMapOutputs(n);
      emit("node-stop"); refresh();
      at(n.lastHb + DEAD_AFTER, () => checkDead(n));
    }
    function checkDead(n) {
      if (n.alive || n.dead) return;
      if (now - n.lastHb < DEAD_AFTER - 0.01) { at(n.lastHb + DEAD_AFTER, () => checkDead(n)); return; }
      if (!nnUp()) { after(5, () => checkDead(n)); return; }
      n.dead = true;
      log(`NameNode: no heartbeat from ${n.name} for 10 min 30 s → marked <b>DEAD</b>. Its ${n.blocks.size} block replica${n.blocks.size === 1 ? "" : "s"} no longer count${n.blocks.size === 1 ? "s" : ""}.`, "bad");
      emit("node-dead");
      if (fastTo) { fastTo = null; setSpeed(1); }
      rereplicate(); refresh();
    }
    function rereplicate(quiet) {
      let missing = 0, queued = 0;
      blocks.forEach(b => {
        const good = [...b.locs].filter(id => !nodes.find(n => n.id === id).dead);
        if (!good.length) { missing++; return; }
        const need = b.repl - good.length;
        if (need <= 0 || b.pending) return;
        const src = nodes.find(n => n.id === good.find(id => nodes.find(x => x.id === id).alive));
        if (!src) return;
        const goodNodes = good.map(id => nodes.find(n => n.id === id));
        const ex = new Set([...b.locs]);
        const racksUsed = new Set(goodNodes.map(n => n.rack));
        let cand = nodes.filter(n => n.alive && !n.dead && !ex.has(n.id));
        if (racksUsed.size === 1 && cand.some(n => !racksUsed.has(n.rack))) cand = cand.filter(n => !racksUsed.has(n.rack));
        if (!cand.length) return;
        const tgt = pick(cand, rnd);
        b.pending = true; queued++;
        after(0.6 + queued * 0.5, () => sendPacket(src.id, tgt.id, 0.4 + b.sizeMB / 256, "#2F7D5B", () => {
          b.pending = false;
          if (tgt.alive) { tgt.blocks.add(b.id); b.locs.add(tgt.id); log(`Re-replicated <code>blk_${b.id}</code> (file ${files[b.fileIdx].name}, block ${b.idx + 1}): ${src.name} → ${tgt.name}.`, "ok"); emit("rereplicated"); }
          refresh(); rereplicate(true);
        }, "copy"));
      });
      if (queued && !quiet) log(`NameNode: ${queued} under-replicated block(s) found. Ordering copies from surviving replicas.`, "info");
      if (missing && !quiet) { log(`NameNode: ${missing} block(s) have NO live replica: those parts of the file are MISSING until a node holding them comes back.`, "bad"); emit("block-missing"); }
    }
    function startNode(n) {
      if (n.alive) return;
      const wasDead = n.dead;
      n.alive = true; n.dead = false; n.lastHb = now;
      log(`${n.name} started again. It sends a heartbeat and a <b>block report</b> listing the ${n.blocks.size} replicas on its disk.`, "ok");
      emit("node-start");
      if (wasDead) {
        // remove excess replicas
        let removed = 0;
        n.blocks.forEach(id => {
          const b = blocks.get(id);
          const good = [...b.locs].filter(x => !nodes.find(m => m.id === x).dead);
          if (good.length > b.repl) {
            const byRack = {};
            good.forEach(x => { const m = nodes.find(k => k.id === x); (byRack[m.rack] = byRack[m.rack] || []).push(m); });
            const crowded = Object.values(byRack).filter(a => a.length > 1).flat();
            const victim = (crowded.length ? crowded : good.map(x => nodes.find(k => k.id === x))).sort((a, c) => c.blocks.size - a.blocks.size)[0];
            victim.blocks.delete(id); b.locs.delete(victim.id); removed++;
          }
        });
        if (removed) log(`NameNode: ${removed} block(s) now had too many copies, so the extra replicas were deleted.`, "info");
      }
      rereplicate(); refresh();
    }

    /* ---------------- NameNode HA ---------------- */
    function stopNN() {
      const a = nn.active;
      if (!nn.up[a]) return;
      nn.up[a] = false;
      if (F.has("ha") && nn.up[a === "nn1" ? "nn2" : "nn1"]) {
        nn.down = true;
        log(`Active NameNode (${a === "nn1" ? "NameNode 1" : "NameNode 2"}) crashed. ZooKeeper notices its session has expired…`, "bad");
        emit("nn-stop");
        after(4, () => { nn.active = a === "nn1" ? "nn2" : "nn1"; nn.down = false; log(`Failover: the standby becomes <b>ACTIVE</b>. It already has the latest edits from the JournalNodes, so clients continue.`, "ok"); emit("nn-failover"); refresh(); });
      } else {
        nn.down = true;
        log("NameNode stopped. With no standby, the whole file system is unavailable: a single point of failure.", "bad");
        emit("nn-stop");
      }
      refresh();
    }

    /* ---------------- MapReduce job ---------------- */
    function runJob() {
      if (job && job.phase !== "done" && job.phase !== "failed") return;
      if (!files.length) { log("Nothing to process. Upload a file first.", "bad"); return; }
      if (!nnUp()) { log("Job cannot start: the NameNode is down, so input splits cannot be found.", "bad"); return; }
      const done = files.filter(x => x.complete);
      if (!done.length) { log("Wait for the upload to finish before running a job.", "bad"); return; }
      const f = done[done.length - 1];
      locality = F.has("locality") ? q('[data-k="loc"]').checked : true;
      job = { file: f, phase: "map", start: now, pending: [], done: 0, total: f.blocks.length, net: 0, local: 0, rack: 0, off: 0, reducers: 2, rdone: 0, ok: true, nodes: aliveNodes().length, locality };
      f.blocks.forEach(id => job.pending.push({ kind: "map", block: id, attempt: 0, label: "" }));
      log(`Job submitted: word count on /data/${esc(f.name)}. ResourceManager starts an ApplicationMaster; it asks for ${job.total} map containers (one per block).${locality ? "" : " Locality is OFF: tasks go to any free node and must pull data over the network."}`, "info");
      refresh(); schedule();
    }
    function freeSlot(n) { return n.alive ? n.run.findIndex((t, i) => i < slots && !t) : -1; }
    function slotOf(n) { for (let s = 0; s < slots; s++) if (!n.run[s]) return s; return -1; }
    function schedule() {
      if (!job || job.phase === "done" || job.phase === "failed") return;
      if (job.phase === "map") {
        for (const level of locality ? ["node", "rack", "off"] : ["any"]) {
          for (let i = 0; i < job.pending.length; i++) {
            const t = job.pending[i], b = blocks.get(t.block);
            const holders = [...b.locs].map(id => nodes.find(n => n.id === id)).filter(n => n.alive);
            if (!holders.length) {
              job.pending.splice(i, 1); i--;
              if (b.locs.size && [...b.locs].some(id => !nodes.find(n => n.id === id).dead)) { after(3, () => { job.pending.push(t); schedule(); }); continue; }
              job.ok = false; job.phase = "failed";
              log(`Map task for block ${b.idx + 1} failed: <code>BlockMissingException</code>. No live replica of blk_${b.id}. Job FAILED.`, "bad");
              emit("job-failed"); finishRun(); refresh(); return;
            }
            let node = null, loc = "node";
            if (locality) {
              // delay scheduling: wait a little for a free slot on a node that holds the data
              if (t.wait === undefined) t.wait = now;
              if (level === "node") node = holders.find(n => slotOf(n) >= 0);
              if (level === "rack" && now - t.wait >= 1.5) { const rset = new Set(holders.map(n => n.rack)); node = aliveNodes().find(n => rset.has(n.rack) && slotOf(n) >= 0); loc = "rack"; }
              if (level === "off" && now - t.wait >= 3) { node = aliveNodes().find(n => slotOf(n) >= 0); loc = "off"; }
            } else {
              const free = aliveNodes().filter(n => slotOf(n) >= 0);
              node = free.length ? pick(free, rnd) : null;
              if (node) loc = b.locs.has(node.id) ? "node" : holders.some(h => h.rack === node.rack) ? "rack" : "off";
            }
            if (!node) continue;
            job.pending.splice(i, 1); i--;
            const s = slotOf(node);
            const transfer = loc === "node" ? 0 : b.sizeMB / (loc === "rack" ? 110 : 45);
            const dur = 2.5 + b.sizeMB / 64 + transfer;
            const task = { kind: "map", block: b.id, attempt: t.attempt, label: `M${b.idx + 1}${t.attempt ? "′" : ""}`, start: now, dur, loc, node: node.id, slot: s };
            node.run[s] = task;
            job[loc === "node" ? "local" : loc]++;
            if (loc !== "node") {
              job.net += b.sizeMB;
              const src = holders.find(h => h.rack === node.rack) || holders[0];
              sendPacket(src.id, node.id, Math.max(0.5, transfer), "#D64545", null, `B${b.idx + 1}`);
            }
            after(dur, () => endTask(task));
          }
        }
        if (job.pending.length && !job.tick) { job.tick = true; after(0.5, () => { if (job) { job.tick = false; schedule(); } }); }
      } else if (job.phase === "reduce" && job.pending.length) {
        for (let i = 0; i < job.pending.length; i++) {
          const t = job.pending[i];
          const node = aliveNodes().filter(n => slotOf(n) >= 0).sort((a, b) => a.run.filter(Boolean).length - b.run.filter(Boolean).length)[0];
          if (!node) break;
          job.pending.splice(i, 1); i--;
          const s = slotOf(node);
          const dur = 3 + job.file.sizeMB / 1024 * 2;
          const task = { kind: "reduce", r: t.r, attempt: t.attempt, label: `R${t.r + 1}${t.attempt ? "′" : ""}`, start: now, dur, node: node.id, slot: s };
          node.run[s] = task;
          // shuffle: every mapper node sends a slice to this reducer
          const mapNodes = [...new Set(job.mapNodes)].map(id => nodes.find(n => n.id === id)).filter(n => n.alive);
          mapNodes.forEach((m, k) => { if (m.id !== node.id) { job.net += job.file.sizeMB * 0.02 / job.reducers; after(k * 0.15, () => sendPacket(m.id, node.id, 1.1, "#8B5CF6", null)); } });
          after(dur, () => endTask(task));
        }
      }
      refresh();
    }
    function endTask(t) {
      const n = nodes.find(x => x.id === t.node);
      if (!job || n.run[t.slot] !== t) return;            // task was killed
      n.run[t.slot] = null;
      if (t.kind === "map") {
        job.done++; (job.mapNodes = job.mapNodes || []).push(n.id); (job.finished = job.finished || []).push({ block: t.block, node: n.id, label: t.label, attempt: t.attempt });
        if (job.done === job.total) {
          job.phase = "reduce";
          log(`All ${job.total} map tasks done (data-local: ${job.local}, rack-local: ${job.rack}, off-rack: ${job.off}). Shuffle: map outputs are copied to ${job.reducers} reducers.`, "info");
          for (let r = 0; r < job.reducers; r++) job.pending.push({ kind: "reduce", r, attempt: 0 });
        }
      } else {
        job.rdone++;
        if (job.rdone === job.reducers) {
          job.phase = "done"; job.time = now - job.start;
          log(`Job SUCCEEDED in ${Math.round(job.time)} s. Output written to HDFS as part-r-00000 and part-r-00001. Network used: ${fmtMB(job.net)}.`, "ok");
          emit(job.locality ? "job-done" : "job-done-nolocal"); finishRun();
        }
      }
      schedule(); refresh();
    }
    function failTask(t, n) {
      if (!job) return;
      if (t.kind === "map") job[t.loc === "node" ? "local" : t.loc]--;
      job.pending.push({ kind: t.kind, block: t.block, r: t.r, attempt: t.attempt + 1 });
      log(`Task ${t.label} on ${n.name} was lost with the node. The ApplicationMaster re-runs it on another node (attempt ${t.attempt + 2}). In a real cluster this is noticed after a timeout; here it is immediate.`, "bad");
      after(1.5, schedule);
    }
    function lostMapOutputs(n) {
      // finished map outputs live on the worker's local disk: if reducers have not finished, they are lost too
      if (!job || (job.phase !== "map" && job.phase !== "reduce") || !job.mapNodes) return;
      const lost = job.finished.filter(f => f.node === n.id);
      if (!lost.length) return;
      job.finished = job.finished.filter(f => f.node !== n.id);
      job.mapNodes = job.finished.map(f => f.node);
      lost.forEach(f => { job.done--; job.pending.push({ kind: "map", block: f.block, attempt: f.attempt + 1 }); });
      log(`Finished map output of ${lost.map(f => f.label).join(", ")} was on ${n.name}'s local disk, so ${lost.length === 1 ? "it is" : "they are"} re-run too.`, "bad");
      if (job.phase === "reduce") {
        job.phase = "map";
        job.pending = job.pending.filter(t => t.kind !== "reduce");
        nodes.forEach(m => m.run.forEach((t, s) => { if (t && t.kind === "reduce") m.run[s] = null; }));
        log("Reducers must wait until those maps finish again.", "info");
      }
      after(1.5, schedule);
    }
    function finishRun() { history.push({ nodes: job.nodes, local: job.local, rack: job.rack, off: job.off, net: job.net, time: job.time, ok: job.phase === "done" }); drawRuns(); }

    /* ---------------- fsck ---------------- */
    function fsck() {
      if (!nnUp()) { log("fsck: cannot connect to the NameNode.", "bad"); return; }
      let total = 0, under = 0, miss = 0;
      blocks.forEach(b => { total++; const g = [...b.locs].filter(id => !nodes.find(n => n.id === id).dead).length; if (!g) miss++; else if (g < b.repl) under++; });
      log(`<code>hdfs fsck /</code>: Total blocks ${total} · Under-replicated ${under} · Missing ${miss} · Status: <b>${miss ? "CORRUPT" : "HEALTHY"}</b>`, miss ? "bad" : "ok");
      emit("fsck");
    }

    /* ---------------- loop ---------------- */
    function setSpeed(v) { speed = v; const s = q('[data-k="speed"]'); if (s) s.value = String(v); }
    function tick(ts) {
      if (!root.isConnected) return;
      const dt = lastFrame ? Math.min(0.1, (ts - lastFrame) / 1000) : 0; lastFrame = ts;
      if (visible) {
        const target = now + dt * speed;
        while (queue.length && queue[0].t <= target) { const e = queue.shift(); now = Math.max(now, e.t); e.fn(); }
        now = target;
        // heartbeats
        nodes.forEach(n => { if (n.alive && now - n.lastHb >= HB) { n.lastHb = Math.floor(now / HB) * HB; if (speed <= 1 && nnUp()) packets.push({ pts: route(n.id, nn.active), t0: now, dur: 0.9, color: "#E05A8A", small: true }); } });
        const finished = packets.filter(pk => now - pk.t0 >= pk.dur);
        if (finished.length) { packets = packets.filter(pk => now - pk.t0 < pk.dur); finished.forEach(pk => pk.onDone && pk.onDone()); }
        if (dirty || ts - lastDraw > 250) { lastDraw = ts; draw(); drawClock(); if (dirty) { drawMeta(); dirty = false; } }
        drawPackets();
      }
      requestAnimationFrame(tick);
    }
    let visible = true, lastDraw = 0;
    if ("IntersectionObserver" in window) new IntersectionObserver(es => es.forEach(e => { visible = e.isIntersecting; lastFrame = 0; })).observe(root);

    /* ---------------- events ---------------- */
    root.addEventListener("click", e => {
      const b = e.target.closest("[data-a]");
      const tab = e.target.closest("[data-tab]");
      if (tab) {
        root.querySelectorAll("[data-tab]").forEach(x => x.classList.toggle("on", x === tab));
        root.querySelectorAll("[data-pane]").forEach(p => { p.hidden = p.dataset.pane !== tab.dataset.tab; });
        if (tab.dataset.tab === "runs") drawRuns();
        return;
      }
      if (!b) return;
      const a = b.dataset.a;
      if (a === "upload") {
        blockMB = +q('[data-k="bsize"]').value; replication = +q('[data-k="repl"]').value;
        const size = +q('[data-k="fsize"]').value;
        const names = ["upi_txns_2025.csv", "irctc_bookings.log", "sale_clicks.json", "canteen_orders.csv"];
        upload(names[files.length % 4].replace(/(\.\w+)$/, files.length >= 4 ? `_${files.length}$1` : "$1"), size);
      }
      if (a === "job") runJob();
      if (a === "chaos") { const al = aliveNodes(); if (al.length) stopNode(pick(al, rnd)); }
      if (a === "nn") stopNN();
      if (a === "fsck") fsck();
      if (a === "reset") reset();
      if (a === "ff") { fastTo = true; setSpeed(120); }
      if (a === "size") {
        const n = +b.dataset.n; nodesPerRack = Math.ceil(n / rackCount);
        reset(true);
        log(`Cluster resized to ${nodes.length} nodes. The same data is loaded again, spread over all nodes.`, "info"); emit("resize");
      }
    });
    const toggleNode = id => { const n = nodes.find(x => x.id === id); if (n) n.alive ? stopNode(n) : startNode(n); };
    svg.addEventListener("pointerdown", e => { const ne = e.target.closest("[data-node]"); if (ne && F.has("fail")) { e.preventDefault(); toggleNode(+ne.dataset.node); } });
    root.addEventListener("keydown", e => { if ((e.key === "Enter" || e.key === " ") && e.target.closest("[data-node]")) { e.preventDefault(); toggleNode(+e.target.closest("[data-node]").dataset.node); } });
    root.addEventListener("change", e => { if (e.target.dataset.k === "speed") { speed = +e.target.value; fastTo = null; } });
    let rw = 0;
    new ResizeObserver(() => { const w = stage.clientWidth; if (Math.abs(w - rw) > 4) { rw = w; layout(); dirty = true; draw(); drawPackets(); } }).observe(stage);

    function reset(keepHistory) {
      const ol = q(".csim__log"); if (ol) ol.innerHTML = "";
      if (!keepHistory) history = [];
      build(); layout();
      (cfg.preload || []).forEach(p => upload(p.name, p.sizeMB, true));
      speed = +(q('[data-k="speed"]').value = String(cfg.speed || 1));
      dirty = true; draw(); drawMeta(); drawRuns(); drawClock();
    }
    history = [];
    reset();
    requestAnimationFrame(tick);
  }

  document.querySelectorAll(".csim").forEach(r => {
    const s = r.querySelector('script[type="application/json"]');
    let cfg = {};
    try { cfg = s ? JSON.parse(s.textContent) : {}; } catch (e) { console.error("Bad csim JSON", e); }
    try { new Sim(r, cfg); } catch (e) { console.error(e); r.insertAdjacentHTML("beforeend", "<p>The playground could not start in this browser.</p>"); }
  });
})();
