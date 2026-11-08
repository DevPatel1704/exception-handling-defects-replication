"""Prepare the manual validation of defect links (issue -> fixing commit -> release files) for two raters.

For every target with a data/new/<id>/manual_validation_sample.csv (the seeded random sample drawn by
defect_mining.py), this writes data/new/<id>/validation/:

  packet.md            one section per link: issue (type, status, resolution, dates, fix versions, summary),
                       full commit message, per-file line counts (git show --numstat), automatic pre-checks
  rating_<Rater>.csv   one blank rating sheet per rater (independent; do not look at the other sheet)

The rating protocol (questions, answer codes, examples) is docs/VALIDATION_GUIDE.md. Agreement and link precision
are computed by src/collect/validation_agreement.py once the sheets are filled in.

Usage: python src/collect/validation_packet.py [--raters Dev,Dhruv] [--targets id1,id2] [--force]
Existing rating sheets are never overwritten unless --force is given.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clone_repo import NEW, load_target, repo_dir  # noqa: E402

QUESTIONS = ["q1_real_bug", "q2_commit_fixes_issue", "q3_files_part_of_fix"]
KEY_RE = re.compile(r"\b[A-Z][A-Z0-9]+-\d+\b")


def git(repo: Path, *args) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8",
                          errors="replace", check=True).stdout


def release_line(tag: str) -> str:
    m = re.search(r"(\d+)\.(\d+)", tag)
    return f"{m.group(1)}.{m.group(2)}" if m else ""


def build(tid: str, raters: list, force: bool) -> int:
    base = NEW / tid
    sample = pd.read_csv(base / "manual_validation_sample.csv")
    t = load_target(tid)
    repo = repo_dir(t)
    issues = json.loads((base / "raw" / "jira_issues.json").read_text(encoding="utf-8"))
    prov = json.loads((base / "provenance.json").read_text())
    rel_date = prov["release"]["commit_date"]
    line = release_line(t["release_tag"])
    out = base / "validation"
    out.mkdir(exist_ok=True)

    rows, md = [], [f"# Defect-link validation packet: {tid}", "",
                    f"Release `{t['release_tag']}` ({rel_date[:10]}) → post-release `{t['post_release_tag']}`. "
                    f"{len(sample)} links drawn at random (seed 2018) by `defect_mining.py`.",
                    "Rate each link in **your own** sheet (`rating_<you>.csv`) following docs/VALIDATION_GUIDE.md; "
                    "do not open the other rater's sheet until both are done.", ""]
    for i, s in enumerate(sample.itertuples(), 1):
        link_id = f"{tid}#{i:02d}"
        iss = issues.get(s.issue, {})
        msg = git(repo, "show", "-s", "--format=%B", s.commit).strip()
        numstat = git(repo, "show", "--numstat", "--format=", s.commit).strip().splitlines()
        linked = set(str(s.files).split(";"))
        changed, linked_lines, total_lines = [], 0, 0
        for ln in numstat:
            parts = ln.split("\t")
            if len(parts) != 3:
                continue
            a, d, path = parts
            n = (int(a) if a.isdigit() else 0) + (int(d) if d.isdigit() else 0)
            total_lines += n
            if path in linked:
                linked_lines += n
            changed.append((path, a, d, path in linked))
        keys_in_msg = sorted(set(KEY_RE.findall(msg)))
        checks = {
            "type_is_bug": iss.get("type") == "Bug",
            "resolution_fixed": iss.get("resolution") in ("Fixed", "Done"),
            "created_after_release": str(iss.get("created", "")) > rel_date,
            "fix_version_in_release_line": any(v.startswith(line + ".") for v in iss.get("fixVersions", [])),
            "commit_is_revert": msg.lower().startswith("revert"),
            "commit_is_merge": len(git(repo, "show", "-s", "--format=%P", s.commit).split()) > 1,
            "other_issue_keys_in_message": [k for k in keys_in_msg if k != s.issue],
            "files_in_commit": len(changed),
            "linked_release_files": len(linked),
            "share_of_changed_lines_in_linked_files": round(linked_lines / total_lines, 2) if total_lines else None,
        }
        rows.append(dict(link_id=link_id, issue=s.issue, issue_type=iss.get("type"), issue_summary=s.issue_summary,
                         fix_versions=s.fix_versions, commit=s.commit[:12], commit_subject=s.commit_subject,
                         linked_files=s.files, issue_url=s.issue_url, commit_url=s.commit_url,
                         auto_flags="; ".join(k for k, v in checks.items()
                                              if (k in ("commit_is_revert", "commit_is_merge") and v)
                                              or (k in ("type_is_bug", "resolution_fixed", "created_after_release",
                                                        "fix_version_in_release_line") and not v)
                                              or (k == "other_issue_keys_in_message" and v))))
        md += [f"## {link_id}: {s.issue}", "",
               f"* **Issue** ({s.issue_url}): {iss.get('type')} · {iss.get('status')} / {iss.get('resolution')} · "
               f"created {str(iss.get('created', ''))[:10]} · resolved {str(iss.get('resolutiondate', ''))[:10]} · "
               f"fix versions {', '.join(iss.get('fixVersions', []))}",
               f"* **Summary:** {s.issue_summary}",
               f"* **Commit** {s.commit[:12]} ({s.commit_url}), {str(s.commit_date)[:10]}",
               "* **Pre-checks:** " + ", ".join(f"{k}={v}" for k, v in checks.items()), "",
               "```", msg[:1500], "```", "",
               "| File | + | − | linked release file |", "|---|---:|---:|:-:|"]
        md += [f"| `{p}` | {a} | {d} | {'✔' if lk else ''} |" for p, a, d, lk in changed[:25]]
        if len(changed) > 25:
            md.append(f"| … {len(changed) - 25} more files | | | |")
        md.append("")
    (out / "packet.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    sheet = pd.DataFrame(rows)
    for q in QUESTIONS:
        sheet[q] = ""
    sheet["notes"] = ""
    for r in raters:
        p = out / f"rating_{r}.csv"
        if p.exists() and not force:
            print(f"{p} exists; kept (use --force to overwrite)")
            continue
        sheet.assign(rater=r).to_csv(p, index=False)
    print(f"{tid}: {len(sheet)} links -> {out}")
    return len(sheet)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raters", default="Dev,Dhruv")
    ap.add_argument("--targets", default=None)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    tids = a.targets.split(",") if a.targets else sorted(p.parent.name for p in NEW.glob("*/manual_validation_sample.csv"))
    total = sum(build(t, a.raters.split(","), a.force) for t in tids)
    print(f"{total} links in {len(tids)} targets")


if __name__ == "__main__":
    main()
