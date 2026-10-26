# Run this in the R console after opening bgl_python.Rproj.
# One-time prerequisite: install.packages("reticulate")
stopifnot(file.exists("requirements.txt"))
if (!requireNamespace("reticulate", quietly = TRUE) ||
    packageVersion("reticulate") < "1.41") {
  stop('Install/update reticulate with install.packages("reticulate"), then restart R.')
}
# Must be set before Python starts. "managed" gives py_require priority over
# Python installations previously selected in RStudio or environment variables.
Sys.setenv(RETICULATE_PYTHON = "managed")
requirements <- readLines("requirements.txt")
requirements <- trimws(sub("#.*$", "", requirements))
requirements <- requirements[nzchar(requirements)]
reticulate::py_require(requirements, python_version = ">=3.12,<3.13")
print(reticulate::py_config())
message("Ready. Open lessons/01_intro.py and run selected blocks in order.")
