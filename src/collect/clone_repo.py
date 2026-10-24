"""Clone a target repository (once) and check out its release tag in a dedicated worktree.

Usage: python src/collect/clone_repo.py <target-id>        (targets defined in src/collect/targets.json)
Result:
  data/new/repos/<repo-name>.git/           bare-ish full clone (shared by targets of the same repo)
  data/new/<id>/src/                        worktree checked out at release_tag (detached)
  data/new/<id>/provenance.json             repo URL, tags, resolved commit SHAs + dates, detected language
"""
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NEW = ROOT / "data" / "new"


def git(*args, cwd=None) -> str:
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def load_target(tid: str) -> dict:
    t = json.loads((ROOT / "src" / "collect" / "targets.json").read_text())
    if tid not in t:
        raise SystemExit(f"unknown target {tid}; choose from {[k for k in t if not k.startswith('_')]}")
    return {"id": tid, **t[tid]}


def repo_dir(t: dict) -> Path:
    return NEW / "repos" / (t["repo"].rstrip("/").split("/")[-1].removesuffix(".git") + ".git")


def tag_info(rd: Path, tag: str) -> dict:
    sha = git("rev-list", "-n", "1", tag, cwd=rd)
    date = git("log", "-1", "--format=%cI", sha, cwd=rd)
    return {"tag": tag, "commit": sha, "commit_date": date}


def detect_language(src: Path) -> str:
    c = Counter(p.suffix for p in src.rglob("*") if p.suffix in (".java", ".cs"))
    return {".java": "java", ".cs": "csharp"}.get(c.most_common(1)[0][0], "unknown") if c else "unknown"


def main(tid: str) -> dict:
    t = load_target(tid)
    rd = repo_dir(t)
    if not rd.exists():
        rd.parent.mkdir(parents=True, exist_ok=True)
        print(f"cloning {t['repo']} -> {rd}", flush=True)
        git("clone", "--no-checkout", "-c", "core.longpaths=true", t["repo"], str(rd))
    else:
        git("fetch", "--tags", "origin", cwd=rd)
    out = NEW / tid
    wt = out / "src"
    if not wt.exists():
        out.mkdir(parents=True, exist_ok=True)
        git("-c", "core.longpaths=true", "worktree", "add", "--detach", str(wt), t["release_tag"], cwd=rd)
    prov = {
        "target": tid, "repo": t["repo"],
        "release": tag_info(rd, t["release_tag"]),
        "post_release": tag_info(rd, t["post_release_tag"]),
        "prev_release": tag_info(rd, t["prev_release_tag"]),
        "worktree_head": git("rev-parse", "HEAD", cwd=wt),
        "language_declared": t["language"], "language_detected": detect_language(wt),
    }
    (out / "provenance.json").write_text(json.dumps(prov, indent=2))
    print(json.dumps(prov, indent=2))
    return prov


if __name__ == "__main__":
    main(sys.argv[1])
