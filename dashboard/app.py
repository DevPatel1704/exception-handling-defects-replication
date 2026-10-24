"""Local dashboard: give it a repository link, it runs the replication pipeline and shows the results.

Start (inside the conda env, so R / Java 8 / Python deps are found):
    ./envrun.sh python dashboard/app.py [--port 8000]
then open http://localhost:8000/

Design: stdlib only; binds to 127.0.0.1; one background worker runs one job at a time (JTratch needs ~6 GB);
jobs and step logs persist in data/jobs/<job-id>/ and survive restarts (an interrupted job is marked so).

API
  GET  /api/health                 tool availability (git, Rscript, Java 8, Understand)
  GET  /api/tags?repo=URL          tags of a public repository + suggested release / post-release / previous tags
  GET  /api/targets                known targets (curated + registered from this dashboard)
  POST /api/jobs                   {repo, release_tag, post_release_tag, prev_release_tag, language, tracker:{...},
                                    include_regex, exclude_regex, repeats, reuse}  -> {job_id, target, reused}
  GET  /api/jobs                   all jobs, newest first
  GET  /api/jobs/<id>              one job with step states and the tail of the running step's log
  GET  /api/jobs/<id>/log/<step>   full log of one step (text)
  POST /api/jobs/<id>/cancel       stop a queued or running job
  GET  /api/results/<target>       results/new/<target>/summary.json
Static files: dashboard/, results/, data/new/<id>/{input,*.csv,*.json} only.
"""
import argparse
import json
import queue
import re
import shutil
import subprocess
import sys
import threading
import time
import traceback
import urllib.parse
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "collect"))
sys.path.insert(0, str(ROOT / "src" / "pipeline"))
import targets_api  # noqa: E402
from clone_repo import all_targets, register_target  # noqa: E402
from run_target import Runner, steps_template  # noqa: E402

JOBS = ROOT / "data" / "jobs"
STATIC_OK = [re.compile(p) for p in (r"^dashboard/[\w.-]+$", r"^results/[\w./-]+\.(png|csv|md|json|txt|pdf)$",
                                     r"^data/new/[\w.-]+/(input/)?[\w.-]+\.(csv|json)$", r"^src/collect/targets\.json$")]
TAGS_CACHE, TAGS_TTL = {}, 600


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Jobs:
    def __init__(self):
        JOBS.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()
        self.jobs = {}
        self.q = queue.Queue()
        self.current = None          # (job_id, Runner)
        for f in sorted(JOBS.glob("*/job.json")):
            j = json.loads(f.read_text())
            if j["status"] in ("queued", "running"):
                j["status"] = "interrupted"
                for s in j["steps"]:
                    if s["status"] in ("running", "pending"):
                        s["status"], s["message"] = "cancelled", "server restarted"
            self.jobs[j["id"]] = j
            self._save(j)
        threading.Thread(target=self._worker, daemon=True).start()

    def _save(self, j):
        d = JOBS / j["id"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "job.json").write_text(json.dumps(j, indent=1))

    def submit(self, tid, form, reused) -> dict:
        jid = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + tid
        steps = [s.__dict__.copy() for s in steps_template()]
        j = {"id": jid, "target": tid, "status": "queued", "created": now(), "reused_target": reused,
             "repeats": int(form.get("repeats") or 5), "reuse": bool(form.get("reuse", True)),
             "steps": steps, "cancel": False}
        with self.lock:
            self.jobs[jid] = j
            self._save(j)
        self.q.put(jid)
        return j

    def cancel(self, jid) -> dict:
        with self.lock:
            j = self.jobs[jid]
            j["cancel"] = True
            if j["status"] == "queued":
                j["status"] = "cancelled"
            self._save(j)
        if self.current and self.current[0] == jid:
            self.current[1].cancel.set()
            self.current[1].kill()
        return j

    def _worker(self):
        while True:
            jid = self.q.get()
            j = self.jobs[jid]
            if j.get("cancel"):
                continue
            j["status"], j["started"] = "running", now()
            self._save(j)

            def update(runner, j=j):
                with self.lock:
                    j["steps"] = [s.__dict__.copy() for s in runner.steps]
                    self._save(j)
            try:
                r = Runner(j["target"], j["repeats"], j["reuse"], log_dir=JOBS / jid, on_update=update)
                self.current = (jid, r)
                steps = r.run()
                bad = [s for s in steps if s.status in ("failed", "blocked")]
                j["status"] = ("cancelled" if j.get("cancel") else "finished with problems" if bad else "finished")
            except Exception as e:  # noqa: BLE001
                j["status"], j["error"] = "error", f"{e}\n{traceback.format_exc()[-1500:]}"
            finally:
                self.current = None
                j["ended"] = now()
                self._save(j)

    def view(self, jid) -> dict:
        j = dict(self.jobs[jid])
        run = next((s for s in j["steps"] if s["status"] == "running"), None)
        if run:
            log = JOBS / jid / f"{run['name']}.log"
            if log.exists():
                j["log_tail"] = "\n".join(log.read_text(encoding="utf-8", errors="replace").splitlines()[-25:])
        j["queue_position"] = (list(self.q.queue).index(jid) + 1) if jid in list(self.q.queue) else 0
        return j


