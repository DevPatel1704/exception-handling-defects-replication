# Reproduction log

What we ran, with which commands, what came out, and every deviation from the original study.
Paper: G. B. de Pádua and W. Shang, *Studying the Relationship between Exception Handling Practices and
Post-release Defects*, MSR 2018, doi:10.1145/3196398.3196435.

Status (2026-11-08, Milestone 3): **Phase 0 complete** (Table 4 and Table 5 reproduced). Phase A (ML + SHAP)
complete, now with Holm correction. Phases 1–2 complete on four new releases (Hibernate 5.1.0, ZooKeeper 3.6.0 / 3.7.0 /
3.9.0), with the analyzer-variance check (T10) and the forced-BASE sensitivity (S1). Milestone 3 additions: §9.

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
| **D7** | **Empty-model guard (both modes, Milestone 3).** In `analysis_functions.R` `modelSimplification()`, when `fastbw()` keeps no predictor, `refit` is never assigned and R halts (`object 'refit' not found`). We initialise `refit`/`final_form`/`coef` to `NA` just before the `names.kept` test. | Hit on ZooKeeper 3.7.0 (18 defective files): no BSFC predictor survives backward elimination. | None on any earlier run. **Verified:** with D7, Phase 0 (`base_test_1/2.csv`, `predictors_simplified.csv`) and Hibernate 5.1 / ZooKeeper 3.6.0 / 3.9.0 reproduce identically (max ΔR² = 0; runs in `build/verify_d7/`). Such a model is reported as "no predictor survives simplification" (R² n/a). |
| S1 | **Sensitivity only, not part of the replication (`--force-sig`).** Enables the paper's §3.4.6 rule "BASE-significant metrics are kept in BSFC/BSAP": the released code's branch for it is guarded by a never-true condition (`project=="" && model_type==""`). One budget slot is reserved per BASE-significant metric, the other metrics are reduced by the authors' own dynamic-cutoff rule to the remaining budget, then the BASE-significant metrics are added. Output: `results/new/<id>/fixed_forcesig/`. | ZooKeeper's BSFC/BSAP fall *below* BASE because the second reduction drops `# Bugs (pre)` (F2, §8). S1 tests whether that, and not the EH metrics, explains it. | Reported separately (§9). Identical to the main run whenever no BASE predictor is dropped (Hibernate 5.1: all three models identical). |

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

## 4. Phase A: ML prediction (RQ3) and SHAP (RQ4) on the released dataset

### Commands

```bash
./envrun.sh python -W ignore src/ml/train_eval.py          # -> results/ml_results.{csv,md}, ml_uplift.csv, ml_folds.csv (~30 min here)
./envrun.sh python -W ignore src/explain/shap_analysis.py  # -> results/shap_*.{png,csv,md}
./envrun.sh jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=3600 \
    notebooks/phaseA_ml_shap.ipynb                         # runs both and displays the results
```

### Protocol

* Data: the authors' released dataset, files with ≥ 1 catch block (the paper's presented setting): Umbraco 230
  files (9.6% defective), Hadoop 890 (16.1%), Hibernate 440 (21.1%). Label = `Distinct.count.of.Issue.Key.POST > 0`.
* Feature sets, from the authors' own data-source groups: TRAD (Git/Jira + Understand; 35–44 non-constant
  features), TRAD+FLOW (+ try/flow metrics), TRAD+AP (+ catch/anti-pattern metrics), TRAD+EH (+ both). Throws
  metrics excluded, as in the paper's presented models. Constant columns dropped per project.
* Learners, fixed and **untuned** (so the comparison is between feature sets, not tuning effort): LR (log10(x+1) as in
  the paper, standardised, L2, class-balanced); RF (500 trees, min_samples_leaf=2, balanced_subsample); XGBoost
  (300 trees, depth 4, lr 0.05, subsample/colsample 0.8, scale_pos_weight = neg/pos). Seed 2018.
