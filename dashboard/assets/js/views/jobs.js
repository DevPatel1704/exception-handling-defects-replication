// Analysis Jobs: job list (search + status filter) | selected job: progress, 11-step pipeline, live log, log drawer.
import * as api from "../api.js";
import { icon } from "../icons.js";
import { $, $$, copyText, dialog, drawer, emptyState, errorBox, esc, fmtDate, fmtDur, html, jobBadge, relTime, repoName,
         skeleton, stepBadge, stepIcon, toast } from "../ui.js";
import { STEPS } from "../glossary.js";

let el, ctx, jobs = [], selected = null, stopJob = null, listTimer = null, filter = "all", query = "", current = null, lastSig = "";
const ACTIVE = (s) => s === "queued" || s === "running";
const FILTERS = [["all", "All"], ["active", "Active"], ["finished", "Finished"], ["problems", "Problems"], ["cancelled", "Cancelled"]];
const match = (j) => (filter === "all" || (filter === "active" && ACTIVE(j.status)) || (filter === "finished" && j.status === "finished")
  || (filter === "problems" && ["finished with problems", "error", "interrupted"].includes(j.status)) || (filter === "cancelled" && j.status === "cancelled"))
  && (!query || `${j.target} ${j.repo} ${j.release}`.toLowerCase().includes(query));

export default {
  mount(root, c) {
    el = root; ctx = c;
    el.innerHTML = `
      <div class="page-head"><div><h1>Analysis jobs</h1><p>Each job runs the full pipeline for one release. Steps update live; open any step's log.</p></div>
        <a class="btn btn-primary" href="#/analyze">${icon("play", 14)} New analysis</a></div>
      <div class="jobs-layout">
        <div class="card" style="overflow:hidden">
          <div style="padding:12px 12px 10px;border-bottom:1px solid var(--border)" class="stack" >
            <div class="input-wrap"><span class="lead">${icon("search", 15)}</span><input class="input" id="jobSearch" placeholder="Search repository or release" aria-label="Search jobs"></div>
            <div class="seg" role="group" aria-label="Filter by status">${FILTERS.map(([k, l]) => `<button data-f="${k}" aria-pressed="${k === filter}">${l}</button>`).join("")}</div>
          </div>
          <div class="joblist" id="jobList">${skeleton(5, 30)}</div>
        </div>
        <div class="card" id="jobDetail"><div class="card-body">${emptyState("jobs", "Select a job", "Choose a job on the left to see its pipeline and logs.")}</div></div>
      </div>`;
    $("#jobSearch", el).addEventListener("input", (e) => { query = e.target.value.trim().toLowerCase(); paintList(); });
    $$(".seg button", el).forEach(b => b.onclick = () => { filter = b.dataset.f; $$(".seg button", el).forEach(x => x.setAttribute("aria-pressed", x === b)); paintList(); });
    // one delegated handler on the stable container: buttons survive the 2.5 s re-renders
    $("#jobDetail", el).addEventListener("click", (e) => {
      const lg = e.target.closest("[data-log]"); if (lg && current) return openLog(current.id, lg.dataset.log, lg.dataset.title);
      if (e.target.closest("#cancelJob") && current) confirmCancel(current);
    });
  },
  show(param) {
    refreshList();
    if (param && param !== selected) select(param);
    else if (!param && !selected) setTimeout(() => { const first = jobs.find(match); if (first && !selected) select(first.id, true); }, 400);
  },
};

async function refreshList() {
  clearTimeout(listTimer);
  try { jobs = await api.listJobs(); paintList(); }
  catch (e) { $("#jobList", el).innerHTML = `<div class="card-body">${errorBox(e.message)}</div>`; }
  if (!el.classList.contains("hidden")) listTimer = setTimeout(refreshList, jobs.some(j => ACTIVE(j.status)) ? 3000 : 10000);
}

function paintList() {
  const rows = jobs.filter(match);
  if (!jobs.length) { $("#jobList", el).innerHTML = emptyState("jobs", "No analyses yet", "Start one from <b>Analyze Repository</b>.", `<a class="btn btn-secondary btn-sm" href="#/analyze" style="margin-top:8px">Analyze a repository</a>`); return; }
  if (!rows.length) { $("#jobList", el).innerHTML = `<div class="empty small">No jobs match this filter.</div>`; return; }
  $("#jobList", el).innerHTML = rows.map(j => {
    const pct = j.progress && j.progress.total ? Math.round(100 * j.progress.finished / j.progress.total) : 0;
    return `<button class="job-item ${j.id === selected ? "sel" : ""}" data-id="${esc(j.id)}" aria-current="${j.id === selected}">
      <div class="j-top"><span class="j-name">${esc(repoName(j.repo) || j.target)}</span>${jobBadge(j.status)}</div>
      <div class="j-sub"><span class="mono">${esc(j.release || j.target)}</span><span>·</span><span title="${esc(fmtDate(j.created))}">${esc(relTime(j.created))}</span>
        ${j.current_step ? `<span>·</span><span>${esc(j.current_step.replace("_", " "))}</span>` : ""}</div>
      ${ACTIVE(j.status) ? `<div class="progress" aria-label="${pct}% of steps finished"><div style="width:${pct}%"></div></div>` : ""}</button>`;
  }).join("");
  $$(".job-item", el).forEach(b => b.onclick = () => select(b.dataset.id));
}

