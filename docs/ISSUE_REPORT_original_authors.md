# Issue report for the MSR 2018 replication package (draft to send)

**To:** G. B. de Pádua and W. Shang (replication package: https://guipadua.github.io/eh-model-defects2018/)
**From:** Group 8 (Dev Patel, Priyanka Gupta, Dhruv Patel, Slesha Vora, Pulkit Chopra), Software Maintenance and Evolution
**Subject:** Replication of "Studying the relationship between exception handling practices and post-release defects" (MSR 2018): three issues in the released R scripts

Dear authors,

We replicated your MSR 2018 study from the released package (`eh-model-defects2018_scripts_with_input_data.zip`,
SHA-256 `2d6387a9…7eaa`). With one change, all nine optimism-reduced R² values of Table 4 reproduce within ±0.004
and all 35 entries of Table 5 to rounding, so the published results are correct. While doing so we found three issues
in the released code that affect anyone reusing it. Each comes with a minimal fix and evidence; our repository has
the full logs: https://github.com/DevPatel1704/exception-handling-defects-replication (tag `final-submission`,
`docs/REPRODUCTION.md` §3 and §9).

1. **The BSFC model is built from the anti-pattern data.** In `construction_functions.R`,
   `dataApplyReductionByModel()` begins with `data_list = all_list_omitted_m2`, which overwrites its argument. The
   BSFC call therefore receives BSAP's data: as released, "BSFC" has the same formula, predictors and apparent R²
   as BSAP (also visible in `output/base_test_2_BKP.csv` and the knitted HTML). Removing that one line reproduces the
   paper's BSFC values (0.09 / 0.37 / 0.28) and Table 5 rows HA-8–HA-12 and HB-6–HB-8 exactly.

2. **The "keep BASE-significant metrics" rule of §3.4.6 is disabled.** The branch that re-adds BASE-significant
   metrics in `dataApplyReductionByModel()` is guarded by `if(project=="" && model_type=="")`, which is never true;
   the code only prints `Significant ------ STILL ------ missing`. This never matters on the paper's data, but on
   smaller releases the budget-based reduction drops the strongest BASE predictor (on Apache ZooKeeper 3.6.0, BSFC
   R² 0.041 vs. BASE 0.423). Enabling the branch while reserving the predictors' degrees of freedom gives 0.458.

3. **`modelSimplification()` halts when no predictor survives.** In `analysis_functions.R`, if `fastbw()` keeps no
   variable, `refit` is never assigned and R stops with `object 'refit' not found` (we hit this on ZooKeeper
   3.7.0). Initialising `refit`, `final_form` and `coef` to `NA` before the `names.kept` test records an empty model
   instead; it changes no result on your data.

We also observed that JTratch (commit af7c232) is not run-to-run deterministic for six flow metrics (e.g.
`Avg Depth`), while all catch/anti-pattern metrics are stable; details are in §9.4 of our reproduction log.

Thank you for publishing the package, which made this replication possible.

Kind regards,
Group 8
