// Research Results for one analysed release: header, metric cards, caveats, models (RQ1/2), anti-patterns,
// ML (RQ3), SHAP (RQ4). Everything rendered comes from results/new/<target>/summary.json and its files.
import * as api from "../api.js";
import { icon } from "../icons.js";
import { $, $$, copyText, dialog, drawer, emptyState, errorBox, esc, fmt, fmtDate, fmtInt, fmtP, fmtPct, fmtSigned, html,
         infoTip, isNum, repoName, shortSha, skeleton, sortableTable } from "../ui.js";
import { hbar, diverging } from "../charts.js";
import { mlPanel } from "../components/mlpanel.js";
import { CARDS, MODEL_INFO, describeMetric, explainPredictor } from "../glossary.js";

let el, ctx, index = [], current = null, S = null;

export default {
  mount(root, c) {
    el = root; ctx = c;
    el.innerHTML = `<div class="page-head"><div><h1>Research results</h1><p>Results of one analysed release, from the authors' explanatory models to our ML and SHAP extensions.</p></div>
      <div class="row"><label class="sr-only" for="resPick">Analysed release</label><select class="input" id="resPick" style="min-width:280px"></select></div></div>
      <div id="resBody">${skeleton(6, 20)}</div>`;
    $("#resPick", el).onchange = (e) => ctx.navigate(`#/results/${encodeURIComponent(e.target.value)}`);
    window.addEventListener("themechange", () => { if (S && !el.classList.contains("hidden")) paint(); });
  },
  async show(param) {
    try { index = await api.listResults(); }
    catch (e) { $("#resBody", el).innerHTML = errorBox(e.message); return; }
    if (!index.length) {
      $("#resPick", el).innerHTML = ""; $("#resBody", el).innerHTML = `<div class="card">${emptyState("results", "No results yet",
        "Results appear here when an analysis job reaches its summary step.", `<a class="btn btn-primary btn-sm" href="#/analyze" style="margin-top:8px">Analyze a repository</a>`)}</div>`; return;
    }
    const t = param && index.some(i => i.target === param) ? param : index[0].target;
    $("#resPick", el).innerHTML = index.map(i => `<option value="${esc(i.target)}" ${i.target === t ? "selected" : ""}>${esc(repoName(i.repo))} · ${esc(i.release)}</option>`).join("");
    if (t === current && S) return;
    current = t; $("#resBody", el).innerHTML = skeleton(10, 18);
    try { S = await api.getSummary(t); paint(); } catch (e) { $("#resBody", el).innerHTML = errorBox(e.message); }
  },
};

function card(id, title, sub, bodyHtml, headExtra = "") {
  return `<section class="card" id="${id}"><div class="card-head"><div><h2>${title}</h2>${sub ? `<p>${sub}</p>` : ""}</div>${headExtra}</div><div class="card-body">${bodyHtml}</div></section>`;
}
const unavailable = (what, why) => `<div class="empty small" style="padding:22px"><div class="e-ic">${icon("info", 20)}</div><h3>${esc(what)} not available</h3><p>${why}</p></div>`;

