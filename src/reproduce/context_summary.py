"""One view over every study context: the paper's three releases (reproduction) and our new releases.

Reads what the other phases wrote (nothing is recomputed except confidence intervals from saved folds):
  reproduction: results/reproduce/fixed/base_test_2.csv, results/ml_*.csv, results/shap_alignment.csv
  new contexts: results/new/<id>/fixed/, fixed_forcesig/ (sensitivity S1), variance/ (analyzer runs),
                ml/ (RQ3/RQ4), data/new/<id>/dataset_manifest.json
Writes:
  results/contexts_summary.csv / .md       one row per context (RQ1-RQ4 + validity checks)
  results/ml_uplift_ci.csv                 ΔPR-AUC / ΔROC-AUC (TRAD+EH − TRAD) with corrected-t 95% CI, all contexts
  results/figures/fig_r2_contexts.{png,pdf}     R² of BASE/BSFC/BSAP per context (+ analyzer-run range)
  results/figures/fig_bsfc_variance.{png,pdf}   BSFC R² over 10 analyzer runs vs. forced-BASE sensitivity
  results/figures/fig_ml_uplift.{png,pdf}       ΔPR-AUC with 95% CI per context and learner

Usage: python src/reproduce/context_summary.py
"""
import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RES = ROOT / "results"
FIG = RES / "figures"
MODELS = ["BASE", "BSFC", "BSAP"]
ORIG = {"umbraco-7.6": "Umbraco 7.6", "hadoop-2.6": "Hadoop 2.6", "hibernate-5.0": "Hibernate 5.0"}
PAPER_R2 = {("umbraco-7.6", "BASE"): .09, ("umbraco-7.6", "BSFC"): .09, ("umbraco-7.6", "BSAP"): .18,
            ("hadoop-2.6", "BASE"): .33, ("hadoop-2.6", "BSFC"): .37, ("hadoop-2.6", "BSAP"): .35,
            ("hibernate-5.0", "BASE"): .21, ("hibernate-5.0", "BSFC"): .28, ("hibernate-5.0", "BSAP"): .23}
# Reference palette, categorical slots 1-3 (validated all-pairs, light); hatches give the secondary encoding.
COLORS = {"BASE": "#2a78d6", "BSFC": "#eb6834", "BSAP": "#1baf7a"}
HATCH = {"BASE": "", "BSFC": "////", "BSAP": "...."}
LEARNER_COLORS = {"LR": "#2a78d6", "RF": "#eb6834", "XGB": "#1baf7a"}
LEARNER_MARKER = {"LR": "o", "RF": "s", "XGB": "D"}
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"


def label(tid: str) -> str:
    if tid in ORIG:
        return ORIG[tid]
    return tid.replace("zookeeper-release-", "ZooKeeper ").replace("hibernate-", "Hibernate ")


def models_of(path: Path) -> dict:
    if not path.exists():
        return {}
    d = pd.read_csv(path)
    d = d[d.file_set == "CAT"]
    return {r.metric_set: r for r in d.itertuples()}


def sig_eh(row, base: set) -> list:
    s = getattr(row, "signifcant_r", "")
    return [x.strip() for x in str(s).split(",") if x.strip() not in ("", "TOTAL", "nan") and x.strip() not in base]


