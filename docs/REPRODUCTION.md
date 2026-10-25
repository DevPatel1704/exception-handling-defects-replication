# Reproduction log

What we ran, with which commands, what came out, and every deviation from the original study.
Paper: G. B. de Pádua and W. Shang, *Studying the Relationship between Exception Handling Practices and
Post-release Defects*, MSR 2018, doi:10.1145/3196398.3196435.

Status (Milestone 2, 2026-10-25): **Phase 0 complete**: Table 4 and Table 5 reproduced. **Phase 1 complete**: the data pipeline
runs end to end on Hibernate ORM 5.1.0 and Apache ZooKeeper 3.6.0. **Phase 2 in progress**: the authors' models fitted on both new
contexts. Remaining work: §6.

---

## 1. The authors' replication package: what is actually there

Landing page: <https://guipadua.github.io/eh-model-defects2018/> (fetched 2026-10-24). Everything is downloaded by
`bash src/reproduce/fetch_package.sh`, which also checks the SHA-256 of each archive.

| Artifact on the page | URL | Local path | SHA-256 |
|---|---|---|---|
| "Single CSV with merged data with no missing" | `/resources/eh-model-defects2018_data_without_missing.zip` | `external/data_without_missing/all_no_missing.csv` (copy: `data/original/all_no_missing.csv`) | zip `6a8eee1f…2610`; csv `2e68a28a…5efb36f`* |
| "Input, Scripts and Output" (full modeling package) | `/resources/eh-model-defects2018_scripts_with_input_data.zip` | `external/scripts_with_input_data/` | `2d6387a9…eaa` |
| Knitted notebook: data processing | `/resources/eh-model-defects2018-0-DataSourcesAnalysis.html` | `external/downloads/` | `44d32a58…4123` |
| Knitted notebook: model construction | `/resources/eh-model-defects2018-1-Model_Construction.html` | `external/downloads/` | `7cf367be…6cd5` |
| Camera-ready paper | `/resources/eh-model-defects2018_cr.pdf` | `external/downloads/` | `17cea4b2…0dafe0d` |
| "Metrics and aggregation rules" (Google Sheet) | docs.google.com/spreadsheets/d/11fb_6Flb… | `docs/aggregation_rules/metrics_and_aggregation_rules_MSR18.xlsx` | (exported xlsx) |
| JTratch metric data elements (Google Sheet, linked from the JTratch README) | docs.google.com/spreadsheets/d/1AsQqDld… | `docs/aggregation_rules/jtratch_metric_data_elements.xlsx` | (exported xlsx) |
| "Java Binary and Source" → github.com/guipadua/JTratch, tag `eh-model-defects2018` | | `external/JTratch/` @ `af7c232f5e77de143a5a00e1d9b3151c22ebfc66` | |
| "C# Binary and Source" → github.com/guipadua/NTratch, tag `eh-model-defects2018` | | `external/NTratch/` @ `6f6e9722979f374228723cd3ad13f07cbff1d0c1` | |
| Analyzer binaries (attached only to the older release `2017icpc_era_cr`) | `JTratch-Rel.zip`, `NTratch-Rel.zip` | `external/downloads/bin/` | `bfff8528…1a51`, `64fd0d4a…7840` |

\* full csv hash: `2e68a28a5acdac879ab13df164372ce020e023d850c8ac74e6c4ec68f5efb36f`. Full archive hashes are in `fetch_package.sh`.

Contents of `scripts_with_input_data/` (macOS `__MACOSX`/`.DS_Store` debris removed):

| File | Role |
|---|---|
| `0-DataSourcesAnalysis.Rmd` | Loads the 5 input CSVs, merges them per project, missing-data analysis (MC1), saves `0-all_no_missing.RData` + `all_no_missing.csv` |
| `1-Model_Construction.Rmd` | Section 1: preliminary models on all files. Section 2 (**the presented results**): files with ≥1 catch block, BASE / BSAP / BSFC |
| `construction_functions.R` | MC2–MC7: budget, correlation (`caret::findCorrelation`, Spearman, 0.7), redundancy (`Hmisc::redun`, R²>0.9), budget-based correlation, `rms::lrm` on log10(x+1) data |
| `analysis_functions.R` | MA1–MA4: `rms::validate(B=1000)` (optimism-reduced Nagelkerke R²), `fastbw(rule="p", sls=.05)`, refit, `anova` Wald χ², effect at mean+10% |
| `input/File_Level-{Git-Jira,Understand,Catch_Based,Try_Based,Throws_Based}.csv` | The five file-level data sources (10,195+ files over 3 projects) |
| `output/base_test_1_BKP.csv`, `output/base_test_2_BKP.csv` | **The authors' own run outputs** (section 1 and section 2) |