function paint() {
  const s = S, p = s.provenance || {}, d = s.dataset || {}, dm = s.defect_mining || {}, eh = s.eh_profile || {};
  const commit = (lab, x) => x ? `<tr><th scope="row">${lab}</th><td class="mono">${esc(x.tag)}</td><td class="mono">${esc(shortSha(x.commit))}
      <button class="btn btn-ghost btn-sm" data-copy="${esc(x.commit)}" aria-label="Copy commit ${esc(x.commit)}">${icon("copy", 13)}</button></td><td>${esc(fmtDate(x.commit_date))}</td></tr>`
    : `<tr><th scope="row">${lab}</th><td colspan="3" class="muted">start of history</td></tr>`;
  const trk = s.tracker || {}, trkText = trk.type === "jira" ? `Jira (${(trk.project_keys || []).join(", ") || "auto"})` : trk.type === "github" ? "GitHub Issues" : "none";
  const metric = (ic, label, val, sub, tip) => `<div class="metric"><div class="m-top"><span class="m-ic">${icon(ic, 14)}</span>${esc(label)} ${infoTip(tip)}</div>
    <div class="m-val">${val}</div>${sub ? `<div class="m-sub">${sub}</div>` : ""}</div>`;
  const defFiles = dm.defective_files ?? d.post_release_defective_files;

  $("#resBody", el).innerHTML = `<div class="stack-lg">
    <section class="card"><div class="card-body">
      <div class="row" style="justify-content:space-between;align-items:flex-start">
        <div><h2 style="font-size:18px;display:flex;gap:8px;align-items:center">${icon("github", 18)} <a href="${esc(s.repo)}" target="_blank" rel="noopener">${esc(repoName(s.repo))}</a></h2>
          <div class="row small muted" style="margin-top:6px;gap:8px"><span class="badge b-acc">release ${esc(s.tags.release)}</span><span class="badge b-mute">${esc(s.language)}</span>
            <span class="badge b-mute">tracker: ${esc(trkText)}</span><span class="badge b-mute">product metrics: ${esc(s.product_metrics_backend || "—")}</span>
            <span>generated ${esc(fmtDate(s.generated))}</span></div></div>
        <div class="row"><button class="btn btn-secondary btn-sm" id="copyRepro">${icon("copy", 13)} Copy reproducibility details</button>
          <a class="btn btn-secondary btn-sm" href="#/downloads/${encodeURIComponent(s.target)}">${icon("downloads", 13)} Artifacts</a></div>
      </div>
      <div class="table-wrap" style="margin-top:12px"><table class="t t-mid"><thead><tr><th>Role</th><th>Tag</th><th>Commit</th><th>Commit date</th></tr></thead>
        <tbody>${commit("Previous release", p.prev_release)}${commit("Release (studied)", p.release)}${commit("Latest post-release", p.post_release)}</tbody></table></div>
    </div></section>

    <div class="metrics">
      ${metric("file", "Source files studied", fmtInt(d.release_files), "", CARDS.files)}
      ${metric("bug", "Post-release defective files", fmtInt(defFiles), isNum(defFiles) && d.release_files ? fmtPct(100 * defFiles / d.release_files) + " of files" : "", CARDS.defective)}
      ${metric("bug", "Post-release bugs", fmtInt(dm.post_release_defect_issues), "", CARDS.bugs)}
      ${metric("brace", "Files with catch blocks", fmtInt(eh.files_with_catch), "", CARDS.catchFiles)}
      ${metric("target", "Defective files with catch", fmtInt(d.defective_files_with_catch), isNum(d.defective_files_with_catch) && eh.files_with_catch ? fmtPct(100 * d.defective_files_with_catch / eh.files_with_catch) + " prevalence" : "", CARDS.defCatch)}
      ${metric("layers", "Catch / try blocks", `${fmtInt(eh.catch_blocks)} <span class="muted" style="font-size:15px">/ ${fmtInt(eh.try_blocks)}</span>`, "", CARDS.blocks)}
      ${metric("zap", "Possible exceptions / try", fmt(eh.mean_possible_exceptions_per_try, 2), "", CARDS.pe)}
    </div>

    ${(s.caveats || []).length ? `<section class="card"><div class="card-head"><div><h2>${icon("alert", 17)} Read with care</h2><p>Limitations that apply to this run. They are listed here, not hidden in tooltips.</p></div></div>
      <div class="card-body"><div class="caveats">${s.caveats.map(c => `<div class="caveat"><span class="c-ic">${icon("alert", 16)}</span><div>${esc(c)}</div></div>`).join("")}</div>
      <details class="acc" style="margin-top:12px"><summary>${icon("info", 15)} Method notes<span class="chev">${icon("chevDown", 16)}</span></summary><div class="acc-body small stack" style="gap:6px;padding-top:12px">
        <div>Models follow the authors' R code (rms::lrm on log10(x+1) metrics; Spearman |ρ| &gt; 0.7 and redundancy filtering; a predictor budget of files/15;
          fast backward elimination at p = 0.05; optimism-reduced Nagelkerke R² from 1,000 bootstrap samples), with the one-line BSFC bug fixed.</div>
        <div>Only files with at least one catch block (and try data) are modelled, as in the paper. Results are associations, not causal effects.</div>
        <div>ML: untuned learners, repeated stratified 5-fold CV; the p-values come from the Nadeau–Bengio corrected resampled t-test and are not corrected for multiple comparisons.</div></div></details>
      </div></section>` : ""}

    <div id="secModels"></div><div id="secAP"></div><div id="secML"></div><div id="secSHAP"></div>
  </div>`;
  $$("[data-copy]", el).forEach(b => b.onclick = () => copyText(b.dataset.copy, "Commit ID copied"));
  $("#copyRepro", el).onclick = () => copyText(reproText(), "Reproducibility details copied");
  paintModels(); paintAP(); paintML(); paintSHAP();
}

