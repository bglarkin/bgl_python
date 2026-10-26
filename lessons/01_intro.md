# Lesson 1: an R analyst's first hour of Python

Open this guide and `01_intro.py` side by side. Complete [setup](../SETUP.md)
first. Run the numbered Python sections in order; the explanations below refer
to the objects created there. Pause at each checkpoint before moving on.
All results are from simulated data.

## 1. Read Python through your R knowledge — 0–10 minutes

Run section 1. `import pandas as pd` makes the pandas package available under
the conventional short name `pd`. It does not download it. You installed packages
during setup; you import them again in each new Python session. `pd` is a nickname
we choose, not a keyword. `from scipy import stats` imports just a named component.

An **interpreter** executes Python code. A **package** is installed software; a
**module** is an importable unit, often a `.py` file. People say **library** broadly
for reusable code. An **environment** holds a particular interpreter and installed
packages. Installing a package into one environment does not install it into all
of them. `requirements.txt` records this lesson's direct package versions.

The tools have distinct jobs:

| Tool | Role | Familiar R comparison |
|---|---|---|
| pandas | Rectangular data and wrangling | data.frame/tibble and dplyr |
| NumPy | Numeric arrays and vectorized math | numeric vectors/matrices |
| SciPy | Tests and scientific routines | selected functions from stats |
| statsmodels | Fitted statistical models and inference | lm/glm and summaries |
| Matplotlib | Figures and saved graphics | base plotting or a plotting backend |
| pathlib | Filesystem paths; part of Python itself | file.path and related tools |

Python uses `=` for assignment and `==` for comparison. Names are case-sensitive.
Strings use quotes; booleans are `True`/`False`; `None` means absence of a value.
`#` starts a comment. There is no need for a semicolon at the end of a line.

A Python list uses square brackets, starts counting at **0**, and is not an R
numeric vector. `heights[:2]` returns positions 0 and 1: the stop position is
excluded. `heights * 2` repeats a list; `np.array(heights) * 2` doubles the values.
This distinction matters later when images are represented as arrays.

A **function** is called as `function(arguments)`. A **method** is a function
attached to an object: `df.head()`. An **attribute** is information on an object:
`df.shape`. `df["height_cm"]` retrieves a column. There is no universal `$`
operator corresponding to R's; use brackets for column selection here.

`def` creates a function; `return` sends its result back. A colon and four spaces
of indentation define its body. `for` and `if` blocks use the same convention.
The parentheses around long expressions allow line breaks without backslashes.

**Try:** change the function call to `cm_to_mm(7.2)`. Predict, then run.
**Checkpoint:** the result is `72.0`; `heights[0]` gives `10.0`.

## 2. Import, inspect, and wrangle — 10–25 minutes

Run section 2 in small blocks. `Path.cwd()` is the current working folder,
analogous to `getwd()`. `/` joins path components for a `Path` object; it is not
division in this context. Paths are relative to the open project folder.

`pd.read_csv(...)` returns a pandas **DataFrame**. A single column such as
`raw["height_cm"]` is a **Series**, a one-dimensional labeled data object.
The row index labels are separate from columns; our real identifier is
`seedling_id`, not the automatically assigned row index.

Inspect `head()`, `shape`, `info()`, and `isna().sum()` before analyzing.
`info()` reports column types and nonmissing counts; it prints directly rather
than returning a table to print. Empty numeric CSV cells become missing `NaN`.
Use `isna()` rather than testing equality to `NaN`.

We drop rows missing height, moisture, or treatment and explicitly print the
number lost. `.copy()` creates a separate working table. This is complete-case
analysis for a teaching example, not a general missing-data prescription.
The height-only analysis could retain 58 observations; here every section uses
the same 57 complete cases to make the workflow easy to follow.

The key wrangling patterns in the script are:

```python
df["height_mm"] = df["height_cm"] * 10        # mutate
df[["seedling_id", "height_cm"]]              # select columns (double brackets)
df.loc[df["height_cm"] > 25, ["seedling_id"]] # filter rows and select columns
df.sort_values("height_cm", ascending=False)  # arrange descending
```

`.loc[rows, columns]` selects by labels/conditions; `.iloc[rows, columns]`
selects by integer positions. `df.iloc[0]` gets the first row. After dropping
rows, index labels can have gaps; `.loc[5]` and `.iloc[5]` need not refer to
the same observation.

For Series, combine conditions using **`&`** (and), **`|`** (or), and **`~`**
(not), with parentheses around each comparison. Python's plain `and`/`or`
operate on single truth values and will fail on a whole Series.

`groupby(...).agg(...)` is the analogue of `group_by()` plus `summarise()`.
`n=("height_cm", "size")` names an output column and says which input column
and operation to use. `reset_index()` brings group labels back into ordinary
columns. Chaining methods with dots is common in pandas. Most return a result;
assign that result if you want to keep it. Avoid chained assignment like
`df[df["height_cm"] > 25]["flag"] = True`; use `.loc` to assign instead.

**Try:** inspect `df[["height_cm", "height_mm"]].head()` and verify the units.
**Checkpoint:** 60 raw rows, 57 clean rows; treatment counts 29 control and
28 fertilized. The CSV has two missing heights and one missing moisture value.

## 3. Summarize one variable and test a mean — 25–35 minutes

