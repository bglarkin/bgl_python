# Validation and numerical checkpoints

Checked October 26, 2026 using Python 3.12.14 on macOS arm64, with the versions
in `requirements.txt` and the full environment snapshot in `requirements-tested.txt`.
These are tested teaching versions, not the latest-release recommendation.

The data generator, full analysis (including optional diagnostics), and exercise
solutions were executed. Exported tables and graphics were checked; the main
relationship figure was visually inspected. R scripts were checked for parse
errors. RStudio's interactive UI and reticulate's first-run managed downloads
were **not** exercised; those instructions follow the linked official documentation.
Windows/Linux execution has not been separately tested.

## Expected results

Small floating-point differences in the last digits are harmless.

| Check | Expected |
|---|---|
| Raw table | 60 rows, 4 columns |
| Missing data | 2 heights, 1 moisture, 0 treatment |
| Complete cases | 57; 29 control, 28 fertilized |
| Mean height, all complete cases | 24.884386 cm |
| Mean height, control | 22.953448 cm |
| Mean height, fertilized | 26.884286 cm |
| Control one-sample t-test vs 23 cm | t ≈ -0.055, df = 28, p ≈ 0.9566 |
| 95% CI for control mean | approximately [21.2181, 24.6888] cm |
| OLS intercept | 6.654551 |
| OLS fertilized-minus-control coefficient | 4.371069 cm |
| OLS moisture coefficient | 0.537062 cm per percentage point |
| R-squared | approximately 0.8693 |
| Exercise A | 14 rows |
| Exercise B | 0.24884386 m |
| Exercise C group means | control 0.22953448 m; fertilized 0.26884286 m |

The t-test gives little evidence against a control mean of 23 cm; it does not
prove equality. The model estimates taller seedlings at higher moisture and
for the fertilized category at equal moisture. Those are properties of this
simulation and model, not findings about real plants.

Terminal verification ran with `MPLBACKEND=Agg` so figures could be saved without
an interactive display. Warnings that `plt.show()` cannot display on that backend
are expected during such a check; leave the backend alone in RStudio.

To repeat the analysis, follow [SETUP.md](SETUP.md) and run the script top to
bottom. To check solutions, run them in the same Python session after the lesson.