function reproText() {
  const s = S, p = s.provenance || {}, line = (l, x) => x ? `- ${l}: ${x.tag} (${x.commit}, ${x.commit_date})` : `- ${l}: start of history`;
  const t = s.tracker || {};
  return [`# ${repoName(s.repo)} — ExceptionLab analysis (${s.target})`, `Repository: ${s.repo}`, line("Previous release", p.prev_release), line("Release", p.release),
    line("Latest post-release", p.post_release), `Language: ${s.language}`, `Issue tracker: ${t.type}${t.base ? " " + t.base : ""}${t.project_keys ? " keys " + t.project_keys.join(",") : ""}`,
    `File filters: include ${s.file_filters?.include} | exclude ${s.file_filters?.exclude}`, `Product metrics: ${s.product_metrics_backend}`,
    `Summary generated: ${s.generated}`, `Regenerate: ./envrun.sh python src/pipeline/run_target.py ${s.target}`].join("\n");
}

// ---------- models (RQ1 / RQ2) ----------
function paintModels() {
  const m = S.models, box = $("#secModels", el);
  if (!m || !m.presented.length) { box.innerHTML = card("cardModels", `${icon("flask", 17)} Explanatory Models`, "", unavailable("Explanatory models",
    S.dataset && S.dataset.has_outcome === false ? "No defect labels: choose an issue tracker to fit the models." : "The models step was skipped or failed for this release; see its job log.")); return; }
  const ref = S.paper_reference, maxR2 = Math.max(0.5, ...m.presented.map(x => x.r2_optimism_reduced || 0), ...(ref ? Object.values(ref.r2_optimism_reduced) : [0]));
  const base = m.presented.find(x => x.model === "BASE");
  const bar = (x) => { const v = x.r2_optimism_reduced, pr = ref ? ref.r2_optimism_reduced[x.model] : null;
    return `<div class="r2bar"><span class="num" style="width:44px;font-weight:650">${fmt(v)}</span><div class="track" aria-hidden="true">
      <div class="fill ${x.model === "BASE" ? "base" : ""}" style="width:${Math.max(0, 100 * (v || 0) / maxR2)}%"></div>
      ${pr !== null && pr !== undefined ? `<div class="mark" style="left:${100 * pr / maxR2}%" title="paper ${pr}"></div>` : ""}</div></div>`; };
  const delta = (x) => (x.model !== "BASE" && base && isNum(x.r2_optimism_reduced) && isNum(base.r2_optimism_reduced))
    ? `<span class="${x.r2_optimism_reduced - base.r2_optimism_reduced >= 0 ? "delta-pos" : "delta-neg"} small">${fmtSigned(x.r2_optimism_reduced - base.r2_optimism_reduced)} vs BASE</span>` : "";
  const rows = m.presented.map((x, i) => `<tr>
      <td><b>${x.model}</b> ${infoTip(MODEL_INFO[x.model])}<div class="tiny muted">${esc(MODEL_INFO[x.model].split(":")[0].split("(")[0])}</div>
        ${(x.dropped_base_significant || []).length ? `<div class="badge b-warn" style="margin-top:4px" data-tip="The budget-based reduction dropped BASE-significant ${esc(x.dropped_base_significant.join(", "))}; see Read with care.">${icon("alert", 11)} dropped BASE predictor</div>` : ""}</td>
      <td style="min-width:190px">${bar(x)}${delta(x)}</td><td class="r">${fmt(x.r2_apparent)}</td>
      ${ref ? `<td class="r">${fmt(ref.r2_optimism_reduced[x.model], 2)}</td>` : ""}
      <td class="r">${fmtInt(x.files)}</td><td class="r">${fmtInt(x.potential_predictors)} <span class="tiny muted">/ ${x.budget}</span></td>
      <td>${x.predictors.length ? x.predictors.map((q, j) => `<button class="pchip ${q.group !== "traditional" ? "eh" : ""}" data-pm="${i}" data-pq="${j}"
          aria-label="${esc(q.name)} details"><span class="dir ${q.direction === "+" ? "up" : "down"}">${q.direction === "+" ? "↑" : "↓"}</span>${esc(q.name)}</button>`).join("") : '<span class="muted small">none</span>'}</td></tr>`).join("");
  box.innerHTML = card("cardModels", `${icon("flask", 17)} Explanatory Models`,
    "Do exception-handling metrics explain post-release defects beyond traditional software metrics? BSFC tests exception-flow characteristics (RQ1), BSAP tests anti-patterns (RQ2).",
    `<div class="table-wrap"><table class="t"><thead><tr><th>Model</th><th>Optimism-reduced R² ${infoTip("Nagelkerke R² after 1,000-sample bootstrap optimism correction, on the simplified model. Higher = more of the variation in post-release defects explained.")}</th>
      <th class="r">Apparent R²</th>${ref ? `<th class="r">Paper R² ${infoTip(`The paper's value for ${ref.release} (Table 4). Shown as the dark tick on the bar.`)}</th>` : ""}
      <th class="r">Files</th><th class="r">Potential predictors ${infoTip("Metrics left after correlation and redundancy filtering / the predictor budget (files ÷ 15).")}</th><th>Significant predictors ${infoTip("Click a predictor for details. ↑ = higher values go with more defects. Indigo = exception-handling metric.")}</th></tr></thead>
      <tbody>${rows}</tbody></table></div>
      <div class="legend" style="margin-top:10px"><span><i style="background:var(--accent)"></i>exception-handling predictor</span><span><i style="background:var(--surface-3);border:1px solid var(--border-2)"></i>traditional predictor</span>
        ${ref ? `<span><i style="background:var(--text);width:3px"></i>paper R²</span>` : ""}</div>
      ${(m.preliminary_all_files || []).length ? `<details class="acc" style="margin-top:12px"><summary>${icon("layers", 15)} Preliminary models on all files (paper §3.6)<span class="chev">${icon("chevDown", 16)}</span></summary>
        <div class="acc-body" style="padding-top:10px"><table class="t"><thead><tr><th>Model</th><th class="r">R² (opt.)</th><th>Significant</th></tr></thead><tbody>
        ${m.preliminary_all_files.map(x => `<tr><td class="mono">${esc(x.model)}</td><td class="r">${fmt(x.r2_optimism_reduced)}</td><td class="small">${esc(x.significant.join(", "))}</td></tr>`).join("")}</tbody></table></div></details>` : ""}`);
  $$("[data-pm]", box).forEach(b => b.onclick = () => openPredictor(m.presented[b.dataset.pm], m.presented[b.dataset.pm].predictors[b.dataset.pq]));
}