Run section 3. `describe()` supplies count, mean, sample SD, min, quartiles,
and max. `value_counts()` counts category membership. `.T` transposes the
summary so each variable occupies one row.

The one-sample t-test asks whether **control seedlings' population mean height
differs from 23 cm**. This arbitrary practice benchmark is specified in advance;
it has no real biological meaning. R analogue:

```r
t.test(df$height_cm[df$treatment == "control"], mu = 23)
```

`stats.ttest_1samp(...)` returns an object. `.statistic`, `.pvalue`, and `.df`
are attributes of that result. Its `.confidence_interval()` is a method returning
a 95% interval for the **population mean**, not the mean-minus-23 difference.

Interpret the estimated mean and interval first. A p-value measures incompatibility
with the null model; it is not the probability that the null hypothesis is true.
This test assumes independent observations and an adequately well-behaved sampling
distribution of the mean; examine the histogram for extreme skew/outliers.
It does not compare the two treatments. Changing the benchmark changes the
question, not just a software setting.

**Try:** locate `n`, `mean_cm`, `p_value`, `mean_ci_low`, and `mean_ci_high`
in `t_table`. Explain the interval in words before reading the validation notes.

## 4. Fit a familiar parametric model — 35–48 minutes

Run section 4. The model is:

`height_cm = intercept + moisture slope * soil_moisture_pct + treatment offset + error`

`smf.ols("height_cm ~ soil_moisture_pct + C(treatment)", data=df).fit()`
uses a quoted R-style formula and fits ordinary least squares. The formula
interface includes an intercept. `C(treatment)` explicitly encodes treatment
as categorical; the categories set earlier make **control** the reference.
R counterpart: `lm(height_cm ~ soil_moisture_pct + treatment, data=df)` with
the same reference category.

Read the coefficient table as you would an R linear model:

- `soil_moisture_pct`: expected height difference in cm for a **one percentage
  point** increase in moisture, holding treatment fixed.
- `C(treatment)[T.fertilized]`: expected fertilized-minus-control height
  difference in cm at the same moisture.
- `Intercept`: predicted control height at zero moisture. Zero is outside our
  observed range, so this parameter is needed mathematically but has limited
  scientific interpretation here.
- Confidence intervals and p-values describe coefficient uncertainty conditional
  on the model. R-squared describes in-sample variation explained, not causality
  or predictive accuracy on new observations.

The `+` assumes the same moisture slope for both groups. We have not fitted an
interaction. The plotted lines are fitted **means**, with no confidence or
prediction bands. They are not trajectories of individual seedlings.

Check independence from study design, linearity, residual spread, outliers, and
residual normality for small-sample inference. Normality concerns the errors,
not a requirement that moisture itself be normally distributed. The optional
diagnostic block makes residual-vs-fitted and Q–Q plots; run it after the hour
or before drawing substantive conclusions from a real analysis. A plot cannot
establish independence. Multiple seedlings in a plot or repeated measurements
would need attention to the sampling structure.

**Try:** find the moisture coefficient and interpret its units. Does the treatment
estimate have the same sign as the difference in group means? The model adjusts
for moisture; the simple group means do not.

## 5. Make figures and export results — 48–56 minutes

Run section 5. `fig` is the whole figure; `ax` is the plotting area within it.
You add points, lines, labels, and a legend to `ax`, then save `fig`. The loop
does the same plotting steps for each treatment; the colon and indentation
define the repeated commands.

`model.predict(grid)` predicts expected heights from a new DataFrame containing
the model's predictors. The grid spans each group's observed moisture range
to avoid drawing lines beyond that group's data. `np.linspace(..., 100)` creates
100 evenly spaced values.

Save before closing a figure. PNG at 300 dpi is convenient for documents; PDF
preserves vector lines/text. `to_csv(index=False)` prevents the automatic row
index becoming an extra CSV column. Keep scientific precision in exported
numbers; round the display or final presentation table as appropriate.
The HTML coefficient table opens in a browser. The text summary records the
model results, while CSV tables are ready for R or spreadsheet software.

**Checkpoint:** open `outputs/height_vs_moisture.png` and
`outputs/model_coefficients.csv`. Check units, category labels, and column names.
Rerunning overwrites the same outputs. See [the output inventory](../outputs/README.md).

## 6. Four-minute independent task — 56–60 minutes

1. Select control seedlings with moisture **greater than 30%**. Count them.
2. Add a `height_m` column in meters and compute its overall mean.
3. Export mean `height_m` by treatment to `outputs/practice_summary.csv`.

Use the script and [translation reference](../reference/r_to_python.md), then
check [the solutions](01_solutions.py). Being able to modify an analysis is the
goal; memorizing every method name is not necessary.

## After the hour

Run the optional diagnostic block, then try changing the model to
`"height_cm ~ soil_moisture_pct"`. Compare its moisture estimate with the
adjusted model. That is a different model question, so keep the distinction clear.
Use [VALIDATION.md](../VALIDATION.md) for numerical checks.

Official references for follow-up: [Python basics](https://docs.python.org/3/tutorial/introduction.html),
[pandas for R users](https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_r.html),
[statsmodels formulas](https://www.statsmodels.org/stable/example_formulas.html),
[SciPy's one-sample test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_1samp.html),
and [Matplotlib export](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html).
