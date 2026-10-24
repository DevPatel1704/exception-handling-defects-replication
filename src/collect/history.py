"""Shared helpers: rename-aware git history over a commit range, mapped onto the files of the release,
and a small cached Jira client (issue type / resolution / created date for issue keys)."""
import json
import re
import subprocess
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

SEP_C, SEP_F = "\x1e", "\x1f"


@dataclass
class Commit:
    sha: str
    author_email: str
    timestamp: int
    message: str
    files: dict = field(default_factory=dict)   # release-relative path -> (added, deleted)


def release_files(worktree: Path, include: str, exclude: str) -> list:
    out = subprocess.run(["git", "ls-files"], cwd=worktree, capture_output=True, text=True,
                         encoding="utf-8").stdout.splitlines()
    inc, exc = re.compile(include), re.compile(exclude)
    return sorted(p for p in out if inc.search("/" + p) and not exc.search("/" + p))


_BRACE = re.compile(r"^(.*)\{(.*) => (.*)\}(.*)$")


def _split_rename(path: str) -> tuple:
    """numstat rename syntax: 'a/{old => new}/b' or 'old => new'. Returns (old, new)."""
    m = _BRACE.match(path)
    if m:
        pre, old, new, post = m.groups()
        clean = lambda s: re.sub(r"//+", "/", s)  # noqa: E731
        return clean(pre + old + post), clean(pre + new + post)
    if " => " in path:
        old, new = path.split(" => ", 1)
        return old, new
    return path, path


def walk(repo: Path, rev_range: str, files: list, direction: str) -> list:
    """Commits in rev_range touching release files, with paths mapped to their name AT the release.

    direction="backward": range ends at the release (pre-release window). Walk newest -> oldest; when a
                          commit renames old->new, earlier commits refer to the file as `old`.
    direction="forward":  range starts at the release (post-release window). Walk oldest -> newest; when a
                          commit renames old->new, later commits refer to the file as `new`.
    Merge commits are skipped (their changes are attributed to the merged commits), as is usual for churn.
    """
    args = ["git", "log", "--no-merges", "-M", "--numstat", f"--format={SEP_C}%H{SEP_F}%ae{SEP_F}%at{SEP_F}%B{SEP_F}",
            rev_range]
    if direction == "forward":
        args.insert(2, "--reverse")
    raw = subprocess.run(args, cwd=repo, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    alias = {p: p for p in files}          # path as currently seen in the walk -> release path
    commits = []
    for chunk in raw.split(SEP_C)[1:]:
        sha, email, ts, msg, stat = chunk.split(SEP_F, 4)
        c = Commit(sha, email.lower(), int(ts), msg.strip())
        renames = []
        for line in stat.strip().splitlines():
            parts = line.split("\t")
            if len(parts) != 3:
                continue
            a, d, path = parts
            old, new = _split_rename(path)
            added = int(a) if a.isdigit() else 0
            deleted = int(d) if d.isdigit() else 0
            key = new if direction == "backward" else old
            if key in alias:
                rel = alias[key]
                pa, pd_ = c.files.get(rel, (0, 0))
                c.files[rel] = (pa + added, pd_ + deleted)
                if old != new:
                    renames.append((old, new, rel))
        for old, new, rel in renames:
            if direction == "backward":
                alias.pop(new, None); alias[old] = rel
            else:
                alias.pop(old, None); alias[new] = rel
        if c.files:
            commits.append(c)
    return commits


def issue_keys(message: str, project_keys: list) -> set:
    pat = re.compile(r"\b(" + "|".join(map(re.escape, project_keys)) + r")-(\d+)\b")
    return {f"{p}-{n}" for p, n in pat.findall(message)}


class Jira:
    """Anonymous read-only Jira client with an on-disk JSON cache."""

    def __init__(self, base: str, api: str, cache: Path):
        self.base, self.api, self.cache = base.rstrip("/"), api, cache
        self.data = json.loads(cache.read_text()) if cache.exists() else {}

    def _get(self, url: str) -> dict:
        for attempt in range(5):
            try:
                req = urllib.request.Request(url, headers={"Accept": "application/json",
                                                           "User-Agent": "eh-replication-research"})
                with urllib.request.urlopen(req, timeout=60) as r:
                    return json.loads(r.read().decode("utf-8"))
            except Exception:  # noqa: BLE001
                if attempt == 4:
                    raise
                time.sleep(2 ** attempt)

    def fetch(self, keys) -> dict:
        todo = sorted(k for k in set(keys) if k not in self.data)
        fields = "issuetype,created,resolution,resolutiondate,status,summary,fixVersions"
        for i in range(0, len(todo), 50):
            batch = todo[i:i + 50]
            jql = urllib.parse.quote(f"key in ({','.join(batch)})")
            if self.api == "cloud":
                url = f"{self.base}/rest/api/3/search/jql?jql={jql}&fields={fields}&maxResults=100"
            else:
                url = f"{self.base}/rest/api/2/search?jql={jql}&fields={fields}&maxResults=100"
            try:
                res = self._get(url)
            except Exception:  # noqa: BLE001 - a key that no longer exists makes the whole JQL fail; go one by one
                res = {"issues": []}
                for k in batch:
                    try:
                        res["issues"].append(self._get(f"{self.base}/rest/api/2/issue/{k}?fields={fields}"))
                    except Exception:  # noqa: BLE001
                        self.data[k] = None
            for iss in res.get("issues", []):
                f = iss["fields"]
                self.data[iss["key"]] = {
                    "type": (f.get("issuetype") or {}).get("name"),
                    "created": f.get("created"),
                    "resolution": (f.get("resolution") or {}).get("name"),
                    "resolutiondate": f.get("resolutiondate"),
                    "status": (f.get("status") or {}).get("name"),
                    "summary": f.get("summary"),
                    "fixVersions": [v.get("name") for v in f.get("fixVersions") or []],
                }
            for k in batch:   # keys that moved project or were deleted
                self.data.setdefault(k, None)
            self.cache.parent.mkdir(parents=True, exist_ok=True)
            self.cache.write_text(json.dumps(self.data, indent=1))
            print(f"  jira: {min(i + 50, len(todo))}/{len(todo)}", flush=True)
        return {k: self.data.get(k) for k in keys}


def is_fixed_bug(issue) -> bool:
    return bool(issue) and issue["type"] == "Bug" and (issue["resolution"] or "") in ("Fixed", "Done")
