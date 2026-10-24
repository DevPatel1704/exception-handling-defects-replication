# Dashboard: give it a repository link, get the replication results

```bash
./envrun.sh python dashboard/app.py            # inside the conda env (R, Java 8, Python deps)
# open http://localhost:8000/
```

**Open the page through this server.** Opening `index.html` with VS Code's *Live Server* (port 5500), another
static server, or as a file shows the page, but none of the buttons can work: there is no API behind them. The page
then shows a red "dashboard server is not running" banner and disables its buttons.

1. **Repository**: paste a public `https://` repository URL and click *Load tags*. Tags are read with
   `git ls-remote` (no clone yet). Release, post-release and previous-release tags are pre-selected with the same
   heuristics that reproduce the paper's own choices (Hibernate 5.0.0.Final → 5.0.16; Hadoop 2.6.0 → 2.6.5).
2. **Window and tracker**: adjust the tags if needed and choose the issue tracker:
   * **Jira**: base URL (Apache and Hibernate are pre-filled). Leave *project keys* blank to detect them from
     the commit messages (e.g. `ZOOKEEPER-1234`). Cloud vs. Server API is detected automatically.
   * **GitHub Issues**: closed issues/PRs with a bug-like label, referenced as `#123` / `GH-123`. This
     **deviates from the paper** (Jira type Bug + resolution Fixed), and the result page says so. Set
     `GITHUB_TOKEN` before starting the server to raise GitHub's rate limits.
   * **None**: metrics only; no defect labels, so no models.
3. **Run analysis**: the job runs in the background; the page shows each step live with its log.
4. **Results**: data tiles, exception-handling anti-pattern profile, the authors' BASE / BSFC / BSAP models
   (optimism-reduced R², significant predictors with direction, Wald χ² and effect), ML prediction (RQ3), SHAP
   (RQ4), caveats, and download links for every intermediate file.

The *Original study* tab shows the reproduction of the paper (Phase 0), the new-context table and Phase A.

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
`GET /api/jobs/<id>`, `GET /api/jobs/<id>/log/<step>`, `POST /api/jobs/<id>/cancel`, `GET /api/results/<target>`.
See the docstring of `dashboard/app.py`.
