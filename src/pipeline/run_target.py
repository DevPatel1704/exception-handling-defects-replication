"""Run the whole pipeline for one target: collect -> analyse -> build dataset -> authors' models -> ML -> SHAP
-> summary. Used by the dashboard's worker; also runnable on its own:

    ./envrun.sh python src/pipeline/run_target.py <target-id> [--repeats 5] [--no-reuse]

Each step writes a log to <log_dir>/<step>.log. With reuse on (default), a step whose inputs are byte-identical to
its last successful run (content hash stored in data/new/<id>/stamps.json) and whose outputs exist is skipped, so
re-running a target does not repeat the ~35 min analyzer run or the R bootstraps.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src" / "collect"))
sys.path.insert(0, str(HERE.parent))
from clone_repo import CURATED, NEW, load_target, register_target, repo_dir  # noqa: E402
from history import detect_issue_prefixes, release_files, tracker_config  # noqa: E402
from targets_api import GENERIC_JAVA_INCLUDE, MAVEN_INCLUDE  # noqa: E402

PY = sys.executable
RESULTS = ROOT / "results" / "new"
MIN_DEFECTIVE = 10      # files with catch blocks needed in each class before models / ML are attempted


@dataclass
class Step:
    name: str
    title: str
    deps: list = field(default_factory=list)
    status: str = "pending"          # pending | running | done | reused | skipped | failed | blocked | cancelled
    message: str = ""
    started: str = None
    ended: str = None
    seconds: float = None


def steps_template() -> list:
    return [
        Step("clone", "Clone repository and check out the release"),
        Step("configure", "Detect language, source filters and issue keys", ["clone"]),
        Step("process_metrics", "Pre-release process metrics (git)", ["configure"]),
        Step("defect_mining", "Post-release defects (issue tracker)", ["configure"]),
        Step("product_metrics", "Product metrics (Understand or fallback)", ["configure"]),
        Step("analyzer", "Exception-flow analysis (JTratch)", ["configure"]),
        Step("dataset", "File-level dataset in the authors' format", ["process_metrics", "product_metrics", "analyzer"]),
        Step("models", "Authors' BASE / BSFC / BSAP models (R)", ["dataset", "defect_mining"]),
        Step("ml", "ML prediction: LR / RF / XGBoost (RQ3)", ["models"]),
        Step("shap", "SHAP explanations (RQ4)", ["ml"]),
        Step("summary", "Summary for the dashboard", []),
    ]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _hash(paths) -> str:
    h = hashlib.sha256()
    for p in sorted(Path(x) for x in paths):
        h.update(str(p.relative_to(ROOT)).encode())
        h.update(p.read_bytes() if p.exists() else b"<missing>")
    return h.hexdigest()


class Runner:
    def __init__(self, tid: str, repeats: int = 5, reuse: bool = True, log_dir: Path = None,
                 on_update=None, cancel_event: threading.Event = None):
        self.tid, self.repeats, self.reuse = tid, repeats, reuse
        self.out, self.res = NEW / tid, RESULTS / tid
        self.log_dir = log_dir or (self.out / "logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.steps = steps_template()
        self.on_update = on_update or (lambda runner: None)
        self.cancel = cancel_event or threading.Event()
        self.proc = None
        self.stamps_path = self.out / "stamps.json"

    # ---------- helpers ----------
    def step(self, name) -> Step:
        return next(s for s in self.steps if s.name == name)

    def _stamps(self) -> dict:
        return json.loads(self.stamps_path.read_text()) if self.stamps_path.exists() else {}

    def _fresh(self, name, inputs, outputs, extra="") -> tuple:
        digest = _hash(inputs) + extra
        ok = self.reuse and all(Path(o).exists() for o in outputs) and self._stamps().get(name) == digest
        return ok, digest

    def _stamp(self, name, digest):
        st = self._stamps()
        st[name] = digest
        self.out.mkdir(parents=True, exist_ok=True)
        self.stamps_path.write_text(json.dumps(st, indent=1))

    def run_cmd(self, name, cmd, env_extra=None) -> None:
        log = self.log_dir / f"{name}.log"
        env = {**os.environ, "PYTHONUNBUFFERED": "1", "PYTHONWARNINGS": "ignore", **(env_extra or {})}
        with open(log, "a", encoding="utf-8") as fh:
            fh.write(f"$ {' '.join(map(str, cmd))}\n")
            fh.flush()
            self.proc = subprocess.Popen([str(c) for c in cmd], cwd=ROOT, stdout=fh, stderr=subprocess.STDOUT, env=env)
            while self.proc.poll() is None:
                if self.cancel.is_set():
                    self.kill()
                    raise InterruptedError("cancelled")
                time.sleep(0.5)
            rc, self.proc = self.proc.returncode, None
        if rc != 0:
            tail = log.read_text(encoding="utf-8", errors="replace").strip().splitlines()[-1:] or [""]
            raise RuntimeError(f"exit code {rc}: {tail[0][:300]}")

    def kill(self) -> None:
        p = self.proc
        if p and p.poll() is None:
            if os.name == "nt":   # kill the whole tree (python -> java, Rscript -> R)
                subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
            else:
                p.kill()

    def log(self, name, text):
        with open(self.log_dir / f"{name}.log", "a", encoding="utf-8") as fh:
            fh.write(text.rstrip() + "\n")

    # ---------- steps ----------
    def s_clone(self):
        self.run_cmd("clone", [PY, "src/collect/clone_repo.py", self.tid])
        return f"release commit {json.loads((self.out / 'provenance.json').read_text())['release']['commit'][:10]}"

    def s_configure(self):
        t = load_target(self.tid)
        prov = json.loads((self.out / "provenance.json").read_text())
        curated = self.tid in json.loads(CURATED.read_text())
        notes, upd = [], {}
        lang = t.get("language", "auto")
        if lang == "auto":
            lang = prov["language_detected"]
            if lang not in ("java", "csharp"):
                raise RuntimeError("no Java or C# sources found at the release tag")
            upd["language"] = lang
            notes.append(f"language={lang}")
        if t.get("include_regex") == "auto":
            wt = self.out / "src"
            allj = release_files(wt, GENERIC_JAVA_INCLUDE, t["exclude_regex"])
            mvn = release_files(wt, MAVEN_INCLUDE, t["exclude_regex"])
            inc = MAVEN_INCLUDE if allj and len(mvn) >= 0.5 * len(allj) else GENERIC_JAVA_INCLUDE
            upd["include_regex"] = inc
            notes.append(f"{'Maven layout' if inc == MAVEN_INCLUDE else 'all .java files'} "
                         f"({len(mvn)} of {len(allj)} non-test .java files under src/main/java)")
        tr = tracker_config(t)
        if tr["type"] == "jira" and not tr.get("project_keys"):
            keys = detect_issue_prefixes(repo_dir(t), f"{t['release_tag']}..{t['post_release_tag']}",
                                         jira_base=tr["base"])
            if keys:
                upd["tracker"] = {**tr, "project_keys": keys}
                notes.append(f"Jira keys detected from commit messages: {', '.join(keys)}")
            else:
                upd["tracker"] = {"type": "none"}
                notes.append("no Jira-style issue keys in post-release commit messages; defect mining disabled")
        if upd and not curated:
            register_target(self.tid, {**t, **upd})
        self.log("configure", "\n".join(notes) or "nothing to configure")
        return "; ".join(notes) or "configuration complete"

    def s_process_metrics(self):
        self.run_cmd("process_metrics", [PY, "src/collect/process_metrics.py", self.tid])
        return "process_metrics.csv written"

    def s_defect_mining(self):
        if tracker_config(load_target(self.tid))["type"] == "none":
            return ("skipped", "no issue tracker: defects not labelled (metrics only)")
        self.run_cmd("defect_mining", [PY, "src/collect/defect_mining.py", self.tid])
        st = json.loads((self.out / "defect_mining_stats.json").read_text())
        return f"{st['post_release_defect_issues']} post-release bugs in {st['defective_files']} of {st['files']} files"

    def s_product_metrics(self):
        self.run_cmd("product_metrics", [PY, "src/collect/traditional_metrics.py", self.tid])
        return f"back-end: {json.loads((self.out / 'product_metrics_meta.json').read_text())['backend']}"

    def s_analyzer(self):
        t = load_target(self.tid)
        if t["language"] != "java":
            return ("skipped", "C# (NTratch) analysis is not wired into the pipeline yet (docs/REPRODUCTION.md T5)")
        raw = self.out / "raw" / "analyzer"
        outs = [raw / f"src_{k}.csv" for k in ("CatchBlock", "CatchBlock_Meta", "PossibleExceptionsBlock", "ThrowsBlock")]
        # JTratch is not deterministic: repeated runs on identical sources differ in some flow metrics (call depth,
        # declaring methods, doc/declaration/throw source shares; see docs/REPRODUCTION.md §8). So one analyzer run
        # is kept as a fixed artifact per release commit and reused, never silently re-run.
        commit = json.loads((self.out / "provenance.json").read_text())["release"]["commit"]
        fresh, digest = self._fresh("analyzer", [], outs, f"commit:{commit}")
        if fresh or (self.reuse and all(o.exists() for o in outs) and "analyzer" not in self._stamps()):
            self._stamp("analyzer", digest)
            return ("reused", f"reused the JTratch output for release commit {commit[:10]} (kept fixed: JTratch "
                              f"is not run-to-run deterministic)")
        for o in raw.glob("*.csv"):
            o.unlink()
        self.run_cmd("analyzer", [PY, "src/collect/run_analyzers.py", self.tid])
        if not all(o.exists() for o in outs):
            raise RuntimeError("JTratch produced no output (see log)")
        self._stamp("analyzer", digest)
        return "JTratch finished"

    def s_dataset(self):
        self.run_cmd("dataset", [PY, "src/collect/build_dataset.py", self.tid])
        m = json.loads((self.out / "dataset_manifest.json").read_text())
        return (f"{m['files_with_catch']} files with catch blocks ({m['defective_files_with_catch']} defective); "
                f"{m['try_based_rows']} with try data")

    def s_models(self):
        m = json.loads((self.out / "dataset_manifest.json").read_text())
        if not m.get("has_outcome", True):
            return ("skipped", "no defect labels")
        pos = m["defective_files_with_catch"]
        if pos < MIN_DEFECTIVE or m["files_with_catch"] - pos < MIN_DEFECTIVE:
            return ("skipped", f"only {pos} defective of {m['files_with_catch']} files with catch blocks "
                               f"(need >= {MIN_DEFECTIVE} in each class)")
        rscript = shutil.which("Rscript")
        if not rscript:
            raise RuntimeError("Rscript not found: start the dashboard with ./envrun.sh")
        inputs = sorted((self.out / "input").glob("File_Level-*.csv"))
        outs = [self.res / "fixed" / f for f in ("base_test_2.csv", "predictors_simplified.csv",
                                                  "metric_groups.csv", "all_no_missing_regenerated.csv")]
        fresh, digest = self._fresh("models", inputs, outs)
        if fresh:
            return ("reused", "inputs unchanged since the last model run")
        self.run_cmd("models", [rscript, "src/reproduce/run_original.R", "fixed", "--input",
                                (self.out / "input").relative_to(ROOT).as_posix(), "--out",
                                self.res.relative_to(ROOT).as_posix()])
        self._stamp("models", digest)
        import pandas as pd
        d = pd.read_csv(self.res / "fixed" / "base_test_2.csv")
        return "; ".join(f"{r.metric_set} R²={r.r2_c_r:.3f}" for r in d[d.file_set == "CAT"].itertuples())

    def s_ml(self):
        data = self.res / "fixed" / "all_no_missing_regenerated.csv"
        outs = [self.res / "ml" / f for f in ("ml_results.csv", "ml_uplift.csv", "ml_results.md")]
        fresh, digest = self._fresh("ml", [data, self.res / "fixed" / "metric_groups.csv"], outs, f"r{self.repeats}")
        if fresh:
            return ("reused", "inputs unchanged since the last ML run")
        self.run_cmd("ml", [PY, "src/ml/train_eval.py", "--data", data, "--groups", self.res / "fixed" / "metric_groups.csv",
                            "--projects", self.tid, "--out", self.res / "ml", "--repeats", str(self.repeats),
                            "--title", f"{self.tid} (newly collected data)"])
        self._stamp("ml", digest)
        import pandas as pd
        r = pd.read_csv(self.res / "ml" / "ml_results.csv")
        best = r.sort_values("pr_auc_mean", ascending=False).iloc[0]
        return f"best PR-AUC {best.pr_auc_mean:.3f} ({best.learner}, {best.feature_set}); prevalence {best.prevalence:.3f}"

    def s_shap(self):
        ins = [self.res / "ml" / "ml_results.csv", self.res / "fixed" / "all_no_missing_regenerated.csv",
               self.res / "fixed" / "predictors_simplified.csv"]
        outs = [self.res / "ml" / f"shap_bar_{self.tid}.png", self.res / "ml" / "shap_top_eh.csv"]
        fresh, digest = self._fresh("shap", ins, outs)
        if fresh:
            return ("reused", "inputs unchanged since the last SHAP run")
        self.run_cmd("shap", [PY, "src/explain/shap_analysis.py", "--ml-results", ins[0], "--data", ins[1],
                              "--groups", self.res / "fixed" / "metric_groups.csv", "--phase0", ins[2],
                              "--projects", self.tid, "--out", self.res / "ml"])
        self._stamp("shap", digest)
        return "figures written"

    def s_summary(self):
        from summary import build
        s = build(self.tid)
        return f"summary.json written ({len(s.get('files', {}))} downloadable files)"

    # ---------- driver ----------
    def run(self) -> list:
        for s in self.steps:
            if self.cancel.is_set():
                s.status, s.message = "cancelled", "cancelled before start"
                continue
            bad = [d for d in s.deps if self.step(d).status not in ("done", "reused")]
            if s.name == "models" and self.step("defect_mining").status == "skipped":
                bad = []   # handled inside s_models ("no defect labels")
            if bad:
                s.status, s.message = "blocked", "needs: " + ", ".join(
                    f"{d} ({self.step(d).status})" for d in bad)
                self.on_update(self)
                continue
            s.status, s.started = "running", _now()
            self.on_update(self)
            t0 = time.time()
            try:
                r = getattr(self, f"s_{s.name}")()
                s.status, s.message = r if isinstance(r, tuple) else ("done", r)
            except InterruptedError:
                s.status, s.message = "cancelled", "cancelled by user"
            except Exception as e:  # noqa: BLE001 - report, continue with independent steps
                s.status, s.message = "failed", str(e)[:500]
                self.log(s.name, f"FAILED: {e}")
            s.ended, s.seconds = _now(), round(time.time() - t0, 1)
            self.on_update(self)
        return self.steps


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--no-reuse", action="store_true")
    a = ap.parse_args()
    seen = {}

    def show(r):
        for s in r.steps:
            if seen.get(s.name) != s.status:
                seen[s.name] = s.status
                print(f"[{s.status:>9}] {s.name:16s} {s.message}", flush=True)
    steps = Runner(a.target, a.repeats, not a.no_reuse, on_update=show).run()
    sys.exit(0 if all(s.status in ("done", "reused", "skipped") for s in steps) else 1)


if __name__ == "__main__":
    main()
