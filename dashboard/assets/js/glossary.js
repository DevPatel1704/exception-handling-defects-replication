// Plain-language descriptions. Metric definitions follow the paper's Tables 2–3 and the authors' rule sheet
// (docs/aggregation_rules/metrics_and_aggregation_rules_MSR18.xlsx). Nothing here is computed.

export const STEPS = {
  clone: "Clone the repository and check out the release commit.",
  configure: "Detect the language, the source folders and the issue-tracker keys.",
  process_metrics: "Pre-release changes, authors, churn and fixed bugs per file (paper §3.3.3).",
  defect_mining: "Label files with bugs reported after the release (paper §3.3.1).",
  product_metrics: "Size and complexity per file (paper §3.3.2).",
  analyzer: "JTratch: try/catch flow characteristics and 17 anti-patterns (paper §3.3.4).",
  dataset: "Merge everything into one row per file in the authors' input format.",
  models: "The authors' R code: BASE, BSFC and BSAP logistic models (RQ1, RQ2).",
  ml: "Cross-validated LR / RF / XGBoost on four feature sets (RQ3).",
  shap: "TreeSHAP on the best tree model (RQ4).",
  summary: "Collect all outputs for this dashboard.",
};

export const TOOLS = {
  git: ["Git", "Clones repositories and reads their history."],
  Rscript: ["R", "Runs the authors' statistical model code (rms, Hmisc, caret)."],
  java8: ["Java 8", "Runs JTratch, the authors' exception-flow analyzer (needs Java 8)."],
  understand: ["Understand", "SciTools Understand: the commercial product-metrics tool the paper used. Not available here, so 12 open-source approximations (lizard) are used instead."],
  authors_package: ["Authors' package", "The paper's released scripts and data, needed for the original-study reproduction and the input format."],
};

export const CARDS = {
  files: "Source files at the release that match the include filter (tests excluded).",
  defective: "Files changed by at least one fix of a bug reported after the release.",
  bugs: "Distinct post-release bug reports linked to a fixing commit.",
  catchFiles: "Files with at least one catch block. The paper's models use only these files.",
  defCatch: "Defective files among those with catch blocks: the positive class of the models.",
  blocks: "Total catch blocks (try blocks in parentheses) found by JTratch in the release files.",
  pe: "Mean number of distinct possible exceptions per try block, as found by JTratch.",
};

const FAMILY = [
  [/^% Handled with (.+)$/, (m) => `Share of a try block's possible exceptions whose handler performs the "${m[1]}" action.`],
  [/^# Handled with (.+)$/, (m) => `Number of a try block's possible exceptions whose handler performs the "${m[1]}" action (averaged over the file's try blocks).`],
  [/^(Avg\. AP|AP|Sum of AP) (.+)$/, (m) => `${m[1] === "Avg. AP" ? "Share" : "Number"} of the file's catch blocks showing the "${m[2]}" anti-pattern.`],
  [/^% Try in (.+)$/, (m) => `Share of the file's try blocks declared inside a ${m[1].toLowerCase()} scope.`],
  [/^# Try in (.+)$/, (m) => `Number of the file's try blocks declared inside a ${m[1].toLowerCase()} scope.`],
  [/Possible Exceptions/, () => "Distinct possible exceptions that can reach a handler (flow quantity)."],
  [/Propagated and Potentially Recoverable/, () => "Possible exceptions that are potentially recoverable (checked) but propagated rather than handled."],
  [/Propagated/, () => "Possible exceptions the handler does not catch, so they propagate to callers."],
  [/Exc Type Prevalence/, () => "How many try blocks in the project share the same possible-exception types; low = rare exception types."],
  [/Declaring Methods/, () => "Average number of methods that declare each possible exception."],
  [/Invoked Method/, () => "Average number of invoked methods each possible exception can come from (ambiguity of its source)."],
  [/Depth/, () => "Call-graph depth (relative to the handler) at which possible exceptions are found."],
  [/% Specific/, () => "Share of possible exceptions caught by a handler of exactly their type."],
  [/% Subsumption/, () => "Share of possible exceptions caught by a handler of a supertype (subsumption)."],
  [/% Doc in Comment/, () => "Share of possible exceptions found through Javadoc @throws in the source."],
  [/% External Doc/, () => "Share of possible exceptions found through external documentation (empty here: the authors' file is unpublished)."],
  [/% Method Declaration/, () => "Share of possible exceptions found through throws declarations (binding information)."],
  [/% Throw Statement/, () => "Share of possible exceptions found through explicit throw statements."],
  [/Catch .*LOC|Catch SLOC|Catch LOC/, () => "Size of the file's catch blocks."],
  [/Try .*LOC|Try SLOC|Try LOC/, () => "Size of the file's try blocks."],
  [/Recoverab/, () => "Recoverability class of the caught exception type (checked = potentially recoverable)."],
  [/^# Catch$/, () => "Number of catch blocks in the file."],
  [/^# Throws$/, () => "Number of methods with a throws clause."],
  [/Num Distinct Methods/, () => "Distinct methods invoked inside the file's try blocks."],
  [/Churn/, () => "Lines added plus deleted before the release (process metric)."],
  [/# Changes/, () => "Number of commits touching the file before the release (process metric)."],
  [/# Authors/, () => "Distinct authors of the file before the release (process metric)."],
  [/# Bugs \(pre\)/, () => "Fixed bugs linked to the file before the release (pre-release quality)."],
  [/^Count|^Avg|^Max|^Sum|Ratio|fileSize/, () => "Traditional product metric (size, complexity or documentation)."],
];

export function describeMetric(name) {
  for (const [rx, f] of FAMILY) { const m = name.match(rx); if (m) return f(m); }
  return "Metric from the authors' metric set.";
}

/** Non-causal explanation of one significant predictor of an explanatory logistic model. */
export function explainPredictor(p) {
  const up = p.direction === "+";
  return `In this release, files with higher "${p.name}" had a ${up ? "higher" : "lower"} probability of a post-release defect, ` +
    `holding the model's other predictors at their means. Raising it by 10% above its mean changes the predicted probability by ` +
    `${p.effect_pct > 0 ? "+" : ""}${(+p.effect_pct).toFixed(1)}% (relative). This is an association in an explanatory model, not a causal effect.`;
}

export const MODEL_INFO = {
  BASE: "Traditional metrics only: size, complexity, changes, authors, pre-release bugs.",
  BSFC: "BASE plus exception-flow characteristics (RQ1).",
  BSAP: "BASE plus exception-handling anti-patterns (RQ2).",
};