* Evaluation: repeated stratified 5-fold CV × 10 repeats (50 folds; identical splits for every feature set and
  learner). PR-AUC (average precision) is the primary metric, with ROC-AUC and F1 (threshold 0.5); mean ± std over
  folds. Uplift over TRAD is tested with the Nadeau–Bengio corrected resampled t-test (paired by fold).
* SHAP: TreeSHAP on the best tree learner per project (by TRAD+EH CV PR-AUC; RF for all three), refit on all
  files. RF SHAP values are in **probability** units. Agreement with Phase 0 counts a top-10 EH feature as
  matching if it *is*, or is correlated |ρ| > 0.7 with, an EH predictor significant in the simplified BSFC/BSAP
  models of the bug-fixed run.

### RQ3 results: mean PR-AUC over 50 folds (`results/ml_results.md` has ± std, ROC-AUC, F1)

| Project (prevalence) | Learner | TRAD | TRAD+FLOW | TRAD+AP | TRAD+EH |
|---|---|---:|---:|---:|---:|
| Umbraco (0.096) | LR | 0.221 | 0.332 | 0.281 | 0.314 |
| | RF | 0.350 | 0.400 | 0.361 | 0.395 |
| | XGB | 0.303 | 0.368 | 0.310 | 0.364 |
| Hadoop (0.161) | LR | 0.552 | 0.526 | 0.486 | 0.468 |
| | RF | 0.597 | 0.595 | 0.603 | 0.597 |
| | XGB | 0.582 | 0.590 | 0.586 | 0.585 |
| Hibernate (0.211) | LR | 0.460 | 0.433 | 0.435 | 0.411 |
| | RF | 0.506 | 0.548 | 0.538 | 0.555 |
| | XGB | 0.489 | 0.547 | 0.498 | 0.544 |

Plainly (Holm-adjusted p-values added in Milestone 3, `p_holm` in `results/ml_uplift.csv`; family = the 9
comparisons of one project and metric):
* **PR-AUC (primary): no learner on any project improves significantly** when EH metrics are added (all corrected
  p ≥ 0.091 before, p_Holm ≥ 0.82 for every positive uplift after correction). Tree models gain somewhat on Hibernate (RF +0.049 PR-AUC with
  TRAD+EH, better in 43/50 folds, p = 0.091). On Umbraco, trees gain +0.007 to +0.065 and LR +0.060 to +0.111, but
  std ≈ 0.10–0.14 with only 4–5 positives per test fold. Hadoop: within ±0.01 for trees.
* **ROC-AUC:** Umbraco tree models improve (RF +0.122 FLOW / +0.133 EH; XGB +0.090 to +0.112; raw p = 0.019–0.041;
  43–45/50 folds), and Hadoop RF+AP marginally (+0.010, raw p = 0.047). **None of these survives Holm**
  (p_Holm ≥ 0.17).
* **Logistic regression gets worse** with EH metrics on Hadoop (PR-AUC −0.067 AP, −0.084 EH; raw p = 0.008, 0.014;
  p_Holm = 0.07, 0.11), plausibly because, unlike the paper's models, it gets 100+ highly correlated features with
  no correlation/redundancy filtering (only L2 shrinkage).
* **After Holm correction, 0 of 81 uplift tests (27 per metric) are significant** in either direction. We therefore
  report "no detectable predictive gain from EH metrics", with the direction of the point estimates (positive on
  Umbraco/Hibernate trees, negative for LR on Hadoop) as descriptive only. The summaries were regenerated from the
  saved folds (`python src/ml/train_eval.py --from-folds`; `ml_results.csv` byte-identical).

### RQ4 results (`results/shap_alignment.md`, figures `results/shap_bar_all.png`, `results/shap_beeswarm_*.png`)

* Traditional metrics dominate every ranking: pre-release churn, authors and changes are top in Hadoop and
  Hibernate; blank lines and statement counts in Umbraco.
