# Phase 0 driver: run the authors' released R notebooks on their released input data.
#
# Usage (from repo root):
#   Rscript src/reproduce/run_original.R asis    # authors' code, unmodified
#   Rscript src/reproduce/run_original.R fixed   # same, with the BSFC data-list bug fixed
#
# What it does:
#   1. Copies external/scripts_with_input_data/ into build/reproduce_<mode>/ (external/ stays pristine).
#   2. In "fixed" mode, patches ONE line in construction_functions.R (see docs/REPRODUCTION.md).
#   3. set.seed(2018), then knitr::purl + source 0-DataSourcesAnalysis.Rmd and 1-Model_Construction.Rmd
#      in the global environment, exactly in the authors' order.
#   4. Copies output/base_test_*.csv to results/reproduce/<mode>/ and writes, for the presented models
#      (files with catch blocks: CAT.BASE / CAT.BSAP / CAT.BSFC), a per-predictor table with Wald chi2,
#      p-value and the MA4 effect (+10% of mean), recomputed from the simplified formulas.

suppressMessages({ library(knitr) })

#   Phase 2 (new data in the authors' input format, see src/collect/build_dataset.py):
#   Rscript src/reproduce/run_original.R fixed --input data/new/hibernate-5.1/input --out results/new/hibernate-5.1
#
#   Sensitivity S1 (--force-sig, with "fixed"): enable the authors' own "keep BASE-significant metrics" branch in
#   dataApplyReductionByModel(), which the paper describes (§3.4.6) but which the released code guards with a
#   condition that is never true (project=="" && model_type==""). Output goes to <out>/fixed_forcesig.
#   Rscript src/reproduce/run_original.R fixed --force-sig --input data/new/<id>/input --out results/new/<id>

args <- commandArgs(trailingOnly = TRUE)
mode <- if (length(args) > 0 && !startsWith(args[1], "--")) args[1] else "asis"
stopifnot(mode %in% c("asis", "fixed"))
opt <- function(name) { i <- match(name, args); if (is.na(i)) NULL else args[i + 1] }
force_sig <- "--force-sig" %in% args
if (force_sig && mode != "fixed") stop("--force-sig is a sensitivity analysis on top of the 'fixed' mode")
sub_dir <- if (force_sig) "fixed_forcesig" else mode
SEED <- 2018

file_arg <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
script_dir <- dirname(normalizePath(sub("^--file=", "", file_arg)))
repo <- normalizePath(file.path(script_dir, "..", ".."))
src_pkg <- file.path(repo, "external", "scripts_with_input_data")
input_dir <- if (is.null(opt("--input"))) file.path(src_pkg, "input") else normalizePath(opt("--input"))
tag <- if (is.null(opt("--out"))) sub_dir else paste0(basename(opt("--out")), "_", sub_dir)
work <- file.path(repo, "build", paste0("reproduce_", tag))
out <- if (is.null(opt("--out"))) file.path(repo, "results", "reproduce", sub_dir) else file.path(repo, opt("--out"), sub_dir)
if (!dir.exists(src_pkg)) stop("Authors' package not found at ", src_pkg, " (see README: fetch_package.sh)")

unlink(work, recursive = TRUE)
dir.create(file.path(work, "input"), recursive = TRUE)
dir.create(file.path(work, "output"), recursive = TRUE)
dir.create(out, recursive = TRUE, showWarnings = FALSE)
for (f in c("0-DataSourcesAnalysis.Rmd", "1-Model_Construction.Rmd",
            "analysis_functions.R", "construction_functions.R"))
  file.copy(file.path(src_pkg, f), file.path(work, f))
for (f in list.files(input_dir, pattern = "^File_Level-.*\\.csv$"))
  file.copy(file.path(input_dir, f), file.path(work, "input", f))
cat("Input:", input_dir, "\n")

