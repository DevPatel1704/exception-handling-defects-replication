"""Run the authors' exception-flow analyzers on a checked-out release.

Java  -> JTratch, built from source at tag `eh-model-defects2018` (external/JTratch), run on a Java 8 JVM
         (JDT 3.11 needs the Java 8 boot classpath; JAXB was removed from Java 11+).
C#    -> NTratch.exe from the authors' 2017 binary release (.NET Framework; Windows only). Attempted, may be blocked.

Usage: python src/collect/run_analyzers.py <target-id> [--java8 <path to java.exe>] [--m2 <maven repo dir>]
JVM heap: env JTRATCH_XMX (default 6g).
Writes raw analyzer CSVs to data/new/<id>/raw/analyzer/ and a log; aggregation to file level is done by
build_dataset.py (rules in docs/aggregation_rules/metrics_and_aggregation_rules_MSR18.xlsx).

Known deviations (recorded in docs/REPRODUCTION.md):
  * The external-Javadoc XML used by the authors (/Users/gbp/javadoc/javadoc.xml) is not published, so the
    "External Doc" source of possible exceptions is empty for our runs.
  * Third-party binding resolution depends on the jars available in --m2 (the authors pointed JTratch at
    their whole local Maven repo). Without it, exceptions declared by third-party APIs are under-counted.
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clone_repo import NEW, ROOT, load_target  # noqa: E402

JT = ROOT / "external" / "JTratch"
JT_BUILD = ROOT / "build" / "jtratch"


def find_java8(explicit=None) -> str:
    cands = [explicit] if explicit else []
    if os.environ.get("CONDA_PREFIX"):
        cands += [str(Path(os.environ["CONDA_PREFIX"]) / "Library" / "bin" / "java.exe"),
                  str(Path(os.environ["CONDA_PREFIX"]) / "bin" / "java")]
    if os.environ.get("JAVA8_HOME"):
        cands.append(str(Path(os.environ["JAVA8_HOME"]) / "bin" / "java"))
    for c in cands:
        if c and Path(c).exists():
            v = subprocess.run([c, "-version"], capture_output=True, text=True).stderr
            if '"1.8' in v:
                return c
    raise SystemExit("No Java 8 runtime found (activate the ehrepl conda env, set JAVA8_HOME, or pass --java8).")


def build_jtratch(java: str) -> str:
    """Compile JTratch sources (excluding samples) with the Java 8 javac next to `java`, or any javac --release 8."""
    classes = JT_BUILD / "classes"
    cp = os.pathsep.join(sorted(glob.glob(str(JT / "lib" / "*.jar"))))
    if not (classes / "ca" / "concordia" / "jtratch" / "JTratch.class").exists():
        javac = Path(java).with_name("javac.exe" if os.name == "nt" else "javac")
        javac = str(javac) if javac.exists() else shutil.which("javac")
        srcs = [str(p) for p in (JT / "src" / "main" / "java").rglob("*.java") if "sample" not in p.parts]
        classes.mkdir(parents=True, exist_ok=True)
        (JT_BUILD / "sources.txt").write_text("\n".join(srcs))
        rel = [] if "1.8" in subprocess.run([javac, "-version"], capture_output=True, text=True).stderr else ["--release", "8"]
        subprocess.run([javac, *rel, "-nowarn", "-encoding", "UTF-8", "-cp", cp, "-d", str(classes),
                        f"@{JT_BUILD / 'sources.txt'}"], check=True)
    return os.pathsep.join([str(classes), str(JT / "conf"), cp])


def run_jtratch(t: dict, java: str, m2: str) -> Path:
    src = (NEW / t["id"] / "src").resolve()
    out = NEW / t["id"] / "raw" / "analyzer"
    out.mkdir(parents=True, exist_ok=True)
    cp = build_jtratch(java)
    cmd = [java, f"-Xmx{os.environ.get('JTRATCH_XMX', '6g')}", "-cp", cp, "ca.concordia.jtratch.JTratch", "ByFolder", src.as_posix(), m2 or "NONE"]
    print("running JTratch:", cmd[1], "ByFolder", src.as_posix(), flush=True)
    with open(out / "jtratch_stdout.txt", "w", encoding="utf-8") as fh:
        r = subprocess.run(cmd, cwd=out, stdout=fh, stderr=subprocess.STDOUT)
    produced = sorted(p.name for p in out.glob("*.csv"))
    print(f"JTratch exit={r.returncode}; CSVs: {produced}")
    if r.returncode != 0 or not produced:
        (out / "BLOCKED.txt").write_text(f"JTratch failed (exit {r.returncode}); see jtratch_stdout.txt and logs/\n")
    return out


def run_ntratch(t: dict) -> Path:
    out = NEW / t["id"] / "raw" / "analyzer"
    out.mkdir(parents=True, exist_ok=True)
    exe = ROOT / "build" / "ntratch" / "NTratch-Rel" / "NTratch" / "NTratch.exe"
    if not exe.exists():
        import zipfile
        zipfile.ZipFile(ROOT / "external" / "downloads" / "bin" / "NTratch-Rel.zip").extractall(ROOT / "build" / "ntratch")
    sln = sorted((NEW / t["id"] / "src").rglob("*.sln"))
    if os.name != "nt" or not sln:
        msg = "NTratch needs Windows/.NET Framework and a .sln file" + ("" if sln else " (none found)")
        (out / "BLOCKED.txt").write_text(msg + "\n")
        raise SystemExit(msg)
    cmd = [str(exe), "ByFolder", str((NEW / t["id"] / "src").resolve())]
    with open(out / "ntratch_stdout.txt", "w", encoding="utf-8") as fh:
        r = subprocess.run(cmd, cwd=out, stdout=fh, stderr=subprocess.STDOUT, timeout=6 * 3600)
    print(f"NTratch exit={r.returncode}; CSVs: {sorted(p.name for p in out.glob('*.csv'))}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--java8")
    ap.add_argument("--m2", help="directory of dependency jars for binding resolution (optional)")
    a = ap.parse_args()
    t = load_target(a.target)
    if t["language"] == "java":
        run_jtratch(t, find_java8(a.java8), a.m2)
    else:
        run_ntratch(t)


if __name__ == "__main__":
    main()