* Highest-ranked EH features: Umbraco `% Subsumption` (#3 overall), Hibernate `Avg Exc Type Prevalence` (#3),
  Hadoop `% Handled with Log` (#12).
* Agreement with Phase 0 (top-10 EH features matching a significant BSFC/BSAP predictor, exactly or via a
  |ρ| > 0.7 proxy): **Hadoop 6/10, Hibernate 3/10, Umbraco 2/10**. For every matched feature the SHAP direction
  agrees with the sign of the Phase 0 coefficient (e.g. Hibernate type prevalence −, throw-wrap −, invoked-methods
  +; Hadoop % log +, % specific +; Umbraco dummy handler +, generic catch +). Some Phase 0 predictors rank low
  under SHAP (Hadoop `AP Log and Throw` #134, `# Try in Other` #140; Hibernate `Sum of AP Dummy Handler` #84):
  significant in a parsimonious logistic model is not the same as important to a forest over 124–146 features.

## 5. Phase 1: new-release data pipeline

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

## 6. Phase 2: statistical replication on new data (partial)

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
paper), and flow metrics come from JTratch under reduced binding resolution. Done: Hibernate 5.1. Not done:
Hadoop 2.7, a C# context (see §7).

## 7. Open TODOs and known failures

| # | Item | Status / plan |
|---|---|---|
| T1 | Regenerate the external-Javadoc XML (`MyRoot` / `MyPackage` / `MyClass` / `MyMethod` / `MyThrowTag`, see `external/JTratch/src/main/java/ca/concordia/jpexjd/`) from `@throws` tags of JDK 8 sources and the target's dependencies | **Dropped in Milestone 3** (§9.6); documented limitation |
| T2 | Give JTratch dependency jars (`--m2`): resolve Hibernate 5.1's Gradle deps (Java 8), point `--m2` at the jar cache | **Dropped in Milestone 3** (§9.6) |
| T3 | Manual validation of the 40 defect links (`data/new/hibernate-5.1/manual_validation_sample.csv`), two raters | Milestone 3: packets + independent sheets for all 131 links of the 4 new contexts, agreement script tested (§9, VALIDATION_GUIDE.md); **ratings pending** |
| T4 | Hadoop 2.7.0 → 2.7.7 (target configured; large repo, 4 Jira projects; JTratch needs ≥ 6 GB heap) | **Dropped in Milestone 3** (§9.6) |
| T5 | C# context: NTratch.exe (2017 .NET binary) on Umbraco 7.7; Umbraco 7's YouTrack tracker is decommissioned, so defect labels need another source (GitHub issues/PR links) | **Dropped in Milestone 3** (§9.6): no defect labels |
| T6 | Understand licence (academic) for a faithful BASE on new data | Ask instructor/department |
| T7 | Report the BSFC bug (D1) to the authors | To do |
| T8 | Multiple-comparison correction (Holm) for the RQ3 uplift tests; optionally nested-CV tuning | **Done** (Holm; §9.2). Nested-CV tuning not done (learners deliberately untuned) |
| T10 | Quantify JTratch run-to-run variance (F1, §8): ≥ 10 analyzer runs per target, report BSFC R² and predictor stability | **Done** for ZooKeeper 3.6/3.7/3.9 (10 runs each, §9.4); Hibernate 5.1 running |
| T9 | Dashboard (Phase 5) | **Working** for Java repositories (§8); C# limited to metrics without EH analysis (T5) |

Known failures encountered and resolved are listed under §3 (Phase 0). In Phase 1: our first JTratch attempt on
Java 24 is not viable (JAXB); `conda run` races when parallel (→ `envrun.sh`); our first defect-mining run ignored
Jira's timezone offset (fixed; counts unchanged).

## 8. Phase 5: dashboard (repository link in, results out)

`./envrun.sh python dashboard/app.py`, then open <http://localhost:8000/>. Paste a repository URL; the page lists
its tags (`git ls-remote`), pre-selects release / post-release / previous-release tags, and suggests the issue
tracker. One click then runs the whole pipeline as a background job (`src/pipeline/run_target.py`: the same scripts
as §5–§6 plus ML and SHAP on the new data) and renders `results/new/<target>/summary.json`. Details, limits and
API: [dashboard/README.md](../dashboard/README.md).

Additions made for it, kept backwards-compatible with Phases 0–2:

| Change | Why | Effect on earlier results |
|---|---|---|
| Issue-tracker abstraction (`history.py`): Jira with automatic Cloud/Server API detection and key-prefix detection; **GitHub Issues** (closed issues/PRs with a bug-like label) | Arbitrary repositories; many Java projects track bugs on GitHub | None for Jira targets. GitHub-tracked targets deviate from the paper's definition, and their summary says so |
| `data/targets.local.json` for dashboard-registered targets; owner-qualified clone directories | Don't modify the curated `targets.json`; avoid clashes between same-named repositories | None |
| `--data/--groups/--projects/--out` options for `train_eval.py` and `shap_analysis.py` | Run RQ3/RQ4 on any target | Defaults unchanged: Phase A CSV/MD outputs byte-identical after the refactor |
| Deterministic defect-link order (sorted iteration over issue keys) | Python's per-process string hashing changed row order between runs, and with it the 40-link manual sample | Same 489 links and labels; the (still unfilled) manual sample was regenerated once |
| Seeded SHAP beeswarm jitter | Figures were not byte-reproducible | Cosmetic: point jitter in 3 PNGs |
| Content-hash reuse of steps (`stamps.json`) | Re-runs skip JTratch / R / ML when inputs are unchanged | None |

Verification: offline unit tests for tag parsing, suggestions and URL validation
(`./envrun.sh python -m unittest discover -s tests -v`, 7 tests); a headless browser test (jsdom) of the page
against the live server (no JS errors; form, job view, results and original-study tab render); and end-to-end
jobs listed below.

### End-to-end dashboard jobs (2026-10-24)

| Job | Target | Steps | Result |
|---|---|---|---|
| 1 | Hibernate ORM 5.1.0 → 5.1.17 (form maps onto the curated `hibernate-5.1`) | 11/11 done; JTratch reused; ~7 min | BASE 0.238, BSFC 0.275, BSAP 0.264, identical to §6; best PR-AUC 0.639 (RF, TRAD+EH; prevalence 0.213) |
| 2 | Apache ZooKeeper release-3.6.0 → release-3.6.4, fresh clone; Jira keys auto-detected | 11/11 done; ~6 min | 469 files, 43 post-release bugs in 39 files; 161 files with catch + try data (31 defective); BASE 0.423, BSAP 0.417, BSFC 0.041 (see below) |
| 3 | ZooKeeper again, unchanged inputs (CLI runner) | analyzer, models, ML and SHAP reused; ~20 s | identical |

### Two findings from running new targets

**F1: JTratch is not run-to-run deterministic.** Four JTratch runs on identical ZooKeeper 3.6.0 sources: catch-level
output (and therefore every catch/anti-pattern metric) was identical every time, but the possible-exception
traversal differed. Two runs were identical; the other two changed 6 flow metrics (`Avg Depth`, `Avg Max Depth`,
`Avg # Declaring Methods`, `% Doc in Comment`, `% Method Declaration`, `% Throw Statement`) in 72 and 76 of
161 files. Refitting the authors' models on each run: BASE and BSAP were identical (R² 0.423 / 0.417, same
predictors). BSFC was R² 0.041 in three runs and **0.108** in one, with a different predictor set (`Avg Depth`
entered). Likely cause: the inter-procedural search records depth/sources on first visit, in hash-map order.
Consequences: (i) the pipeline keeps one analyzer run per release commit as a fixed artifact and reuses it;
(ii) result pages flag findings that rest on these metrics; (iii) **RQ1 (flow) results on new data are conditional on
the analyzer run, RQ2 (anti-pattern) results are not**. The authors' released metrics come from a single run, so
the same caveat may apply to the original flow metrics. TODO T10: report BSFC over ≥ 10 JTratch runs per target.

**F2: BASE-significant metrics are not actually forced into BSFC/BSAP.** The paper (§3.4.6) says they are kept.
The released `dataApplyReductionByModel()` re-adds them, but its second budget-based reduction can drop them again,
and it only logs `Significant ------ STILL ------ missing` and continues. This never happens on the paper's data or on
Hibernate 5.1 (0 occurrences in those logs), so Phase 0/2 are unaffected. It does happen on small targets: ZooKeeper
has budget 10 (161 files / 15), BSFC's cutoff drops to 0.24 and loses `# Bugs (pre)`, hence BSFC R² 0.041 < BASE
0.423. We keep the authors' behaviour for faithfulness, and the dashboard flags it ("⚠ dropped BASE predictor" plus a
caveat) so the comparison is not misread.