# R-compatibility patch (BOTH modes). R >= 4.3 errors on `&&` with a length > 1 operand; R 3.x (used by the
# authors) silently took the first element. analysis_functions.R:270 has `!is.na(refit)` on an lrm object
# (a list), so we make the first-element semantics explicit. Behaviour is identical to R 3.x.
af <- file.path(work, "analysis_functions.R")
code <- readLines(af)
hit <- grep('if(class_refit != "try-error" && !is.na(refit)) {', code, fixed = TRUE)
if (length(hit) != 1) stop("Expected the R>=4.3 incompatible line in analysis_functions.R, found ", length(hit))
code[hit] <- sub("!is.na(refit)) {", "!is.na(refit)[1]) {  # [replication compat: R>=4.3]", code[hit], fixed = TRUE)
# Empty-model guard (BOTH modes; deviation D7 in docs/REPRODUCTION.md). In modelSimplification(), when fastbw()
# removes every predictor, `refit` is never assigned and the run halts with "object 'refit' not found". This never
# happens on the paper's data (the authors' runs would have halted) or on Hibernate 5.1 / ZooKeeper 3.6 / 3.9; it
# happens on small new releases (ZooKeeper 3.7.0: 18 defective files). We initialise refit / final_form / coef to NA
# so such a model is recorded as "no predictor survives simplification" (error = TRUE, R2 NA) and the run continues.
guard <- grep("if (length(s_fastbw$names.kept) > 0)", code, fixed = TRUE)
if (length(guard) != 1) stop("Expected one fastbw names.kept test in analysis_functions.R, found ", length(guard))
code <- append(code, "      refit = NA; final_form = NA; coef = NA  # [replication guard D7: empty simplified model]",
               after = guard - 1)
writeLines(code, af)
message("Applied R>=4.3 compatibility patch at analysis_functions.R line ", hit,
        "; empty-model guard (D7) before line ", guard)

if (mode == "fixed") {
  cf <- file.path(work, "construction_functions.R")
  code <- readLines(cf)
  bug <- grep("^\\s*data_list = all_list_omitted_m2\\s*$", code)
  if (length(bug) != 1) stop("Expected exactly one buggy line in construction_functions.R, found ", length(bug))
  code[bug] <- paste0("  # [replication fix] removed: data_list = all_list_omitted_m2  (overrode the BSFC input)")
  writeLines(code, cf)
  message("Patched construction_functions.R line ", bug)
  if (force_sig) {
    code <- readLines(cf)
    hits <- grep('if(project=="" && model_type=="")', code, fixed = TRUE)
    if (length(hits) != 2) stop("Expected two never-true keep-significant guards, found ", length(hits))
    code[hits] <- sub('if(project=="" && model_type=="")',
                      'if(TRUE)  # [sensitivity S1: keep BASE-significant metrics, paper 3.4.6]', code[hits], fixed = TRUE)
    # Simply adding the BASE-significant metrics back can exceed the d.f. budget, and over-budget models are not fit
    # by the authors' code. So S1 reserves one budget slot per BASE-significant metric: the other metrics are
    # reduced by the authors' own dynamic-cutoff rule (as in myfindCorrelation) to budget - |sig|, then sig is added.
    add <- which(trimws(code) == "variables_to_add = sig")[1]
    if (is.na(add)) stop("S1: 'variables_to_add = sig' not found in construction_functions.R")
    code <- append(code[-add], c(
      "          sig_real = setdiff(unlist(sig), 'TOTAL')  # [sensitivity S1: reserve budget for sig]",
      "          x_ns = data[, !(names(data) %in% c(sig_real, dropToPredict))]",
      "          kept_ns = s1ReduceToBudget(x_ns, floor(nrow(x_ns) / 15) - length(sig_real))",
      "          variables_to_keep = c(kept_ns, dropToPredict)",
      "          variables_to_add = sig_real"), after = add - 1)
    code <- c(code, "",
      "# [sensitivity S1] myfindCorrelation's dynamic-cutoff reduction with an explicit budget",
      "s1ReduceToBudget <- function(x, budget) {",
      "  cors <- cor(x, method = 'spearman'); dyn_cutoff <- CORR_THRESHOLD; vars <- names(x)",
      "  while (length(vars) > budget) {",
      "    dyn_cutoff <- dyn_cutoff - 0.001",
      "    vars <- vars[!(vars %in% findCorrelation(cors, cutoff = dyn_cutoff, names = TRUE))]",
      "  }",
      "  print(paste('S1: kept', length(vars), 'non-significant metrics at cutoff', dyn_cutoff, 'for budget', budget))",
      "  vars",
      "}")
    writeLines(code, cf)
    message("Sensitivity S1: enabled keep-significant branch at construction_functions.R lines ",
            paste(hits, collapse = ", "))
  }
}