def ci_rows(folds: pd.DataFrame, context: str, source: str) -> list:
    out = []
    for (proj, learner), g in folds.groupby(["project", "learner"], sort=False):
        base = g[g.feature_set == "TRAD"].sort_values("fold")
        ext = g[g.feature_set == "TRAD+EH"].sort_values("fold")
        for metric in ("pr_auc", "roc_auc"):
            diff = ext[metric].to_numpy() - base[metric].to_numpy()
            k = len(diff)
            se = np.sqrt((1 / k + base.n_test.iloc[0] / base.n_train.iloc[0]) * np.var(diff, ddof=1))
            h = stats.t.ppf(0.975, k - 1) * se
            out.append(dict(context=context if context else label(proj), source=source, learner=learner, metric=metric,
                            trad=base[metric].mean(), trad_eh=ext[metric].mean(), delta=diff.mean(),
                            ci_low=diff.mean() - h, ci_high=diff.mean() + h, folds=k))
    return out


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    rows, ci = [], []
    groups0 = pd.read_csv(RES / "reproduce" / "fixed" / "metric_groups.csv")
    base0 = set(groups0.loc[groups0.group == "base", "metric"])
    m0 = pd.read_csv(RES / "reproduce" / "fixed" / "base_test_2.csv")
    up0 = pd.read_csv(RES / "ml_uplift.csv")
    res0 = pd.read_csv(RES / "ml_results.csv")
    al0 = pd.read_csv(RES / "shap_alignment.csv")
    ci += ci_rows(pd.read_csv(RES / "ml_folds.csv"), None, "reproduction")

    contexts = [(t, "reproduction") for t in ORIG] + [
        (p.parent.parent.name, "new") for p in sorted((RES / "new").glob("*/fixed/base_test_2.csv"))]
    for tid, source in contexts:
        r = dict(context=label(tid), id=tid, source=source)
        if source == "reproduction":
            mods = {x.metric_set: x for x in m0[(m0.file_set == "CAT") & (m0.project == tid)].itertuples()}
            base, up, mlr, al = base0, up0[up0.project == tid], res0[res0.project == tid], al0[al0.project == tid]
            r["files_with_catch"] = int(next(iter(mods.values())).n)
            r["defective_pct"] = round(100 * mlr.prevalence.iloc[0], 1)
        else:
            nd = RES / "new" / tid
            g = pd.read_csv(nd / "fixed" / "metric_groups.csv")
            base = set(g.loc[g.group == "base", "metric"])
            mods = models_of(nd / "fixed" / "base_test_2.csv")
            forced = models_of(nd / "fixed_forcesig" / "base_test_2.csv")
            man = json.loads((ROOT / "data" / "new" / tid / "dataset_manifest.json").read_text())
            r["files_with_catch"] = int(next(iter(mods.values())).n)
            r["defective_pct"] = round(100 * man["defective_files_with_catch"] / man["files_with_catch"], 1)
            for m in MODELS:
                if m in forced:
                    r[f"{m}_r2_forced_base"] = round(forced[m].r2_c_r, 3) if pd.notna(forced[m].r2_c_r) else None
            vs = nd / "variance" / "summary.csv"
            if vs.exists():
                v = pd.read_csv(vs).set_index("model")
                for m in MODELS:
                    r[f"{m}_r2_runs_min"], r[f"{m}_r2_runs_max"] = v.loc[m, "r2_min"], v.loc[m, "r2_max"]
                    r[f"{m}_r2_runs_mean"], r[f"{m}_r2_runs_sd"] = v.loc[m, "r2_mean"], v.loc[m, "r2_sd"]
                    r[f"{m}_predictor_sets"] = int(v.loc[m, "distinct_predictor_sets"])
                r["analyzer_runs"] = int(v.runs.iloc[0])
            log = (nd / "fixed" / "run_log.txt").read_text(encoding="utf-8", errors="replace")
            r["base_predictors_dropped"] = log.count("Significant missing")
            mlp = nd / "ml"
            up = pd.read_csv(mlp / "ml_uplift.csv") if (mlp / "ml_uplift.csv").exists() else pd.DataFrame()
            mlr = pd.read_csv(mlp / "ml_results.csv") if (mlp / "ml_results.csv").exists() else pd.DataFrame()
            al = pd.read_csv(mlp / "shap_alignment.csv") if (mlp / "shap_alignment.csv").exists() else pd.DataFrame()
            if (mlp / "ml_folds.csv").exists():
                ci += ci_rows(pd.read_csv(mlp / "ml_folds.csv"), label(tid), "new")
        for m in MODELS:
            x = mods.get(m)
            r[f"{m}_r2"] = round(x.r2_c_r, 3) if x is not None and pd.notna(x.r2_c_r) else None
            r[f"{m}_sig_eh"] = "; ".join(sig_eh(x, base)) if x is not None else ""
            if source == "reproduction":
                r[f"{m}_r2_paper"] = PAPER_R2[(tid, m)]
        if len(mlr):
            tr = mlr[mlr.feature_set == "TRAD"].sort_values("pr_auc_mean").iloc[-1]
            eh = mlr[mlr.feature_set == "TRAD+EH"].sort_values("pr_auc_mean").iloc[-1]
            r.update(prevalence=round(tr.prevalence, 3), best_pr_auc_trad=round(tr.pr_auc_mean, 3),
                     best_pr_auc_trad_eh=round(eh.pr_auc_mean, 3), ml_folds=None)
        if len(up):
            pr = up[up.metric == "pr_auc"]
            r["pr_auc_uplifts_positive"] = f"{int((pr.delta_mean > 0).sum())}/{len(pr)}"
            if "p_holm" in pr:
                r["pr_auc_sig_holm"] = f"{int((pr.p_holm < 0.05).sum())}/{len(pr)}"
                ro = up[up.metric == "roc_auc"]
                r["roc_auc_sig_holm"] = f"{int((ro.p_holm < 0.05).sum())}/{len(ro)}"
            r["min_p_raw_pr_auc"] = round(pr.p_corrected_ttest.min(), 3)
        if len(al):
            top = al[al.eh_rank <= 10]
            r["shap_top10_eh_matching_sig"] = f"{int(top.matches_phase0_sig.notna().sum())}/{len(top)}"
            r["shap_eh_in_overall_top10"] = int((top.overall_rank <= 10).sum())
        rows.append(r)

    summ = pd.DataFrame(rows).drop(columns=["ml_folds"], errors="ignore")
    summ.to_csv(RES / "contexts_summary.csv", index=False)
    cdf = pd.DataFrame(ci)
    holm_rows = []
    for tid, source in contexts:
        f = RES / "ml_uplift.csv" if source == "reproduction" else RES / "new" / tid / "ml" / "ml_uplift.csv"
        if f.exists():
            u = pd.read_csv(f)
            u = u[(u.feature_set == "TRAD+EH") & (u.project == tid)] if source == "reproduction" else u[u.feature_set == "TRAD+EH"]
            holm_rows += [dict(context=label(tid), learner=x.learner, metric=x.metric, p_holm=x.p_holm)
                          for x in u.itertuples()]
    cdf = cdf.merge(pd.DataFrame(holm_rows), on=["context", "learner", "metric"], how="left")
    cdf.to_csv(RES / "ml_uplift_ci.csv", index=False, float_format="%.4f")
    write_md(summ, cdf)
    fig_r2(summ)
    fig_variance(summ)
    fig_uplift(cdf)
    print(summ[["context", "BASE_r2", "BSFC_r2", "BSAP_r2"]].to_string(index=False))


