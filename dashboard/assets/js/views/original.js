// Original Study: fixed reproduction results on the paper's own data (Phase 0, Phase A) plus newly collected
// contexts (Phase 2), kept visually separate. All numbers are read from the stored CSVs in results/.
import * as api from "../api.js";
import { icon } from "../icons.js";
import { $, $$, errorBox, esc, fmt, fmtSigned, infoTip, isNum, skeleton, sortableTable } from "../ui.js";
import { hbar } from "../charts.js";
import { mlPanel } from "../components/mlpanel.js";

let el, loaded = false;
const PROJ = { "umbraco-7.6": "Umbraco 7.6 (C#)", "hadoop-2.6": "Hadoop 2.6 (Java)", "hibernate-5.0": "Hibernate 5.0 (Java)" };
const RUNS = { authors: "Authors' released output (base_test_2_BKP.csv)", asis: "Ours: authors' code as released", fixed: "Ours: authors' code + BSFC bug fix" };

export default {
  mount(root) {
    el = root;
    el.innerHTML = `<div class="stack-lg">
      <div class="banner info"><span class="b-ic">${icon("info", 18)}</span><div class="small"><b>Fixed reproduction results, not a live analysis.</b>
        These come from running the authors' released package (scripts and data) and our extensions on the paper's three projects.
        Regenerate them with <code>src/reproduce/run_original.R</code>, <code>build_comparison.py</code> and the Phase A notebook (docs/REPRODUCTION.md).</div></div>
      <section class="card" id="oTable4"><div class="card-head"><div><h2><span class="step-num">A</span> Paper Table 4: reproduction</h2>
        <p>Optimism-reduced Nagelkerke R² of the simplified models (files with catch blocks), from the paper, from the authors' own released output, and from our runs.</p></div></div>
        <div class="card-body">${skeleton(5)}</div></section>
      <section class="card" id="oNew"><div class="card-head"><div><h2><span class="step-num">B</span> New release contexts <span class="badge b-acc">newly collected</span></h2>
        <p>The authors' pipeline (bug-fixed) on releases we collected ourselves, next to the paper's value for the same project. These are new data, not the paper's.</p></div></div>
        <div class="card-body">${skeleton(4)}</div></section>
      <section class="card" id="oML"><div class="card-head"><div><h2><span class="step-num">C</span> ML on the released data (RQ3)</h2>
        <p>Our extension on the authors' released dataset: do exception-handling metrics improve prediction?</p></div><div class="seg" role="group" aria-label="Project" id="mlProj"></div></div>
        <div class="card-body"><div id="oMLPanel">${skeleton(5)}</div></div></section>
      <section class="card" id="oSHAP"><div class="card-head"><div><h2><span class="step-num">D</span> SHAP on the released data (RQ4)</h2>
        <p>Mean |SHAP| of the 12 most influential features for the best tree model of each original project.</p></div></div>
        <div class="card-body"><div class="grid-2" id="oSHAPGrid" style="grid-template-columns:repeat(auto-fit,minmax(320px,1fr))">${skeleton(5)}</div>
          <div class="legend" style="margin-top:10px"><span><i class="hatch" style="background-color:var(--eh)"></i>exception-handling metric</span><span><i style="background:var(--trad)"></i>traditional metric</span></div></div></section>
    </div>`;
  },
  async show() {
    if (loaded) return; loaded = true;
    await Promise.all([table4(), contexts(), ml(), shap()]);
  },
};

const body = (id) => $(`#${id} .card-body`, el);

async function table4() {
  let rows, t5;
  try { rows = await api.getCsv("/results/reproduction_comparison.csv"); } catch (e) { body("oTable4").innerHTML = errorBox(e.message); return; }
  try { t5 = await api.getCsv("/results/reproduction_table5.csv"); } catch { t5 = []; }
  const key = (r) => `${r.Project}|${r.Model}`, by = {};
  rows.forEach(r => { (by[key(r)] ??= { project: r.Project, model: r.Model, paper: +r["Original R2"] })[
    r.Run === RUNS.authors ? "authors" : r.Run === RUNS.asis ? "asis" : r.Run === RUNS.fixed ? "fixed" : "other"] = +r["Reproduced R2"]; });
  const piv = Object.values(by).map(x => ({ ...x, diff: isNum(x.fixed) ? x.fixed - x.paper : null }));
  const maxAbs = Math.max(...piv.filter(x => isNum(x.diff)).map(x => Math.abs(x.diff)));
  const bsfcAsIs = piv.filter(x => x.model === "BSFC").map(x => Math.abs(x.asis - x.paper));
  const chi = t5.filter(r => isNum(r.chi2_diff)).map(r => Math.abs(+r.chi2_diff));
  body("oTable4").innerHTML = `
    <div class="metrics" style="margin-bottom:14px">
      <div class="metric"><div class="m-top"><span class="m-ic">${icon("check", 14)}</span>Bug-fixed run vs paper</div><div class="m-val">±${fmt(maxAbs)}</div>
        <div class="m-sub">largest |difference| over all ${piv.length} R² values</div></div>
      <div class="metric"><div class="m-top"><span class="m-ic">${icon("alert", 14)}</span>BSFC as released vs paper</div><div class="m-val">up to ${fmt(Math.max(...bsfcAsIs), 2)}</div>
        <div class="m-sub">the released code fits BSAP data into BSFC</div></div>
      ${chi.length ? `<div class="metric"><div class="m-top"><span class="m-ic">${icon("layers", 14)}</span>Table 5 predictors</div><div class="m-val">${chi.length}/${t5.length}</div>
        <div class="m-sub">reproduced; max |Δχ²| ${fmt(Math.max(...chi), 3)}</div></div>` : ""}
    </div>
    <div id="t4"></div>
    <p class="small muted" style="margin-top:10px">${maxAbs <= 0.0045 ? `With the one-line fix, every value matches the paper within ±${fmt(maxAbs)} (bootstrap noise; the authors set no random seed).` : ""}
      The fix comments out <code>data_list = all_list_omitted_m2</code> in <code>dataApplyReductionByModel()</code>, which made "BSFC" a second BSAP model.</p>`;
  sortableTable($("#t4", el), [
    { key: "project", label: "Project" }, { key: "model", label: "Model" },
    { key: "paper", label: "Paper", num: true, render: r => fmt(r.paper, 2) },
    { key: "authors", label: "Authors' output", num: true, render: r => fmt(r.authors), tip: "output/base_test_2_BKP.csv shipped in the authors' package" },
    { key: "asis", label: "Ours, as released", num: true, render: r => `<span class="${Math.abs(r.asis - r.paper) > 0.01 ? "delta-neg" : ""}">${fmt(r.asis)}</span>` },
    { key: "fixed", label: "Ours, bug fixed", num: true, render: r => `<b>${fmt(r.fixed)}</b>` },
    { key: "diff", label: "Fixed − paper", num: true, render: r => `<span class="${Math.abs(r.diff) <= 0.005 ? "delta-pos" : "delta-neg"}">${fmtSigned(r.diff)}</span>` }],
    piv, { sortKey: null, rowClass: r => (r.model === "BSFC" ? "hl" : "") });
}

