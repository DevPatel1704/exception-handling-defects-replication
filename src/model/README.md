# src/model

BASE / BSFC / BSAP models on new data are built with the **authors' own R code**, not a re-implementation, so
the method is identical to Phase 0:

```bash
./envrun.sh Rscript src/reproduce/run_original.R fixed --input data/new/<target>/input --out results/new/<target>
./envrun.sh python src/reproduce/build_comparison.py   # adds the "New context" section
```

`src/collect/build_dataset.py` writes the new data in the authors' five input formats
(`File_Level-{Git-Jira,Understand,Catch_Based,Try_Based,Throws_Based}.csv`, same columns and order), which is
what makes this possible. A Python port of the modeling steps is intentionally not provided.
