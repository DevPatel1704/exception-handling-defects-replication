"""Validity check for RQ1 on new data: how much do the authors' models move when only the analyzer run changes?

JTratch is not run-to-run deterministic (docs/REPRODUCTION.md §8, F1): on identical sources, some flow (try-based)
metrics differ between JVM runs. This script re-runs JTratch N times on the *same* release checkout, rebuilds the
authors' five input CSVs from each run (everything except the analyzer output is held fixed: process metrics,
product metrics and defect labels are read from data/new/<id>/), refits BASE / BSFC / BSAP with the authors'
bug-fixed R code, and reports

  * which exception-handling metrics change between runs and in how many files (metric_stability.csv),
  * the optimism-reduced R² of every model in every run (runs.csv),
  * how often each predictor is significant in the simplified model, with its sign (predictor_stability.csv),
  * a readable summary (variance.md), with the run kept as the pipeline's fixed artifact shown for reference.

Usage: python src/collect/analyzer_variance.py <target-id> [--runs 10] [--xmx 4g] [--summarise-only]
Runs are resumable: a run whose model output already exists is not repeated.
Work files: build/variance/<id>/ (gitignored). Results: results/new/<id>/variance/.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_dataset  # noqa: E402
from clone_repo import NEW, ROOT, load_target  # noqa: E402
from run_analyzers import build_jtratch, find_java8  # noqa: E402

KEY = "File Path"
MODELS = ["BASE", "BSFC", "BSAP"]


def run_one(tid: str, i: int, java: str, xmx: str) -> Path:
    """One analyzer run + dataset + models. Returns the model output dir (…/fixed)."""
    rel = Path("build") / "variance" / tid / f"{tid}_run{i:02d}"
    work = ROOT / rel
    res = work / "fixed"
    if (res / "base_test_2.csv").exists() and (res / "predictors_simplified.csv").exists():
        print(f"run {i:02d}: reused", flush=True)
        return res
    raw, inp = work / "analyzer", work / "input"
    shutil.rmtree(raw, ignore_errors=True)
    raw.mkdir(parents=True)
    src = (NEW / tid / "src").resolve()
    t0 = time.time()
    with open(raw / "jtratch_stdout.txt", "w", encoding="utf-8") as fh:
        r = subprocess.run([java, f"-Xmx{xmx}", "-cp", build_jtratch(java), "ca.concordia.jtratch.JTratch",
                            "ByFolder", src.as_posix(), "NONE"], cwd=raw, stdout=fh, stderr=subprocess.STDOUT)
    if r.returncode != 0 or not list(raw.glob("*_PossibleExceptionsBlock.csv")):
        raise SystemExit(f"run {i:02d}: JTratch failed (exit {r.returncode}); see {raw / 'jtratch_stdout.txt'}")
    t1 = time.time()
    build_dataset.main(tid, raw_dir=raw, inp_dir=inp)
    rscript = shutil.which("Rscript")
    if not rscript:
        raise SystemExit("Rscript not found: run through ./envrun.sh")
    with open(work / "models.log", "w", encoding="utf-8") as fh:
        r = subprocess.run([rscript, "src/reproduce/run_original.R", "fixed", "--input", (rel / "input").as_posix(),
                            "--out", rel.as_posix()], cwd=ROOT, stdout=fh, stderr=subprocess.STDOUT)
    if r.returncode != 0:
        raise SystemExit(f"run {i:02d}: R models failed; see {work / 'models.log'}")
    print(f"run {i:02d}: JTratch {t1 - t0:.0f}s, models {time.time() - t1:.0f}s", flush=True)
    return res


def model_rows(res: Path, run: str, groups: pd.DataFrame) -> tuple:
    group_of = dict(zip(groups.metric, groups.group))
    bt = pd.read_csv(res / "base_test_2.csv")
    bt = bt[bt.file_set == "CAT"]
    pr = pd.read_csv(res / "predictors_simplified.csv")
    pr["model"] = pr["model"].str.split(".").str[1]
    runs, preds = [], []
    for _, x in bt.iterrows():
        sig = pr[(pr.model == x.metric_set) & (pr.p_value < 0.05)]
        runs.append(dict(run=run, model=x.metric_set, r2_optimism_reduced=round(x.r2_c_r, 4),
                         r2_apparent=round(x.r2_r, 4), files=int(x.n), budget=int(x.budget),
                         potential_predictors=int(x.nvar_initial), cutoff=x.cutoff,
                         significant_eh="; ".join(sorted(p for p in sig.predictor if group_of.get(p) != "base")),
                         significant_base="; ".join(sorted(p for p in sig.predictor if group_of.get(p) == "base"))))
        for _, p in sig.iterrows():
            preds.append(dict(run=run, model=x.metric_set, predictor=p.predictor,
                              group=group_of.get(p.predictor, "?"), sign="+" if p.coef > 0 else "-",
                              wald_chi2=p.wald_chi2))
    return runs, preds


def metric_stability(inputs: dict) -> pd.DataFrame:
    """For every EH metric: in how many files does any run disagree with the first run?"""
    rows = []
    for name in ("Catch_Based", "Try_Based", "Throws_Based"):
        frames = {r: pd.read_csv(p / f"File_Level-{name}.csv").set_index(KEY) for r, p in inputs.items()}
        ref_run, ref = next(iter(frames.items()))
        for col in ref.columns:
            if not pd.api.types.is_numeric_dtype(ref[col]):
                continue
            differs = pd.Series(False, index=ref.index)
            max_abs = 0.0
            for r, f in frames.items():
                if r == ref_run:
                    continue
                other = f[col].reindex(ref.index)
                d = (other - ref[col]).abs()
                differs |= d.fillna(1) > 1e-9
                max_abs = max(max_abs, float(d.max(skipna=True) or 0))
            rows.append(dict(source=name, metric=col, files=len(ref), files_differing=int(differs.sum()),
                             share_differing=round(differs.mean(), 4), max_abs_diff=round(max_abs, 4)))
    return pd.DataFrame(rows)


def summarise(tid: str, n_runs: int) -> None:
    out = ROOT / "results" / "new" / tid / "variance"
    out.mkdir(parents=True, exist_ok=True)
    kept = ROOT / "results" / "new" / tid / "fixed"
    groups = pd.read_csv(kept / "metric_groups.csv")
    run_dirs = {f"run{i:02d}": ROOT / "build" / "variance" / tid / f"{tid}_run{i:02d}" for i in range(1, n_runs + 1)}
    run_dirs = {r: d for r, d in run_dirs.items() if (d / "fixed" / "base_test_2.csv").exists()}
    if not run_dirs:
        raise SystemExit("no finished runs")

    all_runs, all_preds = model_rows(kept, "kept", groups)
    for r, d in run_dirs.items():
        a, b = model_rows(d / "fixed", r, groups)
        all_runs += a
        all_preds += b
    runs = pd.DataFrame(all_runs)
    preds = pd.DataFrame(all_preds)
    runs.to_csv(out / "runs.csv", index=False)

    fresh = runs[runs.run != "kept"]
    n = len(run_dirs)
    stab = (preds[preds.run != "kept"].groupby(["model", "predictor", "group"])
            .agg(runs_significant=("run", "nunique"), signs=("sign", lambda s: "".join(sorted(set(s)))),
                 median_wald_chi2=("wald_chi2", "median")).reset_index())
    kept_sig = set(zip(preds[preds.run == "kept"].model, preds[preds.run == "kept"].predictor))
    stab["share"] = (stab.runs_significant / n).round(3)
    stab["in_kept_run"] = [(m, p) in kept_sig for m, p in zip(stab.model, stab.predictor)]
    stab = stab.sort_values(["model", "runs_significant"], ascending=[True, False],
                            key=lambda s: s.map({m: i for i, m in enumerate(MODELS)}) if s.name == "model" else s)
    stab.to_csv(out / "predictor_stability.csv", index=False)

    ms = metric_stability({r: d / "input" for r, d in run_dirs.items()})
    ms.to_csv(out / "metric_stability.csv", index=False)

    summ = []
    for m in MODELS:
        f = fresh[fresh.model == m]
        k = runs[(runs.run == "kept") & (runs.model == m)]
        sets = f.significant_eh.fillna("") + " | " + f.significant_base.fillna("")
        modal = sets.mode().iloc[0] if len(sets) else ""
        summ.append(dict(target=tid, model=m, runs=len(f), r2_kept=float(k.r2_optimism_reduced.iloc[0]),
                         r2_mean=round(f.r2_optimism_reduced.mean(), 4), r2_sd=round(f.r2_optimism_reduced.std(ddof=1), 4),
                         r2_min=f.r2_optimism_reduced.min(), r2_max=f.r2_optimism_reduced.max(),
                         distinct_r2=f.r2_optimism_reduced.round(3).nunique(),
                         distinct_predictor_sets=sets.nunique(),
                         share_runs_modal_set=round((sets == modal).mean(), 3),
                         share_runs_same_set_as_kept=round(
                             (sets == (k.significant_eh.fillna("") + " | " + k.significant_base.fillna("")).iloc[0]).mean(), 3)))
    summ = pd.DataFrame(summ)
    summ.to_csv(out / "summary.csv", index=False)

    varying = ms[ms.files_differing > 0].sort_values("files_differing", ascending=False)
    md = [f"# Analyzer run-to-run variance: {tid}", "",
          f"{n} fresh JTratch runs on the identical release checkout (`data/new/{tid}/src`); process metrics, product "
          f"metrics and defect labels held fixed; the authors' bug-fixed models refit on each run. 'kept' = the "
          f"analyzer run the pipeline keeps as its fixed artifact (`results/new/{tid}/fixed`).",
          f"Generated by `python src/collect/analyzer_variance.py {tid} --runs {n_runs}`.", "",
          "## Model fit across runs (optimism-reduced Nagelkerke R²)", "",
          "| Model | kept | mean ± sd | min – max | distinct R² | distinct predictor sets | runs with kept run's set |",
          "|---|---:|---|---|---:|---:|---:|"]
    for _, r in summ.iterrows():
        md.append(f"| {r.model} | {r.r2_kept:.3f} | {r.r2_mean:.3f} ± {r.r2_sd:.3f} | {r.r2_min:.3f} – {r.r2_max:.3f} | "
                  f"{r.distinct_r2} | {r.distinct_predictor_sets} | {r.share_runs_same_set_as_kept:.0%} |")
    md += ["", "## Exception-handling metrics that change between runs", "",
           f"{len(varying)} of {len(ms)} file-level EH metrics differ in at least one file across the {n} runs "
           f"(by source: " + ", ".join(f"{s} {int((varying.source == s).sum())}/{int((ms.source == s).sum())}"
                                       for s in ('Catch_Based', 'Try_Based', 'Throws_Based')) + ").", ""]
    if len(varying):
        md += ["| Source | Metric | files differing | max abs. diff |", "|---|---|---:|---:|"]
        md += [f"| {r.source} | {r.metric} | {r.files_differing} / {r.files} | {r.max_abs_diff:g} |"
               for _, r in varying.head(20).iterrows()]
    md += ["", "## Significant predictors (p < 0.05) across runs", "",
           "| Model | Predictor | Group | runs significant | sign | in kept run |", "|---|---|---|---:|:-:|:-:|"]
    md += [f"| {r.model} | {r.predictor} | {r.group} | {r.runs_significant}/{n} | {r.signs} | {'yes' if r.in_kept_run else 'no'} |"
           for _, r in stab.iterrows()]
    md += ["", "## Per run", "", "| Run | Model | R² | Cutoff | # potential | Significant EH predictors |",
           "|---|---|---:|---:|---:|---|"]
    md += [f"| {r.run} | {r.model} | {r.r2_optimism_reduced:.3f} | {r.cutoff:g} | {r.potential_predictors} | "
           f"{r.significant_eh if isinstance(r.significant_eh, str) and r.significant_eh else '—'} |"
           for _, r in runs.iterrows()]
    (out / "variance.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(summ.to_string(index=False))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--runs", type=int, default=10)
    ap.add_argument("--xmx", default=os.environ.get("JTRATCH_XMX", "4g"))
    ap.add_argument("--summarise-only", action="store_true")
    a = ap.parse_args()
    t = load_target(a.target)
    if t["language"] != "java":
        raise SystemExit("JTratch variance applies to Java targets only")
    if not a.summarise_only:
        java = find_java8()
        for i in range(1, a.runs + 1):
            run_one(a.target, i, java, a.xmx)
    summarise(a.target, a.runs)
    (ROOT / "results" / "new" / a.target / "variance" / "settings.json").write_text(json.dumps(
        {"runs": a.runs, "jvm_heap": a.xmx, "analyzer": "JTratch @ eh-model-defects2018 (af7c232)",
         "models": "src/reproduce/run_original.R fixed (seed 2018)"}, indent=1))


if __name__ == "__main__":
    main()
