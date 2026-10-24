"""Turn dashboard input (a repository link + tags) into a validated pipeline target.

Pure functions, used by dashboard/app.py and usable from Python:
  normalize_repo_url(url)          -> canonical https URL (no .git, no trailing slash) or ValueError
  list_tags(url)                   -> tag names via `git ls-remote` (no clone needed)
  suggest_tags(tags, release=None) -> {"release", "post_release", "prev_release", "notes"}
  target_from_form(form)           -> (target_id, cfg, reused_existing)
"""
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "collect"))
from clone_repo import GIT_ENV, all_targets  # noqa: E402

URL_RE = re.compile(r"^https://[A-Za-z0-9.-]+(?::\d+)?(/[A-Za-z0-9._~-]+)+$")
KEY_RE = re.compile(r"^[A-Z][A-Z0-9]{1,15}$")
PRE_RE = re.compile(r"(?i)(alpha|beta|[^a-z]rc\d*|\bcr\d*|[^a-z]m\d+|snapshot|preview|\bdev\b|\bea\b|milestone)")
DEFAULT_FILTERS = {
    "java": ("auto", r"(^|/)(test|tests|testing|it|test-?utils?|examples?|samples?|benchmarks?|jmh)/|Test\.java$|Tests\.java$|IT\.java$"),
    "csharp": (r"\.cs$", r"(?i)(^|/)(tests?|.*\.tests?|samples?|benchmarks?)/|/obj/|/bin/"),
}
MAVEN_INCLUDE = r"/src/main/java/.*\.java$"
GENERIC_JAVA_INCLUDE = r"\.java$"


def normalize_repo_url(url: str) -> str:
    u = (url or "").strip().rstrip("/")
    u = u[:-4] if u.endswith(".git") else u
    if not URL_RE.match(u) or ".." in u:
        raise ValueError("Enter a public https repository URL, e.g. https://github.com/hibernate/hibernate-orm")
    return u


def list_tags(url: str) -> list:
    url = normalize_repo_url(url)
    r = subprocess.run(["git", "-c", "protocol.allow=never", "-c", "protocol.https.allow=always",
                        "ls-remote", "--tags", "--refs", url + ".git"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=GIT_ENV, timeout=120)
    if r.returncode != 0:
        raise ValueError(f"Could not read tags from {url} (is it public and spelled correctly?): "
                         f"{r.stderr.strip()[:300]}")
    tags = [ln.split("refs/tags/", 1)[1] for ln in r.stdout.splitlines() if "refs/tags/" in ln]
    return sorted(tags, key=version_key, reverse=True)


VERSION_RE = re.compile(r"(?<![\d.])(\d{1,3})[._](\d{1,4})(?:[._](\d{1,4}))?(?!\d)")   # 2.6.5, 5.0.0.Final, LANG_3_0_1; not dates


def _ver(tag: str):
    m = VERSION_RE.search(tag)
    return tuple(int(x or 0) for x in m.groups()) if m else None


def version_key(tag: str) -> tuple:
    v = _ver(tag)
    return (1 if v else 0, v or (0, 0, 0), 0 if is_prerelease(tag) else 1, tag)


def is_prerelease(tag: str) -> bool:
    return (bool(PRE_RE.search(tag)) or bool(re.search(r"(?i)[._-]b\d+$", tag))      # e.g. LANG_3_0_B3
            or bool(re.search(r"\d+\.\d+\.\d+-\d+$", tag)))                         # ZooKeeper RCs: release-3.9.7-0


def _skeleton(tag: str) -> str:
    return re.sub(r"\d+", "#", tag)


def suggest_tags(tags: list, release: str = None) -> dict:
    """Heuristics mirroring the paper's choices (Hibernate 5.0.0.Final -> 5.0.16; Hadoop 2.6.0 -> 2.6.5):
    release = first release of the newest line (among the 10 newest) with >= 3 later patch releases;
    post    = the latest stable release of the same x.y line (else the next release);
    prev    = the first release of the previous x.y line.
    Versions decide; the tag's naming pattern only breaks ties (release-2.6.5 vs rel/release-2.6.5)."""
    stable = [t for t in tags if _ver(t) and not is_prerelease(t)]
    notes = []
    if release is None:
        lines = {}
        for t in stable:
            lines.setdefault(_ver(t)[:2], []).append(t)
        newest = sorted(lines, reverse=True)[:10]
        for need in (4, 2):
            cands = [ln for ln in newest if len({_ver(t) for t in lines[ln]}) >= need]
            if cands:
                ln = max(cands)
                release = min(lines[ln], key=lambda t: (_ver(t), t))
                notes.append(f"Release suggested: first release of the newest line with >= {need - 1} later "
                             f"patch release(s).")
                break
        else:
            if len(stable) >= 2:
                release = sorted(stable, key=version_key)[-2]
                notes.append("Release suggested: second-newest release (the newest one ends the window).")
    if release is None or not _ver(release):
        return {"release": release, "post_release": None, "prev_release": None,
                "notes": notes + ["No version-like tags found; pick tags manually."]}
    rv, sk = _ver(release), _skeleton(release)
    tie = lambda t: (_ver(t), _skeleton(t) == sk)  # noqa: E731

    same_line = [t for t in stable if _ver(t)[:2] == rv[:2] and _ver(t) > rv]
    if same_line:
        post = max(same_line, key=tie)
    else:
        later = [t for t in stable if _ver(t) > rv]
        post = min(later, key=lambda t: (_ver(t), _skeleton(t) != sk)) if later else None
        notes.append("No later patch release on the same line; the post-release window ends at the next release."
                     if post else "No later release: there is no post-release window yet.")
    older_lines = [t for t in stable if _ver(t)[:2] < rv[:2]]
    if older_lines:
        prev_line = max(_ver(t)[:2] for t in older_lines)
        prev = min((t for t in older_lines if _ver(t)[:2] == prev_line), key=lambda t: (_ver(t), _skeleton(t) != sk))
    else:
        older = [t for t in stable if _ver(t) < rv]
        prev = max(older, key=tie) if older else None
    return {"release": release, "post_release": post, "prev_release": prev, "notes": notes}


def _norm(u: str) -> str:
    return u.lower().rstrip("/").removesuffix(".git")


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9._-]+", "-", s.lower()).strip("-.")[:60]


