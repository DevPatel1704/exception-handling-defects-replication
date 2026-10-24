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
from history import Jira, is_fixed_bug, issue_keys, release_files, walk  # noqa: E402


def main(tid: str) -> pd.DataFrame:
    t = load_target(tid)
    out, wt, rd = NEW / tid, NEW / tid / "src", repo_dir(t)
    files = release_files(wt, t["include_regex"], t["exclude_regex"])
    print(f"{tid}: {len(files)} release files", flush=True)
    commits = walk(rd, f"{t['prev_release_tag']}..{t['release_tag']}", files, "backward")
    print(f"  pre-release commits touching release files: {len(commits)}", flush=True)

    bugs = {}
    if t.get("jira"):
        keys = set().union(*(issue_keys(c.message, t["jira"]["project_keys"]) for c in commits)) if commits else set()
        jira = Jira(t["jira"]["base"], t["jira"]["api"], out / "raw" / "jira_issues.json")
        bugs = {k for k, v in jira.fetch(keys).items() if is_fixed_bug(v)}

    agg = defaultdict(lambda: {"commits": set(), "authors": set(), "churn": 0, "bugs": set()})
    for c in commits:
        ks = issue_keys(c.message, t["jira"]["project_keys"]) & bugs if t.get("jira") else set()
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