function openPredictor(model, q) {
  const grp = { traditional: "Traditional metric", flow: "Exception-flow characteristic", "anti-pattern": "Exception-handling anti-pattern / catch metric" }[q.group] || q.group;
  drawer({ narrow: true, title: `${esc(q.name)}`, body: `<div class="stack">
    <div class="row"><span class="badge ${q.group === "traditional" ? "b-mute" : "b-acc"}">${esc(grp)}</span><span class="badge b-mute">model ${model.model}</span></div>
    <p class="small" style="margin:0">${esc(describeMetric(q.name))}</p>
    <dl class="kv"><dt>Direction</dt><dd><b class="${q.direction === "+" ? "delta-neg" : "delta-pos"}">${q.direction === "+" ? "↑ positive" : "↓ negative"}</b> association with post-release defects</dd>
      <dt>Wald χ²</dt><dd class="num">${fmt(q.wald_chi2, 2)} <span class="muted small">(p ${fmtP(q.p_value)})</span></dd>
      <dt>+10% of mean</dt><dd class="num">${fmtSigned(q.effect_pct, 1)}% change in defect probability (relative)</dd>
      <dt>Column</dt><dd class="mono small">${esc(q.metric)}</dd></dl>
    <div class="banner info"><span class="b-ic">${icon("info", 16)}</span><div class="small">${esc(explainPredictor(q))}</div></div></div>` });
}

