"""Shared helpers: rename-aware git history over a commit range, mapped onto the files of the release,
and cached issue-tracker clients (Jira, GitHub Issues) behind one small tracker interface."""
import json
import re
import subprocess
import time
import urllib.error
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
        self.data = json.loads(cache.read_text()) if cache and cache.exists() else {}   # cache=None: in-memory only

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

    def _resolve_api(self, jql: str, fields: str) -> None:
        """api='auto': Jira Cloud serves /rest/api/3/search/jql; Jira Server/DC serves /rest/api/2/search."""
        for api, path in (("cloud", "/rest/api/3/search/jql"), ("server", "/rest/api/2/search")):
            try:
                self._get(f"{self.base}{path}?jql={jql}&fields={fields}&maxResults=1")
                self.api = api
                return
            except Exception:  # noqa: BLE001
                continue
        raise RuntimeError(f"No Jira search API answered at {self.base} (tried Cloud v3 and Server v2)")

    def fetch(self, keys) -> dict:
        todo = sorted(k for k in set(keys) if k not in self.data)
        fields = "issuetype,created,resolution,resolutiondate,status,summary,fixVersions"
        if todo and self.api == "auto":
            self._resolve_api(urllib.parse.quote(f"key = {todo[0]}"), fields)
            print(f"  jira: using {self.api} API at {self.base}", flush=True)
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
            if self.cache:
                self.cache.parent.mkdir(parents=True, exist_ok=True)
                self.cache.write_text(json.dumps(self.data, indent=1))
            print(f"  jira: {min(i + 50, len(todo))}/{len(todo)}", flush=True)
        return {k: self.data.get(k) for k in keys}


def is_fixed_bug(issue) -> bool:
    return bool(issue) and issue["type"] == "Bug" and (issue["resolution"] or "") in ("Fixed", "Done")


# ---------------------------------------------------------------------------------------------------------
# Issue-tracker abstraction used by process_metrics.py / defect_mining.py.
#   target["tracker"] = {"type": "jira", "base": URL, "api": "auto|cloud|server", "project_keys": [...]}
#                     | {"type": "github", "bug_label_regex": "(?i)bug|defect|regression"}
#                     | {"type": "none"}
# Legacy targets with a top-level "jira" block are treated as type "jira".
# ---------------------------------------------------------------------------------------------------------

def _parse_ts(s: str):
    from datetime import datetime
    if not s:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z"):
        try:
            return datetime.strptime(s.replace("Z", "+0000"), fmt)
        except ValueError:
            continue
    raise ValueError(f"unparseable timestamp {s!r}")


class JiraTracker:
    kind = "jira"

    def __init__(self, cfg: dict, cache_dir: Path):
        self.cfg = cfg
        self.prefixes = cfg["project_keys"]
        self.client = Jira(cfg["base"], cfg.get("api", "auto"), cache_dir / "jira_issues.json")

    def keys(self, message: str) -> set:
        return issue_keys(message, self.prefixes)

    def fetch(self, keys) -> dict:
        return self.client.fetch(keys)

    def is_fixed_bug(self, info) -> bool:
        return is_fixed_bug(info)

    def created(self, info):
        return _parse_ts(info["created"])

    def url(self, key: str) -> str:
        return f"{self.client.base}/browse/{key}"


