"""Lesson 1: run selected blocks top to bottom in RStudio, from the project root.
Read 01_intro.md alongside this file. This is ordinary Python, also runnable
from a terminal. All observations are simulated. Re-running overwrites outputs.
"""

# %% 1. Imports and language basics (0-10 minutes)
from pathlib import Path                 # standard library: no separate install
import numpy as np                      # numerical arrays
import pandas as pd                     # data frames
from scipy import stats                 # statistical tests
import statsmodels.api as sm            # diagnostic plotting
import statsmodels.formula.api as smf    # R-style model formulas
import matplotlib.pyplot as plt         # figures

height = 12.5                            # R: height <- 12.5
species = "seedling"                     # string
measured = True                          # capital T; R uses TRUE
heights = [10.0, 12.5, 15.0]              # list, NOT an R numeric vector
print(heights[0])                        # first item, not heights[1]
print(heights[:2])                       # stop before position 2
print(heights * 2)                       # repeats the list
print(np.array(heights) * 2)             # elementwise arithmetic

# Functions use def, a colon, and indentation instead of braces.
def cm_to_mm(value):
    return value * 10

print(cm_to_mm(height))
print(type(height))

# %% 2. Read and wrangle (10-25 minutes)
root = Path.cwd()
if not (root / "data" / "seedlings.csv").exists():
    raise FileNotFoundError("Open bgl_python.Rproj and run from the project folder.")
out = root / "outputs"
out.mkdir(exist_ok=True)

raw = pd.read_csv(root / "data" / "seedlings.csv")
print(raw.head())
print(raw.shape)                         # attribute: no parentheses
raw.info()                              # method: parentheses; prints its own output
print(raw.isna().sum())                  # missing counts per column

# Keep only rows with the measurements needed for this analysis.
df = raw.dropna(subset=["height_cm", "soil_moisture_pct", "treatment"]).copy()
print(f"Rows: {len(raw)} raw -> {len(df)} complete; removed {len(raw) - len(df)}")
df["treatment"] = pd.Categorical(
    df["treatment"], categories=["control", "fertilized"]
)
df["height_mm"] = df["height_cm"] * 10

# A boolean mask selects rows; a list of column names selects columns.
subset = df.loc[
    (df["treatment"] == "fertilized") & (df["soil_moisture_pct"] >= 30),
    ["seedling_id", "height_cm", "soil_moisture_pct"],
]
print(subset.head())
print(df.sort_values("height_cm", ascending=False).head(3))

by_treatment = (
    df.groupby("treatment", observed=True)
    .agg(n=("height_cm", "size"),
         mean_height_cm=("height_cm", "mean"),
         sd_height_cm=("height_cm", "std"))
    .reset_index()
)
print(by_treatment.round(2))              # rounds display, keeps full precision above

# %% 3. Univariate statistics (25-35 minutes)
print(df["height_cm"].describe())
print(df["treatment"].value_counts())
height_summary = df[["height_cm", "soil_moisture_pct"]].describe().T

# Teaching question: is mean CONTROL height different from 23 cm?
# 23 cm is an arbitrary exercise benchmark, not a biological threshold.
control_heights = df.loc[df["treatment"] == "control", "height_cm"]
one_sample = stats.ttest_1samp(control_heights, popmean=23)
mean_ci = one_sample.confidence_interval(confidence_level=0.95)
t_table = pd.DataFrame({
    "n": [len(control_heights)], "mean_cm": [control_heights.mean()],
    "null_mean_cm": [23], "t": [one_sample.statistic],
    "df": [one_sample.df], "p_value": [one_sample.pvalue],
    "mean_ci_low": [mean_ci.low], "mean_ci_high": [mean_ci.high],
})
print(t_table.round(4))

