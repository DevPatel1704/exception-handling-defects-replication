# Contributions (Milestone 2)

Roles follow the project proposal (Section V, Responsibilities). Everyone contributed to project selection,
analysis and writing.

| Member | Role (proposal) | Main tasks this milestone | Outputs (artifacts) |
|---|---|---|---|
| Dev Patel | Exception-flow tooling | Built JTratch from source at the paper's tag on Java 8; ran it on the new releases; re-implemented the authors' file-level aggregation; validated it against the authors' released values (Hibernate 5.0.0.Final) | `src/collect/run_analyzers.py`, `aggregate_jtratch.py`, `validate_against_original.py`, `results/pipeline_validation_hibernate-5.0.*` |
| Priyanka Gupta | Traditional and process metrics, defect mining | Git-history process metrics; Jira defect mining with rename-aware file mapping; open-source product-metric fallback; manual-validation samples | `src/collect/process_metrics.py`, `defect_mining.py`, `history.py`, `traditional_metrics.py`, `data/new/*/` |
| Dhruv Patel | Statistical replication in R | Ran the authors' R pipeline; found and fixed the BSFC bug; R ≥ 4.3 compatibility patch; Table 4/5 comparison; BASE/BSFC/BSAP on the new contexts | `src/reproduce/run_original.R`, `build_comparison.py`, `results/reproduction_comparison.*`, `results/reproduce/`, `results/new/*/fixed/` |
| Slesha Vora | ML models and SHAP | Defined the RQ3/RQ4 protocol (feature sets, learners, CV, PR-AUC); dataset schema checks for the ML stage; data-quality review of the new datasets | Protocol in `docs/REPRODUCTION.md` §6 (T9); ML results due next milestone |
| Pulkit Chopra | Orchestration and integration | Reproducible environment (conda, version capture, `envrun.sh`); package download and verification; dataset assembly in the authors' format; repository, README and documentation integration | `environment.yml`, `envrun.sh`, `src/reproduce/fetch_package.sh`, `src/collect/build_dataset.py`, `README.md`, `docs/` |

## Use of AI assistance

No large language model is used in the analysis pipeline (data collection, modelling or evaluation). An AI coding
assistant (Claude, Anthropic; October 2026) was used to help draft scripts and documentation; the team reviewed the
code, and every number reported comes from executing it.