// ---------- anti-patterns ----------
function paintAP() {
  const eh = S.eh_profile, box = $("#secAP", el);
  if (!eh || !eh.anti_patterns) { box.innerHTML = card("cardAP", `${icon("brace", 17)} Exception-Handling Anti-Patterns`, "", unavailable("Anti-pattern profile", "The exception-flow analysis did not produce file-level metrics for this release.")); return; }
  box.innerHTML = card("cardAP", `${icon("brace", 17)} Exception-Handling Anti-Patterns`,
    `How often each of the 17 anti-patterns occurs among the ${fmtInt(eh.catch_blocks)} catch blocks. Descriptive: it does not need defect labels.`,
    `<div class="row" style="justify-content:space-between;margin-bottom:10px"><div class="input-wrap" style="width:280px"><span class="lead">${icon("search", 14)}</span>
      <input class="input" id="apSearch" placeholder="Filter anti-patterns" aria-label="Filter anti-patterns"></div><span class="small muted" id="apCount"></span></div>
     <div class="grid-2" style="align-items:start"><div class="chart" id="apChart"></div><div id="apTable"></div></div>`);
  const rows = eh.anti_patterns;
  const tbl = sortableTable($("#apTable", box), [
    { key: "anti_pattern", label: "Anti-pattern" },
    { key: "catch_blocks", label: "Catch blocks", num: true, render: r => fmtInt(r.catch_blocks) },
    { key: "pct_of_catch_blocks", label: "% of catch", num: true, render: r => fmtPct(r.pct_of_catch_blocks) },
    { key: "files", label: "Files", num: true, render: r => fmtInt(r.files) }], rows, { sortKey: "catch_blocks", filterKeys: ["anti_pattern"] });
  const chart = (q) => {
    const f = rows.filter(r => r.anti_pattern.toLowerCase().includes(q)).sort((a, b) => b.pct_of_catch_blocks - a.pct_of_catch_blocks).slice(0, 12);
    $("#apCount", box).textContent = `${f.length} of ${rows.length} shown in chart`;
    if (!f.length) { $("#apChart", box).innerHTML = '<div class="empty small">No anti-pattern matches.</div>'; return; }
    hbar($("#apChart", box), f.map(r => ({ label: r.anti_pattern, value: +r.pct_of_catch_blocks,
      tip: `<b>${esc(r.anti_pattern)}</b><br>${fmtPct(r.pct_of_catch_blocks)} of catch blocks · ${fmtInt(r.catch_blocks)} blocks in ${fmtInt(r.files)} files` })),
      { title: "Share of catch blocks per anti-pattern", valueFmt: v => `${v.toFixed(v < 10 ? 1 : 0)}%`, color: "var(--accent)" });
  };
  chart("");
  $("#apSearch", box).addEventListener("input", (e) => { const q = e.target.value.trim().toLowerCase(); tbl.setFilter(q); chart(q); });
}