# %% 4. Parametric relationships: ordinary least squares (35-48 minutes)
# R: lm(height_cm ~ soil_moisture_pct + treatment, data = df)
# C() marks a categorical predictor. The ordered category list makes control
# the reference. The formula API includes an intercept automatically.
model = smf.ols("height_cm ~ soil_moisture_pct + C(treatment)", data=df).fit()
print(model.summary())
ci = model.conf_int()
coefficients = pd.DataFrame({
    "term": model.params.index,
    "estimate": model.params.to_numpy(),
    "std_error": model.bse.to_numpy(),
    "p_value": model.pvalues.to_numpy(),
    "ci_low": ci.iloc[:, 0].to_numpy(),
    "ci_high": ci.iloc[:, 1].to_numpy(),
})
print(coefficients)                      # retain scientific notation for small p-values

# %% 5. Figures and exports (48-56 minutes)
fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(df["height_cm"], bins=10, color="#247482", edgecolor="white")
ax.set(xlabel="Seedling height (cm)", ylabel="Number of seedlings",
       title="Simulated seedling heights")
fig.tight_layout()
fig.savefig(out / "height_histogram.png", dpi=300)
plt.show()
plt.close(fig)

# The loop repeats plotting for two treatments; indentation defines its body.
fig, ax = plt.subplots(figsize=(6, 4))
for treatment, color in [("control", "#247482"), ("fertilized", "#C06B35")]:
    group = df.loc[df["treatment"] == treatment]
    ax.scatter(group["soil_moisture_pct"], group["height_cm"],
               color=color, alpha=0.8, label=treatment)
    grid = pd.DataFrame({
        "soil_moisture_pct": np.linspace(group["soil_moisture_pct"].min(),
                                         group["soil_moisture_pct"].max(), 100),
        "treatment": treatment,
    })
    ax.plot(grid["soil_moisture_pct"], model.predict(grid), color=color)
ax.set(xlabel="Soil moisture (%)", ylabel="Seedling height (cm)",
       title="Simulated data and fitted mean relationships")
ax.legend(title="Treatment")
fig.tight_layout()
fig.savefig(out / "height_vs_moisture.png", dpi=300)
fig.savefig(out / "height_vs_moisture.pdf")
plt.show()
plt.close(fig)

# CSVs open in R, Excel, and text editors. index=False avoids an extra row-index column.
df.to_csv(out / "clean_seedlings.csv", index=False)
by_treatment.to_csv(out / "summary_by_treatment.csv", index=False)
height_summary.to_csv(out / "descriptive_statistics.csv", index_label="variable")
t_table.to_csv(out / "one_sample_t_test.csv", index=False)
coefficients.to_csv(out / "model_coefficients.csv", index=False)
(out / "model_summary.txt").write_text(model.summary().as_text(), encoding="utf-8")
coefficients.to_html(out / "model_coefficients.html", index=False, float_format="%.4g")
print(f"Saved tables, model summary, and figures to {out}")

# %% 6. Your turn (56-60 minutes)
# Without looking at the solutions:
# A. Select control seedlings with soil_moisture_pct > 30. How many rows?
# B. Add height_m (meters) to df. What is the mean height_m?
# C. Export mean height_m per treatment to outputs/practice_summary.csv.
# Answers: 14 rows; pooled mean about 0.24884 m. See 01_solutions.py after trying.

# %% Optional after the hour: inspect model assumptions
# R: plot(model, which = 1); plot(model, which = 2)
fig, axes = plt.subplots(1, 2, figsize=(9, 4))
axes[0].scatter(model.fittedvalues, model.resid, alpha=0.7)
axes[0].axhline(0, color="black", linestyle="--")
axes[0].set(xlabel="Fitted height (cm)", ylabel="Residual (cm)",
            title="Look for curves or a widening spread")
sm.qqplot(model.resid, line="s", ax=axes[1])
axes[1].set_title("Residual Q–Q plot")
fig.tight_layout()
fig.savefig(out / "model_diagnostics.png", dpi=200)
plt.show()
plt.close(fig)
