"""Shared data loading and feature-group definitions for Phase A (RQ3/RQ4).

Feature groups follow the authors' own data-source split (0-DataSourcesAnalysis.Rmd):
  TRAD   = Git/Jira process metrics + Understand product metrics   (authors' `base_names`)
  FLOW   = try-block / exception-flow metrics                       (authors' `try_names`)   -> BSFC
  AP     = catch-block / anti-pattern metrics                       (authors' `catch_names`) -> BSAP
Throws metrics are excluded, as in the paper's presented models.

Column names are the R-mangled names used in the released CSV. In the try group, a trailing ".1"
marks the percentage variant ("% Handled with Log" -> X..Handled.with.Log.1), while the name without
the suffix is the count ("# Handled with Log" -> X..Handled.with.Log).
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "original" / "all_no_missing.csv"
GROUPS = ROOT / "results" / "reproduce" / "asis" / "metric_groups.csv"
OUTCOME = "Distinct.count.of.Issue.Key.POST"
ID_COLS = ["File.Path", "Project", "File", "Kind", "Name", "Table.Name", "Language"]
NON_FEATURES = set(ID_COLS) | {OUTCOME, "Number.of.Records", "X..Bugs.Post"}
PROJECTS = ["umbraco-7.6", "hadoop-2.6", "hibernate-5.0"]
SEED = 2018


def metric_groups() -> dict:
    g = pd.read_csv(GROUPS)
    return {k: [m for m in g.loc[g.group == k, "metric"] if m not in NON_FEATURES]
            for k in ("base", "catch", "try", "throws")}


def feature_sets() -> dict:
    g = metric_groups()
    return {
        "TRAD": g["base"],
        "TRAD+FLOW": g["base"] + g["try"],
        "TRAD+AP": g["base"] + g["catch"],
        "TRAD+EH": g["base"] + g["try"] + g["catch"],
    }


def load_project(project: str, catch_only: bool = True) -> pd.DataFrame:
    """Files of one project; by default only files with >=1 catch block (the paper's presented setting)."""
    d = pd.read_csv(DATA)
    d = d[d["Project"] == project]
    if catch_only:
        d = d[d["X..Catch"] > 0]
    return d.reset_index(drop=True)


def xy(d: pd.DataFrame, cols: list) -> tuple:
    X = d[cols].astype(float)
    X = X.loc[:, X.var() > 0]          # drop constants (e.g. Java-only Understand metrics in C#, = -1)
    y = (d[OUTCOME] > 0).astype(int).to_numpy()
    return X, y


def _r_make_names(names: list) -> list:
    """R's make.names(unique=TRUE) as applied by read.csv: prefix X if the first char is invalid, map invalid
    chars to '.', then de-duplicate with .1, .2, ..."""
    import re
    out, seen = [], {}
    for n in names:
        m = ("X" + n) if not (n[:1].isalpha() or n[:1] == ".") else n
        m = re.sub(r"[^A-Za-z0-9._]", ".", m)
        if m in seen:
            seen[m] += 1
            m = f"{m}.{seen[m]}"
        else:
            seen[m] = 0
        out.append(m)
    return out


SHORT = {"Distinct count of Author Email PRE": "# Authors (pre)", "Distinct count of Commit Hash PRE": "# Changes (pre)",
         "Distinct count of Issue Key PRE": "# Bugs (pre)", "Churn PRE": "Churn (pre)"}


def pretty_names() -> dict:
    """R-mangled column name -> the authors' original metric name (from the released input CSV headers)."""
    inp = ROOT / "external" / "scripts_with_input_data" / "input"
    mapping = {}
    for f in sorted(inp.glob("File_Level-*.csv")):
        raw = list(pd.read_csv(f, nrows=0).columns)
        mapping.update({m: SHORT.get(r, r) for m, r in zip(_r_make_names(raw), raw)})
    return mapping


def log_transform(X: pd.DataFrame) -> pd.DataFrame:
    """log10(x+1) as in the paper (MC3); the -1 'not applicable' sentinel is mapped to 0 first."""
    return np.log10(X.clip(lower=0) + 1)