def health() -> dict:
    sys.path.insert(0, str(ROOT / "src" / "collect"))
    from run_analyzers import find_java8
    from traditional_metrics import find_understand
    try:
        java8 = find_java8()
    except SystemExit:
        java8 = None
    return {"git": shutil.which("git"), "Rscript": shutil.which("Rscript"), "java8": java8,
            "understand": find_understand(), "python": sys.executable,
            "authors_package": (ROOT / "external" / "scripts_with_input_data").exists(),
            "jtratch_source": (ROOT / "external" / "JTratch").exists()}


class Handler(SimpleHTTPRequestHandler):
    jobs: Jobs = None

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def log_message(self, fmt, *args):   # quiet: only errors
        if args and str(args[1])[:1] in "45":
            super().log_message(fmt, *args)

    def _json(self, obj, code=200):
        body = json.dumps(obj, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _text(self, text, code=200):
        body = text.encode("utf-8", errors="replace")
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        p = u.path
        try:
            if p in ("/", "/index.html"):
                self.send_response(HTTPStatus.FOUND)
                self.send_header("Location", "/dashboard/index.html")
                self.end_headers()
                return
            if p == "/api/health":
                return self._json(health())
            if p == "/api/tags":
                repo = targets_api.normalize_repo_url(urllib.parse.parse_qs(u.query).get("repo", [""])[0])
                hit = TAGS_CACHE.get(repo)
                if not hit or time.time() - hit[0] > TAGS_TTL:
                    hit = (time.time(), targets_api.list_tags(repo))
                    TAGS_CACHE[repo] = hit
                tags = hit[1]
                rel = urllib.parse.parse_qs(u.query).get("release", [None])[0]
                return self._json({"repo": repo, "tags": tags, "suggested": targets_api.suggest_tags(tags, rel),
                                   "github": repo.lower().startswith("https://github.com/")})
            if p == "/api/targets":
                return self._json({k: v for k, v in all_targets().items() if not k.startswith("_")})
            if p == "/api/jobs":
                js = sorted(self.jobs.jobs.values(), key=lambda j: j["created"], reverse=True)
                return self._json([{k: j[k] for k in ("id", "target", "status", "created")} for j in js])
            m = re.match(r"^/api/jobs/([\w.-]+)$", p)
            if m and m.group(1) in self.jobs.jobs:
                return self._json(self.jobs.view(m.group(1)))
            m = re.match(r"^/api/jobs/([\w.-]+)/log/(\w+)$", p)
            if m and m.group(1) in self.jobs.jobs:
                f = JOBS / m.group(1) / f"{m.group(2)}.log"
                return self._text(f.read_text(encoding="utf-8", errors="replace") if f.exists() else "(no log)")
            m = re.match(r"^/api/results/([\w.-]+)$", p)
            if m:
                f = ROOT / "results" / "new" / m.group(1) / "summary.json"
                return self._json(json.loads(f.read_text())) if f.exists() else self._json({"error": "no results yet"}, 404)
            rel = urllib.parse.unquote(p.lstrip("/"))
            if any(rx.match(rel) for rx in STATIC_OK) and ".." not in rel:
                return super().do_GET()
            self.send_error(HTTPStatus.NOT_FOUND)
        except ValueError as e:
            self._json({"error": str(e)}, 400)
        except Exception as e:  # noqa: BLE001
            self._json({"error": f"{type(e).__name__}: {e}"}, 500)

    def do_POST(self):
        p = urllib.parse.urlparse(self.path).path
        try:
            n = int(self.headers.get("Content-Length") or 0)
            if n > 65536:
                return self._json({"error": "request too large"}, 413)
            body = json.loads(self.rfile.read(n) or b"{}")
            if p == "/api/jobs":
                tid, cfg, reused = targets_api.target_from_form(body)
                if not reused:
                    register_target(tid, cfg)
                j = self.jobs.submit(tid, body, reused)
                return self._json({"job_id": j["id"], "target": tid, "reused": reused}, 201)
            m = re.match(r"^/api/jobs/([\w.-]+)/cancel$", p)
            if m and m.group(1) in self.jobs.jobs:
                return self._json(self.jobs.cancel(m.group(1)))
            self.send_error(HTTPStatus.NOT_FOUND)
        except ValueError as e:
            self._json({"error": str(e)}, 400)
        except subprocess.TimeoutExpired:
            self._json({"error": "the repository did not answer in time"}, 504)
        except Exception as e:  # noqa: BLE001
            self._json({"error": f"{type(e).__name__}: {e}"}, 500)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8000)
    a = ap.parse_args()
    Handler.jobs = Jobs()
    h = health()
    missing = [k for k in ("git", "Rscript", "java8") if not h[k]]
    print(f"Dashboard: http://localhost:{a.port}/   (serving {ROOT})", flush=True)
    if missing:
        print(f"WARNING: missing {missing}: start with ./envrun.sh python dashboard/app.py", flush=True)
    if not h["authors_package"]:
        print("WARNING: authors' package not found; run bash src/reproduce/fetch_package.sh first", flush=True)
    with ThreadingHTTPServer(("127.0.0.1", a.port), Handler) as srv:
        srv.serve_forever()


if __name__ == "__main__":
    main()