log_con <- file(file.path(out, "run_log.txt"), open = "wt")
sink(log_con, split = FALSE); sink(log_con, type = "message")
on.exit({ sink(type = "message"); sink() }, add = TRUE)

setwd(work)
pdf(file.path(out, "figures_from_authors_code.pdf"))   # captures varclus / naclus / Ecdf plots
set.seed(SEED)
t0 <- Sys.time()
for (rmd in c("0-DataSourcesAnalysis.Rmd", "1-Model_Construction.Rmd")) {
  cat("\n\n######## RUNNING", rmd, "########\n")
  tmp <- tempfile(tmpdir = ".", fileext = ".R")
  knitr::purl(rmd, output = tmp, quiet = TRUE)
  source(tmp, local = globalenv(), echo = FALSE)
  unlink(tmp)
}
dev.off()
cat("\nElapsed:", format(Sys.time() - t0), "\n")

for (f in c("base_test_1.csv", "base_test_2.csv"))
  file.copy(file.path(work, "output", f), file.path(out, f), overwrite = TRUE)
file.copy(file.path(work, "all_no_missing.csv"), file.path(out, "all_no_missing_regenerated.csv"), overwrite = TRUE)

# Metric groups (R-mangled column names) for downstream Python code.
grp <- rbind(
  data.frame(metric = base_names,   group = "base"),
  data.frame(metric = catch_names,  group = "catch"),
  data.frame(metric = try_names,    group = "try"),
  data.frame(metric = throws_names, group = "throws"))
write.csv(grp, file.path(out, "metric_groups.csv"), row.names = FALSE)

# Per-predictor stats of the simplified (refit) models, same computations as the authors'
# modelSimplification(): lrm refit, anova Wald chi2, and predict at mean vs mean*1.1.
predictor_rows <- list()
collect <- function(models, things) {
  for (i in seq_along(models)) {
    m <- models[[i]]; t <- things[[i]]
    if (is.null(t$final_form) || is.na(t$final_form) || t$final_form == "NA") next
    d <- m$data
    dd <<- datadist(d); options(datadist = "dd")
    refit <- lrm(as.formula(t$final_form), data = d, x = TRUE, y = TRUE)
    an <- anova(refit, test = "Chisq")
    coefs <- setdiff(names(refit$coefficients), "Intercept")
    newdata <- as.data.frame(lapply(setNames(coefs, coefs), function(cn) mean(10^d[[cn]] - 1)))
    p0 <- predict(refit, log10(newdata + 1), type = "fitted.ind")
    for (cn in coefs) {
      nd <- newdata; nd[[cn]] <- 1.1 * nd[[cn]]
      p1 <- predict(refit, log10(nd + 1), type = "fitted.ind")
      predictor_rows[[length(predictor_rows) + 1]] <<- data.frame(
        model = m$name, project = m$project, predictor = cn,
        wald_chi2 = an[cn, "Chi-Square"], p_value = an[cn, "P"],
        coef = unname(refit$coefficients[cn]),
        p_at_mean = unname(p0), p_at_mean_plus10 = unname(p1),
        effect_rel_pct = 100 * (unname(p1) - unname(p0)) / unname(p0),
        effect_abs_pp = 100 * (unname(p1) - unname(p0)))
    }
  }
}
collect(models_2_BASE, model_things_2_BASE)
collect(models_2_BSAP, model_things_2_BSAP)
collect(models_2_BSFC, model_things_2_BSFC)
write.csv(do.call(rbind, predictor_rows), file.path(out, "predictors_simplified.csv"), row.names = FALSE)

writeLines(c(paste("mode:", mode), paste("force_sig:", force_sig), paste("seed:", SEED),
             capture.output(sessionInfo())),
           file.path(out, "sessionInfo.txt"))
cat("DONE\n")
