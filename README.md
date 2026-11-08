# Exception handling practices vs. post-release defects: replication + extensions

Graduate Software Maintenance & Evolution group project. We replicate and extend

> G. B. de Pádua and W. Shang. *Studying the Relationship between Exception Handling Practices and Post-release
> Defects.* MSR 2018. doi:[10.1145/3196398.3196435](https://doi.org/10.1145/3196398.3196435) ·
> replication package: <https://guipadua.github.io/eh-model-defects2018/>

The paper builds explanatory logistic models (BASE = traditional metrics; BSFC = BASE + exception-flow
characteristics; BSAP = BASE + 17 catch anti-patterns) for Hadoop 2.6, Hibernate 5.0 and Umbraco 7.6, and compares
optimism-reduced Nagelkerke R². No causal claims.

| RQ | Question | Where |
|---|---|---|
| RQ1 (replication) | Do exception-flow characteristics add explanatory power? | Phase 0, Phase 2 |
| RQ2 (replication) | Do exception-handling anti-patterns add explanatory power? | Phase 0, Phase 2 |
| RQ3 (extension) | Do EH metrics improve ML *prediction* over traditional metrics? | Phase A |
| RQ4 (extension) | Which EH features drive predictions (SHAP), and do they agree with RQ1–2? | Phase A |

## Headline results (Milestone 3, 2026-11-08)

Milestone 3 report: [`docs/reports/Milestone3_Group8_Report.pdf`](docs/reports/Milestone3_Group8_Report.pdf).
All contexts side by side: [`results/contexts_summary.md`](results/contexts_summary.md) and
[`results/figures/`](results/figures/). What changed since Milestone 2: [`docs/REPRODUCTION.md`](docs/REPRODUCTION.md) §9.

* **Reproduction (authors' data):** the released R scripts contain a one-line bug that makes "BSFC" a copy of BSAP.
  With it fixed, **all 9 Table 4 R² values reproduce within ±0.004 and all 35 Table 5 entries (Wald χ², effects) to
  rounding.** → [`results/reproduction_comparison.md`](results/reproduction_comparison.md)
* **New contexts (our data, 4 releases):** Hibernate 5.1.0 keeps the paper's ordering (BASE 0.238 < BSAP 0.264 <
  BSFC 0.275). On ZooKeeper 3.6.0 / 3.7.0 / 3.9.0 the EH models fall *below* BASE, but only because the released code
  drops a BASE-significant metric; applying the paper's own rule (sensitivity S1) puts them at or slightly above BASE
  (BSFC +0.035 / −0.004 / +0.017).
* **RQ3 (prediction):** after Holm correction **no learner gains from EH metrics in any of the 7 contexts** (1 of
  189 tests significant, and it is a loss: LR on ZooKeeper 3.9.0). Tree learners' point estimates are mostly
  positive, LR's mostly negative. → [`results/ml_uplift_ci.csv`](results/ml_uplift_ci.csv)
* **RQ4 (SHAP):** traditional metrics dominate; 0–6 of the top-10 EH features match a significant explanatory
  predictor, always with the same sign. → [`results/shap_alignment.md`](results/shap_alignment.md), `results/new/*/ml/`
* **Validity check (analyzer non-determinism):** over 10 JTratch runs per ZooKeeper release, only 6 flow metrics
  change; catch/anti-pattern metrics never do. BSFC is stable on 2 of 3 releases and swings 0.041–0.458 on
  ZooKeeper 3.6.0. → `results/new/*/variance/variance.md`
* **Defect-link validation:** rating packets for 131 links and two independent sheets are ready
  ([`docs/VALIDATION_GUIDE.md`](docs/VALIDATION_GUIDE.md)); ratings pending.
* **Dashboard:** paste any public Java repository URL; the page runs the whole pipeline and shows data, models, ML
  and SHAP. → [`dashboard/README.md`](dashboard/README.md)

## Reproduce everything from scratch

Prerequisites: git, conda (Anaconda/Miniconda), bash (Git Bash on Windows), ~10 GB disk, ≥ 8 GB RAM recommended.

```bash
git clone <this repo> && cd exception-handling-replication
conda env create -n ehrepl -f environment.yml
# Windows only: conda-forge's ModelMetrics DLL is broken, so replace it (caret needs it); see docs/ENVIRONMENT.md
./envrun.sh Rscript -e 'install.packages("ModelMetrics", repos="https://cloud.r-project.org", type="win.binary", lib=.libPaths()[1])'

# Phase 0: reproduce the paper (~37 min per run)
bash src/reproduce/fetch_package.sh
./envrun.sh Rscript src/reproduce/run_original.R asis
./envrun.sh Rscript src/reproduce/run_original.R fixed
./envrun.sh python src/reproduce/build_comparison.py

# Phase A: ML + SHAP on the released data (~30 min)
./envrun.sh jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=3600 notebooks/phaseA_ml_shap.ipynb

# Phase 1: new-release data (Hibernate 5.1.0; ~1 h incl. ~35 min JTratch)
for s in clone_repo process_metrics defect_mining traditional_metrics run_analyzers build_dataset; do
  ./envrun.sh python -W ignore src/collect/$s.py hibernate-5.1; done
# pipeline validation against the authors' values (Hibernate 5.0.0.Final)
for s in clone_repo run_analyzers; do ./envrun.sh python src/collect/$s.py hibernate-5.0-validation; done
./envrun.sh python -W ignore src/collect/validate_against_original.py

# Phase 2: the authors' models on the new data
./envrun.sh Rscript src/reproduce/run_original.R fixed --input data/new/hibernate-5.1/input --out results/new/hibernate-5.1
./envrun.sh python src/reproduce/build_comparison.py

# Milestone 3: more contexts, Holm, analyzer variance, sensitivity S1, validation packets, summary + figures
# (full list with timings: docs/REPRODUCTION.md §9)
./envrun.sh python src/pipeline/run_target.py zookeeper-release-3.7.0 --repeats 10
./envrun.sh python src/ml/train_eval.py --from-folds
./envrun.sh python -W ignore src/collect/analyzer_variance.py zookeeper-release-3.6.0 --runs 10
./envrun.sh Rscript src/reproduce/run_original.R fixed --force-sig --input data/new/zookeeper-release-3.6.0/input --out results/new/zookeeper-release-3.6.0
./envrun.sh python src/collect/validation_packet.py && ./envrun.sh python src/collect/validation_agreement.py
./envrun.sh python src/reproduce/context_summary.py

# Dashboard: paste a repository link, get the full pipeline's results (see dashboard/README.md)
./envrun.sh python dashboard/app.py     # http://localhost:8000/
./envrun.sh python -m unittest discover -s tests -v     # offline tests of the dashboard's tag/URL handling
```

`envrun.sh` runs a command inside the `ehrepl` env without `conda activate` (it avoids a `conda run` race on
Windows). Every result file names the command that regenerates it.

## Repository map

```
README.md  CONTRIBUTIONS.md  environment.yml  requirements.txt  r-packages.txt  envrun.sh
docs/
  REPRODUCTION.md      what we ran, outputs, deviations (D1 bug fix, D2 R-4.3 patch, ...), TODOs
  DATA.md              data sources, tags + commit SHAs, collection/cleaning, validation, limitations, "no LLM"
  ENVIRONMENT.md       OS, R/Python/Java versions, unavailable tools
  aggregation_rules/   the authors' metric & aggregation-rule sheets (exported)
external/              authors' package + JTratch/NTratch clones (gitignored; fetch_package.sh)
data/
  original/all_no_missing.csv   authors' released merged dataset (provenance in docs/DATA.md)
  new/<target>/        provenance.json, process/product/defect metrics, input/File_Level-*.csv,
                       manual_validation_sample.csv (raw analyzer output and repos are gitignored)
src/
  reproduce/   fetch_package.sh, run_original.R (authors' notebooks, asis|fixed, --input/--out, --force-sig), build_comparison.py,
               context_summary.py (all contexts: tables + figures)
  collect/     targets.json, clone_repo, process_metrics, defect_mining, traditional_metrics, run_analyzers,
               aggregate_jtratch (rule re-implementation), build_dataset, validate_against_original, history (git/Jira),
               analyzer_variance (T10), validation_packet + validation_agreement (defect-link validation)
  model/       (Phase 2 uses src/reproduce/run_original.R --input; see src/model/README.md)
  ml/          common.py (data + feature groups), train_eval.py (RQ3)
  explain/     shap_analysis.py (RQ4)
notebooks/     phaseA_ml_shap.ipynb (reruns RQ3 + RQ4 end to end)
results/       reproduction_comparison.{csv,md}, reproduction_table5.csv, reproduce/{asis,fixed}/,
               ml_*.{csv,md}, shap_*.{png,csv,md}, pipeline_validation_hibernate-5.0.*, new/<target>/, new_context_comparison.csv
src/pipeline/  run_target.py (whole pipeline for one target), targets_api.py (URL/tag validation, suggestions),
               summary.py (results/new/<target>/summary.json)
dashboard/     app.py (local server + job worker), index.html + assets/ (ExceptionLab UI: ES modules, no build)
tests/         offline unit tests; tests/ui/ headless-browser UI tests (puppeteer-core)
```

## Use of LLMs

The analysis pipeline uses **no LLM**. The initial scaffold of this repository was written with an LLM coding
assistant; the disclosure is in [CONTRIBUTIONS.md](CONTRIBUTIONS.md).