def target_from_form(form: dict):
    repo = normalize_repo_url(form.get("repo"))
    tags = set(list_tags(repo))
    rel, post = form.get("release_tag"), form.get("post_release_tag")
    prev = form.get("prev_release_tag") or ""
    for name, tag in (("release", rel), ("post-release", post)):
        if not tag or tag not in tags:
            raise ValueError(f"{name} tag {tag!r} does not exist in {repo}")
    if prev and prev not in tags:
        raise ValueError(f"previous-release tag {prev!r} does not exist in {repo}")
    if _ver(post) and _ver(rel) and _ver(post) <= _ver(rel):
        raise ValueError("the post-release tag must be a later version than the release tag")

    # same repository + same tags as an existing (e.g. curated) target -> reuse it and its cached outputs
    for tid, t in all_targets().items():
        if tid.startswith("_") or not isinstance(t, dict):
            continue
        if _norm(t.get("repo", "")) == _norm(repo) and t.get("release_tag") == rel \
                and t.get("post_release_tag") == post and (t.get("prev_release_tag") or "") == prev:
            return tid, {"id": tid, **t}, True

    lang = form.get("language") or "auto"
    if lang not in ("auto", "java", "csharp"):
        raise ValueError("language must be auto, java or csharp")
    tr = form.get("tracker") or {"type": "none"}
    ttype = tr.get("type", "none")
    if ttype == "jira":
        base = (tr.get("base") or "").strip().rstrip("/")
        if not URL_RE.match(base):
            raise ValueError("Jira base URL must look like https://issues.apache.org/jira")
        keys = [k.strip().upper() for k in re.split(r"[,\s]+", tr.get("project_keys") or "") if k.strip()]
        bad = [k for k in keys if not KEY_RE.match(k)]
        if bad:
            raise ValueError(f"invalid Jira project key(s): {bad}")
        tracker = {"type": "jira", "base": base, "api": "auto", "project_keys": keys}   # [] = auto-detect
    elif ttype == "github":
        if not repo.lower().startswith("https://github.com/"):
            raise ValueError("GitHub Issues tracking needs a github.com repository")
        rx = tr.get("bug_label_regex") or r"(?i)\b(bug|defect|regression)\b"
        re.compile(rx)
        tracker = {"type": "github", "bug_label_regex": rx}
    elif ttype == "none":
        tracker = {"type": "none"}
    else:
        raise ValueError("tracker type must be jira, github or none")

    d_inc, d_exc = DEFAULT_FILTERS["csharp" if lang == "csharp" else "java"]
    inc = form.get("include_regex") or d_inc
    exc = form.get("exclude_regex") or d_exc
    for rx in (inc, exc):
        if rx != "auto":
            if len(rx) > 300:
                raise ValueError("file filter regex too long")
            re.compile(rx)

    existing = all_targets()
    base_id = _slug(f"{repo.split('/')[-1]}-{rel.split('/')[-1]}")
    tid, i = base_id, 2
    while tid in existing:
        tid, i = f"{base_id}-{i}", i + 1
    cfg = {"repo": repo + ".git", "language": lang, "prev_release_tag": prev, "release_tag": rel,
           "post_release_tag": post, "tracker": tracker, "include_regex": inc, "exclude_regex": exc,
           "_source": "dashboard"}
    return tid, {"id": tid, **cfg}, False