Things the page or the paper implies but that are **not** in the package:
* The Tableau workbook used to aggregate analyzer output to file level (only the rules sheet is published).
* `/Users/gbp/javadoc/javadoc.xml`, the external-Javadoc database JTratch reads (hard-coded path in `CodeAnalyzer.java`).
* Raw analyzer output (catch/try/possible-exception level) and the raw git/Jira extraction.

## 2. Environment

See [ENVIRONMENT.md](ENVIRONMENT.md). In short: Windows 11, conda env `ehrepl`, R 4.3.3, rms 6.8.1, Hmisc 5.2.3,
caret 6.0.94, Python 3.11.17, OpenJDK 8. Use `./envrun.sh <cmd>` to run inside the env.

## 3. Phase 0: reproducing Table 4 and Table 5

### Commands

```bash
bash src/reproduce/fetch_package.sh                          # download + verify package
./envrun.sh Rscript src/reproduce/run_original.R asis        # authors' code, as released (~37 min)
./envrun.sh Rscript src/reproduce/run_original.R fixed       # + one-line BSFC fix         (~37 min)
./envrun.sh python  src/reproduce/build_comparison.py        # -> results/reproduction_comparison.{csv,md},
                                                             #    results/reproduction_table5.csv
```

`run_original.R` copies the package into `build/reproduce_<mode>/` (so `external/` stays untouched), applies the
patches listed below, calls `set.seed(2018)`, then `knitr::purl`s and `source`s **both** notebooks in the authors'
order in the global environment, exactly as knitting would. Outputs in `results/reproduce/<mode>/`:
`base_test_1.csv` and `base_test_2.csv` (the authors' own output format), `predictors_simplified.csv` (Wald χ²,
p-value, coefficient and MA4 effect of each predictor in each simplified model, recomputed with the authors'
formulas), `metric_groups.csv`, `all_no_missing_regenerated.csv`, `run_log.txt` (full console log, including every
`lrm` print), `figures_from_authors_code.pdf` (varclus/naclus/Ecdf plots), `sessionInfo.txt`.

### Results

Full tables: [`results/reproduction_comparison.md`](../results/reproduction_comparison.md).

| Project | Model | Paper (Table 4) | Authors' released output | Ours: as released | Ours: BSFC fixed |
|---|---|---:|---:|---:|---:|
| Umbraco | BASE | 0.09 | 0.092 | 0.090 | 0.090 |
| Umbraco | BSFC | 0.09 | 0.182 | 0.179 | **0.089** |
| Umbraco | BSAP | 0.18 | 0.177 | 0.176 | 0.176 |
| Hadoop | BASE | 0.33 | 0.329 | 0.331 | 0.331 |
| Hadoop | BSFC | 0.37 | 0.350 | 0.351 | **0.372** |
| Hadoop | BSAP | 0.35 | 0.352 | 0.351 | 0.351 |
| Hibernate | BASE | 0.21 | 0.213 | 0.211 | 0.211 |
| Hibernate | BSFC | 0.28 | 0.231 | 0.232 | **0.279** |
| Hibernate | BSAP | 0.23 | 0.235 | 0.233 | 0.233 |

* **With the fix, all 9 optimism-reduced R² values reproduce within ±0.004.** The remaining differences are
  bootstrap noise (`validate()` resamples; the authors set no seed). The *apparent* (uncorrected) R² of every model
  is deterministic and identical across runs.
* The model-construction indicators of Table 4 also reproduce exactly in the fixed run: budgets 15/59/29;
  # potential predictors BASE 12/10/18, BSFC 23/31/27, BSAP 16/23/19; adjusted cutoffs 0.70 everywhere except
  Umbraco BSFC (paper 0.24, ours 0.241) and Umbraco BSAP (paper 0.67, ours 0.671).
* **Table 5: all 35 entries (significant predictors, Wald χ², effects) reproduce** to the paper's rounding
  (max |Δχ²| = 0.005, max |Δeffect| = 0.05 pp), and our simplified models contain no significant predictors that
  Table 5 does not list. The paper's "Effect" is the *relative* change of the predicted probability
  (`effect_rel_pct` in `predictors_simplified.csv`).
