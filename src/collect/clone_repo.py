"""Clone a target repository (once) and check out its release tag in a dedicated worktree.

Usage: python src/collect/clone_repo.py <target-id>
Targets: src/collect/targets.json, plus optional local targets in data/targets.local.json
(same schema; ids in targets.json win on conflict).
Result:
  data/new/repos/<repo-name>.git/           full clone without checkout (shared by targets of the same repo)
  data/new/<id>/src/                        worktree checked out at release_tag (detached)
  data/new/<id>/provenance.json             repo URL, tags, resolved commit SHAs + dates, detected language
"""
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NEW = ROOT / "data" / "new"
CURATED = ROOT / "src" / "collect" / "targets.json"
LOCAL = ROOT / "data" / "targets.local.json"
GIT_ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_ASKPASS": "", "SSH_ASKPASS": ""}


def git(*args, cwd=None, timeout=None) -> str:
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=GIT_ENV, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def all_targets() -> dict:
    local = json.loads(LOCAL.read_text()) if LOCAL.exists() else {}
    curated = json.loads(CURATED.read_text())
    return {**local, **curated}


def load_target(tid: str) -> dict:
    t = all_targets()
    if tid not in t or tid.startswith("_"):
        raise SystemExit(f"unknown target {tid}; choose from {[k for k in t if not k.startswith('_')]}")
    return {"id": tid, **t[tid]}


def register_target(tid: str, cfg: dict) -> None:
    """Add or update a local target in data/targets.local.json (never touches targets.json)."""
    if tid in json.loads(CURATED.read_text()):
        raise ValueError(f"{tid} is a curated target and cannot be changed from here")
    local = json.loads(LOCAL.read_text()) if LOCAL.exists() else {}
    local[tid] = {k: v for k, v in cfg.items() if k != "id"}
    LOCAL.parent.mkdir(parents=True, exist_ok=True)
    LOCAL.write_text(json.dumps(local, indent=2))


def repo_dir(t: dict) -> Path:
    parts = t["repo"].rstrip("/").removesuffix(".git").split("/")
    plain = NEW / "repos" / (parts[-1] + ".git")
    if plain.exists():
        try:
            if git("config", "--get", "remote.origin.url", cwd=plain).rstrip("/").removesuffix(".git") \
                    != t["repo"].rstrip("/").removesuffix(".git"):
                return NEW / "repos" / f"{parts[-2]}__{parts[-1]}.git"   # same name, different repository
        except RuntimeError:
            pass
    return plain


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
        "prev_release": tag_info(rd, t["prev_release_tag"]) if t.get("prev_release_tag") else None,
        "worktree_head": git("rev-parse", "HEAD", cwd=wt),
        "language_declared": t["language"], "language_detected": detect_language(wt),
    }
    (out / "provenance.json").write_text(json.dumps(prov, indent=2))
    print(json.dumps(prov, indent=2))
    return prov


if __name__ == "__main__":
    main(sys.argv[1])
