"""Aggregate raw JTratch output (catch / possible-exception / throws rows) to the authors' FILE-level
metrics, using the column names of the authors' input CSVs (File_Level-Catch_Based.csv, -Try_Based.csv,
-Throws_Based.csv).

The authors aggregated in Tableau; the workbook was not released. This module re-implements the rules of
docs/aggregation_rules/metrics_and_aggregation_rules_MSR18.xlsx. Where the sheet leaves a choice open, the
choice is a named rule below and is checked empirically by validate_against_original.py, which runs this
module on Hibernate 5.0.0.Final (the paper's own release) and compares with the authors' released values.

Usage (library): from aggregate_jtratch import aggregate; catch, tri, throws = aggregate(raw_dir, src_root)
"""
from pathlib import Path

import numpy as np
import pandas as pd

# Rule choices below were selected by validate_against_original.py on Hibernate 5.0.0.Final (paper's release):
# each was the variant that matched the authors' released per-file values best (see docs/REPRODUCTION.md §9).
GENERIC_TYPES = {"java.lang.Exception", "java.lang.Throwable", "java.lang.RuntimeException"}
# The authors' "LOC" of a catch/try block is (end line - start line + 2): physical lines + 1 (matches 459/459
# files for Catch LOC). "SLOC" is JTratch's CatchLOC/TryLOC (statement lines of the block body).
LOC_OFFSET = 2
# Exception-type prevalence counted over release files only ("release") or all analysed files ("all").
PREVALENCE_SCOPE = "release"
# JDT ASTNode type ids (org.eclipse.jdt.core.dom.ASTNode, JLS8) -> the paper's "Try Scope" categories.
SCOPE = {}
for t in (31, 28, 55, 71, 81, 86):     # METHOD_DECLARATION, INITIALIZER, TYPE_DECLARATION, ENUM_DECL, ANNOTATION_TYPE_DECL, LAMBDA
    SCOPE[t] = "Declaration"
for t in (25, 50, 16, 49):             # IF, SWITCH, CONDITIONAL_EXPRESSION, SWITCH_CASE
    SCOPE[t] = "Conditional"
for t in (24, 70, 61, 19):             # FOR, ENHANCED_FOR, WHILE, DO
    SCOPE[t] = "Loop"
for t in (54, 12):                     # TRY_STATEMENT, CATCH_CLAUSE
    SCOPE[t] = "EH Feature"
SCOPES = ["Conditional", "Declaration", "EH Feature", "Loop", "Other"]
ACTIONS = ["Abort", "Continue", "Default", "Empty", "Log", "Method", "Nested Try", "Return",
           "Throw with New", "Throw without New", "Throw Wrap", "ToDo"]


def _read(raw: Path, suffix: str) -> pd.DataFrame:
    f = sorted(raw.glob(f"*_{suffix}.csv"))
    if not f:
        raise FileNotFoundError(f"no *_{suffix}.csv in {raw}")
    return pd.read_csv(f[0], dtype={"ExceptionType": str}, keep_default_na=False, na_values=[""])


def _rel(series: pd.Series, src_root: Path) -> pd.Series:
    root = str(src_root.resolve()).replace("\\", "/").rstrip("/") + "/"
    return series.str.replace("\\", "/", regex=False).map(lambda p: p[len(root):] if p.startswith(root) else p)


def catch_actions(c: pd.DataFrame) -> pd.DataFrame:
    """Per-catch handler actions (sheet 'Catch Level', Action rows)."""
    a = pd.DataFrame(index=c.index)
    a["Abort"] = c.Abort > 0
    a["Continue"] = c.Continue > 0
    a["Default"] = c.Default > 0
    a["Empty"] = c.EmptyBlock > 0
    a["Log"] = c.Logged > 0
    a["Method"] = c.OtherInvocation > 0
    a["Nested Try"] = c.RecoverFlag > 0
    a["Return"] = c.Return > 0
    a["Throw with New"] = c.NumThrowNew > 0
    a["Throw without New"] = (c.NumThrown - c.NumThrowNew) > 0
    a["Throw Wrap"] = c.NumThrowWrapCurrentException > 0
    a["ToDo"] = c.ToDo > 0
    return a


