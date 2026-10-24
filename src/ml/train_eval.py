"""RQ3: do exception-handling metrics improve ML prediction of post-release defects?

For each project (files with >=1 catch block, as in the paper's presented models), each learner
(Logistic Regression, Random Forest, XGBoost) and each feature set (TRAD, TRAD+FLOW, TRAD+AP, TRAD+EH),
run repeated stratified k-fold CV (5 folds x 10 repeats, identical splits across feature sets) and record
PR-AUC (average precision), ROC-AUC and F1 (threshold 0.5, class-weighted learners).

No hyper-parameter tuning: fixed, documented defaults (see LEARNERS) so the comparison is about the
feature sets, not tuning effort. Uplift vs TRAD is tested with the Nadeau-Bengio corrected resampled
t-test, which accounts for overlapping training sets across folds.

Usage: python src/ml/train_eval.py [--folds 5] [--repeats 10]
Writes: results/ml_folds.csv, results/ml_results.csv, results/ml_uplift.csv, results/ml_results.md
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, f1_score, roc_auc_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from xgboost import XGBClassifier

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import PROJECTS, ROOT, SEED, feature_sets, load_project, log_transform, xy  # noqa: E402

RES = ROOT / "results"


def make_learner(name: str, y: np.ndarray):
    pos, neg = int(y.sum()), int(len(y) - y.sum())
    if name == "LR":
        return make_pipeline(FunctionTransformer(log_transform), StandardScaler(),
                             LogisticRegression(C=1.0, class_weight="balanced", max_iter=5000))
    if name == "RF":
        return RandomForestClassifier(n_estimators=500, min_samples_leaf=2, class_weight="balanced_subsample",
                                      n_jobs=-1, random_state=SEED)
    if name == "XGB":
        return XGBClassifier(n_estimators=300, max_depth=4, learning_rate=0.05, subsample=0.8,
                             colsample_bytree=0.8, scale_pos_weight=neg / max(pos, 1),
                             eval_metric="logloss", n_jobs=4, random_state=SEED, verbosity=0)
    raise ValueError(name)


LEARNERS = ["LR", "RF", "XGB"]


def corrected_ttest(diff: np.ndarray, n_train: int, n_test: int) -> float:
    """Nadeau & Bengio (2003) corrected resampled t-test, two-sided p-value."""
    k = len(diff)
    var = np.var(diff, ddof=1)
    if var == 0:
        return float("nan")
    t = diff.mean() / np.sqrt((1 / k + n_test / n_train) * var)
    return float(2 * stats.t.sf(abs(t), df=k - 1))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--repeats", type=int, default=10)
    a = ap.parse_args()
    fsets = feature_sets()

    rows = []
    for project in PROJECTS:
        d = load_project(project)
        y_all = (d["Distinct.count.of.Issue.Key.POST"] > 0).astype(int).to_numpy()
        cv = RepeatedStratifiedKFold(n_splits=a.folds, n_repeats=a.repeats, random_state=SEED)
        splits = list(cv.split(np.zeros(len(y_all)), y_all))
        print(f"{project}: n={len(d)} defective={y_all.sum()} ({y_all.mean():.1%})", flush=True)
        for fs_name, cols in fsets.items():
            X, y = xy(d, cols)
            for lname in LEARNERS:
                for fold, (tr, te) in enumerate(splits):
                    m = make_learner(lname, y[tr])
                    m.fit(X.iloc[tr], y[tr])
                    p = m.predict_proba(X.iloc[te])[:, 1]
                    rows.append(dict(project=project, learner=lname, feature_set=fs_name, fold=fold,
                                     n_features=X.shape[1], n_train=len(tr), n_test=len(te),
                                     pr_auc=average_precision_score(y[te], p),
                                     roc_auc=roc_auc_score(y[te], p),
                                     f1=f1_score(y[te], (p >= 0.5).astype(int), zero_division=0),
                                     prevalence=y[te].mean()))
                print(f"  {fs_name:10s} {lname:4s} PR-AUC={np.mean([r['pr_auc'] for r in rows[-len(splits):]]):.3f}",
                      flush=True)

    folds = pd.DataFrame(rows)
    folds.to_csv(RES / "ml_folds.csv", index=False)

    agg = (folds.groupby(["project", "learner", "feature_set"], sort=False)
           .agg(n_features=("n_features", "first"), prevalence=("prevalence", "mean"),
                pr_auc_mean=("pr_auc", "mean"), pr_auc_std=("pr_auc", "std"),
                roc_auc_mean=("roc_auc", "mean"), roc_auc_std=("roc_auc", "std"),
                f1_mean=("f1", "mean"), f1_std=("f1", "std")).reset_index())
    agg.to_csv(RES / "ml_results.csv", index=False, float_format="%.4f")

    up = []
    for (project, lname), g in folds.groupby(["project", "learner"], sort=False):
        base = g[g.feature_set == "TRAD"].sort_values("fold")
        for fs_name in fsets:
            if fs_name == "TRAD":
                continue
            o = g[g.feature_set == fs_name].sort_values("fold")
            for metric in ("pr_auc", "roc_auc", "f1"):
                diff = o[metric].to_numpy() - base[metric].to_numpy()
                up.append(dict(project=project, learner=lname, feature_set=fs_name, metric=metric,
                               trad_mean=base[metric].mean(), ext_mean=o[metric].mean(),
                               delta_mean=diff.mean(), delta_std=diff.std(ddof=1),
                               folds_improved=f"{(diff > 0).sum()}/{len(diff)}",
                               p_corrected_ttest=corrected_ttest(diff, int(base.n_train.iloc[0]),
                                                                 int(base.n_test.iloc[0]))))
    uplift = pd.DataFrame(up)
    uplift.to_csv(RES / "ml_uplift.csv", index=False, float_format="%.4f")

    md = ["# RQ3: ML prediction results on the authors' released dataset", "",
          f"Files with >=1 catch block; repeated stratified {a.folds}-fold CV x {a.repeats} repeats "
          f"(seed {SEED}); mean ± std over {a.folds * a.repeats} folds. F1 at threshold 0.5.",
          "Generated by `python src/ml/train_eval.py`.", "",
          "| Project | Learner | Feature set | #feat | PR-AUC | ROC-AUC | F1 |", "|---|---|---|---:|---|---|---|"]
    for _, r in agg.iterrows():
        md.append(f"| {r.project} | {r.learner} | {r.feature_set} | {r.n_features} | "
                  f"{r.pr_auc_mean:.3f} ± {r.pr_auc_std:.3f} | {r.roc_auc_mean:.3f} ± {r.roc_auc_std:.3f} | "
                  f"{r.f1_mean:.3f} ± {r.f1_std:.3f} |")
    md += ["", "PR-AUC of a random classifier equals the prevalence: " +
           ", ".join(f"{p} {agg[agg.project == p].prevalence.iloc[0]:.3f}" for p in PROJECTS) + ".",
           "", "## Uplift over TRAD (PR-AUC)", "",
           "| Project | Learner | Feature set | ΔPR-AUC (mean ± std) | folds improved | p (corrected t-test) |",
           "|---|---|---|---|---|---:|"]
    for _, r in uplift[uplift.metric == "pr_auc"].iterrows():
        md.append(f"| {r.project} | {r.learner} | {r.feature_set} | {r.delta_mean:+.3f} ± {r.delta_std:.3f} | "
                  f"{r.folds_improved} | {r.p_corrected_ttest:.3f} |")
    (RES / "ml_results.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("wrote results/ml_results.{csv,md}, ml_uplift.csv, ml_folds.csv")


if __name__ == "__main__":
    main()
