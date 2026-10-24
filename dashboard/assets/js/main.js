// App shell: hash router, sidebar, header, theme, system status, research header with tabs.
import * as api from "./api.js";
import { icon } from "./icons.js";
import { $, $$, esc, initTooltips } from "./ui.js";
import { TOOLS } from "./glossary.js";
import overview from "./views/overview.js";
import analyze from "./views/analyze.js";
import jobs from "./views/jobs.js";
import results from "./views/results.js";
import original from "./views/original.js";
import downloads from "./views/downloads.js";

const VIEWS = {
  overview: { mod: overview, label: "Overview", icon: "overview", title: "Overview", desc: "What this tool does, its current state and recent analyses." },
  analyze: { mod: analyze, label: "Analyze Repository", icon: "analyze", title: "Analyze a repository", desc: "Configure a release window and start a new study.", research: true },
  jobs: { mod: jobs, label: "Analysis Jobs", icon: "jobs", title: "Analysis jobs", desc: "Pipeline progress, step logs and cancellation." },
  results: { mod: results, label: "Research Results", icon: "results", title: "Research results", desc: "Models, anti-patterns, ML and SHAP for an analysed release." },
  original: { mod: original, label: "Original Study", icon: "original", title: "Original study", desc: "Fixed reproduction results on the paper's own data.", research: true },
  downloads: { mod: downloads, label: "Downloads", icon: "downloads", title: "Downloads", desc: "Every artifact produced by the pipeline, with sizes." },
};

const ctx = {
  health: null, noServer: false,
  navigate: (h) => { if (location.hash === h) route(); else location.hash = h; },
  setRunningCount: (n) => { const c = $("#runCount"); if (c) { c.textContent = n; c.classList.toggle("hidden", !n); } },
  onHealth: [],
};
const mounted = new Set();

// ---------- sidebar / header ----------
$("#nav").innerHTML = '<div class="nav-label">Workspace</div>' + Object.entries(VIEWS).map(([k, v]) =>
  `<a href="#/${k}" data-view="${k}" data-tip="${esc(v.label)}">${icon(v.icon, 18)}<span>${esc(v.label)}</span>${k === "jobs" ? '<span class="count hidden" id="runCount" aria-label="running jobs"></span>' : ""}</a>`).join("");
$("#menuBtn").innerHTML = icon("menu", 18);
$("#menuBtn").onclick = () => $("#app").classList.toggle("drawer-open");
$("#app").addEventListener("click", (e) => { if ($("#app").classList.contains("drawer-open") && !e.target.closest(".sidebar") && !e.target.closest("#menuBtn")) $("#app").classList.remove("drawer-open"); });
const setCollapse = (c) => { $("#app").classList.toggle("collapsed", c); $(".cb-ic").innerHTML = icon(c ? "chevRight" : "chevLeft", 15);
  $("#collapseBtn").setAttribute("aria-label", c ? "Expand sidebar" : "Collapse sidebar"); try { localStorage.setItem("sidebar", c ? "1" : "0"); } catch {} };
let collapsed = false; try { collapsed = localStorage.getItem("sidebar") === "1"; } catch {}
setCollapse(collapsed); $("#collapseBtn").onclick = () => setCollapse(!$("#app").classList.contains("collapsed"));
const paintTheme = () => { const d = document.documentElement.getAttribute("data-theme") === "dark"; $("#themeBtn").innerHTML = icon(d ? "sun" : "moon", 17);
  $("#themeBtn").setAttribute("aria-label", d ? "Switch to light mode" : "Switch to dark mode"); };
$("#themeBtn").onclick = () => { const t = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", t); try { localStorage.setItem("theme", t); } catch {} paintTheme();
  window.dispatchEvent(new Event("themechange")); };
paintTheme();

