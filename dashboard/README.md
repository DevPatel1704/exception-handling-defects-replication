# Dashboard (Phase 5, scaffold)

A static page (`index.html`, no dependencies) that renders the existing result files:

* reproduction table (`results/reproduction_comparison.csv`),
* new-context comparison (`results/new_context_comparison.csv`),
* ML results with PR-AUC / ROC-AUC / F1 tabs (`results/ml_results.csv`),
* SHAP figure (`results/shap_bar_all.png`),
* the curated target list (`src/collect/targets.json`).

Run: `python dashboard/serve.py`, then open <http://localhost:8000/dashboard/>.

## Scope (deliberately narrow)

Input = repository URL + release tag + post-release tag + language, **restricted to the curated, pre-validated
targets in `src/collect/targets.json`**. The page does not analyse arbitrary repositories.

## Future work

1. Job queue + worker (e.g. a small FastAPI app with a single background worker) that runs the documented
   Phase 1 commands for a curated target and then `run_original.R fixed --input … --out results/new/<id>`.
2. Per-target result pages (metrics distribution, BASE/BSFC/BSAP, SHAP per target).
3. Auth and resource limits before exposing it beyond localhost (JTratch needs ~6 GB heap and ~35 min per release).