function select(id, replace = false) {
  selected = id; lastSig = ""; paintList();
  const h = `#/jobs/${encodeURIComponent(id)}`;
  if (location.hash !== h) { replace ? history.replaceState(null, "", h) : (location.hash = h); }
  $("#jobDetail", el).innerHTML = `<div class="card-body">${skeleton(8, 18)}</div>`;
  stopJob && stopJob();
  stopJob = api.poll(() => api.getJob(id), 2500, (j) => ACTIVE(j.status) && selected === id && !el.classList.contains("hidden"),
    (j) => { if (selected === id) paintJob(j); }, (e) => { $("#jobDetail", el).innerHTML = `<div class="card-body">${errorBox(e.message)}</div>`; });
}

function paintJob(j) {
  current = j;
  const sig = JSON.stringify([j.status, (j.steps || []).map(s => [s.status, s.message, s.seconds]), j.queue_position, j.error, j.log_tail]);
  if (sig === lastSig) return;          // nothing changed: keep the DOM (focus, hover, scroll) as it is
  lastSig = sig;
  const focusKey = document.activeElement && $("#jobDetail", el).contains(document.activeElement)
    ? (document.activeElement.dataset.log || document.activeElement.id) : null;
  const steps = j.steps || [], fin = steps.filter(s => !["pending", "running"].includes(s.status)).length;
  const counts = {}; steps.forEach(s => counts[s.status] = (counts[s.status] || 0) + 1);
  const summaryDone = steps.find(s => s.name === "summary" && s.status === "done");
  const elapsed = j.started ? ((j.ended ? new Date(j.ended) : new Date()) - new Date(j.started)) / 1000 : null;
  const running = steps.find(s => s.status === "running");
  const wasLive = $("#liveLog", el); const keepScroll = wasLive && wasLive.scrollTop + wasLive.clientHeight >= wasLive.scrollHeight - 30;
  $("#jobDetail", el).innerHTML = `
    <div class="card-head" style="align-items:center">
      <div style="min-width:0"><h2 style="flex-wrap:wrap">${icon("analyze", 17)} ${esc(repoName(j.repo) || j.target)} ${jobBadge(j.status)}</h2>
        <p><span class="mono">${esc(j.release || "")}</span> → <span class="mono">${esc(j.post_release || "")}</span> · target <span class="mono">${esc(j.target)}</span>
          · created ${esc(fmtDate(j.created))}${elapsed !== null ? ` · ${ACTIVE(j.status) ? "running for" : "took"} ${fmtDur(elapsed)}` : ""}</p></div>
      <div class="row" style="flex-wrap:nowrap">
        ${summaryDone ? `<a class="btn btn-primary btn-sm" href="#/results/${encodeURIComponent(j.target)}">${icon("results", 14)} Open results</a>` : ""}
        ${ACTIVE(j.status) ? `<button class="btn btn-danger btn-sm" id="cancelJob">${icon("stop", 12)} Cancel job</button>` : ""}
      </div>
    </div>
    <div class="card-body stack">
      ${j.queue_position ? `<div class="banner info"><span class="b-ic">${icon("clock", 18)}</span><div class="small">Waiting in the queue (position ${j.queue_position}). One job runs at a time.</div></div>` : ""}
      ${j.error ? errorBox(j.error) : ""}
      <div>
        <div class="row" style="justify-content:space-between"><b class="small">${fin} of ${steps.length} steps finished</b>
          <div class="summary-strip">${Object.entries(counts).map(([k, n]) => `${stepBadge(k)}<span class="tiny muted" style="margin:0 6px 0 -4px">${n}</span>`).join("")}</div></div>
        <div class="progress" style="height:6px"><div style="width:${steps.length ? (100 * fin / steps.length) : 0}%"></div></div>
      </div>
      <ol class="stepper" aria-label="Pipeline steps">${steps.map((s, i) => `
        <li class="s-${s.status}">
          <span class="s-ic" aria-hidden="true">${stepIcon(s.status)}</span>
          <div><div class="s-title"><span>${i + 1}. ${esc(s.title)}</span>${stepBadge(s.status)}</div>
            <div class="s-desc">${esc(STEPS[s.name] || "")}</div>
            ${s.message ? `<div class="s-msg">${s.status === "skipped" ? "Skipped: " : s.status === "blocked" ? "Blocked: " : ""}${esc(s.message)}</div>` : ""}</div>
          <div class="s-side">${s.seconds != null ? `<span class="tiny muted num">${fmtDur(s.seconds)}</span>` : ""}
            ${s.status !== "pending" ? `<button class="btn btn-ghost btn-sm" data-log="${s.name}" data-title="${esc(s.title)}" aria-label="Open log of ${esc(s.title)}">${icon("terminal", 14)} Log</button>` : ""}</div>
        </li>`).join("")}</ol>
      ${running ? `<div><div class="row" style="justify-content:space-between;margin-bottom:6px"><b class="small">${icon("terminal", 14)} Live log: ${esc(running.title)}</b>
          <span class="tiny muted">updates every 2.5 s</span></div>
        <div class="term"><div class="term-body short" id="liveLog">${renderLines(j.log_tail || "(waiting for output…)", true)}</div></div></div>` : ""}
    </div>`;
  if (focusKey) ($(`#jobDetail [data-log="${focusKey}"]`, el) || $(`#${focusKey}`, el))?.focus();
  const live = $("#liveLog", el); if (live && (keepScroll || !wasLive)) live.scrollTop = live.scrollHeight;
  if (!ACTIVE(j.status)) refreshList();
}