// ---------- health / status ----------
function toolState(h, k) { if (!h) return "no"; if (k === "understand") return h.understand ? "ok" : "alt"; return h[k] ? "ok" : "no"; }
function statusChips(h) {
  return Object.entries(TOOLS).map(([k, [label, desc]]) => {
    const st = toolState(h, k);
    const tip = st === "ok" ? `${label}: available. ${desc}` : st === "alt" ? `${label}: not available. ${desc}` : `${label}: not found. ${desc}`;
    return `<span class="status-chip ${st}" tabindex="0" data-tip="${esc(tip)}"><span class="ic">${icon(st === "ok" ? "check" : st === "alt" ? "alert" : "x", 12)}</span>${esc(label)}<span class="sr-only">${st === "ok" ? "available" : "not available"}</span></span>`;
  }).join("");
}
function paintStatus() {
  const h = ctx.health;
  $("#sideStatus").innerHTML = Object.entries(TOOLS).map(([k, [label, desc]]) => {
    const st = toolState(h, k);
    return `<li class="${st}" data-tip="${esc(label + ": " + (st === "ok" ? "available" : st === "alt" ? "fallback in use" : "missing") + ". " + desc)}"><span class="dot"></span><span>${esc(label)}</span></li>`;
  }).join("");
  const missing = h ? ["git", "Rscript", "java8"].filter(k => !h[k]) : ["server"];
  $("#globalStatus").innerHTML = ctx.noServer ? `<span class="badge b-bad">${icon("x", 12)} Server offline</span>`
    : missing.length ? `<span class="badge b-warn" data-tip="Missing: ${esc(missing.join(", "))}">${icon("alert", 12)} Degraded</span>`
    : `<span class="badge b-ok" data-tip="Git, R and Java 8 are available. Product metrics use the open-source fallback.">${icon("dot", 10)} All systems ready</span>`;
  const hc = $("#heroChips"); if (hc) hc.innerHTML = statusChips(h);
}
async function loadHealth() {
  try { ctx.health = await api.getHealth(); ctx.noServer = false; $("#noServer").classList.add("hidden"); }
  catch (e) {
    ctx.health = null; ctx.noServer = !!e.noServer;
    if (e.noServer) {
      $("#noServer").innerHTML = `<span class="b-ic">${icon("alert", 20)}</span><div><b>The dashboard server is not running behind this page.</b>
        <div class="small" style="margin-top:4px">This page only works when it is opened through <code>dashboard/app.py</code>. A static file server
        (such as VS Code's Live Server on port 5500) or opening the file directly cannot run the pipeline. In a terminal:</div>
        <pre>cd "D:\\Software Maint Project\\exception-handling-replication"\n./envrun.sh python dashboard/app.py</pre>
        <div class="small" style="margin-top:6px">Then open <a href="http://localhost:8000/">http://localhost:8000/</a>.</div></div>`;
      $("#noServer").classList.remove("hidden");
    }
  }
  paintStatus(); ctx.onHealth.forEach(f => f(ctx.health));
}

// ---------- research header with tabs ----------
function buildResearchHead() {
  $("#researchHead").innerHTML = `
    <div class="hero">
      <h1>Exception Handling &amp; Defect Analysis</h1>
      <p>Replicate and extend the de Pádua &amp; Shang (MSR 2018) study to investigate how exception-handling practices relate to post-release software defects.</p>
      <div class="row" id="heroChips"></div>
    </div>
    <div class="tabs" role="tablist" aria-label="Study mode">
      <button class="tab" role="tab" id="tab-analyze" aria-controls="view-analyze" data-go="analyze">${icon("analyze", 16)} Analyze a Repository</button>
      <button class="tab" role="tab" id="tab-original" aria-controls="view-original" data-go="original">${icon("original", 16)} Original Study</button>
      <span class="tab-ink" aria-hidden="true"></span>
    </div>`;
  $$("#researchHead .tab").forEach(t => { t.onclick = () => ctx.navigate(`#/${t.dataset.go}`); });
  $("#researchHead .tabs").addEventListener("keydown", (e) => {
    if (!["ArrowLeft", "ArrowRight"].includes(e.key)) return;
    const tabs = $$("#researchHead .tab"), i = tabs.indexOf(document.activeElement); if (i < 0) return;
    const n = tabs[(i + (e.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length]; n.focus(); n.click();
  });
}
function paintTabs(view) {
  $$("#researchHead .tab").forEach(t => { const on = t.dataset.go === view; t.setAttribute("aria-selected", on); t.tabIndex = on ? 0 : -1; });
  const on = $(`#researchHead .tab[data-go="${view}"]`), ink = $("#researchHead .tab-ink");
  if (on && ink) { ink.style.left = `${on.offsetLeft}px`; ink.style.width = `${on.offsetWidth}px`; }
}

// ---------- router ----------
function parse() { const [, view, ...rest] = (location.hash || "#/overview").split("/"); return { view: VIEWS[view] ? view : "overview", param: rest.map(decodeURIComponent).join("/") || null }; }
function route() {
  const { view, param } = parse(), v = VIEWS[view];
  $$("section[data-view]").forEach(s => s.classList.toggle("hidden", s.dataset.view !== view));
  $$("#nav a").forEach(a => { const on = a.dataset.view === view; a.classList.toggle("active", on); on ? a.setAttribute("aria-current", "page") : a.removeAttribute("aria-current"); });
  $("#researchHead").classList.toggle("hidden", !v.research);
  if (v.research) paintTabs(view);
  $("#crumbs").innerHTML = `ExceptionLab ${icon("chevRight", 12)} <b>${esc(v.title)}</b>${param ? ` ${icon("chevRight", 12)} <span class="mono">${esc(param)}</span>` : ""}`;
  document.title = `${v.title} · ExceptionLab`;
  const el = $(`section[data-view="${view}"]`); el.id = `view-${view}`;
  if (!mounted.has(view)) { mounted.add(view); v.mod.mount(el, ctx); }
  v.mod.show && v.mod.show(param);
  $("#app").classList.remove("drawer-open");
  if (!v.research) window.scrollTo({ top: 0 });
}
window.addEventListener("hashchange", route);
window.addEventListener("resize", () => { const { view } = parse(); if (VIEWS[view].research) paintTabs(view); });

// running-jobs counter in the sidebar
async function refreshCount() {
  try { const js = await api.listJobs(); ctx.setRunningCount(js.filter(j => j.status === "running" || j.status === "queued").length); } catch { /* offline */ }
  setTimeout(refreshCount, 8000);
}

initTooltips();
buildResearchHead();
route();
loadHealth().then(refreshCount);
