# Working environment

All results in `results/` were produced on the machine and software stack below (captured 2026-10-24).
Re-capture with `./envrun.sh Rscript src/reproduce/env_versions.R` and the Python snippet at the end.

## Machine / OS

| Item | Value |
|---|---|
| OS | Microsoft Windows 11 Home Single Language, build 10.0.26300 (x64) |
| CPU / RAM | 12 logical cores, 7.4 GB RAM (JTratch is run with `-Xmx6g`; avoid running it next to two R jobs) |
| Shell | Git Bash (MINGW64) for `*.sh` scripts; PowerShell 5.1 also present |
| git | 2.50.1.windows.1 |
| conda | 25.7.0 (Anaconda) — environment `ehrepl`, fully pinned in [`environment.yml`](../environment.yml) |

## Environment `ehrepl` (conda-forge)

Create: `conda env create -n ehrepl -f environment.yml`, then apply the ModelMetrics fix below.
Run anything inside it with `./envrun.sh <cmd>` (sets PATH directly; avoids a `conda run` race on Windows).

### R (runs the authors' scripts unmodified, see docs/REPRODUCTION.md)

| Package | Version | Notes |
|---|---|---|
| R | 4.3.3 (2024-02-29 ucrt) | The authors used R 3.x (2017–18). One R ≥ 4.3 incompatibility is patched (REPRODUCTION.md §Deviations D2). |
| rms | 6.8.1 | `lrm`, `validate` (bootstrap), `fastbw`, `anova` |
| Hmisc | 5.2.3 | `varclus`, `redun`, `naclus` |
| caret | 6.0.94 | `findCorrelation` |
| e1071 | 1.7.16 | `skewness`, `kurtosis` |
| knitr / rmarkdown | 1.50 / 2.29 | `knitr::purl` to extract the Rmd code |
| ModelMetrics | 1.2.2.2 | **CRAN Windows binary** — the conda-forge build's DLL fails to load ("procedure could not be found"), which silently breaks `require(caret)`. Fix: `./envrun.sh Rscript -e 'install.packages("ModelMetrics", repos="https://cloud.r-project.org", type="win.binary", lib=.libPaths()[1])'` |
| plotly, BiodiversityR, logistf | not installed | Loaded with `require()` by the authors' scripts but only used in `glm`/`logistf` branches never reached by the presented `lrm` models. |

Full list: [`r-packages.txt`](../r-packages.txt).

### Python (data collection; the ML packages are installed for RQ3/RQ4)

| Package | Version |
|---|---|
| Python | 3.11.17 (conda-forge, MSC v.1944 64-bit) |
| pandas | 3.1.0 |
| numpy | 2.4.6 |
| scipy | 1.17.1 |
| scikit-learn | 1.9.1 |
| xgboost | 3.4.2 |
| shap | 0.51.0 (numba 0.68.0) |
| matplotlib | 3.11.2 |
| lizard | 1.24.2 (open-source fallback for product metrics) |
| openpyxl | 3.1.5 (reads the authors' aggregation-rule sheet) |
| jupyter_core / nbconvert / ipykernel | 5.9.1 / 7.17.2 / 7.4.0 |

Pinned in [`requirements.txt`](../requirements.txt).

### Java (exception-flow analyzer)

| Item | Version | Notes |
|---|---|---|
| JDK for running JTratch | OpenJDK 1.8.0_472 (Zulu 8.90, conda-forge `openjdk=8`) | Required: JDT 3.11 resolves JRE types from the Java 8 boot classpath, and JTratch uses JAXB (removed in Java 11). |
| JDT core bundled with JTratch | org.eclipse.jdt.core 3.11.2.v20160128 | From `external/JTratch/lib/` |
| System JDK (not used for runs) | Oracle JDK 24.0.1 | Running JTratch on it fails (JAXB missing). |

### Tools that are NOT available

| Tool | Status | Consequence |
|---|---|---|
| SciTools Understand | Commercial; no license on this machine | `src/collect/traditional_metrics.py` uses the documented open-source fallback; new-data BASE models are an *extension*, not a faithful BASE. Original-data results (Phase 0/A) are unaffected (they use the authors' released Understand metrics). |
| Maven / Gradle dependency cache | Not present (`~/.m2` absent) | JTratch's third-party binding resolution is reduced on new releases (see REPRODUCTION.md). |
| .NET Framework build of NTratch | Binary present (`NTratch-Rel.zip`, 2017); not yet exercised on a C# target | See REPRODUCTION.md, Phase 1 status. |
| LLMs | **Not used anywhere in the analysis pipeline** | — |

## Re-capturing versions

```bash
./envrun.sh Rscript src/reproduce/env_versions.R
./envrun.sh python -c "import sys,pandas,numpy,scipy,sklearn,xgboost,shap,matplotlib,lizard; print(sys.version); [print(m.__name__, getattr(m,'__version__',getattr(m,'version',''))) for m in (pandas,numpy,scipy,sklearn,xgboost,shap,matplotlib,lizard)]"
./envrun.sh java -version
```
