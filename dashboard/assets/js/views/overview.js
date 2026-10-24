// Overview: what the tool does, system state, the reproduction headline (read from results/), recent jobs and results.
import * as api from "../api.js";
import { icon } from "../icons.js";
import { $, emptyState, esc, fmt, isNum, jobBadge, relTime, repoName, skeleton } from "../ui.js";
import { TOOLS } from "../glossary.js";

let el, ctx;

export default {
  mount(root, c) {
    el = root; ctx = c;
    el.innerHTML = `
      <div class="page-head"><div><h1>Exception Handling &amp; Defect Analysis</h1>
        <p>Replicate and extend the de Pádua &amp; Shang (MSR 2018) study: do exception-handling practices (flow characteristics and 17 anti-patterns) relate to post-release defects?</p></div>
        <a class="btn btn-primary" href="#/analyze">${icon("play", 14)} Analyze a repository</a></div>
      <div class="howto" style="margin-bottom:16px">
        <div class="card"><span class="step-num">1</span><h4>Point it at a release</h4><p class="small muted" style="margin:0">Paste a repository link, pick the release and the defect window. Tags are suggested with the paper's convention.</p></div>
        <div class="card"><span class="step-num">2</span><h4>Run the authors' pipeline</h4><p class="small muted" style="margin:0">Git and issue-tracker mining, JTratch exception-flow analysis, and the authors' own R models, with every step logged.</p></div>
        <div class="card"><span class="step-num">3</span><h4>Read the evidence</h4><p class="small muted" style="margin:0">BASE / BSFC / BSAP models (RQ1–2), ML prediction (RQ3) and SHAP (RQ4), with the limitations listed next to them.</p></div>
      </div>
      <div class="ov-grid">
        <div class="stack">
          <section class="card"><div class="card-head"><div><h2>${icon("jobs", 17)} Recent analyses</h2><p>Latest jobs started from this dashboard.</p></div><a class="btn btn-ghost btn-sm" href="#/jobs">All jobs ${icon("chevRight", 13)}</a></div>
            <div id="ovJobs">${skeleton(4, 22)}</div></section>
          <section class="card"><div class="card-head"><div><h2>${icon("results", 17)} Analysed releases</h2><p>Releases with a results summary.</p></div></div><div id="ovRes">${skeleton(3, 22)}</div></section>
        </div>
        <div class="stack">
          <section class="card"><div class="card-head"><div><h2>${icon("original", 17)} Reproduction of the paper</h2><p>Table 4, from the authors' package.</p></div></div><div class="card-body" id="ovRepro">${skeleton(3)}</div></section>
          <section class="card"><div class="card-head"><div><h2>${icon("shield", 17)} System</h2><p>Tools the pipeline needs.</p></div></div><div class="card-body" id="ovSys">${skeleton(3)}</div></section>
        </div>
      </div>`;
    ctx.onHealth.push(paintSys);
  },
  async show() { paintSys(ctx.health); jobs(); results(); repro(); },
};

function paintSys(h) {
  const box = $("#ovSys", el); if (!box) return;
  if (ctx.noServer) { box.innerHTML = '<p class="small" style="color:var(--bad);margin:0">The dashboard server is not reachable; see the banner above.</p>'; return; }
  if (!h) return;
  box.innerHTML = `<ul style="list-style:none;margin:0;padding:0;display:grid;gap:8px">${Object.entries(TOOLS).map(([k, [label, desc]]) => {
    const ok = !!h[k], alt = k === "understand" && !ok;
    return `<li class="row" style="flex-wrap:nowrap;align-items:flex-start"><span class="badge ${ok ? "b-ok" : alt ? "b-warn" : "b-bad"}" style="min-width:86px;justify-content:center">${icon(ok ? "check" : alt ? "alert" : "x", 11)} ${ok ? "available" : alt ? "fallback" : "missing"}</span>
      <div class="small"><b>${esc(label)}</b><div class="muted">${esc(desc)}</div></div></li>`;
  }).join("")}</ul>`;
}

async function jobs() {
  try {
    const js = (await api.listJobs()).slice(0, 5);
    $("#ovJobs", el).innerHTML = js.length ? js.map(j => `<a class="job-item" href="#/jobs/${encodeURIComponent(j.id)}" style="display:block;text-decoration:none">
      <div class="j-top"><span class="j-name">${esc(repoName(j.repo) || j.target)}</span>${jobBadge(j.status)}</div>
      <div class="j-sub"><span class="mono">${esc(j.release || "")}</span><span>·</span><span>${esc(relTime(j.created))}</span></div></a>`).join("")
      : emptyState("jobs", "No analyses yet", "Start with an example repository such as Apache ZooKeeper.", `<a class="btn btn-secondary btn-sm" href="#/analyze" style="margin-top:8px">Analyze a repository</a>`);
  } catch (e) { $("#ovJobs", el).innerHTML = `<div class="card-body small" style="color:var(--bad)">${esc(e.message)}</div>`; }
}

async function results() {
  try {
    const rs = await api.listResults();
    $("#ovRes", el).innerHTML = rs.length ? `<div class="table-wrap"><table class="t"><thead><tr><th>Repository</th><th>Release</th><th>Tracker</th><th>Models</th><th></th></tr></thead><tbody>
      ${rs.map(r => `<tr><td>${esc(repoName(r.repo))}</td><td class="mono">${esc(r.release)}</td><td>${esc(r.tracker)}</td>
        <td>${r.has_models ? `<span class="badge b-ok">${icon("check", 11)} fitted</span>` : '<span class="badge b-mute">not fitted</span>'}</td>
        <td class="r"><a class="btn btn-ghost btn-sm" href="#/results/${encodeURIComponent(r.target)}">Open ${icon("chevRight", 12)}</a></td></tr>`).join("")}</tbody></table></div>`
      : emptyState("results", "No analysed releases", "Results appear when a job finishes.");
  } catch (e) { $("#ovRes", el).innerHTML = `<div class="card-body small" style="color:var(--bad)">${esc(e.message)}</div>`; }
}

async function repro() {
  try {
    const rows = await api.getCsv("/results/reproduction_comparison.csv");
    const fixed = rows.filter(r => r.Run === "Ours: authors' code + BSFC bug fix" && isNum(r.Difference));
    const maxAbs = Math.max(...fixed.map(r => Math.abs(+r.Difference)));
    $("#ovRepro", el).innerHTML = `<div class="kpi-big">±${fmt(maxAbs)}</div>
      <p class="small" style="margin:4px 0 10px">Largest difference between the paper's Table 4 R² and our bug-fixed run of the authors' code, over ${fixed.length} values.</p>
      <p class="small muted" style="margin:0 0 12px">As released, the authors' scripts fit the anti-pattern data into "BSFC". A one-line fix makes all three models match the paper.</p>
      <a class="btn btn-secondary btn-sm" href="#/original">${icon("original", 13)} See the reproduction</a>`;
  } catch (e) { $("#ovRepro", el).innerHTML = `<p class="small muted" style="margin:0">Reproduction results not found (${esc(e.message)}).</p>`; }
}