def catch_antipatterns(c: pd.DataFrame, meta: pd.DataFrame, uncaught_try: pd.Series) -> pd.DataFrame:
    """Per-catch binary anti-pattern flags (sheet 'Catch Level', Anti-pattern rows)."""
    act = catch_actions(c)
    ret_null = meta["Return"].fillna("").str.contains(r"return\s+null", regex=True)
    body = meta["CatchBlock"].fillna("")
    caught_here = (c.NumSpecificHandler + c.NumSubsumptionHandler)
    only_display = (act["Log"] | act["Default"]) & ~(act["Abort"] | act["Continue"] | act["Method"] | act["Nested Try"]
                                                     | act["Return"] | (c.NumThrown > 0))
    ap = pd.DataFrame(index=c.index)
    ap["Catch and do nothing"] = act["Empty"]
    ap["Catch and Return null"] = act["Return"] & ret_null
    # "propagates the exception as a new exception": a new exception that wraps the caught one
    ap["Destructive Wrapping"] = (c.NumThrowNew > 0) & (c.NumThrowWrapCurrentException > 0)
    ap["Dummy Handler"] = only_display
    ap["Generic Catch"] = c.ExceptionType.isin(GENERIC_TYPES)
    ap["Ignoring Interrupted Exception"] = (c.ExceptionType == "java.lang.InterruptedException") & (c.NumThrown == 0) \
        & ~body.str.contains(r"\binterrupt\s*\(", regex=True)
    ap["Incomplete implementation"] = act["ToDo"] & (act["Empty"] | only_display)
    ap["Log and Return null"] = act["Log"] & act["Return"] & ret_null
    ap["Log and Throw"] = act["Log"] & (c.NumThrown > 0) & (c.NumThrowWrapCurrentException == 0)
    ap["Multi-line log messages"] = c.MultiLog > 0
    ap["Nested try block"] = c.ParentNodeType == 54          # try statement directly inside another try
    ap["Overcatch"] = c.NumSubsumptionHandler > 0            # catches >=1 lower-level possible exception
    ap["Overcatch and Abort"] = ap["Overcatch"] & act["Abort"]
    ap["Relying on getCause()"] = c.GetCause > 0
    ap["Throw within finally"] = c.FinallyThrowing > 0
    ap["Unhandled exceptions"] = uncaught_try.reindex(c.index).fillna(False).astype(bool)
    ap["Unreachable Catch Handler"] = (c.Binded == 1) & (caught_here == 0)
    return ap


def recoverability(kind: pd.Series) -> pd.DataFrame:
    """JTratch Kind: 0 RuntimeException, 1 Exception (checked), 2 Error, 3 Throwable, -1/-9 unknown.
    Potentially recoverable = checked exceptions; potentially unrecoverable = RuntimeException or Error
    (JLS ch.11 view); otherwise (Throwable, unresolved) not relevant."""
    return pd.DataFrame({"Potentially Recoverable": kind == 1,
                         "Potentially UnRecoverable": kind.isin([0, 2]),
                         "Recoverability Not Relevant": ~kind.isin([0, 1, 2])})


def _type_prevalence(c: pd.DataFrame, pe: pd.DataFrame) -> pd.Series:
    """Number of distinct try blocks in which each possible-exception type occurs (sheet: 'Try ID Count')."""
    key2try = dict(zip(c.FilePath + "#" + c.StartLine.astype(str), c.FilePath + "#" + c.TryStartLine.astype(str)))
    tk = (pe.FilePath + "#" + pe.StartLine.astype(str)).map(key2try)
    return pd.DataFrame({"t": tk, "x": pe.ThrownType}).dropna().groupby("x")["t"].nunique()


