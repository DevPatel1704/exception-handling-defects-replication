# Contributions

Team: Dev Patel, Priyanka Gupta, Dhruv Patel, Slesha Vora, Pulkit Chopra.

The roles below are **suggested** starting points so work can be split along the repository's structure.
Each member should replace the *Tasks completed* / *Artifacts* cells with what they actually did, and keep
them current for each milestone. Commit links can be taken from `git log --author=<name>`.

| Member | Suggested role | Primary areas (repo paths) | Tasks completed (fill in) | Artifacts / commits (fill in) |
|---|---|---|---|---|
| Dev Patel | Reproduction lead (Phase 0) — R environment, running the authors' scripts, reproduction comparison table | `src/reproduce/`, `results/reproduction_comparison.*`, `docs/REPRODUCTION.md` | | |
| Priyanka Gupta | ML & explainability lead (RQ3/RQ4) — CV protocol, models, SHAP analysis and figures | `src/ml/`, `src/explain/`, `notebooks/`, `results/ml_*`, `results/shap_*` | | |
| Dhruv Patel | Data-collection lead (Phase 1) — cloning, analyzers (JTratch/NTratch), product metrics | `src/collect/clone_repo.py`, `src/collect/run_analyzers.py`, `src/collect/traditional_metrics.py` | | |
| Slesha Vora | Defect-mining & data-quality lead — process metrics, Jira mining, manual validation of defect links | `src/collect/process_metrics.py`, `src/collect/defect_mining.py`, `data/new/*/manual_validation_sample.csv`, `docs/DATA.md` | | |
| Pulkit Chopra | Statistical replication on new data (Phase 2) & dashboard; integration, README, environment docs | `src/model/`, `dashboard/`, `README.md`, `docs/ENVIRONMENT.md` | | |

## Shared responsibilities

| Activity | Owner(s) (fill in) | Notes |
|---|---|---|
| Manual validation of `manual_validation_sample.csv` (two raters, disagreements resolved) | | Record rater agreement in `docs/DATA.md`. |
| Report writing — study context & data sections | | |
| Report writing — results & reproduction table | | |
| Report writing — threats / limitations | | |
| Code review of each phase before commit | | |

## Note on tooling

No LLM is used anywhere in the analysis pipeline (data collection, modeling, evaluation). If any member uses an
LLM-based assistant to help write code or text, record it here (tool, model id, date, and what it was used for),
in line with the course's disclosure requirements.

| Member | Tool / model id | Date(s) | Used for |
|---|---|---|---|
| (team member who ran it — fill in) | Claude Code, model `claude-opus-5-5` (Anthropic) | 2026-10-24 | Generated the initial repository scaffold: Phase 0 driver, comparison builder, ML/SHAP scripts, Phase 1 collectors, and first drafts of the docs. All numbers in `results/` come from running that code, not from the assistant. Review and own each script before relying on it. |
| (fill in) | | | |
