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

args <- commandArgs(trailingOnly = TRUE)
mode <- if (length(args) > 0 && !startsWith(args[1], "--")) args[1] else "asis"
stopifnot(mode %in% c("asis", "fixed"))
opt <- function(name) { i <- match(name, args); if (is.na(i)) NULL else args[i + 1] }
SEED <- 2018

file_arg <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
script_dir <- dirname(normalizePath(sub("^--file=", "", file_arg)))
repo <- normalizePath(file.path(script_dir, "..", ".."))
src_pkg <- file.path(repo, "external", "scripts_with_input_data")
input_dir <- if (is.null(opt("--input"))) file.path(src_pkg, "input") else normalizePath(opt("--input"))
tag <- if (is.null(opt("--out"))) mode else paste0(basename(opt("--out")), "_", mode)
work <- file.path(repo, "build", paste0("reproduce_", tag))
out <- if (is.null(opt("--out"))) file.path(repo, "results", "reproduce", mode) else file.path(repo, opt("--out"), mode)
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
writeLines(code, af)
message("Applied R>=4.3 compatibility patch at analysis_functions.R line ", hit)

if (mode == "fixed") {
  cf <- file.path(work, "construction_functions.R")
  code <- readLines(cf)
  bug <- grep("^\\s*data_list = all_list_omitted_m2\\s*$", code)
  if (length(bug) != 1) stop("Expected exactly one buggy line in construction_functions.R, found ", length(bug))
  code[bug] <- paste0("  # [replication fix] removed: data_list = all_list_omitted_m2  (overrode the BSFC input)")
  writeLines(code, cf)
  message("Patched construction_functions.R line ", bug)
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

writeLines(c(paste("mode:", mode), paste("seed:", SEED), capture.output(sessionInfo())),
           file.path(out, "sessionInfo.txt"))
cat("DONE\n")