def aggregate(raw: Path, src_root: Path, project: str, keep_files=None):
    c = _read(raw, "CatchBlock")
    m = _read(raw, "CatchBlock_Meta")
    pe = _read(raw, "PossibleExceptionsBlock")
    th = _read(raw, "ThrowsBlock")
    for d in (c, m, pe, th):
        d["FilePath"] = _rel(d["FilePath"], src_root)
    prevalence_all = _type_prevalence(c, pe)   # over ALL analysed files (incl. tests)
    if keep_files is not None:
        keep = set(keep_files)
        c, m, pe, th = (d[d.FilePath.isin(keep)].copy() for d in (c, m, pe, th))
    m = m.set_index("id").reindex(c["id"]).reset_index()
    m.index = c.index

    # ---- try identity and possible-exception (PE) level -----------------------------------------
    c["try_key"] = c.FilePath + "#" + c.TryStartLine.astype(str)
    catch_key = c.FilePath + "#" + c.StartLine.astype(str)
    key2try = dict(zip(catch_key, c.try_key))
    act = catch_actions(c)
    act_by_catch = act.set_axis(catch_key.values)
    pe["try_key"] = (pe.FilePath + "#" + pe.StartLine.astype(str)).map(key2try)
    pe = pe.dropna(subset=["try_key"])
    pe["caught"] = pe.HandlerTypeCode.isin([0, 1])
    pe_catch_key = pe.FilePath + "#" + pe.StartLine.astype(str)
    for a in ACTIONS:   # an action applies to a PE if a catch that handles it (specific/subsumption) has it
        pe["act_" + a] = pe["caught"] & pe_catch_key.map(act_by_catch[a].groupby(level=0).max()).fillna(False).astype(bool)
    pe["strategy"] = np.where(pe.HandlerTypeCode == 0, 0, np.where(pe.HandlerTypeCode == 1, 1, 9))
    g = pe.groupby(["try_key", "ThrownType"])
    pel = g.agg(strategy=("strategy", "min"), kind=("Kind", "max"),
                n_decl=("DeclaringMethod", "nunique"), n_inv=("InvokedMethod", "nunique"),
                lvl_avg=("LevelFound", "mean"), lvl_max=("LevelFound", "max"),
                binding=("IsBindingInfo", "max"), docsem=("IsDocSemantic", "max"),
                docsyn=("IsDocSyntax", "max"), isthrow=("IsThrow", "max"),
                **{"act_" + a: ("act_" + a, "max") for a in ACTIONS}).reset_index()
    prevalence = _type_prevalence(c, pe) if PREVALENCE_SCOPE == "release" else prevalence_all
    pel["prevalence"] = pel.ThrownType.map(prevalence)
    pel["propagated"] = pel.strategy == 9
    pel["prop_recov"] = pel.propagated & (pel.kind == 1)

    # ---- try level ------------------------------------------------------------------------------
    tries = c.groupby("try_key").agg(FilePath=("FilePath", "first"), TryLOC=("TryLOC", "first"),
                                     TryStartLine=("TryStartLine", "first"), TryEndLine=("TryEndLine", "first"),
                                     ParentNodeType=("ParentNodeType", "first"),
                                     NumDistinctMethods=("NumDistinctMethods", "max"))
    tries["TryPhysLOC"] = tries.TryEndLine - tries.TryStartLine + LOC_OFFSET
    tries["scope"] = tries.ParentNodeType.map(SCOPE).fillna("Other")
    gp = pel.groupby("try_key")
    tl = pd.DataFrame({
        "n_pe": gp.size(), "n_prop": gp.propagated.sum(), "n_prop_rec": gp.prop_recov.sum(),
        "pct_docsyn": gp.docsyn.mean(), "pct_docsem": gp.docsem.mean(), "pct_binding": gp.binding.mean(),
        "pct_throw": gp.isthrow.mean(), "pct_specific": gp.strategy.apply(lambda s: (s == 0).mean()),
        "pct_subs": gp.strategy.apply(lambda s: (s == 1).mean()),
        "avg_decl": gp.n_decl.mean(), "avg_inv": gp.n_inv.mean(), "avg_depth": gp.lvl_avg.mean(),
        "max_depth": gp.lvl_max.max(), "avg_prev": gp.prevalence.mean(),
        **{"n_" + a: gp["act_" + a].sum() for a in ACTIONS}})
    tries = tries.join(tl, how="inner")   # tries with >=1 possible exception (as in the authors' Try_Based data)
    tries["pct_prop"] = tries.n_prop / tries.n_pe
    tries["pct_prop_rec"] = tries.n_prop_rec / tries.n_pe
    for a in ACTIONS:
        tries["pct_" + a] = tries["n_" + a] / tries.n_pe

    ft = tries.groupby("FilePath")
    T = pd.DataFrame({"File Path": list(ft.groups), "Project": project})
    T = T.set_index("File Path")
    for s in SCOPES:
        T[f"# Try in {s}"] = ft.scope.apply(lambda x, s=s: (x == s).sum())
    T["# Try"] = ft.size()
    for s in SCOPES:
        T[f"% Try in {s}"] = T[f"# Try in {s}"] / T["# Try"]
    T["Avg Max Depth"] = ft.max_depth.mean()
    T["Avg Try LOC"] = ft.TryPhysLOC.mean()
    T["Avg Try SLOC"] = ft.TryLOC.mean()
    for a in ACTIONS:
        T[f"# Handled with {a}"] = ft["n_" + a].mean()
    T["# Possible Exceptions"] = ft.n_pe.mean()
    T["# Propagated and Potentially Recoverable"] = ft.n_prop_rec.mean()
    T["# Propagated"] = ft.n_prop.mean()
    T["% Doc in Comment"] = ft.pct_docsyn.mean()
    T["% External Doc"] = ft.pct_docsem.mean()
    for a in ACTIONS:
        T[f"% Handled with {a}"] = ft["pct_" + a].mean()
    T["% Method Declaration"] = ft.pct_binding.mean()
    T["% Propagated and Potentially Recoverable"] = ft.pct_prop_rec.mean()
    T["% Propagated"] = ft.pct_prop.mean()
    T["% Specific"] = ft.pct_specific.mean()
    T["% Subsumption"] = ft.pct_subs.mean()
    T["% Throw Statement"] = ft.pct_throw.mean()
    T["Avg # Declaring Methods"] = ft.avg_decl.mean()
    T["Avg # Invoked Method"] = ft.avg_inv.mean()
    T["Avg Depth"] = ft.avg_depth.mean()
    T["Avg Exc Type Prevalence"] = ft.avg_prev.mean()
    T["Num Distinct Methods"] = ft.NumDistinctMethods.mean()
    T["Sum of Num Distinct Methods"] = ft.NumDistinctMethods.sum()
    T["Try LOC"] = ft.TryPhysLOC.sum()
    T["Try SLOC"] = ft.TryLOC.sum()
    T.insert(0, "Language", "Java")
    T = T.reset_index()

    # ---- catch level -> file ---------------------------------------------------------------------
    uncaught = c.try_key.map(pel.groupby("try_key").propagated.any()).fillna(False)
    ap = catch_antipatterns(c, m, uncaught)
    rec = recoverability(c.Kind)
    c["CatchPhysLOC"] = c.CatchEndLine - c.CatchStartLine + LOC_OFFSET
    fc = c.groupby("FilePath")
    C = pd.DataFrame(index=pd.Index(list(fc.groups), name="File Path"))
    C["Language"] = "Java"
    C["Project"] = project
    C["# Catch"] = fc.size()
    C["Avg Catch LOC"] = fc.CatchPhysLOC.mean()
    C["Avg Catch SLOC"] = fc.CatchLOC.mean()
    apf = ap.groupby(c.FilePath).sum()
    recf = rec.groupby(c.FilePath).sum()
    for name in ap.columns:
        C[f"Avg. AP {name}"] = apf[name] / C["# Catch"]
    for name in rec.columns:
        C[f"Avg. {name}"] = recf[name] / C["# Catch"]
    sum_prefixed = {"Destructive Wrapping", "Dummy Handler", "Generic Catch", "Log and Return null",
                    "Overcatch and Abort", "Overcatch", "Unhandled exceptions", "Unreachable Catch Handler"}
    for name in ap.columns:   # the authors' Tableau export prefixes some (not all) counts with "Sum of"
        C[("Sum of AP " if name in sum_prefixed else "AP ") + name] = apf[name]
    C["Catch LOC"] = fc.CatchPhysLOC.sum()
    C["Catch SLOC"] = fc.CatchLOC.sum()
    for name in rec.columns:
        C[name] = recf[name]
    C = C.reset_index()

    # ---- throws ------------------------------------------------------------------------------------
    th["throw_key"] = th.FilePath + "#" + th.Line.astype(str)
    tm = th.groupby("throw_key").agg(FilePath=("FilePath", "first"), gen=("ThrowsException", "max"),
                                     ks=("ThrowsKitchenSink", "max"))
    ftm = tm.groupby("FilePath")
    TH = pd.DataFrame({"File Path": list(ftm.groups)})
    TH["Language"], TH["Project"] = "Java", project
    TH = TH.set_index("File Path")
    TH["# Throws"] = ftm.size()
    TH["Avg. Max. Generic Throws"] = ftm.gen.mean()
    TH["Avg. Max. Throws Kitchen Sink"] = ftm.ks.mean()
    TH["Max. Generic Throws"] = ftm.gen.sum()
    TH["Max. Throws Kitchen Sink"] = ftm.ks.sum()
    TH = TH.reset_index()
    return C, T, TH