class GitHubTracker:
    """Bug = a CLOSED GitHub issue or pull request carrying a bug-like label (default regex bug|defect|regression),
    referenced from a commit message as `#123` or `GH-123`. Report date = the issue/PR creation date.
    DEVIATION from the paper (Jira issue type "Bug", resolution "Fixed"); recorded in each target's summary.

    Uses the search API, so a whole repository's bug-labelled history costs a handful of requests. Without a token
    GitHub allows 10 search requests/min; set GITHUB_TOKEN to raise the limits."""
    kind = "github"
    API = "https://api.github.com"

    def __init__(self, cfg: dict, repo_url: str, cache_dir: Path):
        import os
        m = re.match(r"https://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$", repo_url)
        if not m:
            raise ValueError("GitHub Issues tracking needs a https://github.com/<owner>/<repo> URL")
        self.owner, self.repo = m.groups()
        self.label_re = re.compile(cfg.get("bug_label_regex") or r"(?i)\b(bug|defect|regression)\b")
        self.cache = cache_dir / "github_bugs.json"
        self.token = os.environ.get("GITHUB_TOKEN")
        self.data = json.loads(self.cache.read_text()) if self.cache.exists() else None

    def _get(self, url: str):
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "eh-replication-research"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        for attempt in range(8):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as r:
                    return json.loads(r.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                if e.code in (403, 429) and attempt < 7:      # rate limited: wait for the reset (max ~65 s)
                    reset = e.headers.get("X-RateLimit-Reset")
                    wait = max(5, min(65, int(reset) - int(time.time()) + 2)) if reset else 30
                    print(f"  github: rate limited, waiting {wait}s", flush=True)
                    time.sleep(wait)
                    continue
                raise
            except Exception:  # noqa: BLE001
                if attempt >= 4:
                    raise
                time.sleep(2 ** attempt)

    def _bug_labels(self) -> list:
        labels, page = [], 1
        while True:
            res = self._get(f"{self.API}/repos/{self.owner}/{self.repo}/labels?per_page=100&page={page}")
            labels += [lab["name"] for lab in res]
            if len(res) < 100:
                break
            page += 1
        return [lab for lab in labels if self.label_re.search(lab)]

    def _search(self, label: str, start: str = "2000-01-01", end: str = "2100-01-01") -> list:
        q = f'repo:{self.owner}/{self.repo} label:"{label}" is:closed created:{start}..{end}'
        first = self._get(f"{self.API}/search/issues?q={urllib.parse.quote(q)}&per_page=100&page=1")
        if first["total_count"] > 1000:   # the search API returns at most 1000 hits per query: split the range
            from datetime import date, timedelta
            a, b = date.fromisoformat(start), date.fromisoformat(min(end, date.today().isoformat()))
            mid = a + (b - a) / 2
            if mid <= a:
                return first["items"]
            return (self._search(label, start, mid.isoformat())
                    + self._search(label, (mid + timedelta(days=1)).isoformat(), end))
        items, page = list(first["items"]), 1
        while len(items) < first["total_count"]:
            page += 1
            time.sleep(0 if self.token else 6.5)          # stay under 10 search requests/min without a token
            res = self._get(f"{self.API}/search/issues?q={urllib.parse.quote(q)}&per_page=100&page={page}")
            if not res["items"]:
                break
            items += res["items"]
        return items

    def _load(self) -> dict:
        if self.data is None:
            labels = self._bug_labels()
            if not labels:
                raise RuntimeError(f"{self.owner}/{self.repo} has no bug-like labels matching "
                                   f"{self.label_re.pattern!r}; cannot classify issues as bugs")
            print(f"  github: bug labels {labels}", flush=True)
            bugs = {}
            for lab in labels:
                for it in self._search(lab):
                    bugs[f"#{it['number']}"] = {
                        "type": "Bug", "created": it["created_at"], "resolution": "closed",
                        "summary": it["title"], "fixVersions": [], "is_pr": "pull_request" in it,
                        "labels": [x["name"] for x in it.get("labels", [])]}
                time.sleep(0 if self.token else 6.5)
            self.data = {"labels": labels, "bugs": bugs}
            self.cache.parent.mkdir(parents=True, exist_ok=True)
            self.cache.write_text(json.dumps(self.data, indent=1))
            print(f"  github: {len(bugs)} closed bug-labelled issues/PRs", flush=True)
        return self.data

    def keys(self, message: str) -> set:
        return {f"#{n}" for n in re.findall(r"(?:(?<![\w/&])#|\bGH-)(\d+)\b", message)}

    def fetch(self, keys) -> dict:
        bugs = self._load()["bugs"]
        return {k: bugs.get(k, {"type": "Other", "created": None, "resolution": None, "summary": None,
                                "fixVersions": []}) for k in keys}

    def is_fixed_bug(self, info) -> bool:
        return bool(info) and info["type"] == "Bug"

    def created(self, info):
        return _parse_ts(info["created"])

    def url(self, key: str) -> str:
        return f"https://github.com/{self.owner}/{self.repo}/issues/{key.lstrip('#')}"


def tracker_config(t: dict) -> dict:
    if t.get("tracker"):
        return t["tracker"]
    if t.get("jira"):
        return {"type": "jira", **t["jira"]}
    return {"type": "none"}


def make_tracker(t: dict, cache_dir: Path):
    cfg = tracker_config(t)
    if cfg["type"] == "jira":
        return JiraTracker(cfg, cache_dir)
    if cfg["type"] == "github":
        return GitHubTracker(cfg, t["repo"], cache_dir)
    return None


NOT_JIRA = {"CVE", "CWE", "GHSA", "UTF", "ISO", "RFC", "SHA", "JSR", "JEP", "GH", "PR", "ID", "TLS", "SSL", "HTTP"}


def detect_issue_prefixes(repo: Path, rev_range: str, min_share: float = 0.1, max_n: int = 6,
                          jira_base: str = None) -> list:
    """Most frequent Jira-style key prefixes (ABC-123) in the commit messages of rev_range. Common non-Jira
    identifiers (CVE-2021-1234, UTF-8, ...) are dropped; with jira_base, each prefix must also exist as a project."""
    from collections import Counter
    msgs = subprocess.run(["git", "log", "--no-merges", "--format=%B", rev_range], cwd=repo, capture_output=True,
                          text=True, encoding="utf-8", errors="replace").stdout
    c = Counter(p for p in re.findall(r"\b([A-Z][A-Z0-9]{1,15})-\d+\b", msgs) if p not in NOT_JIRA)
    total = sum(c.values())
    keys = [p for p, n in c.most_common(max_n) if total and n / total >= min_share]
    if jira_base:
        client = Jira(jira_base, "auto", None)
        ok = []
        for k in keys:
            try:
                client._get(f"{client.base}/rest/api/2/project/{k}")
                ok.append(k)
            except Exception:  # noqa: BLE001 - not a project on this Jira (or not public)
                pass
        keys = ok
    return keys