async function confirmCancel(j) {
  const running = (j.steps || []).find(s => s.status === "running");
  const v = await dialog({ title: "Cancel this job?", body: `<p class="small">The running step (${esc(running ? running.title : "queued")}) is stopped and the remaining steps are marked cancelled. Outputs of finished steps are kept.</p>`,
    actions: [{ label: "Keep running", value: null, autofocus: true }, { label: "Cancel job", value: "yes", kind: "btn-danger" }] });
  if (v !== "yes") return;
  try { await api.cancelJob(j.id); toast("Job cancelled"); select(j.id, true); refreshList(); } catch (e) { toast(e.message, "bad"); }
}

// ---------- logs ----------
function classify(t) {
  if (/^\$ /.test(t)) return "cmd";
  const words = t.replace(/[A-Za-z]:\[^\s']+|\/[\w./-]+/g, " ");   // ignore file paths ("exception-handling-replication")
  if (/\b(error|traceback|fatal|halted|failed|exit code [1-9])\b|\bexception\b(?!-)/i.test(words) && !/no errors/i.test(words)) return "err";
  if (/\b(warn(ing)?|deprecat\w*)\b/i.test(words)) return "warn";
  if (/(\bdone\b|wrote |finished|reused|\bok\b)/i.test(t)) return "okk";
  return "";
}
function renderLines(text, short = false) {
  const lines = text.replace(/\s+$/, "").split("\n");
  const start = short ? 0 : 0;
  return lines.map((ln, i) => {
    const m = ln.match(/^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ) \| (.*)$/);
    const ts = m ? m[1].slice(11, 19) : "", body = m ? m[2] : ln;
    return `<div class="ln"><span class="n">${start + i + 1}</span><span class="ts">${ts}</span><span class="${classify(body)}">${esc(body) || " "}</span></div>`;
  }).join("");
}
async function openLog(jobId, step, title) {
  const tb = `<div class="term-bar" role="toolbar" aria-label="Log tools">
      <button data-a="ts" aria-pressed="true">${icon("clock", 13)} Timestamps</button>
      <button data-a="wrap" aria-pressed="true">${icon("wrap", 13)} Wrap</button>
      <button data-a="copy">${icon("copy", 13)} Copy</button>
      <a data-a="dl" href="${api.logUrl(jobId, step)}" download="${esc(jobId)}-${esc(step)}.log" style="color:#CBD5E1;font:12px var(--font);display:inline-flex;gap:6px;align-items:center;padding:4px 8px;text-decoration:none">${icon("downloads", 13)} Download</a>
      <button data-a="end">${icon("arrowDown", 13)} Jump to end</button>
      <button data-a="reload">${icon("refresh", 13)} Refresh</button>
      <span style="margin-left:auto" class="tiny" id="logMeta"></span></div>`;
  const body = html(`<div class="term" style="height:100%;display:flex;flex-direction:column">${tb}<div class="term-body" style="max-height:none;flex:1" id="logBody">${skeleton(6)}</div></div>`);
  const d = drawer({ title: `${icon("terminal", 16)} ${esc(title)} <span class="muted small" style="font-weight:400">log</span>`, body });
  d.body.style.padding = "0";
  let text = "";
  const load = async () => {
    try { text = await api.getLog(jobId, step); $("#logBody", body).innerHTML = renderLines(text);
      $("#logMeta", body).textContent = `${text.trim().split("\n").length} lines`; }
    catch (e) { $("#logBody", body).innerHTML = `<div class="ln"><span class="n"></span><span></span><span class="err">${esc(e.message)}</span></div>`; }
  };
  await load();
  $$("[data-a]", body).forEach(b => b.onclick = (e) => {
    const a = b.dataset.a;
    if (a === "ts") { const on = b.getAttribute("aria-pressed") !== "true"; b.setAttribute("aria-pressed", on); body.classList.toggle("no-ts", !on); }
    if (a === "wrap") { const on = b.getAttribute("aria-pressed") !== "true"; b.setAttribute("aria-pressed", on); body.classList.toggle("nowrap", !on); }
    if (a === "copy") copyText(text, "Log copied");
    if (a === "end") { const lb = $("#logBody", body); lb.scrollTop = lb.scrollHeight; }
    if (a === "reload") load();
    if (a === "dl") return; e.preventDefault?.();
  });
}
