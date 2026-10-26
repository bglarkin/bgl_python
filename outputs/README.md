# Generated outputs

Run `lessons/01_intro.py` from the project root to create:

- `clean_seedlings.csv`: the 57 complete cases, including converted height units.
- `summary_by_treatment.csv`: group sizes, means, sample standard deviations.
- `descriptive_statistics.csv`: numeric summaries, with variable names retained.
- `one_sample_t_test.csv`: control-group test, mean, and 95% interval for the mean.
- `model_coefficients.csv` and `.html`: coefficients, standard errors, p-values, 95% CIs.
- `model_summary.txt`: full fitted-model summary.
- `height_histogram.png`: distribution of all complete-case heights.
- `height_vs_moisture.png` and `.pdf`: observations and model fitted mean lines.
- `model_diagnostics.png`: optional residual and Q–Q plots.

The practice solution adds `practice_summary.csv`.
Files are overwritten on rerun and excluded from version control. The analysis
uses all complete cases consistently, including for summaries; this is why a
height-only summary has 57 observations even though 58 raw heights were measured.
