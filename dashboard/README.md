# Dashboard: give it a repository link, get the replication results

```bash
./envrun.sh python dashboard/app.py            # inside the conda env (R, Java 8, Python deps)
# open http://localhost:8000/
```

**Open the page through this server.** Opening `index.html` with VS Code's *Live Server* (port 5500), another
static server, or as a file shows the page, but none of the buttons can work: there is no API behind them. The page
then shows a red "dashboard server is not running" banner and disables its buttons.

## Pages

| Page (sidebar) | What it shows |
|---|---|
| **Overview** | How it works, recent jobs, analysed releases, the reproduction headline (largest R² difference to the paper, read from `results/`), tool status. |
| **Analyze Repository** | A: repository URL (validated) → *Load tags* (`git ls-remote`, no clone). B: release, latest post-release and previous-release tags (pre-selected with the paper's convention: Hibernate 5.0.0.Final → 5.0.16, Hadoop 2.6.0 → 2.6.5), a live timeline of the pre-/post-release windows, language, issue tracker (Jira with key auto-detection, GitHub Issues, or none). *Advanced*: include/exclude patterns, test exclusion, CV repeats, reuse. *Run Analysis* confirms, then creates a real backend job. |
| **Analysis Jobs** | Job list (search, status filter, progress bars). Selected job: progress summary, the 11-step pipeline with status, duration, explanation and message, a live log while running, and per-step logs in a drawer (timestamps, wrap, copy, download, jump to end). *Cancel job* asks for confirmation. |
| **Research Results** | One analysed release: commits/dates with copy buttons, *Copy reproducibility details*, 7 metric cards, the *Read with care* limitations (always visible), Explanatory Models (BASE / BSFC / BSAP, R² bars with the paper's value as a tick, predictor chips → detail panel), anti-pattern chart + sortable table, ML (learner / feature-set / metric filters driving chart and table together, prevalence baseline, corrected-t-test p-values), SHAP (top-15 chart, top EH features, per-file explanations). |
| **Original Study** | Fixed reproduction results: Table 4 (paper vs. authors' output vs. ours as released vs. bug-fixed; the ±0.004 headline is computed from the CSV), Table 5 agreement, new release contexts (labelled as newly collected), ML and SHAP on the released data. |
| **Downloads** | Every artifact by category with type and size, per release or for the original study, plus a server-built zip (*Download all*). |

Issue trackers:
* **Jira**: base URL (Apache and Hibernate are pre-filled). Leave *project keys* blank to detect them from the
  commit messages; each detected prefix is checked against the Jira instance (so `CVE-2021-…` is ignored).
  Cloud vs. Server API is detected automatically.
* **GitHub Issues**: closed issues/PRs with a bug-like label, referenced as `#123` / `GH-123`. This **deviates
  from the paper** (Jira type Bug + resolution Fixed), and the result page says so. Set `GITHUB_TOKEN` before
  starting the server to raise GitHub's rate limits.
* **None**: metrics only; no defect labels, so no models.

Front end: plain ES modules, no build step and no network dependencies (`dashboard/assets/`): `api.js` (service
layer and JSDoc data types), `ui.js` (tooltips, dialogs, drawers, toasts, sortable tables, skeletons, empty
states), `charts.js` (SVG bar, grouped and diverging charts with tooltips and aria labels), `glossary.js` (plain-
language metric and step descriptions), `components/mlpanel.js`, `views/*.js` (one module per page). Light and
dark themes; keyboard-accessible tabs, dialogs and drawers; respects `prefers-reduced-motion`. The four
feature-set colours were checked with the dataviz palette validator (both themes).

## What runs (same code as the documented command-line pipeline)

`src/pipeline/run_target.py` runs, per target: clone → configure (language, source filter, Jira keys) →
process metrics → defect mining → product metrics → JTratch → dataset in the authors' format → the authors' R
models (`run_original.R fixed`) → ML → SHAP → `results/new/<target>/summary.json`. The same runner works without
the dashboard:

```bash
./envrun.sh python src/pipeline/run_target.py <target-id> [--repeats 5] [--no-reuse]
```

Targets created from the dashboard are stored in `data/targets.local.json` (curated ones stay in
`src/collect/targets.json`). Submitting the same repository and tags as an existing target reuses that target.
With *reuse* on, a step whose inputs are byte-identical to its last run (content hashes in
`data/new/<target>/stamps.json`) is skipped, and an existing JTratch output for the same release commit is reused.

## Limits

| | |
|---|---|
| Languages | **Java** end to end. **C#**: clone, process metrics, defect mining and product metrics run; the NTratch analysis and C# aggregation are not wired in yet (docs/REPRODUCTION.md T5), so there are no EH metrics or models. |
| Size / time | JTratch needs ~6 GB heap (`JTRATCH_XMX`) and ~35 min for a Hibernate-sized release; R ~10–15 min. One job runs at a time; the rest queue. |
| Models | Run only with ≥ 10 defective **and** ≥ 10 non-defective files that have catch blocks. |
| Fidelity | Same caveats as Phase 1/2: fallback product metrics without an Understand license; JTratch without the authors' external-Javadoc file and dependency jars. Shown on every result page. |
| Security | Binds to 127.0.0.1 only; https URLs only (validated; `git` runs non-interactively with only the https protocol allowed); the analysed code is parsed, never built or executed; static files are served from an allowlist. Not meant to be exposed beyond localhost. |

## API

`GET /api/health`, `GET /api/tags?repo=URL[&release=TAG]`, `GET /api/targets`, `POST /api/jobs`, `GET /api/jobs`,
`GET /api/jobs/<id>`, `GET /api/jobs/<id>/log/<step>`, `POST /api/jobs/<id>/cancel`, `GET /api/results`,
`GET /api/results/<target>`, `GET /api/metric-names`, `GET /api/artifacts/<target>`, `GET /api/archive/<target>.zip`.
See the docstring of `dashboard/app.py`. Updates use polling (2.5 s for a running job). Step logs carry UTC
timestamps per line.

## Tests

```bash
./envrun.sh python -m unittest discover -s tests -v       # tag parsing, suggestions, URL validation (offline)
cd tests/ui && npm install && cd ../..                     # puppeteer-core; uses your installed Edge/Chrome
node tests/ui/uitest.js pages                              # every page and interaction, screenshots in tests/ui/shots/
node tests/ui/uitest.js cancel                             # submits a real job through the form and cancels it
```
