# Decision rules

This file records, before each check is run, the condition under which a conclusion changes. The commit that adds a
rule is the evidence that it predates the result.

## Rules recorded in commit `bed1a5f` (tag `milestone-4`), quoted from the Milestone 4 report as committed

* **R1** (recorded after Hibernate analyzer run 1, before runs 2–3): "If any further Hibernate analyzer run changes
  BSFC R² by more than 0.02 or removes % Propagated from the model, the Hibernate RQ1 result is reported as
  analyzer-dependent."
* **R3** (recorded before E1): "If RQ3 on strict labels (E1) yields any Holm-significant PR-AUC gain, the null result
  for RQ3 is revised for that context."
* **R4** (recorded before E4): "If the clean-machine rerun (E4) changes any reported number beyond bootstrap noise
  (±0.005 R²), that result is flagged as not reproducible until resolved."
* R2 (strict labels reverse the Hibernate ordering) and R5 (S1 and the released code disagree on the sign of an EH
  effect) were written in the same commit **after** the strict-label and S1 results were known. They are consistency
  checks, not prior rules.

## Rules for the remaining checks (recorded before either check is run)

* **R6, multi-seed RQ3 rerun.** Rerun all 108 strict-label RQ3 tests (4 releases × 3 learners × 3 extended feature
  sets × 3 metrics) with seeds 2019, 2020, 2021, 2022 and 2023, each with repeated stratified 5-fold CV × 10, Holm
  within each release and metric as before. Report the number of Holm-significant gains and losses per seed. The
  random-forest TRAD+AP gain on Hibernate 5.1 is kept only if it is Holm-significant in at least 4 of the 5 seeds;
  otherwise RQ3 reverts to a pure null. New seeds change only the fold splits, so this tests sensitivity to the
  splits, not new data.
* **R7, bootstrap interval for the Hibernate 5.1 R² increase.** Draw 1,000 bootstrap resamples of the 404 modelled
  Hibernate 5.1 files (seed 2018), refit BASE, BSFC and BSAP with their final simplified formulas on each resample,
  and compute the 95% percentile interval of R²(BSFC) − R²(BASE) and R²(BSAP) − R²(BASE). If an interval includes 0,
  the corresponding Hibernate result is downgraded from "Moderate" to "Weak".
* **R8, second-machine rerun of the final tag.** Clone the final tag on a second laptop, create the environment from
  `environment.yml`, run the unit tests and regenerate the models and tables from the committed inputs. Any number that
  changes by more than ±0.005 R² is flagged as not reproducible.