// ---------- ML (RQ3) ----------
function paintML() {
  const ml = S.ml, box = $("#secML", el);
  if (!ml) { box.innerHTML = card("cardML", `${icon("target", 17)} Machine-Learning Prediction (RQ3)`, "", unavailable("ML results", "The ML step was skipped or failed (it needs the model step's merged dataset and enough defective files).")); return; }
  box.innerHTML = card("cardML", `${icon("target", 17)} Machine-Learning Prediction (RQ3)`,
    "Do exception-handling metrics improve prediction over traditional metrics? Mean ± std over repeated stratified 5-fold CV.", '<div id="mlPanel"></div>');
  mlPanel($("#mlPanel", box), ml.results, ml.uplift || [], "resml");
}

// ---------- SHAP (RQ4) ----------
function paintSHAP() {
  const sh = S.shap, box = $("#secSHAP", el);
  if (!sh) { box.innerHTML = card("cardSHAP", `${icon("zap", 17)} What Drives the Predictions? (RQ4)`, "", unavailable("SHAP explanations", "The SHAP step was skipped or failed for this release.")); return; }
  const unit = sh.learner === "RF" ? "probability" : "log-odds";
  box.innerHTML = card("cardSHAP", `${icon("zap", 17)} What Drives the Predictions? (RQ4)`,
    `TreeSHAP on the best tree model (${esc(sh.learner === "RF" ? "Random Forest" : sh.learner === "XGB" ? "XGBoost" : sh.learner)}), refit on all files with catch blocks. Mean |SHAP| in ${unit} units.`,
    `<div class="grid-2" style="align-items:start">
       <div><div class="chart" id="shapChart"></div>
         <div class="legend" style="margin-top:8px"><span><i class="hatch" style="background-color:var(--eh)"></i>exception-handling metric</span><span><i style="background:var(--trad)"></i>traditional metric</span></div></div>
       <div><h3 class="small" style="margin-bottom:8px">Most influential exception-handling features</h3><div id="shapTable"></div>
         <div class="row" style="margin-top:12px">${sh.per_file_values ? `<button class="btn btn-secondary btn-sm" id="perFile">${icon("file", 13)} View per-file SHAP details</button>` : ""}
           <a class="btn btn-ghost btn-sm" href="${esc(sh.figures.beeswarm)}" target="_blank" rel="noopener">${icon("external", 13)} Beeswarm plot</a></div></div></div>`);
  hbar($("#shapChart", box), sh.top_features.map(f => ({ label: f.name, value: f.mean_abs_shap, hatch: f.group !== "base",
    color: f.group === "base" ? "var(--trad)" : null, tip: `<b>${esc(f.name)}</b><br>${f.group === "base" ? "traditional" : "exception-handling"} metric<br>mean |SHAP| ${f.mean_abs_shap.toFixed(4)} (${unit})` })),
    { title: "Top 15 features by mean absolute SHAP", valueFmt: v => v.toFixed(v < 0.01 ? 4 : 3), barH: 16 });
  sortableTable($("#shapTable", box), [
    { key: "rank", label: "#", num: true, render: r => `${r.rank}<span class="tiny muted"> (${r.overall_rank})</span>` },
    { key: "name", label: "Feature", render: r => `${esc(r.name)} ${infoTip(describeMetric(r.name))}` },
    { key: "direction", label: "Dir.", render: r => `<b class="${r.direction === "+" ? "delta-neg" : "delta-pos"}">${r.direction === "+" ? "↑" : "↓"}</b>` },
    { key: "matches_significant_predictor", label: "Also significant in models?", render: r => r.matches_significant_predictor
      ? `<span class="badge b-ok" data-tip="${esc(r.matches_significant_predictor)}">${icon("check", 11)} yes</span>` : '<span class="muted small">no</span>' }],
    sh.top_eh, { sortKey: "rank", desc: false });
  const pf = $("#perFile", box); if (pf) pf.onclick = () => perFile(sh.per_file_values, unit);
}

