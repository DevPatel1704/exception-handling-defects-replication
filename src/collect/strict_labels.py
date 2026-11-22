"""Label-noise sensitivity (check V2): rebuild the outcome from *strict* defect links only and refit the models.

Key-based issue-commit linking can mislabel files (Bird et al., FSE 2009): reverts and merges carry an issue key
without fixing anything, commits that name several issues mix fixes ("tangled" changes), and an issue fixed only in
a later release line may not concern the analysed release. This script applies four automatic rules to every
(issue, commit) link of a target, recomputes `Distinct count of Issue Key POST` from the links that pass all
rules, writes the authors' five input CSVs with only that column changed, and (unless --no-models) refits BASE /
BSFC / BSAP with the bug-fixed authors' code.

Rules (a link is dropped if any applies):
  R1 revert    commit subject starts with "Revert"
  R2 merge     commit has more than one parent
  R3 tangled   commit message names more than one issue key of the tracker's projects
  R4 off-line  none of the issue's fix versions belongs to the release line (e.g. 3.6.x for release 3.6.0)

Usage: python src/collect/strict_labels.py <target-id> [--no-models]
Writes: data/new/<id>/input_strict/ (5 CSVs), data/new/<id>/strict_links.csv (every link with its flags),
        results/new/<id>/strict/fixed/ (models), results/new/<id>/strict/summary.json
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clone_repo import NEW, ROOT, load_target, repo_dir  # noqa: E402
from history import tracker_config  # noqa: E402


def git(repo: Path, *args) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8",
                          errors="replace", check=True).stdout


def release_line(tag: str) -> str:
    m = re.search(r"(\d+)\.(\d+)", tag)
    return f"{m.group(1)}.{m.group(2)}." if m else ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--no-models", action="store_true")
    a = ap.parse_args()
    tid = a.target
    t = load_target(tid)
    base = NEW / tid
    repo = repo_dir(t)
    keys = tracker_config(t).get("project_keys") or []
    key_re = re.compile(r"\b(?:" + "|".join(map(re.escape, keys)) + r")-\d+\b") if keys else re.compile(r"\b[A-Z][A-Z0-9]+-\d+\b")
    line = release_line(t["release_tag"])

    L = pd.read_csv(base / "defect_links.csv")
    per = L.groupby(["issue", "commit"], sort=True).agg(fix_versions=("fix_versions", "first"),
                                                        subject=("commit_subject", "first")).reset_index()
    flags = []
    for r in per.itertuples():
        info = git(repo, "show", "-s", "--format=%P%n%B", r.commit)
        parents, _, msg = info.partition("\n")
        issue_keys = set(key_re.findall(msg))
        fv = str(r.fix_versions) if pd.notna(r.fix_versions) else ""
        flags.append(dict(issue=r.issue, commit=r.commit,
                          r1_revert=str(r.subject).strip().lower().startswith("revert"),
                          r2_merge=len(parents.split()) > 1,
                          r3_tangled=len(issue_keys | {r.issue}) > 1,
                          r4_off_line=not any(v.strip().startswith(line) for v in fv.split(";") if v.strip())))
    F = pd.DataFrame(flags)
    F["strict"] = ~F[["r1_revert", "r2_merge", "r3_tangled", "r4_off_line"]].any(axis=1)
    F.to_csv(base / "strict_links.csv", index=False)
    S = L.merge(F[["issue", "commit", "strict"]], on=["issue", "commit"])
    S = S[S.strict]

    # outcome from strict links only; everything else in the authors' input format unchanged
    src, dst = base / "input", base / "input_strict"
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst)
    gj = pd.read_csv(dst / "File_Level-Git-Jira.csv")
    counts = S.groupby("File.Path")["issue"].nunique()
    before = int((gj["Distinct count of Issue Key POST"] > 0).sum())
    gj["Distinct count of Issue Key POST"] = gj["File Path"].map(counts).fillna(0).astype(int)
    gj.to_csv(dst / "File_Level-Git-Jira.csv", index=False)
    after = int((gj["Distinct count of Issue Key POST"] > 0).sum())

    summary = dict(target=tid, links=len(F), strict_links=int(F.strict.sum()),
                   dropped={k: int(F[k].sum()) for k in ("r1_revert", "r2_merge", "r3_tangled", "r4_off_line")},
                   issues=int(L.issue.nunique()), strict_issues=int(S.issue.nunique()),
                   defective_files=before, defective_files_strict=after,
                   files_relabelled_clean=before - after)
    print(json.dumps(summary, indent=1))
    out = ROOT / "results" / "new" / tid / "strict"
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(json.dumps(summary, indent=1))
    if a.no_models:
        return
    rscript = shutil.which("Rscript")
    if not rscript:
        raise SystemExit("Rscript not found: run through ./envrun.sh")
    with open(out / "models.log", "w", encoding="utf-8") as fh:
        r = subprocess.run([rscript, "src/reproduce/run_original.R", "fixed", "--input",
                            dst.relative_to(ROOT).as_posix(), "--out", out.relative_to(ROOT).as_posix()],
                           cwd=ROOT, stdout=fh, stderr=subprocess.STDOUT)
    if r.returncode != 0:
        raise SystemExit(f"R models failed; see {out / 'models.log'}")
    d = pd.read_csv(out / "fixed" / "base_test_2.csv")
    print("; ".join(f"{x.metric_set} R2={x.r2_c_r:.3f}" for x in d[d.file_set == "CAT"].itertuples()))


if __name__ == "__main__":
    main()