## 9. Milestone 3 additions (2026-11-08)

All numbers below are produced by the commands listed; the cross-context view is `results/contexts_summary.{csv,md}`
and `results/figures/` (regenerate with `./envrun.sh python src/reproduce/context_summary.py`).

### Commands

```bash
# Fourth new context (pipeline as in §5-§6 and §8, ML with 10 repeats)
./envrun.sh python src/pipeline/run_target.py zookeeper-release-3.7.0 --repeats 10
# RQ3/RQ4 on the new contexts with the same 5x10 CV as Phase A (was 5x5 in Milestone 2)
for t in hibernate-5.1 zookeeper-release-3.6.0 zookeeper-release-3.9.0; do ./envrun.sh python src/pipeline/run_target.py $t --repeats 10; done
# Holm correction (T8): re-summarise the saved folds, no retraining
./envrun.sh python src/ml/train_eval.py --from-folds
# Analyzer run-to-run variance (T10): 10 fresh JTratch runs per release, models refit on each
for t in zookeeper-release-3.6.0 zookeeper-release-3.7.0 zookeeper-release-3.9.0; do ./envrun.sh python -W ignore src/collect/analyzer_variance.py $t --runs 10; done
# Sensitivity S1 (paper §3.4.6 rule: keep BASE-significant metrics; see deviations table)
for t in hibernate-5.1 zookeeper-release-3.6.0 zookeeper-release-3.7.0 zookeeper-release-3.9.0; do
  ./envrun.sh Rscript src/reproduce/run_original.R fixed --force-sig --input data/new/$t/input --out results/new/$t; done
# Defect-link validation (T3): packets + sheets, then agreement once both raters are done
./envrun.sh python src/collect/validation_packet.py
./envrun.sh python src/collect/validation_agreement.py
# Cross-context tables and figures
./envrun.sh python src/reproduce/build_comparison.py && ./envrun.sh python src/reproduce/context_summary.py
```

