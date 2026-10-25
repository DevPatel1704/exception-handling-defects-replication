# Exception Handling and Post-Release Defects: a Replication (Milestone 2)

Software Maintenance and Evolution · Group 8 · Ontario Tech University
Dev Patel · Priyanka Gupta · Dhruv Patel · Slesha Vora · Pulkit Chopra

We replicate and extend G. B. de Pádua and W. Shang, *Studying the Relationship between Exception Handling Practices
and Post-release Defects*, MSR 2018 ([doi:10.1145/3196398.3196435](https://doi.org/10.1145/3196398.3196435);
replication package <https://guipadua.github.io/eh-model-defects2018/>). This branch contains the **working
foundation** reported in Milestone 2: the reproduction of the original study and the pipeline for new study contexts.

| RQ | Question | Status in this milestone |
|---|---|---|
| RQ1 | Do exception-flow characteristics add explanatory power for post-release defects? | Reproduced; first new-context results |
| RQ2 | Do exception-handling anti-patterns add explanatory power? | Reproduced; first new-context results |
| RQ3 | Do exception-handling metrics improve ML defect prediction? | In progress (next milestone) |
| RQ4 | Which exception-handling features drive the predictions (SHAP)? | In progress (next milestone) |

## Results so far

* **Reproduction (Phase 0).** The authors' released R scripts contain a bug that fits the anti-pattern data into
  the "BSFC" model. With a one-line fix, **all 9 optimism-reduced Nagelkerke R² values of the paper's Table 4
  reproduce within ±0.004, and all 35 Table 5 entries (Wald χ², effects) to rounding.**
  → [`results/reproduction_comparison.md`](results/reproduction_comparison.md), [`docs/REPRODUCTION.md`](docs/REPRODUCTION.md) §3
* **Pipeline validation.** Our analyzer run plus aggregation on the paper's own release (Hibernate 5.0.0.Final)
  matches 57/107 file-level exception-handling metrics on ≥ 95% of files.
  → [`results/pipeline_validation_hibernate-5.0.md`](results/pipeline_validation_hibernate-5.0.md)
* **New contexts (Phases 1–2).** Hibernate ORM 5.1.0: BASE 0.238 < BSAP 0.264 < BSFC 0.275 (same ordering as the paper).
  Apache ZooKeeper 3.6.0: BASE 0.423, BSAP 0.417, BSFC 0.041. Two findings (JTratch is not run-to-run
  deterministic; BASE predictors can be dropped from BSFC/BSAP on small samples) are in `docs/REPRODUCTION.md` §5.

## Reproduce everything from scratch

Prerequisites: git, conda, bash (Git Bash on Windows), ~10 GB disk, ≥ 8 GB RAM.

```bash
git clone https://github.com/DevPatel1704/exception-handling-defects-replication.git
cd exception-handling-defects-replication
conda env create -n ehrepl -f environment.yml
# Windows only: replace conda-forge's broken ModelMetrics DLL (caret needs it); see docs/ENVIRONMENT.md
./envrun.sh Rscript -e 'install.packages("ModelMetrics", repos="https://cloud.r-project.org", type="win.binary", lib=.libPaths()[1])'

# Phase 0: reproduce Table 4 / Table 5 (~37 min per run)
bash src/reproduce/fetch_package.sh                      # downloads + SHA-256-verifies the authors' package
./envrun.sh Rscript src/reproduce/run_original.R asis    # authors' code as released
./envrun.sh Rscript src/reproduce/run_original.R fixed   # with the one-line BSFC fix
./envrun.sh python src/reproduce/build_comparison.py     # -> results/reproduction_comparison.{csv,md}

# Phase 1: new-release data (per target; ~1 h for Hibernate incl. ~35 min JTratch)
for t in hibernate-5.1 zookeeper-release-3.6.0; do
  for s in clone_repo process_metrics defect_mining traditional_metrics run_analyzers build_dataset; do
    ./envrun.sh python -W ignore src/collect/$s.py $t; done; done
# pipeline validation against the authors' released values (Hibernate 5.0.0.Final)
for s in clone_repo run_analyzers; do ./envrun.sh python src/collect/$s.py hibernate-5.0-validation; done
./envrun.sh python -W ignore src/collect/validate_against_original.py

# Phase 2: the authors' models on the new data
for t in hibernate-5.1 zookeeper-release-3.6.0; do
  ./envrun.sh Rscript src/reproduce/run_original.R fixed --input data/new/$t/input --out results/new/$t; done
./envrun.sh python src/reproduce/build_comparison.py     # adds the new-context section
```

`envrun.sh` runs a command inside the `ehrepl` conda env. Every result file names the command that regenerates it.
Note: JTratch is not run-to-run deterministic (`docs/REPRODUCTION.md` §5, F1); the committed analyzer outputs are
the ones the reported results were computed from.

## Repository map

```
docs/REPRODUCTION.md     what we ran, outputs, every deviation, open issues (§6)
docs/DATA.md             data sources, tags + commit SHAs, collection and cleaning, validation, limitations
docs/ENVIRONMENT.md      OS, R / Python / Java versions, unavailable tools
docs/aggregation_rules/  the authors' metric and aggregation-rule sheets (exported)
data/original/           the authors' released merged dataset (provenance in docs/DATA.md)
data/new/<target>/       provenance.json, process/product/defect metrics, input/File_Level-*.csv,
                         defect_links.csv, manual_validation_sample.csv, raw/jira_issues.json (Jira snapshot)
src/reproduce/           fetch_package.sh, run_original.R (asis | fixed, --input/--out), build_comparison.py
src/collect/             targets.json, clone_repo, process_metrics, defect_mining, traditional_metrics,
                         run_analyzers, aggregate_jtratch, build_dataset, validate_against_original, history
results/                 reproduction_comparison.{csv,md}, reproduction_table5.csv, reproduce/{asis,fixed}/,
                         pipeline_validation_hibernate-5.0.*, new/<target>/fixed/, new_context_comparison.csv
CONTRIBUTIONS.md         member roles and tasks
```

Large third-party inputs (the authors' package, analyzer sources, cloned target repositories, raw analyzer output)
are not committed; `fetch_package.sh` and the Phase 1 commands recreate them.

No large language model is used anywhere in the analysis pipeline.