async function perFile(path, unit) {
  const body = html(`<div class="stack"><div class="row"><div class="input-wrap" style="flex:1;min-width:240px"><span class="lead">${icon("search", 14)}</span>
      <input class="input" id="pfSearch" placeholder="Filter files by path" aria-label="Filter files"></div>
      <select class="input" id="pfFile" style="flex:2;min-width:280px" aria-label="File"></select></div>
    <div id="pfInfo" class="small"></div><div class="chart" id="pfChart">${skeleton(6)}</div><div id="pfTable"></div></div>`);
  dialog({ title: "Per-file SHAP explanations", body, wide: true, actions: [{ label: "Close", value: null }] });
  let rows;
  try { rows = await api.getCsv(path); } catch (e) { $("#pfChart", body).innerHTML = errorBox(e.message); return; }
  rows.sort((a, b) => b.predicted - a.predicted);
  const feats = Object.keys(rows[0]).filter(k => k.endsWith("|shap")).map(k => k.slice(0, -5));
  const names = S.shap.per_file_names || {};
  const prettyCol = (c) => c === "all other features" ? c : (names[c] || c);
  const fill = (q) => { const f = rows.filter(r => r["File.Path"].toLowerCase().includes(q));
    $("#pfFile", body).innerHTML = f.slice(0, 400).map(r => `<option value="${esc(r["File.Path"])}">${(+r.predicted).toFixed(2)} · ${+r.defective ? "defective · " : ""}${esc(r["File.Path"].split("/").slice(-2).join("/"))}</option>`).join("");
    draw(); };
  const draw = () => {
    const r = rows.find(x => x["File.Path"] === $("#pfFile", body).value); if (!r) { $("#pfChart", body).innerHTML = '<div class="empty small">No file matches.</div>'; $("#pfTable", body).innerHTML = ""; return; }
    const contrib = feats.map(f => ({ f, label: f === "other_features" ? "all other features" : f, value: +r[`${f}|shap`], v: r[`${f}|value`] }))
      .sort((a, b) => Math.abs(b.value) - Math.abs(a.value));
    $("#pfInfo", body).innerHTML = `<span class="mono">${esc(r["File.Path"])}</span> · predicted defect probability <b>${(+r.predicted).toFixed(3)}</b> ·
      label <b>${+r.defective ? "defective" : "not defective"}</b> <span class="muted">(contributions in ${unit}; ${feats.length - 1} most important features shown individually)</span>`;
    diverging($("#pfChart", body), contrib.slice(0, 12).map(c => ({ label: prettyCol(c.label), value: c.value,
      tip: `<b>${esc(prettyCol(c.label))}</b><br>value ${c.v === undefined ? "—" : esc(niceVal(+c.v))}<br>SHAP ${(c.value > 0 ? "+" : "") + c.value.toFixed(4)}` })),
      { title: "Feature contributions for one file" });
    sortableTable($("#pfTable", body), [{ key: "label", label: "Feature", render: x => esc(prettyCol(x.label)) },
      { key: "v", label: "Metric value", num: true, render: x => x.v === undefined ? "—" : esc(niceVal(+x.v)) },
      { key: "value", label: "SHAP", num: true, render: x => `<span class="${x.value >= 0 ? "delta-neg" : "delta-pos"}">${fmtSigned(x.value, 4)}</span>`, sort: x => Math.abs(x.value) }],
      contrib, { sortKey: "value" });
  };
  fill(""); $("#pfSearch", body).addEventListener("input", (e) => fill(e.target.value.trim().toLowerCase()));
  $("#pfFile", body).onchange = draw;
}

// metric values: integers as integers (with separators), others to 3 significant digits
const niceVal = (v) => Number.isInteger(v) ? v.toLocaleString("en-US") : Math.abs(v) >= 1000 ? Math.round(v).toLocaleString("en-US") : (+v.toPrecision(3)).toString();
