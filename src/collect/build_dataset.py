"""Join everything for one new target into the authors' five input CSVs (same columns, same order), so the
authors' own R pipeline (src/reproduce/run_original.R) can be run on it unchanged (Phase 2).

Inputs  (data/new/<id>/): process_metrics.csv, post_release_defects.csv, product_metrics.csv,
                          raw/analyzer/*_{CatchBlock,CatchBlock_Meta,PossibleExceptionsBlock,ThrowsBlock}.csv
Outputs (data/new/<id>/input/): File_Level-Git-Jira.csv, File_Level-Understand.csv, File_Level-Catch_Based.csv,
                                File_Level-Try_Based.csv, File_Level-Throws_Based.csv
        data/new/<id>/dataset_manifest.json  (row counts, product-metric back-end, missing columns)

Usage: python src/collect/build_dataset.py <target-id>
"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aggregate_jtratch import aggregate  # noqa: E402
from clone_repo import NEW, ROOT, load_target  # noqa: E402
from history import release_files  # noqa: E402

ORIG = ROOT / "external" / "scripts_with_input_data" / "input"


def header(name: str) -> list:
    return list(pd.read_csv(ORIG / f"File_Level-{name}.csv", nrows=0).columns)


def main(tid: str) -> dict:
    t = load_target(tid)
    out, wt = NEW / tid, NEW / tid / "src"
    inp = out / "input"
    inp.mkdir(parents=True, exist_ok=True)
    files = release_files(wt, t["include_regex"], t["exclude_regex"])
    manifest = {"target": tid, "release_files": len(files)}

    # Git-Jira (process metrics + outcome)
    if t["language"] != "java":
        raise SystemExit(f"{tid}: file-level aggregation of analyzer output is implemented and validated for Java "
                         f"(JTratch) only; C# (NTratch) aggregation is future work (docs/REPRODUCTION.md T5).")
    pm = pd.read_csv(out / "process_metrics.csv")
    post_path = out / "post_release_defects.csv"
    manifest["has_outcome"] = post_path.exists()
    if post_path.exists():
        post = pd.read_csv(post_path)
    else:   # no issue tracker / mining failed: metrics only, outcome unknown (recorded; models are skipped)
        post = pd.DataFrame({"File.Path": files, "Distinct.count.of.Issue.Key.POST": 0})
    g = pm.merge(post, on="File.Path", how="left").fillna({"Distinct.count.of.Issue.Key.POST": 0})
    g = g.rename(columns=lambda c: c.replace(".", " ") if c.startswith(("Distinct", "Churn", "File.")) else c)
    g = g[header("Git-Jira")]
    g.to_csv(inp / "File_Level-Git-Jira.csv", index=False)
    manifest["git_jira_rows"] = len(g)
    manifest["post_release_defective_files"] = int((g["Distinct count of Issue Key POST"] > 0).sum())

    # Understand (or fallback) product metrics
    prod = pd.read_csv(out / "product_metrics.csv").rename(columns={"File.Path": "File Path"})
    meta = json.loads((out / "product_metrics_meta.json").read_text())
    uh = header("Understand")
    prod["File"] = prod["File Path"]
    prod["Name"] = prod["File Path"]
    prod["Kind"] = "File"
    prod["Table Name"] = f"{tid}_{meta['backend']}.csv"
    prod["Number of Records"] = 1
    present = [c for c in uh if c in prod.columns]
    manifest["product_metrics_backend"] = meta["backend"]
    manifest["product_metrics_missing_vs_understand"] = [c for c in uh if c not in prod.columns]
    prod[present].to_csv(inp / "File_Level-Understand.csv", index=False)

    # Exception handling (JTratch)
    C, T, TH = aggregate(out / "raw" / "analyzer", wt, tid, keep_files=files)
    for df, name in ((C, "Catch_Based"), (T, "Try_Based"), (TH, "Throws_Based")):
        h = header(name)
        missing = [c for c in h if c not in df.columns]
        if missing:
            raise SystemExit(f"{name}: aggregation is missing columns {missing}")
        df[h].to_csv(inp / f"File_Level-{name}.csv", index=False)
        manifest[f"{name.lower()}_rows"] = len(df)
    manifest["files_with_catch"] = len(C)
    manifest["defective_files_with_catch"] = int(
        g[g["File Path"].isin(C["File Path"])]["Distinct count of Issue Key POST"].gt(0).sum())
    (out / "dataset_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))
    return manifest


if __name__ == "__main__":
    main(sys.argv[1])
