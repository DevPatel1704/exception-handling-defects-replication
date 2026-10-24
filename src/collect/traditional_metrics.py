"""Traditional product metrics per release file (paper Sec. 3.3.2).

Two back-ends:
  understand  SciTools Understand (COMMERCIAL). Used only if `und` is on PATH or UNDERSTAND_HOME is set and a
              license is already configured on this machine. No license is stored or configured here.
              Produces the same 39 file-level metrics the authors used (`und metrics` CSV, File rows).
  fallback    Open-source approximation (lizard + a line scanner). Produces a SUBSET of the Understand metric
              names with approximately equivalent definitions (see FALLBACK_METRICS). A BASE model built on these
              is an EXTENSION, not a faithful BASE; build_dataset.py records which back-end was used.

Usage: python src/collect/traditional_metrics.py <target-id> [--backend auto|understand|fallback]
Writes data/new/<id>/product_metrics.csv and data/new/<id>/product_metrics_meta.json
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clone_repo import NEW, load_target  # noqa: E402
from history import release_files  # noqa: E402

FALLBACK_METRICS = {
    "CountLine": "physical lines",
    "CountLineBlank": "blank lines",
    "CountLineComment": "lines containing a comment (// or inside /* */)",
    "CountLineCode": "lines containing code (non-blank, not comment-only)",
    "RatioCommentToCode": "CountLineComment / CountLineCode",
    "CountDeclFunction": "functions/methods found by lizard",
    "CountDeclClass": "class/interface/enum/struct declarations (regex)",
    "SumCyclomatic": "sum of lizard CCN over functions",
    "MaxCyclomatic": "max lizard CCN",
    "AvgCyclomatic": "mean lizard CCN",
    "AvgLineCode": "mean lizard NLOC per function",
    "CountSemicolon": "semicolons outside comments/strings (approx.)",
}
CLASS_RE = re.compile(r"\b(class|interface|enum|struct|record)\s+[A-Z_a-z]\w*")


def find_understand():
    und = shutil.which("und")
    if not und and os.environ.get("UNDERSTAND_HOME"):
        cand = Path(os.environ["UNDERSTAND_HOME"]) / "bin" / ("und.exe" if os.name == "nt" else "und")
        und = str(cand) if cand.exists() else None
    return und


def run_understand(und: str, t: dict, wt: Path, files: list, out: Path) -> pd.DataFrame:
    db = out / "raw" / f"{t['id']}.und"
    lang = {"java": "java", "csharp": "C#"}[t["language"]]
    db.parent.mkdir(parents=True, exist_ok=True)
    lst = out / "raw" / "understand_files.txt"
    lst.write_text("\n".join(str(wt / f) for f in files))
    subprocess.run([und, "create", "-db", str(db), "-languages", lang], check=True)
    subprocess.run([und, "add", f"@{lst}", str(db)], check=True)
    subprocess.run([und, "settings", "-metrics", "all", "-metricsOutputFile", str(out / "raw" / "understand.csv"),
                    str(db)], check=True)
    subprocess.run([und, "analyze", str(db)], check=True)
    subprocess.run([und, "metrics", str(db)], check=True)
    m = pd.read_csv(out / "raw" / "understand.csv")
    m = m[m["Kind"] == "File"].copy()
    m["File.Path"] = m["File"].map(lambda p: Path(p).resolve().relative_to(wt.resolve()).as_posix())
    return m


def scan_lines(text: str) -> dict:
    blank = comment = code = semis = 0
    in_block = False
    for line in text.splitlines():
        s = line.strip()
        if not s:
            blank += 1
            continue
        has_comment = has_code = False
        i, n = 0, len(s)
        in_str = None
        while i < n:
            ch = s[i]
            if in_block:
                has_comment = True
                if s.startswith("*/", i):
                    in_block = False; i += 2; continue
                i += 1; continue
            if in_str:
                if ch == "\\":
                    i += 2; continue
                if ch == in_str:
                    in_str = None
                i += 1; continue
            if s.startswith("//", i):
                has_comment = True; break
            if s.startswith("/*", i):
                in_block = True; has_comment = True; i += 2; continue
            if ch in "\"'":
                in_str = ch
            if ch == ";":
                semis += 1
            has_code = True
            i += 1
        comment += has_comment
        code += has_code
    return {"CountLine": len(text.splitlines()), "CountLineBlank": blank, "CountLineComment": comment,
            "CountLineCode": code, "CountSemicolon": semis}


def run_fallback(wt: Path, files: list) -> pd.DataFrame:
    import lizard
    rows = []
    for f in files:
        text = (wt / f).read_text(encoding="utf-8", errors="replace")
        r = {"File.Path": f, **scan_lines(text)}
        info = lizard.analyze_file.analyze_source_code(f, text)
        ccn = [fn.cyclomatic_complexity for fn in info.function_list]
        nloc = [fn.nloc for fn in info.function_list]
        r.update(CountDeclFunction=len(ccn), SumCyclomatic=sum(ccn), MaxCyclomatic=max(ccn, default=0),
                 AvgCyclomatic=sum(ccn) / len(ccn) if ccn else 0, AvgLineCode=sum(nloc) / len(nloc) if nloc else 0,
                 CountDeclClass=len(CLASS_RE.findall(re.sub(r"//.*|/\*.*?\*/", "", text, flags=re.S))))
        r["RatioCommentToCode"] = r["CountLineComment"] / r["CountLineCode"] if r["CountLineCode"] else 0
        rows.append(r)
    return pd.DataFrame(rows)


def main(tid: str, backend: str = "auto") -> pd.DataFrame:
    t = load_target(tid)
    out, wt = NEW / tid, NEW / tid / "src"
    files = release_files(wt, t["include_regex"], t["exclude_regex"])
    und = find_understand() if backend in ("auto", "understand") else None
    if backend == "understand" and not und:
        raise SystemExit("Understand requested but `und` not found (set UNDERSTAND_HOME or add it to PATH).")
    if und:
        df, meta = run_understand(und, t, wt, files, out), {"backend": "understand", "und": und}
    else:
        import lizard
        df = run_fallback(wt, files)
        meta = {"backend": "fallback", "lizard_version": lizard.version, "metrics": FALLBACK_METRICS,
                "note": "Understand not available (commercial license). Fallback metrics approximate a subset of the "
                        "39 Understand metrics; BASE models on this data are an extension, not a faithful BASE."}
    df.insert(1, "Project", tid)
    df.to_csv(out / "product_metrics.csv", index=False)
    (out / "product_metrics_meta.json").write_text(json.dumps(meta, indent=2))
    print(f"{tid}: product metrics via {meta['backend']} for {len(df)} files -> {out / 'product_metrics.csv'}")
    return df


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--backend", default="auto", choices=["auto", "understand", "fallback"])
    a = ap.parse_args()
    main(a.target, a.backend)