* `0-DataSourcesAnalysis.Rmd` regenerates the released `all_no_missing.csv` exactly (10,195 × 159, identical file
  IDs, max numeric difference 0). Rows discarded as missing (MC1): Hadoop 36/3,698, Hibernate 38/3,488,
  Umbraco 91/3,174, matching the paper's "< 3%".

### Deviations from the original method (all deliberate, all recorded)

| ID | Deviation | Why | Effect on results |
|---|---|---|---|
| **D1** | **BSFC bug fix (mode `fixed` only).** `construction_functions.R`, `dataApplyReductionByModel()`, line 223 reads `data_list = all_list_omitted_m2`, which overwrites the function's argument. The BSFC call (`dataApplyReductionByModel(all_list_omitted_m3, "BSFC")`) is therefore silently fed the *catch / anti-pattern* data of BSAP. We comment that single line out. | As released, "BSFC" is a second BSAP model: identical formulas, significant predictors and apparent R² to BSAP, differing only by bootstrap noise. This is visible in the authors' own `output/base_test_2_BKP.csv` and in their knitted HTML, whose BSFC "Final variables" are catch/AP metrics. The paper's BSFC numbers (0.09/0.37/0.28, Table 5 HA-8..12, HB-6..8) can only come from a run without this line. | Changes BSFC only. Makes BSFC match the paper (R², indicators, Table 5). BASE and BSAP are byte-identical between modes. |
| **D2** | **R ≥ 4.3 compatibility patch (both modes).** `analysis_functions.R:270` `if(class_refit != "try-error" && !is.na(refit))` → `... && !is.na(refit)[1])`. | R 4.3 made `&&` with a length > 1 operand an error; the authors' R 3.x silently used the first element. `is.na()` on an `lrm` object returns one value per list element (length 26). | None. It makes R 3.x's implicit behaviour explicit. |
| D3 | `set.seed(2018)` before running. | The authors set no seed, so `validate(B=1000)` results vary by about ±0.005 between runs. | Makes our numbers repeatable; does not bias them. |
| D4 | R 4.3.3 + current CRAN-era packages instead of the authors' 2017–18 versions (R 3.x, rms 5.x). | Original versions not recorded in the package and not installable on this OS without effort. | None observed: Table 4/5 reproduce to rounding. |
| D5 | `plotly`, `BiodiversityR`, `logistf` not installed. | Loaded via `require()` only; used in `glm`/`logistf` branches never taken by the `lrm` models. | None. |
| D6 | ModelMetrics replaced with the CRAN binary (see ENVIRONMENT.md). | conda-forge DLL fails to load → `require(caret)` silently FALSE → `findCorrelation` missing. | None (environment fix). |

Failures we hit on the way (kept for the record): (i) first conda solve died on a network reset; retried.
(ii) caret failed to load (D6). (iii) concurrent `conda run` calls race on a temp file → `envrun.sh`.
(iv) R 4.3 `&&` error in section 1 (D2). (v) our first D2 patch put its comment before the `{` and broke the
parse; fixed.

### Implication for the replication

**RQ1 (exception-flow characteristics) as published cannot be regenerated from the released scripts; RQ2 can.**
With the one-line fix, RQ1 reproduces exactly. Section 1's preliminary result (paper §3.6, all files) also
reproduces: in every all-files model with EH constructs, one EH construct count stays significant after
simplification (Hadoop and Umbraco `# Catch`, Hibernate `# Throws`). The significant-predictor sets of all six
section-1 models are identical to the authors' `base_test_1_BKP.csv`, and optimism-reduced R² differs by
≤ 0.003 (`results/reproduce/*/base_test_1.csv`). Because RQ1's evidence rests on the BSFC column, the
bug and its fix should be reported in our write-up and, ideally, to the authors.

## 4. Phase 1: new-release data pipeline

Details: [DATA.md](DATA.md) §1b–§4. Commands (target `hibernate-5.1`; the same steps work for any target in
`src/collect/targets.json`):

