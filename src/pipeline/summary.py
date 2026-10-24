"""Collect everything the pipeline produced for one target into results/new/<id>/summary.json
(what the dashboard renders). Missing pieces are simply absent; caveats explain why.

Usage: python src/pipeline/summary.py <target-id>
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src" / "collect"))
sys.path.insert(0, str(ROOT / "src" / "ml"))
sys.path.insert(0, str(ROOT / "src" / "reproduce"))
from clone_repo import NEW, load_target  # noqa: E402
from common import pretty_names  # noqa: E402
from history import tracker_config  # noqa: E402

PAPER_R2 = {"hadoop": {"BASE": 0.33, "BSFC": 0.37, "BSAP": 0.35}, "hibernate-orm": {"BASE": 0.21, "BSFC": 0.28, "BSAP": 0.23},
            "umbraco-cms": {"BASE": 0.09, "BSFC": 0.09, "BSAP": 0.18}}
# Flow metrics that changed between repeated JTratch runs on identical sources (docs/REPRODUCTION.md §8).
UNSTABLE_JTRATCH = {"Avg Max Depth", "Avg Depth", "Avg # Declaring Methods", "% Doc in Comment", "% Method Declaration",
                    "% Throw Statement"}
PAPER_RELEASE = {"hadoop": "Hadoop 2.6.0", "hibernate-orm": "Hibernate 5.0.0.Final", "umbraco-cms": "Umbraco 7.6.0"}


def _json(p: Path):
    return json.loads(p.read_text()) if p.exists() else None


def _rel(p: Path) -> str:
    return "/" + p.resolve().relative_to(ROOT).as_posix()


def eh_profile(inp: Path) -> dict:
    c = inp / "File_Level-Catch_Based.csv"
    if not c.exists():
        return None
    d = pd.read_csv(c)
    n_catch = int(d["# Catch"].sum())
    aps = []
    for col in d.columns:
        if col.startswith(("AP ", "Sum of AP ")):
            name = col.replace("Sum of AP ", "").replace("AP ", "")
            aps.append({"anti_pattern": name, "catch_blocks": int(d[col].sum()),
                        "pct_of_catch_blocks": round(100 * d[col].sum() / n_catch, 2) if n_catch else None,
                        "files": int((d[col] > 0).sum())})
    t = inp / "File_Level-Try_Based.csv"
    tri = pd.read_csv(t) if t.exists() else None
    return {"files_with_catch": int(len(d)), "catch_blocks": n_catch,
            "try_blocks": int(tri["# Try"].sum()) if tri is not None else None,
            "mean_possible_exceptions_per_try": round(float((tri["# Possible Exceptions"] * tri["# Try"]).sum()
                                                            / tri["# Try"].sum()), 3) if tri is not None and len(tri) else None,
            "anti_patterns": sorted(aps, key=lambda x: -x["catch_blocks"])}


def models(res: Path) -> dict:
    b2 = res / "fixed" / "base_test_2.csv"
    if not b2.exists():
        return None
    pretty = pretty_names()
    d = pd.read_csv(b2)
    pred = pd.read_csv(res / "fixed" / "predictors_simplified.csv") if (res / "fixed" / "predictors_simplified.csv").exists() else pd.DataFrame()
    groups = pd.read_csv(res / "fixed" / "metric_groups.csv")
    group_of = dict(zip(groups.metric, groups.group))
    out = []
    for _, x in d[d.file_set == "CAT"].iterrows():
        p = pred[pred.model == x["name"]] if len(pred) else pred
        out.append({"model": x["metric_set"], "r2_optimism_reduced": round(float(x["r2_c_r"]), 3) if pd.notna(x["r2_c_r"]) else None,
                    "r2_apparent": round(float(x["r2_r"]), 3) if pd.notna(x["r2_r"]) else None,
                    "files": int(x["n"]), "budget": int(x["budget"]), "potential_predictors": int(x["nvar_initial"]),
                    "cutoff": float(x["cutoff"]), "over_budget": bool(x["over_budget"]),
                    "predictors": [{"metric": r.predictor, "name": pretty.get(r.predictor, r.predictor),
                                    "group": {"base": "traditional", "catch": "anti-pattern", "try": "flow"}.get(
                                        group_of.get(r.predictor), group_of.get(r.predictor)),
                                    "wald_chi2": round(float(r.wald_chi2), 2), "p_value": float(r.p_value),
                                    "direction": "+" if r.coef > 0 else "-",
                                    "effect_pct": round(float(r.effect_rel_pct), 2)} for r in p.itertuples()]})
    # The paper (Sec. 3.4.6) keeps BASE-significant metrics in BSFC/BSAP. The released code re-adds them but its
    # second budget-based reduction can drop them again (it logs "Significant ... STILL ... missing" and carries
    # on). Never triggered on the paper's data; it does on small targets, so flag it.
    base = next((m for m in out if m["model"] == "BASE"), None)
    if base:
        base_sig = {p["metric"] for p in base["predictors"] if p["group"] == "traditional"}
        for m in out:
            if m["model"] != "BASE":
                cand = str(d.loc[d.metric_set == m["model"], "form"].iloc[0])
                m["dropped_base_significant"] = sorted(
                    pretty.get(v, v) for v in base_sig if v not in set(re.split(r"[\s+]+", cand)))
    order = {"BASE": 0, "BSFC": 1, "BSAP": 2}
    prelim = []
    b1 = res / "fixed" / "base_test_1.csv"
    if b1.exists():
        for _, x in pd.read_csv(b1).iterrows():
            prelim.append({"model": x["name"], "r2_optimism_reduced": round(float(x["r2_c_r"]), 3) if pd.notna(x["r2_c_r"]) else None,
                           "significant": [s.strip() for s in str(x["signifcant_r"]).split(",") if s.strip() not in ("TOTAL", "nan", "")]})
    return {"presented": sorted(out, key=lambda m: order.get(m["model"], 9)), "preliminary_all_files": prelim}


def ml(res: Path) -> dict:
    r = res / "ml" / "ml_results.csv"
    if not r.exists():
        return None
    out = {"results": pd.read_csv(r).round(4).to_dict("records")}
    u = res / "ml" / "ml_uplift.csv"
    if u.exists():
        out["uplift"] = pd.read_csv(u).round(4).to_dict("records")
    return out


def shap(res: Path, tid: str) -> dict:
    s = res / "ml" / "shap_top_eh.csv"
    if not s.exists():
        return None
    pretty = pretty_names()
    top = pd.read_csv(s)
    al = res / "ml" / "shap_alignment.csv"
    match = {}
    if al.exists():
        a = pd.read_csv(al)
        match = dict(zip(a.feature, a.matches_phase0_sig.fillna("")))
    imp = pd.read_csv(res / "ml" / "shap_importance.csv")
    return {"learner": str(top.learner.iloc[0]) if len(top) else None,
            "top_features": [{"name": pretty.get(f, f), "group": g, "mean_abs_shap": round(float(v), 5)}
                             for f, g, v in imp.head(15)[["feature", "group", "mean_abs_shap"]].itertuples(index=False)],
            "top_eh": [{"rank": int(r.eh_rank), "overall_rank": int(r["rank"]), "name": pretty.get(r.feature, r.feature),
                        "direction": "+" if r.direction > 0 else "-", "mean_abs_shap": round(float(r.mean_abs_shap), 5),
                        "matches_significant_predictor": match.get(r.feature, "")} for _, r in top.iterrows()],
            "figures": {"bar": _rel(res / "ml" / f"shap_bar_{tid}.png"),
                        "beeswarm": _rel(res / "ml" / f"shap_beeswarm_{tid}.png")},
            "per_file_values": _rel(res / "ml" / f"shap_values_{tid}.csv")
            if (res / "ml" / f"shap_values_{tid}.csv").exists() else None,
            "per_file_names": _per_file_names(res / "ml" / f"shap_values_{tid}.csv", pretty)}


def _per_file_names(path: Path, pretty: dict) -> dict:
    """R-mangled feature column -> the authors' metric name, for the per-file SHAP table."""
    if not path.exists():
        return {}
    cols = pd.read_csv(path, nrows=0).columns
    feats = [c[:-5] for c in cols if c.endswith("|shap") and c != "other_features|shap"]
    return {f: pretty.get(f, f) for f in feats}


