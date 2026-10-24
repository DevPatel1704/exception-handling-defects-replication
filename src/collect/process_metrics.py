"""Pre-release process metrics per release file (paper Sec. 3.3.3), same column names as the released data.

Pre-release window = commits in prev_release_tag..release_tag (reachable from the release, not from the
previous release), non-merge, rename-aware. Per file:
  Distinct.count.of.Commit.Hash.PRE   number of changes
  Churn.PRE                           lines added + deleted
  Distinct.count.of.Author.Email.PRE  unique author e-mails
  Distinct.count.of.Issue.Key.PRE     distinct fixed Bug issues (Jira) referenced by those commits
  fileSize                            bytes at the release

Usage: python src/collect/process_metrics.py <target-id>
Writes data/new/<id>/process_metrics.csv
"""
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clone_repo import NEW, load_target, repo_dir  # noqa: E402
from history import make_tracker, release_files, walk  # noqa: E402


def main(tid: str) -> pd.DataFrame:
    t = load_target(tid)
    out, wt, rd = NEW / tid, NEW / tid / "src", repo_dir(t)
    files = release_files(wt, t["include_regex"], t["exclude_regex"])
    print(f"{tid}: {len(files)} release files", flush=True)
    # no previous release given -> the whole history up to the release
    rev = f"{t['prev_release_tag']}..{t['release_tag']}" if t.get("prev_release_tag") else t["release_tag"]
    commits = walk(rd, rev, files, "backward")
    print(f"  pre-release commits ({rev}) touching release files: {len(commits)}", flush=True)

    bugs, meta = set(), {"pre_release_range": rev, "tracker_ok": True}
    tracker = make_tracker(t, out / "raw")
    if tracker is not None:
        try:
            keys = set().union(*(tracker.keys(c.message) for c in commits)) if commits else set()
            bugs = {k for k, v in tracker.fetch(keys).items() if tracker.is_fixed_bug(v)}
        except Exception as e:  # noqa: BLE001 - pre-release bug counts are one metric; don't lose the others
            meta.update(tracker_ok=False, tracker_error=str(e))
            print(f"  WARNING: issue tracker failed ({e}); Distinct.count.of.Issue.Key.PRE set to 0", flush=True)
    (out / "process_metrics_meta.json").write_text(__import__("json").dumps(meta, indent=2))

    agg = defaultdict(lambda: {"commits": set(), "authors": set(), "churn": 0, "bugs": set()})
    for c in commits:
        ks = tracker.keys(c.message) & bugs if tracker is not None else set()
        for f, (a, d) in c.files.items():
            r = agg[f]
            r["commits"].add(c.sha); r["authors"].add(c.author_email); r["churn"] += a + d; r["bugs"] |= ks
    rows = []
    for f in files:
        r = agg.get(f, {"commits": (), "authors": (), "churn": 0, "bugs": ()})
        rows.append({"File.Path": f, "Project": tid, "fileSize": (wt / f).stat().st_size,
                     "Distinct.count.of.Author.Email.PRE": len(r["authors"]),
                     "Distinct.count.of.Commit.Hash.PRE": len(r["commits"]),
                     "Distinct.count.of.Issue.Key.PRE": len(r["bugs"]),
                     "Churn.PRE": r["churn"]})
    df = pd.DataFrame(rows)
    df.to_csv(out / "process_metrics.csv", index=False)
    print(f"  wrote {out / 'process_metrics.csv'} ({len(df)} files; {(df['Distinct.count.of.Commit.Hash.PRE'] > 0).sum()} changed pre-release)")
    return df


if __name__ == "__main__":
    main(sys.argv[1])