### 9.1 New context: ZooKeeper 3.7.0, and a third defect in the released model code (D7)

ZooKeeper 3.7.0 (487 release files; 16 post-release bugs; 181 files with catch blocks, 18 defective; 169 modelled,
budget 11) halted inside the authors' `modelSimplification()`: backward elimination kept no BSFC predictor and
`refit` was never assigned. Guard D7 records such a model as empty. Results: BASE 0.417, BSAP 0.047, BSFC empty.

### 9.2 RQ3 with Holm correction, on all seven contexts

0 of 81 uplift tests on the authors' data and 1 of 108 on the new contexts are significant after Holm (per project
and metric, 9 tests). The one survivor is a **loss**: LR with TRAD+EH on ZooKeeper 3.9.0, ROC-AUC −0.173, worse
in 0/50 folds improved (p_Holm = 0.010). Point estimates for tree learners are mostly positive (PR-AUC: 34 of 42
tree comparisons > 0 across contexts, 12 of 14 for TRAD+EH; largest Hibernate 5.1 RF +0.091, raw p = 0.017,
p_Holm = 0.156); for LR, 16 of 21 PR-AUC differences are negative. Conclusion: **no detectable predictive gain from EH metrics in any context**; adding ~100
correlated EH features tends to hurt the linear learner. Per-context CIs: `results/ml_uplift_ci.csv`,
`results/figures/fig_ml_uplift.*`.

### 9.3 RQ4 on the new contexts

