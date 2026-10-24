"""Label post-release defects per release file (paper Sec. 3.3.1).

Following the paper (not full SZZ): a post-release defect of file F is a FIXED Jira issue of type Bug,
REPORTED AFTER the release date, whose key is referenced by a bug-fixing commit in the post-release window
(release_tag..post_release_tag) that modifies F. Paths are mapped back to the release name through renames.
Outcome column: Distinct.count.of.Issue.Key.POST (distinct such issues per file), as in the released data.
For targets tracked on GitHub Issues, "Bug" = a closed issue/PR with a bug-like label (see history.GitHubTracker).

Note: SZZ's second step (finding the bug-INTRODUCING commit) is not needed for a file-level post-release
label and is not used by the paper; we only use the fix-commit -> file link.

Usage: python src/collect/defect_mining.py <target-id> [--sample 40]
Writes:
  data/new/<id>/post_release_defects.csv      File.Path, Distinct.count.of.Issue.Key.POST
  data/new/<id>/defect_links.csv              every (issue, commit, file) link with dates and summaries
  data/new/<id>/manual_validation_sample.csv  random sample of links for manual checking (blank verdict column)
"""
import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clone_repo import NEW, load_target, repo_dir  # noqa: E402
from history import make_tracker, release_files, tracker_config, walk  # noqa: E402


def main(tid: str, sample: int = 40) -> pd.DataFrame:
    t = load_target(tid)
    out, wt, rd = NEW / tid, NEW / tid / "src", repo_dir(t)
    tracker = make_tracker(t, out / "raw")
    if tracker is None:
        msg = (f"{tid}: no issue tracker configured — post-release defect labels cannot be mined. "
               f"{t.get('issue_tracker_note', '')}")
        (out / "BLOCKED_defect_mining.txt").write_text(msg + "\n")
        raise SystemExit(msg)
    files = release_files(wt, t["include_regex"], t["exclude_regex"])
    release_date = datetime.fromisoformat(
        __import__("json").loads((out / "provenance.json").read_text())["release"]["commit_date"])
    commits = walk(rd, f"{t['release_tag']}..{t['post_release_tag']}", files, "forward")
    print(f"{tid}: release {t['release_tag']} ({release_date.date()}); post-release commits touching "
          f"release files: {len(commits)}; tracker: {tracker.kind}", flush=True)

    keys = set().union(*(tracker.keys(c.message) for c in commits)) if commits else set()
    issues = tracker.fetch(keys)

    links, stats = [], {"tracker": tracker_config(t)["type"], "keys_referenced": len(keys), "not_found": 0,
                        "not_fixed_bug": 0, "reported_before_release": 0}
    for c in commits:
        for k in sorted(tracker.keys(c.message)):   # sorted: set order varies per process (hash seed)
            iss = issues.get(k)
            if iss is None:
                stats["not_found"] += 1; continue
            if not tracker.is_fixed_bug(iss):
                stats["not_fixed_bug"] += 1; continue
            created = tracker.created(iss)
            if created <= release_date:
                stats["reported_before_release"] += 1; continue
            for f in sorted(c.files):
                links.append({"issue": k, "issue_created": iss["created"], "issue_summary": iss["summary"],
                              "fix_versions": ";".join(iss["fixVersions"]), "commit": c.sha,
                              "commit_date": datetime.fromtimestamp(c.timestamp, timezone.utc).isoformat(),
                              "commit_subject": c.message.splitlines()[0][:200], "File.Path": f})
    L = pd.DataFrame(links)
    if len(L):
        L = L.sort_values(["issue", "commit", "File.Path"]).reset_index(drop=True)
    L.to_csv(out / "defect_links.csv", index=False)
    counts = L.groupby("File.Path")["issue"].nunique() if len(L) else pd.Series(dtype=int)
    df = pd.DataFrame({"File.Path": files})
    df["Distinct.count.of.Issue.Key.POST"] = df["File.Path"].map(counts).fillna(0).astype(int)
    df.to_csv(out / "post_release_defects.csv", index=False)

    if len(L):
        per_link = (L.groupby(["issue", "commit"], sort=True)
                    .agg(**{c: (c, "first") for c in L.columns if c not in ("issue", "commit", "File.Path")},
                         files=("File.Path", lambda x: ";".join(sorted(set(x)))), n_files=("File.Path", "nunique"))
                    .reset_index())
        s = per_link.sample(n=min(sample, len(per_link)), random_state=2018)
        s = s.assign(issue_url=s["issue"].map(tracker.url),
                     commit_url=t["repo"].removesuffix(".git") + "/commit/" + s["commit"],
                     verdict_is_real_post_release_bug_fix="", verdict_files_correct="", reviewer="", notes="")
        s.to_csv(out / "manual_validation_sample.csv", index=False)
    stats.update(post_release_defect_issues=int(L["issue"].nunique()) if len(L) else 0,
                 defective_files=int((df["Distinct.count.of.Issue.Key.POST"] > 0).sum()), files=len(df))
    print("  " + ", ".join(f"{k}={v}" for k, v in stats.items()))
    (out / "defect_mining_stats.json").write_text(__import__("json").dumps(stats, indent=2))
    return df


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--sample", type=int, default=40)
    a = ap.parse_args()
    main(a.target, a.sample)