```bash
./envrun.sh python src/collect/clone_repo.py hibernate-5.1
./envrun.sh python src/collect/process_metrics.py hibernate-5.1
./envrun.sh python src/collect/defect_mining.py hibernate-5.1
./envrun.sh python src/collect/traditional_metrics.py hibernate-5.1      # Understand if licensed, else fallback
./envrun.sh python src/collect/run_analyzers.py hibernate-5.1            # JTratch on Java 8 (~35 min, 6 GB heap)
./envrun.sh python -W ignore src/collect/build_dataset.py hibernate-5.1  # authors' 5 input CSVs
# pipeline validation on the paper's own release:
./envrun.sh python src/collect/clone_repo.py hibernate-5.0-validation
./envrun.sh python src/collect/run_analyzers.py hibernate-5.0-validation
./envrun.sh python -W ignore src/collect/validate_against_original.py
```

Status: **runs end to end on Hibernate ORM 5.1.0** (3,475 files; 284 post-release-defective; 467 with catch
blocks). JTratch builds from source at the paper's tag and runs on OpenJDK 8; on Java 24 it cannot run (JAXB).

### Validation and rule choices (aggregation re-implementation)

`validate_against_original.py` compares our file-level EH metrics for Hibernate 5.0.0.Final with the authors'
released values: 57/107 metrics identical on ≥ 95% of files (catch-level mean exact-match 0.96, throws 0.99,
try/flow 0.84). Where the rule sheet left a choice open, these variants were scored (exact-match rate of the
per-file count) and the best one adopted:

| Rule | Variants tried (exact-match) | Adopted |
|---|---|---|
| Catch/Try LOC | end−start (0.00), +1 (0.00), −1 (0.00); theirs − (end−start+1) = +1.00 per block on all 459 files | end − start + 2 |
| Destructive Wrapping | new ∧ ¬wrap (0.40), new ∧ wrap (0.95), wrap (0.73), new (0.79) | new exception wrapping the caught one |
| Log and Throw | log ∧ thrown (0.93), log ∧ rethrow-same (0.96), log ∧ new (0.97), log ∧ thrown ∧ ¬wrap (0.99) | log ∧ thrown ∧ ¬wrap |
| Overcatch | subsumption > 1 (0.77), > 0 (0.92), others ≤ 0.80 | subsumption > 0 |
| Recoverability | R={Runtime,checked} (0.63/0.63/0.88), R={checked}, U={Runtime,Error} (0.94/0.94/0.88) | recoverable = checked; unrecoverable = Runtime ∪ Error |
| Generic Catch | {Exception, Throwable} (0.97), + RuntimeException (1.00), + Error (0.97) | + RuntimeException |
| Catch and Return null | ret-null ∧ ¬log (0.97), ret-null (0.98) | ret-null |
| Nested try block | parent ∈ {try, catch} ∨ inner (0.97), inner (0.85), parent = try (1.00) | parent = try |
| Exception-type prevalence scope | all analysed files incl. tests (mean 172.8 vs 138.6), release files (122.4, ρ = 0.91) | release files |

Remaining gap: possible-exception detection, ~25% fewer per try, from the unpublished external-Javadoc XML and
missing dependency jars (DATA.md §3). Flow metrics on new releases are therefore *systematically lower* than the
authors' tool would produce. Rankings are fairly well preserved: Spearman ρ ≥ 0.63 for all 52 Try_Based metrics
with a defined ρ (median exact-match 0.94).

## 5. Phase 2: statistical replication on new data (in progress)

```bash
./envrun.sh Rscript src/reproduce/run_original.R fixed --input data/new/hibernate-5.1/input --out results/new/hibernate-5.1
./envrun.sh python src/reproduce/build_comparison.py     # adds the "New context" section + results/new_context_comparison.csv
```

The authors' code runs unchanged (plus D1, D2) on our newly collected Hibernate 5.1.0 data. Results
(optimism-reduced Nagelkerke R², simplified models; n = 404 files with catch blocks and try data, budget 26):

| Model | Paper, Hibernate 5.0.0 | Ours, Hibernate 5.1.0 | Significant EH predictors (direction) |
|---|---:|---:|---|
| BASE | 0.21 | 0.238 | — |
| BSFC | 0.28 | 0.275 | `# Handled with Throw with New` (+, χ² 6.20), `% Propagated` (+, χ² 15.79) |
| BSAP | 0.23 | 0.264 | `Avg. AP Unhandled exceptions` (+, χ² 12.06) |