def fmt(v, d=3):
    return "—" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.{d}f}"


def write_md(s: pd.DataFrame, ci: pd.DataFrame) -> None:
    md = ["# All study contexts: reproduction vs. new releases", "",
          "Generated by `python src/reproduce/context_summary.py` from the outputs of every phase. Reproduction rows use "
          "the authors' released data; new rows use data we collected (fallback product metrics, JTratch flow metrics "
          "without external Javadoc/dependency jars: an extension, not a faithful replication).", "",
          "## RQ1/RQ2: explanatory models (optimism-reduced Nagelkerke R², simplified models)", "",
          "| Context | Source | Files (defective %) | BASE | BSFC | BSAP | BSFC over 10 analyzer runs (min–max) | "
          "BSFC forced | BSAP forced | BASE-significant metric dropped (events) |", "|---|---|---|---:|---:|---:|---|---:|---:|---:|"]
    for _, r in s.iterrows():
        paper = (lambda m: f" ({r[f'{m}_r2_paper']:.2f})" if r["source"] == "reproduction" else "")
        rng = (f"{r['BSFC_r2_runs_min']:.3f}–{r['BSFC_r2_runs_max']:.3f}"
               if "BSFC_r2_runs_min" in r and pd.notna(r.get("BSFC_r2_runs_min")) else "—")
        md.append(f"| {r.context} | {r.source} | {r.files_with_catch} ({r.defective_pct:.1f}%) | "
                  f"{fmt(r.BASE_r2)}{paper('BASE')} | {fmt(r.BSFC_r2)}{paper('BSFC')} | {fmt(r.BSAP_r2)}{paper('BSAP')} | "
                  f"{rng} | {fmt(r.get('BSFC_r2_forced_base'))} | {fmt(r.get('BSAP_r2_forced_base'))} | "
                  f"{'' if r.source == 'reproduction' else int(r.get('base_predictors_dropped', 0))} |")
    md += ["", "Reproduction rows: our bug-fixed run (paper's Table 4 value in brackets). — for BSFC = no predictor "
           "survives backward elimination (empty simplified model, guard D7). 'Forced' = sensitivity S1 (paper §3.4.6 rule applied).", "",
           "Significant EH predictors (simplified models):", ""]
    for _, r in s.iterrows():
        md.append(f"* **{r.context}**: BSFC: {r.BSFC_sig_eh or 'none'}; BSAP: {r.BSAP_sig_eh or 'none'}")
    md += ["", "## RQ3/RQ4: prediction and SHAP", "",
           "| Context | Prevalence | best PR-AUC TRAD | best PR-AUC TRAD+EH | PR-AUC uplifts > 0 | "
           "significant after Holm (PR-AUC / ROC-AUC) | SHAP top-10 EH matching a significant predictor |",
           "|---|---:|---:|---:|---:|---|---:|"]
    for _, r in s.iterrows():
        md.append(f"| {r.context} | {fmt(r.get('prevalence'))} | {fmt(r.get('best_pr_auc_trad'))} | "
                  f"{fmt(r.get('best_pr_auc_trad_eh'))} | {r.get('pr_auc_uplifts_positive', '—')} | "
                  f"{r.get('pr_auc_sig_holm', '—')} / {r.get('roc_auc_sig_holm', '—')} | "
                  f"{r.get('shap_top10_eh_matching_sig', '—')} |")
    md += ["", "## ΔPR-AUC (TRAD+EH − TRAD) with 95% CI (corrected resampled t)", "",
           "Unadjusted intervals; the Holm-adjusted p-values are in each context's `ml_uplift.csv` "
           "(`results/ml_uplift.csv`, `results/new/<id>/ml/ml_uplift.csv`).", "",
           "| Context | Learner | TRAD | TRAD+EH | Δ | 95% CI | p_Holm |", "|---|---|---:|---:|---:|---|---:|"]
    for _, r in ci[ci.metric == "pr_auc"].iterrows():
        md.append(f"| {r.context} | {r.learner} | {r.trad:.3f} | {r.trad_eh:.3f} | {r.delta:+.3f} | "
                  f"[{r.ci_low:+.3f}, {r.ci_high:+.3f}] | {fmt(r.get('p_holm'))} |")
    (RES / "contexts_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def style(ax):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(INK2)
    ax.tick_params(colors=INK2, labelsize=8)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def save(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(FIG / f"{name}.{ext}", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig_r2(s: pd.DataFrame) -> None:
    plt.rcParams.update({"font.family": "serif", "font.size": 8, "hatch.linewidth": 0.6})
    fig, ax = plt.subplots(figsize=(7.0, 2.5))
    w, x = 0.26, np.arange(len(s))
    for j, m in enumerate(MODELS):
        vals = s[f"{m}_r2"].astype(float).fillna(0).to_numpy()
        pos = x + (j - 1) * w
        ax.bar(pos, vals, w - 0.03, color=COLORS[m], hatch=HATCH[m], edgecolor="white", linewidth=0.4, label=m)
        tops = vals.copy()
        if f"{m}_r2_runs_max" in s:
            tops = np.fmax(vals, s[f"{m}_r2_runs_max"].astype(float).fillna(0).to_numpy())
        for p, top, v, raw in zip(pos, tops, vals, s[f"{m}_r2"]):
            ax.text(p, top + 0.008, "n/a" if pd.isna(raw) else f"{v:.2f}", ha="center", va="bottom", fontsize=5.5,
                    color=INK2, rotation=90)
        if f"{m}_r2_runs_min" in s:
            lo, hi = s[f"{m}_r2_runs_min"].astype(float), s[f"{m}_r2_runs_max"].astype(float)
            ok = lo.notna() & (hi - lo > 1e-6)
            ax.vlines(pos[ok], lo[ok], hi[ok], color=INK, linewidth=0.9)
            ax.scatter(pos[ok], lo[ok], marker="_", color=INK, s=18, linewidth=0.9)
            ax.scatter(pos[ok], hi[ok], marker="_", color=INK, s=18, linewidth=0.9)
        if f"{m}_r2_paper" in s:
            pp = s[f"{m}_r2_paper"].astype(float)
            ok = pp.notna()
            ax.scatter(pos[ok], pp[ok], marker="_", color=INK, s=60, linewidth=1.6, zorder=3)
    n_orig = int((s.source == "reproduction").sum())
    ax.axvline(n_orig - 0.5, color=INK2, linewidth=0.6, linestyle=(0, (3, 3)))
    ax.text(n_orig / 2 - 0.5, 0.56, "Reproduction (authors' data)", ha="center", fontsize=7, color=INK2)
    ax.text(n_orig + (len(s) - n_orig) / 2 - 0.5, 0.56, "New context (our data)", ha="center", fontsize=7, color=INK2)
    ax.set_xticks(x, [c.replace(" ", "\n", 1) for c in s.context], fontsize=7.5)
    ax.set_ylabel("Optimism-reduced R²", color=INK2)
    ax.set_ylim(0, 0.62)
    style(ax)
    h, l_ = ax.get_legend_handles_labels()
    h += [plt.Line2D([], [], color=INK, marker="_", linestyle="", markersize=8, markeredgewidth=1.6),
          plt.Line2D([], [], color=INK, linewidth=0.9)]
    l_ += ["Paper (Table 4)", "Range over 10 analyzer runs"]
    ax.legend(h, l_, ncol=5, fontsize=6.5, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.17))
    save(fig, "fig_r2_contexts")


def fig_variance(s: pd.DataFrame) -> None:
    if "analyzer_runs" not in s:
        return
    new = s[(s.source == "new") & s.analyzer_runs.notna()]
    if new.empty:
        return
    fig, ax = plt.subplots(figsize=(3.4, 2.2))
    for i, (_, r) in enumerate(new.iterrows()):
        runs_p = RES / "new" / r.id / "variance" / "runs.csv"
        if not runs_p.exists():
            continue
        d = pd.read_csv(runs_p)
        v = d[(d.model == "BSFC") & (d.run != "kept")].r2_optimism_reduced
        empty = int(v.isna().sum())
        if empty:
            ax.scatter([i], [0], s=10 + 14 * empty, facecolor="white", edgecolor=COLORS["BSFC"], linewidth=1.2, zorder=3)
            ax.text(i - 0.14, 0, f"{empty}× no\npredictor", fontsize=5.5, va="center", ha="right", color=INK2)
        for val, c in v.dropna().round(3).value_counts().items():
            ax.scatter([i], [val], s=10 + 14 * c, color=COLORS["BSFC"], edgecolor="white", linewidth=0.8, zorder=3)
            ax.text(i - 0.14, val, f"{c}×", fontsize=6, va="center", ha="right", color=INK2)
        b = r.get("BASE_r2")
        ax.scatter([i], [b], marker="_", s=120, color=COLORS["BASE"], linewidth=1.8, zorder=2)
        f = r.get("BSFC_r2_forced_base")
        if f is not None and pd.notna(f):
            ax.scatter([i], [f], marker="x", s=28, color=INK, linewidth=1.0, zorder=4)
    ax.set_xticks(range(len(new)), new.context, fontsize=6.5, rotation=15)
    ax.set_ylabel("BSFC optimism-reduced R²", color=INK2, fontsize=7)
    ax.set_xlim(-0.6, len(new) - 0.4)
    style(ax)
    h = [plt.Line2D([], [], color=COLORS["BSFC"], marker="o", linestyle="", markersize=5),
         plt.Line2D([], [], color=COLORS["BASE"], marker="_", linestyle="", markersize=9, markeredgewidth=1.8),
         plt.Line2D([], [], color=INK, marker="x", linestyle="", markersize=5)]
    ax.legend(h, ["BSFC, one analyzer run (×count)", "BASE (kept run)", "BSFC, BASE predictors forced"],
              fontsize=5.8, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.22), ncol=2)
    save(fig, "fig_bsfc_variance")


def fig_uplift(ci: pd.DataFrame) -> None:
    d = ci[ci.metric == "pr_auc"].copy()
    ctxs = list(dict.fromkeys(d.context))
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    for j, lr in enumerate(["LR", "RF", "XGB"]):
        g = d[d.learner == lr].set_index("context").reindex(ctxs)
        y = np.arange(len(ctxs)) + (j - 1) * 0.22
        ax.hlines(y, g.ci_low, g.ci_high, color=LEARNER_COLORS[lr], linewidth=1.2)
        ax.scatter(g.delta, y, marker=LEARNER_MARKER[lr], s=16, color=LEARNER_COLORS[lr], edgecolor="white",
                   linewidth=0.6, zorder=3, label=lr)
    ax.axvline(0, color=INK, linewidth=0.8)
    ax.set_yticks(range(len(ctxs)), ctxs, fontsize=6.5)
    ax.invert_yaxis()
    n_orig = sum(c in ORIG.values() for c in ctxs)
    ax.axhline(n_orig - 0.5, color=INK2, linewidth=0.6, linestyle=(0, (3, 3)))
    ax.set_xlabel("ΔPR-AUC, TRAD+EH − TRAD (95% CI)", color=INK2, fontsize=7)
    style(ax)
    ax.yaxis.grid(False)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6)
    ax.legend(fontsize=6.5, frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.13))
    save(fig, "fig_ml_uplift")


if __name__ == "__main__":
    main()
