"""RQ4: which exception-handling features most influence predictions (SHAP), and do they agree with
the significant predictors of the Phase 0 logistic models?

Per project: pick the best tree learner (RF or XGB) by mean CV PR-AUC on TRAD+EH from
results/ml_results.csv, refit it on all files with >=1 catch block, compute TreeSHAP values, and rank
features by mean |SHAP|.

Agreement with Phase 0: a SHAP-ranked EH feature "matches" a significant EH predictor of the simplified
BSFC/BSAP models (results/reproduce/fixed/predictors_simplified.csv) either exactly (same column) or as a
correlated proxy (|Spearman rho| > 0.7 on the same files, the paper's own clustering threshold); the
paper's correlation filter keeps only one metric per such cluster, so exact name matches alone understate
agreement.

Usage: python src/explain/shap_analysis.py
       [--ml-results CSV --data CSV --groups CSV --phase0 CSV --projects id --out DIR]   (defaults = Phase A)
Writes: results/shap_importance.csv, results/shap_top_eh.csv, results/shap_alignment.csv,
        results/shap_alignment.md, results/shap_bar_<project>.png, results/shap_beeswarm_<project>.png,
        results/shap_bar_all.png
"""
import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import shap  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ml"))
from common import DATA, GROUPS, PROJECTS, ROOT, feature_sets, load_project, metric_groups, pretty_names, xy  # noqa: E402
from train_eval import make_learner  # noqa: E402

RES = ROOT / "results"
TOP_N = 15
LABEL = {"umbraco-7.6": "Umbraco 7.6", "hadoop-2.6": "Hadoop 2.6", "hibernate-5.0": "Hibernate 5.0"}

plt.rcParams.update({
    "font.family": "serif", "font.size": 8, "axes.titlesize": 9, "axes.labelsize": 8,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
    "axes.edgecolor": "#444444", "axes.linewidth": 0.6, "savefig.dpi": 300,
})
EH_FILL, TRAD_FILL = "#3a3a3a", "#bdbdbd"
# single-hue light->dark ramp for feature value; starts at light gray so low values stay visible on white
VALUE_CMAP = matplotlib.colors.LinearSegmentedColormap.from_list(
    "greys_visible", matplotlib.colormaps["Greys"](np.linspace(0.22, 1.0, 256)))


def shap_matrix(model, X: pd.DataFrame) -> np.ndarray:
    sv = shap.TreeExplainer(model).shap_values(X)
    if isinstance(sv, list):           # older shap, RF: one array per class
        sv = sv[1]
    sv = np.asarray(sv)
    if sv.ndim == 3:                   # newer shap, RF: (n, features, classes)
        sv = sv[:, :, 1]
    return sv


PRETTY = pretty_names()


def unit(learner: str) -> str:
    """TreeSHAP output space: sklearn RF explains predict_proba (probability); XGBoost explains log-odds."""
    return "probability" if learner == "RF" else "log-odds"


def bar(ax, imp: pd.DataFrame, title: str, top_n: int = TOP_N) -> None:
    top = imp.head(top_n).iloc[::-1]
    is_eh = (top.group != "base").to_numpy()
    y = np.arange(len(top))
    ax.barh(y, top.mean_abs_shap, height=0.72, color=np.where(is_eh, EH_FILL, TRAD_FILL), linewidth=0)
    # texture as secondary encoding for EH features (print / CVD safe)
    ax.barh(y[is_eh], top.mean_abs_shap.to_numpy()[is_eh], height=0.72, color="none", edgecolor="white",
            hatch="////", linewidth=0)
    ax.set_yticks(y, [PRETTY.get(f, f) for f in top.feature])
    ax.set_xlabel(f"mean |SHAP| ({unit(imp.learner.iloc[0])})")
    ax.set_title(title)
    ax.grid(axis="x", color="#e0e0e0", linewidth=0.5)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def legend_handles():
    from matplotlib.patches import Patch
    return [Patch(facecolor=EH_FILL, hatch="////", edgecolor="white", label="Exception-handling metric"),
            Patch(facecolor=TRAD_FILL, edgecolor="white", label="Traditional metric")]