Top-10 EH SHAP features matching a significant BSFC/BSAP predictor: Hibernate 5.1 5/10, ZooKeeper 3.9.0 5/10,
ZooKeeper 3.7.0 1/10, ZooKeeper 3.6.0 0/10 (original: Hadoop 6/10, Hibernate 5.0 3/10, Umbraco 2/10).

### 9.4 Analyzer run-to-run variance (T10, the main validity check for RQ1 on new data)

10 fresh JTratch runs per ZooKeeper release (`results/new/<id>/variance/`):

* **Which metrics move:** the same 6 of 107 file-level metrics in every release, all flow (Try_Based):
  `Avg Depth` (68–71 files), `% Doc in Comment`, `Avg Max Depth`, `% Throw Statement`, `Avg # Declaring Methods`,
  `% Method Declaration`. **All 45 catch/anti-pattern and all 5 throws metrics are identical in every run.**
* **Effect on models:** BASE and BSAP identical in all 30 runs (as expected: they do not use flow metrics).
  BSFC identical in all runs for ZooKeeper 3.7.0 (empty) and 3.9.0 (0.092), but **unstable for ZooKeeper 3.6.0:
  0.041 in 6 runs, 0.108 in 2, 0.458 in 2** (3 distinct predictor sets). Mechanism: the perturbed flow metrics
  change the correlation structure, so the authors' budget-based reduction stops at a different cutoff (0.24 vs.
  0.30). At 0.30, `# Bugs (pre)` survives and BSFC becomes 0.458; at 0.24 it is dropped (F2).
* **Conclusion:** RQ2 (anti-patterns) results on new data do not depend on the analyzer run; RQ1 (flow) results
  can, on small releases, through the model-construction step rather than through large metric changes.

### 9.5 Sensitivity S1: was ZooKeeper's "EH models below BASE" an artefact? (F2)

| Context | BASE | BSFC (as released → S1) | BSAP (as released → S1) |
|---|---:|---|---|
| Hibernate 5.1 (control: nothing dropped) | 0.238 | 0.275 → 0.275 | 0.264 → 0.264 |
| ZooKeeper 3.6.0 | 0.423 | 0.041 → 0.458 | 0.417 → 0.417 |
| ZooKeeper 3.7.0 | 0.417 | empty → 0.413 | 0.047 → 0.413 |
| ZooKeeper 3.9.0 | 0.233 | 0.093 → 0.250 | 0.157 → 0.231 |

Yes. With the paper's stated rule, EH models on ZooKeeper are at or slightly above BASE (+0.035 BSFC on 3.6.0,
+0.017 on 3.9.0, none on 3.7.0); the only EH predictors still significant are `Avg Exc Type Prevalence` (3.6.0, −)
and `% Handled with Return` (3.9.0). The ZooKeeper 3.6.0 S1 value equals the analyzer-variance runs in which
`# Bugs (pre)` survived, so §9.4 and §9.5 describe the same mechanism.

### 9.6 Scope reductions and status of the Milestone 2 plan

| Milestone 2 plan item | Status | Reason |
|---|---|---|
| T10 BSFC over ≥ 10 analyzer runs | **Done** for the 3 ZooKeeper releases; Hibernate 5.1 (35 min per run) running in the background | — |
| T8 Holm correction | **Done** | — |
| RQ3/RQ4 on new data | **Done**, 4 releases, 5×10 CV | — |
| T3 manual validation (two raters) | Packets and sheets ready (131 links), agreement script tested; **ratings pending** | Needs the two raters |
| T1/T2 external Javadoc + dependency jars | **Dropped** (documented limitation) | Regenerating the authors' unpublished Javadoc DB is a project of its own; flow metrics rank-preserving (ρ ≥ 0.63) |
| T4 Hadoop 2.7 | **Dropped** | JTratch needs > 6 GB heap for Hadoop on a 7.4 GB machine; ZooKeeper 3.7.0 added instead |
| T5 C# context (Umbraco 7.7) | **Dropped** | Umbraco 7 YouTrack tracker decommissioned: no defect labels |
| T6 Understand licence | Not obtained | New-context BASE stays an extension (fallback metrics) |
