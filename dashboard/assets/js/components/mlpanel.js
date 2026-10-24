// Shared RQ3 panel: learner / feature-set / metric filters driving one grouped chart and one table together.
import { icon } from "../icons.js";
import { $, $$, esc, fmt, fmtP, fmtSigned, isNum, sortableTable } from "../ui.js";
import { grouped, FEATURE_SET_COLORS, FEATURE_SET_LABEL } from "../charts.js";

export const SETS = ["TRAD", "TRAD+FLOW", "TRAD+AP", "TRAD+EH"];
export const LEARNERS = ["LR", "RF", "XGB"];
export const LEARNER_NAME = { LR: "Logistic Regression", RF: "Random Forest", XGB: "XGBoost" };
const METRIC = { pr_auc: "PR-AUC", roc_auc: "ROC-AUC", f1: "F1" };
const SET_DESC = { TRAD: "traditional metrics", "TRAD+FLOW": "+ flow characteristics", "TRAD+AP": "+ anti-patterns", "TRAD+EH": "+ both" };

/**
 * @param {HTMLElement} box
 * @param {import("../api.js").MlResult[]} results  rows for ONE project
 * @param {import("../api.js").MlUplift[]} uplift   rows for the same project
 * @param {string} id  unique prefix for element ids
 */
export function mlPanel(box, results, uplift, id = "ml") {
  const st = { learners: new Set(LEARNERS), sets: new Set(SETS), metric: "pr_auc" };
  const colors = FEATURE_SET_COLORS();
  const n = results.length ? Math.max(...results.map(r => +r.n_features || 0)) : 0;
  box.innerHTML = `
    <div class="row" style="justify-content:space-between;margin-bottom:12px">
      <div class="filters" role="group" aria-label="Learners">${LEARNERS.map(l => `<button class="toggle" data-l="${l}" aria-pressed="true">${esc(LEARNER_NAME[l])}</button>`).join("")}</div>
      <div class="filters" role="group" aria-label="Feature sets">${SETS.map(f => `<button class="toggle" data-fs="${f}" aria-pressed="true"><span class="sw" style="background:${colors[f]}"></span>${FEATURE_SET_LABEL[f]}</button>`).join("")}</div>
      <div class="seg" role="group" aria-label="Metric">${Object.entries(METRIC).map(([k, l]) => `<button data-m="${k}" aria-pressed="${k === "pr_auc"}">${l}</button>`).join("")}</div>
    </div>
    <div class="chart" id="${id}-chart"></div>
    <div class="legend" style="margin:6px 0 12px">${SETS.map(f => `<span><i style="background:${colors[f]}"></i>${FEATURE_SET_LABEL[f]}: ${SET_DESC[f]}</span>`).join("")}</div>
    <div id="${id}-table"></div>
    <p class="small muted" style="margin-top:8px">The orange line is the share of defective files: a random classifier's PR-AUC. Δ = gain over TRAD for the same learner;
      p from the Nadeau–Bengio corrected resampled t-test, not corrected for the ${LEARNERS.length * (SETS.length - 1) * 3} comparisons.
      A positive Δ alone is not evidence of improvement. Up to ${n} features per model.</p>`;
  const draw = () => {
    const res = results.filter(r => st.learners.has(r.learner) && st.sets.has(r.feature_set));
    const prev = results[0]?.prevalence;
    grouped($(`#${id}-chart`, box), LEARNERS.filter(l => st.learners.has(l)).map(l => ({
      label: LEARNER_NAME[l], bars: SETS.filter(f => st.sets.has(f)).map(f => {
        const r = res.find(x => x.learner === l && x.feature_set === f);
        return r && { key: f, label: FEATURE_SET_LABEL[f], value: +r[`${st.metric}_mean`], err: +r[`${st.metric}_std`], color: colors[f] };
      }).filter(Boolean) })),
      { title: `${METRIC[st.metric]} by learner and feature set`, yLabel: METRIC[st.metric], valueFmt: v => v.toFixed(2),
        baseline: st.metric === "pr_auc" && isNum(prev) ? { value: +prev, label: "baseline (prevalence)" } : null });
    const up = (l, f) => uplift.find(u => u.learner === l && u.feature_set === f && u.metric === st.metric);
    const rows = res.map(r => { const u = up(r.learner, r.feature_set);
      return { learner: LEARNER_NAME[r.learner], set: FEATURE_SET_LABEL[r.feature_set], fs: r.feature_set, mean: +r[`${st.metric}_mean`],
               sd: +r[`${st.metric}_std`], delta: u ? +u.delta_mean : null, p: u ? +u.p_corrected_ttest : null, folds: u ? u.folds_improved : "" }; });
    sortableTable($(`#${id}-table`, box), [
      { key: "learner", label: "Learner" },
      { key: "set", label: "Feature set", render: r => `<span class="legend"><span><i style="background:${colors[r.fs]}"></i>${esc(r.set)}</span></span>` },
      { key: "mean", label: `Mean ${METRIC[st.metric]}`, num: true, render: r => fmt(r.mean) },
      { key: "sd", label: "Std", num: true, render: r => fmt(r.sd) },
      { key: "delta", label: "Δ vs TRAD", num: true, render: r => r.delta === null ? '<span class="muted">reference</span>'
        : `<span class="${r.delta >= 0 ? "delta-pos" : "delta-neg"}">${fmtSigned(r.delta)}</span> <span class="tiny muted" data-tip="folds where the extended set beat TRAD">${esc(r.folds)}</span>` },
      { key: "p", label: "Significance", render: r => r.p === null || !isNum(r.p) ? "—" : r.p < 0.05
        ? `<span class="badge ${r.delta >= 0 ? "b-ok" : "b-bad"}">${r.delta >= 0 ? icon("check", 11) : icon("alert", 11)} p ${fmtP(r.p)}</span>`
        : `<span class="badge b-mute">n.s. (p ${fmtP(r.p)})</span>` }], rows, { sortKey: "mean" });
  };
  const toggle = (set, b, key) => { const on = b.getAttribute("aria-pressed") !== "true"; if (!on && set.size === 1) return;
    b.setAttribute("aria-pressed", on); on ? set.add(key) : set.delete(key); draw(); };
  $$("[data-l]", box).forEach(b => b.onclick = () => toggle(st.learners, b, b.dataset.l));
  $$("[data-fs]", box).forEach(b => b.onclick = () => toggle(st.sets, b, b.dataset.fs));
  $$("[data-m]", box).forEach(b => b.onclick = () => { st.metric = b.dataset.m; $$("[data-m]", box).forEach(x => x.setAttribute("aria-pressed", x === b)); draw(); });
  draw();
}