async function contexts() {
  let rows;
  try { rows = await api.getCsv("/results/new_context_comparison.csv"); } catch (e) { body("oNew").innerHTML = errorBox(e.message); return; }
  const names = await prettyNames();
  body("oNew").innerHTML = '<div id="nctx"></div><p class="small muted" style="margin-top:10px">Extension, not a faithful replication: open-source product metrics (no Understand licence) and JTratch without the authors\' external-Javadoc file. Contexts analysed later from the dashboard appear here after <code>python src/reproduce/build_comparison.py</code>; their full results are under Research Results.</p>';
  sortableTable($("#nctx", el), [
    { key: "Context", label: "Context", render: r => `<span class="mono">${esc(r.Context)}</span>` }, { key: "Model", label: "Model" },
    { key: "Paper R2 (original release)", label: "Paper (orig. release)", num: true, render: r => isNum(r["Paper R2 (original release)"]) ? fmt(r["Paper R2 (original release)"], 2) : '<span class="muted">—</span>' },
    { key: "New R2", label: "New release", num: true, render: r => `<b>${fmt(r["New R2"])}</b>` },
    { key: "Files (n)", label: "Files", num: true }, { key: "# potential predictors", label: "Potential pred.", num: true },
    { key: "Significant EH predictors", label: "Significant EH predictors", render: r => r["Significant EH predictors"]
      ? r["Significant EH predictors"].split(";").map(x => esc(names[x.trim()] || x.trim())).join("<br>") : '<span class="muted">—</span>' }],
    rows, { sortKey: null });
}

async function ml() {
  let res, up;
  try { [res, up] = await Promise.all([api.getCsv("/results/ml_results.csv"), api.getCsv("/results/ml_uplift.csv")]); }
  catch (e) { $("#oMLPanel", el).innerHTML = errorBox(e.message); return; }
  const projects = [...new Set(res.map(r => r.project))];
  const seg = $("#mlProj", el);
  seg.innerHTML = projects.map((p, i) => `<button data-p="${p}" aria-pressed="${i === 0}">${esc((PROJ[p] || p).split(" (")[0])}</button>`).join("");
  const draw = (p) => mlPanel($("#oMLPanel", el), res.filter(r => r.project === p), up.filter(u => u.project === p), `oml-${p.replace(/\W/g, "")}`);
  $$("button", seg).forEach(b => b.onclick = () => { $$("button", seg).forEach(x => x.setAttribute("aria-pressed", x === b)); draw(b.dataset.p); });
  draw(projects[0]);
}

async function shap() {
  let rows;
  try { rows = await api.getCsv("/results/shap_importance.csv"); } catch (e) { $("#oSHAPGrid", el).innerHTML = errorBox(e.message); return; }
  const projects = [...new Set(rows.map(r => r.project))];
  const pretty = await prettyNames();
  $("#oSHAPGrid", el).innerHTML = projects.map(p => `<div><h3 class="small" style="margin:0 0 6px">${esc(PROJ[p] || p)} <span class="muted" style="font-weight:400">· ${esc(rows.find(r => r.project === p).learner)}</span></h3>
    <div class="chart" id="shap-${p.replace(/\W/g, "")}"></div></div>`).join("");
  projects.forEach(p => {
    const top = rows.filter(r => r.project === p).sort((a, b) => b.mean_abs_shap - a.mean_abs_shap).slice(0, 12);
    const unit = top[0].learner === "RF" ? "probability" : "log-odds";
    hbar($(`#shap-${p.replace(/\W/g, "")}`, el), top.map(r => ({ label: pretty[r.feature] || r.feature, value: +r.mean_abs_shap, hatch: r.group !== "base",
      color: r.group === "base" ? "var(--trad)" : null, tip: `<b>${esc(pretty[r.feature] || r.feature)}</b><br>${r.group === "base" ? "traditional" : "exception-handling"} · rank ${r.rank}<br>mean |SHAP| ${(+r.mean_abs_shap).toFixed(4)} (${unit})` })),
      { title: `SHAP importance, ${PROJ[p] || p}`, valueFmt: v => v.toFixed(3), barH: 14 });
  });
}

async function prettyNames() {
  try { return await api.getMetricNames(); } catch { return {}; }
}