Same ordering as the paper (BSFC > BSAP > BASE). Comment density is significant in both releases
(`CountLineComment` +, `RatioCommentToCode` −). **This is an extension, not a faithful replication**: BASE uses 12
fallback product metrics instead of 39 Understand metrics (8 potential predictors after reduction vs. 18 in the
paper), and flow metrics come from JTratch under reduced binding resolution. Done: Hibernate 5.1.0 and ZooKeeper 3.6.0 (below). Not done: Hadoop 2.7, a C# context (see §6).

Apache ZooKeeper 3.6.0 → 3.6.4 (same commands; target `zookeeper-release-3.6.0` in `src/collect/targets.json`):
469 release files, 43 post-release bugs in 39 files, 171 files with catch blocks (31 defective), 161 with try data
(budget 10). Optimism-reduced R²: BASE 0.423, BSFC 0.041, BSAP 0.417; see finding F2 for why BSFC < BASE.


### Two findings from the new contexts

**F1: JTratch is not run-to-run deterministic.** Four JTratch runs on identical ZooKeeper 3.6.0 sources: catch-level
output (and therefore every catch/anti-pattern metric) was identical every time, but the possible-exception
traversal differed. Two runs were identical; the other two changed 6 flow metrics (`Avg Depth`, `Avg Max Depth`,
`Avg # Declaring Methods`, `% Doc in Comment`, `% Method Declaration`, `% Throw Statement`) in 72 and 76 of
161 files. Refitting the authors' models on each run: BASE and BSAP were identical (R² 0.423 / 0.417, same
predictors). BSFC was R² 0.041 in three runs and **0.108** in one, with a different predictor set (`Avg Depth`
entered). Likely cause: the inter-procedural search records depth/sources on first visit, in hash-map order.
Consequences: (i) the pipeline keeps one analyzer run per release commit as a fixed artifact and reuses it;
(ii) findings that rest on these metrics are flagged; (iii) **RQ1 (flow) results on new data are conditional on
the analyzer run, RQ2 (anti-pattern) results are not**. The authors' released metrics come from a single run, so
the same caveat may apply to the original flow metrics. TODO T10: report BSFC over ≥ 10 JTratch runs per target.

**F2: BASE-significant metrics are not actually forced into BSFC/BSAP.** The paper (§3.4.6) says they are kept.
The released `dataApplyReductionByModel()` re-adds them, but its second budget-based reduction can drop them again,
and it only logs `Significant ------ STILL ------ missing` and continues. This never happens on the paper's data or on
Hibernate 5.1 (0 occurrences in those logs), so Phase 0/2 are unaffected. It does happen on small targets: ZooKeeper
has budget 10 (161 files / 15), BSFC's cutoff drops to 0.24 and loses `# Bugs (pre)`, hence BSFC R² 0.041 < BASE
0.423. We keep the authors' behaviour for faithfulness, and report it next to every affected model so the comparison is not misread.

## 6. Remaining work, open issues and known failures

| # | Item | Status / plan | Consequence if not done |
|---|---|---|---|
| T1 | Regenerate the external-Javadoc XML (JTratch `MyRoot` schema) from `@throws` tags of JDK 8 and dependency sources | Not started | Flow metrics stay ~25% under-counted (§4) |
| T2 | Resolve dependency jars (Gradle/Maven) and pass them to JTratch (`--m2`) | Not started | Same as T1 |
| T3 | Manual validation of the 40 defect links per target, two raters | Sample generated (`data/new/*/manual_validation_sample.csv`), not yet rated | Label precision unknown |
| T4 | Hadoop 2.7.0 → 2.7.7 (configured) | Not started | One fewer Java context |
| T5 | C# context: NTratch (2017 .NET binary) and a defect source for Umbraco (its YouTrack tracker is decommissioned) | Blocked | RQ1/RQ2 on new data stay Java-only |
| T6 | SciTools Understand licence for a faithful BASE on new data | Requested; fallback in use | New-context BASE is an extension |
| T7 | Report the BSFC bug (D1) to the authors | To do | — |
| T8 | Quantify JTratch run-to-run variance (F1) over ≥ 10 runs per target | Measured once (4 runs, ZooKeeper) | BSFC on new data conditional on one run |
| T9 | RQ3 (ML prediction) and RQ4 (SHAP) | In progress; reported in the next milestone | — |
| T10 | Automated pipeline front end (proposal Phase 5) | In progress; next milestone | — |