def build(tid: str) -> dict:
    t = load_target(tid)
    out, res = NEW / tid, ROOT / "results" / "new" / tid
    res.mkdir(parents=True, exist_ok=True)
    prov = _json(out / "provenance.json")
    manifest = _json(out / "dataset_manifest.json")
    pmeta = _json(out / "product_metrics_meta.json")
    tr = tracker_config(t)
    s = {"target": tid, "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
         "repo": t["repo"].removesuffix(".git"), "language": t.get("language"),
         "tags": {"prev_release": t.get("prev_release_tag"), "release": t["release_tag"], "post_release": t["post_release_tag"]},
         "provenance": prov, "tracker": tr, "file_filters": {"include": t.get("include_regex"), "exclude": t.get("exclude_regex")},
         "defect_mining": _json(out / "defect_mining_stats.json"), "dataset": manifest,
         "product_metrics_backend": (pmeta or {}).get("backend"),
         "eh_profile": eh_profile(out / "input"), "models": models(res), "ml": ml(res), "shap": shap(res, tid)}
    key = t["repo"].lower().removesuffix(".git").rstrip("/").split("/")[-1]
    if key in PAPER_R2:
        s["paper_reference"] = {"release": PAPER_RELEASE[key], "r2_optimism_reduced": PAPER_R2[key]}
    files = {}
    for label, p in [("Git/Jira metrics (authors' format)", out / "input" / "File_Level-Git-Jira.csv"),
                     ("Product metrics", out / "input" / "File_Level-Understand.csv"),
                     ("Catch-block / anti-pattern metrics", out / "input" / "File_Level-Catch_Based.csv"),
                     ("Try-block / flow metrics", out / "input" / "File_Level-Try_Based.csv"),
                     ("Throws metrics", out / "input" / "File_Level-Throws_Based.csv"),
                     ("Post-release defect labels", out / "post_release_defects.csv"),
                     ("Defect links (issue, commit, file)", out / "defect_links.csv"),
                     ("Manual-validation sample", out / "manual_validation_sample.csv"),
                     ("Model output (authors' format)", res / "fixed" / "base_test_2.csv"),
                     ("Predictor table", res / "fixed" / "predictors_simplified.csv"),
                     ("R log", res / "fixed" / "run_log.txt"),
                     ("ML results", res / "ml" / "ml_results.md"),
                     ("SHAP alignment", res / "ml" / "shap_alignment.md")]:
        if p.exists():
            files[label] = _rel(p)
    s["files"] = files
    cav = []
    if s["product_metrics_backend"] == "fallback":
        cav.append("Product metrics come from the open-source fallback (no SciTools Understand license): 12 approximate "
                   "metrics instead of 39, so BASE is not the paper's BASE.")
    if t.get("language") == "java":
        cav.append("Exception-flow metrics come from JTratch without the authors' unpublished external-Javadoc file and "
                   "without dependency jars: about 25% fewer possible exceptions than the authors' tool found on Hibernate 5.0.")
    if tr["type"] == "github":
        cav.append("Defects come from GitHub Issues: closed issues/PRs with a bug-like label, dated by creation. The paper "
                   "used Jira issues of type Bug with resolution Fixed.")
    if tr["type"] == "none":
        cav.append("No issue tracker was given, so post-release defects were not labelled: metrics only, no models.")
    if manifest and manifest.get("defective_files_with_catch", 0) < 30 and s["models"]:
        cav.append(f"Only {manifest['defective_files_with_catch']} defective files with catch blocks: estimates are noisy.")
    used = set()
    for m in (s["models"] or {}).get("presented", []):
        used |= {p["name"] for p in m["predictors"]}
    used |= {x["name"] for x in (s["shap"] or {}).get("top_eh", [])}
    shaky = sorted(used & UNSTABLE_JTRATCH)
    if shaky:
        cav.append("JTratch is not run-to-run deterministic: on ZooKeeper 3.6.0, repeated runs on identical sources changed "
                   "6 flow metrics in up to 76 of 161 files (catch/anti-pattern metrics never changed). Here the results use "
                   f"{', '.join(shaky)}, so the flow-metric findings (BSFC, SHAP) are conditional on this analyzer run.")
    for m in (s["models"] or {}).get("presented", []):
        if m.get("dropped_base_significant"):
            cav.append(f"{m['model']}: the budget of {m['budget']} predictors ({m['files']} files / 15) forced a correlation "
                       f"cutoff of {m['cutoff']:.3f}, which dropped BASE-significant {', '.join(m['dropped_base_significant'])}. "
                       f"The authors' code behaves this way (it does not force them back), so {m['model']} vs BASE is not "
                       f"like-for-like here. This never happened on the paper's data.")
    if t.get("_source") == "dashboard":
        cav.append("Tags and filters were chosen in the dashboard; check them against the project's release notes.")
    s["caveats"] = cav
    (res / "summary.json").write_text(json.dumps(s, indent=1, default=str))
    return s


if __name__ == "__main__":
    print(json.dumps(build(sys.argv[1]), indent=1, default=str)[:3000])
