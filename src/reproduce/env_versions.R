# Print R and package versions used by the reproduction (consumed by docs/ENVIRONMENT.md).
pk <- c("rms", "Hmisc", "caret", "e1071", "knitr", "rmarkdown", "ggplot2", "lattice", "survival",
        "SparseM", "polspline", "plotly", "BiodiversityR", "logistf")
cat(R.version.string, "\n")
for (p in pk) {
  v <- tryCatch(as.character(packageVersion(p)), error = function(e) "NOT INSTALLED")
  cat(sprintf("%-14s %s\n", p, v))
}