def proxies(X: pd.DataFrame, feat: str, candidates: list, thr: float = 0.7) -> list:
    out = []
    for c in candidates:
        if c == feat:
            out.append((c, 1.0))
        elif c in X.columns and feat in X.columns:
            rho = X[feat].corr(X[c], method="spearman")
            if pd.notna(rho) and abs(rho) > thr:
                out.append((c, float(rho)))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ml-results", type=Path, default=RES / "ml_results.csv")
    ap.add_argument("--data", type=Path, default=DATA)
    ap.add_argument("--groups", type=Path, default=GROUPS)
    ap.add_argument("--phase0", type=Path, default=RES / "reproduce" / "fixed" / "predictors_simplified.csv")
    ap.add_argument("--projects", default=",".join(PROJECTS))
    ap.add_argument("--out", type=Path, default=RES)
    a = ap.parse_args()
    projects, out = a.projects.split(","), a.out
    out.mkdir(parents=True, exist_ok=True)

    ml = pd.read_csv(a.ml_results)
    groups = metric_groups(a.groups)
    group_of = {m: g for g, ms in groups.items() for m in ms}
    phase0 = pd.read_csv(a.phase0) if a.phase0.exists() else pd.DataFrame()

    all_imp, top_eh_rows, align_rows = [], [], []
    fig_all, axes_all = plt.subplots(1, len(projects), figsize=(7.16 if len(projects) > 1 else 3.6, 3.4),
                                     layout="constrained", squeeze=False)   # IEEE double / single column
    axes_all = axes_all[0]
    for k, project in enumerate(projects):
        cand = ml[(ml.project == project) & (ml.feature_set == "TRAD+EH") & ml.learner.isin(["RF", "XGB"])]
        best = cand.sort_values("pr_auc_mean", ascending=False).iloc[0]
        d = load_project(project, data_path=a.data)
        X, y = xy(d, feature_sets(a.groups)["TRAD+EH"])
        model = make_learner(best.learner, y).fit(X, y)
        sv = shap_matrix(model, X)
        imp = (pd.DataFrame({"feature": X.columns, "mean_abs_shap": np.abs(sv).mean(axis=0),
                             "mean_shap": sv.mean(axis=0)})
               .assign(group=lambda t: t.feature.map(group_of), project=project, learner=best.learner,
                       cv_pr_auc=best.pr_auc_mean)
               .sort_values("mean_abs_shap", ascending=False).reset_index(drop=True))
        imp["rank"] = np.arange(1, len(imp) + 1)
        # direction: Spearman between the feature value and its SHAP value
        imp["direction"] = imp.feature.map(dict(zip(X.columns, [
            np.sign(pd.Series(X[f].to_numpy()).corr(pd.Series(sv[:, j]), method="spearman"))
            for j, f in enumerate(X.columns)])))
        all_imp.append(imp)

        # per-file explanations (dashboard drill-down): value and SHAP contribution of the 40 most important
        # features, the sum of the remaining contributions, the label and the model's predicted probability
        keep = list(imp.feature.head(40))
        col = {f: j for j, f in enumerate(X.columns)}
        pf = pd.DataFrame({"File.Path": d["File.Path"], "defective": y,
                           "predicted": model.predict_proba(X)[:, 1]})
        for f in keep:
            pf[f"{f}|value"] = X[f].to_numpy()
            pf[f"{f}|shap"] = sv[:, col[f]]
        rest = [col[f] for f in X.columns if f not in set(keep)]
        pf["other_features|shap"] = sv[:, rest].sum(axis=1) if rest else 0.0
        pf.to_csv(out / f"shap_values_{project}.csv", index=False, float_format="%.6g")

        eh = imp[imp.group != "base"].head(10).copy()
        eh["eh_rank"] = np.arange(1, len(eh) + 1)
        top_eh_rows.append(eh)

        sig = []
        if not phase0.empty:
            p0 = phase0[(phase0.project == project) & phase0.model.isin(["CAT.BSFC", "CAT.BSAP"])]
            sig = sorted(set(p0.loc[p0.predictor.map(lambda m: group_of.get(m) != "base"), "predictor"]))
        for _, r in eh.iterrows():
            px = proxies(X, r.feature, sig)
            align_rows.append(dict(project=project, eh_rank=r.eh_rank, overall_rank=r["rank"], feature=r.feature,
                                   group=r.group, mean_abs_shap=r.mean_abs_shap,
                                   shap_direction="+" if r.direction > 0 else "-",
                                   matches_phase0_sig="; ".join(f"{c} (rho={v:.2f})" for c, v in px)))
        for s in sig:   # Phase 0 significant EH predictors and where SHAP ranks them
            rk = imp.loc[imp.feature == s, "rank"]
            align_rows.append(dict(project=project, eh_rank=None, overall_rank=int(rk.iloc[0]) if len(rk) else None,
                                   feature=s, group=group_of.get(s), mean_abs_shap=
                                   float(imp.loc[imp.feature == s, "mean_abs_shap"].iloc[0]) if len(rk) else None,
                                   shap_direction=None, matches_phase0_sig="<Phase 0 significant EH predictor>"))

        fig, ax = plt.subplots(figsize=(3.5, 3.6), layout="constrained")   # IEEE single column
        bar(ax, imp, f"{LABEL.get(project, project)} ({best.learner}, top {TOP_N})")
        ax.legend(handles=legend_handles(), loc="lower right", frameon=False)
        fig.savefig(out / f"shap_bar_{project}.png", bbox_inches="tight")
        plt.close(fig)

        bar(axes_all[k], imp, f"{LABEL.get(project, project)} ({best.learner})", top_n=12)

        plt.figure()   # summary_plot draws into the current figure; keep it off fig_all
        np.random.seed(2018)   # summary_plot jitters points with the global RNG; keep figures reproducible
        shap.summary_plot(sv, X.rename(columns=PRETTY), max_display=TOP_N, show=False,
                          cmap=VALUE_CMAP, plot_size=(5.2, 4.4), color_bar_label="Feature value")
        f = plt.gcf()
        main_ax = f.axes[0]
        main_ax.tick_params(labelsize=7)
        main_ax.set_xlabel(f"SHAP value (impact on {unit(best.learner)} of a post-release defect)", fontsize=8)
        main_ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5, symmetric=True))
        main_ax.set_title(f"{LABEL.get(project, project)} ({best.learner})", fontsize=9)
        for extra in f.axes[1:]:   # colour bar
            extra.tick_params(labelsize=7)
            extra.yaxis.label.set_size(8)
        f.savefig(out / f"shap_beeswarm_{project}.png", dpi=300, bbox_inches="tight")
        plt.close("all")
        print(f"{project}: best tree learner {best.learner} (CV PR-AUC {best.pr_auc_mean:.3f}); "
              f"top EH features: {', '.join(eh.feature.head(5))}", flush=True)

    fig_all.legend(handles=legend_handles(), loc="outside lower center", ncols=2, frameon=False)
    fig_all.savefig(out / "shap_bar_all.png", bbox_inches="tight")
    plt.close(fig_all)

    pd.concat(all_imp).to_csv(out / "shap_importance.csv", index=False, float_format="%.5f")
    pd.concat(top_eh_rows).to_csv(out / "shap_top_eh.csv", index=False, float_format="%.5f")
    al = pd.DataFrame(align_rows)
    al.to_csv(out / "shap_alignment.csv", index=False, float_format="%.5f")

    md = ["# RQ4: SHAP ranking of exception-handling features vs Phase 0 significant predictors", "",
          "Generated by `python src/explain/shap_analysis.py`. SHAP on the best tree learner per project, "
          "refit on all files with >=1 catch block, TRAD+EH feature set.", ""]
    for project in projects:
        a_ = al[al.project == project]
        top = a_[a_.eh_rank.notna()]
        sig = a_[a_.eh_rank.isna()]
        md += [f"## {LABEL.get(project, project)}", "", "Top-10 EH features by mean |SHAP|:", "",
               "| EH rank | Overall rank | Feature | Group | mean abs SHAP | Dir. | Phase 0 match (exact or proxy, abs rho > 0.7) |",
               "|---:|---:|---|---|---:|:-:|---|"]
        for _, r in top.iterrows():
            md.append(f"| {int(r.eh_rank)} | {int(r.overall_rank)} | {r.feature} | {r.group} | {r.mean_abs_shap:.4f} | "
                      f"{r.shap_direction} | {r.matches_phase0_sig or '—'} |")
        md += ["", "Phase 0 significant EH predictors (simplified BSFC/BSAP, bug-fixed run) and their SHAP rank: " +
               (", ".join(f"{r.feature} (#{int(r.overall_rank)})" if pd.notna(r.overall_rank) else f"{r.feature} (n/a)"
                          for _, r in sig.iterrows()) or "none"), ""]
        n_match = (top.matches_phase0_sig.fillna("") != "").sum()
        md += [f"Top-10 EH SHAP features matching a Phase 0 significant EH predictor: **{n_match}/{len(top)}**.", ""]
    (out / "shap_alignment.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("wrote results/shap_*.{csv,md,png}")


if __name__ == "__main__":
    main()
