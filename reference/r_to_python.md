# R → Python desk reference

Examples assume `import pandas as pd`, `import numpy as np`,
`import statsmodels.formula.api as smf`, and a DataFrame named `df`.

| R | Python | Note |
|---|---|---|
| `x <- 3` | `x = 3` | Assignment |
| `TRUE`, `FALSE`, `NULL` | `True`, `False`, `None` | Capitalization matters |
| `c(1, 2, 3)` | `np.array([1, 2, 3])` | A list `[1, 2, 3]` has different arithmetic |
| `x[1]` | `x[0]` | First element by position |
| `x[1:3]` | `x[:3]` | Python stop is excluded |
| `length(x)` | `len(x)` | Number of items |
| `dim(df)` | `df.shape` | Attribute, no `()` |
| `names(df)` | `df.columns` | Column index |
| `str(df)` | `df.info()` | Similar purpose, different return behavior |
| `head(df)` | `df.head()` | Method call |
| `read.csv("file.csv")` | `pd.read_csv("file.csv")` | CSV → data frame |
| `df$height_cm` | `df["height_cm"]` | Returns a Series |
| `df[, c("height_cm", "treatment")]` | `df[["height_cm", "treatment"]]` | Returns a DataFrame |
| `df[1:3, ]` | `df.iloc[:3]` | First three rows by position |
| `subset(df, height_cm > 25)` | `df.loc[df["height_cm"] > 25]` | Filter |
| `mutate(df, height_mm = height_cm * 10)` | `df.assign(height_mm=df["height_cm"] * 10)` | Assign the returned frame |
| `arrange(df, desc(height_cm))` | `df.sort_values("height_cm", ascending=False)` | Sort |
| `is.na(df)` | `df.isna()` | Missing-value mask |
| `mean(x, na.rm=TRUE)` | `x.mean()` | For pandas numeric Series, skips missing by default |
| `sd(x)` | `x.std(ddof=1)` | pandas sample SD; NumPy default differs |
| `table(df$treatment)` | `df["treatment"].value_counts()` | Missing excluded by default |
| `factor(x, levels=c("control", "fertilized"))` | `pd.Categorical(x, categories=["control", "fertilized"])` | Explicit category order |
| `lm(y ~ x, data=df)` | `smf.ols("y ~ x", data=df).fit()` | Formula string, includes intercept |
| `summary(fit)` | `print(fit.summary())` | Fitted-model result |
| `predict(fit, newdata=new)` | `fit.predict(new)` | New predictor DataFrame |
| `write.csv(df, "out.csv", row.names=FALSE)` | `df.to_csv("out.csv", index=False)` | Suppress automatic index |
| `getwd()` | `Path.cwd()` | Requires `from pathlib import Path` |

## Grouped summaries

R:

```r
df |>
  dplyr::group_by(treatment) |>
  dplyr::summarise(n = dplyr::n(), mean_height = mean(height_cm))
```

Python:

```python
summary = (
    df.groupby("treatment", observed=True)
    .agg(n=("height_cm", "size"), mean_height=("height_cm", "mean"))
    .reset_index()
)
```

These means assume the cleaned lesson data. With missing heights, pandas mean
skips them by default whereas R's mean needs `na.rm=TRUE` for that behavior.
`size` counts rows; `count` counts nonmissing values in the selected column.

## Installing versus importing

| Task | Where | Example |
|---|---|---|
| Install the R bridge | R console | `install.packages("reticulate")` |
| Declare Python requirements and obtain managed environment | R console | `source("setup_rstudio.R")` |
| Install into an explicitly selected Python environment (alternative) | Terminal | `.venv/bin/python -m pip install -r requirements.txt` |
| Import already installed Python code | Python | `import pandas as pd` |

Python packages normally come from **PyPI**; R packages commonly come from **CRAN**.
`pip` is a Python package installer. `venv` creates an isolated environment.
`reticulate` is an R package connecting R/RStudio to Python, not a separate
programming language. RStudio is the editor; Python is the language/interpreter.

## Common surprises

- `df.shape` is an attribute; `df.head()` is a method.
- `=` assigns; `==` compares. `<-` is not Python assignment.
- `&`/`|` combine Series masks; surround each comparison with parentheses.
- Lists repeat with `*`; numeric arrays and numeric Series multiply elementwise.
- `.loc` uses labels; `.iloc` uses positions. An index label is not always a row number.
- Many pandas operations return a new result; retain it with assignment.
- Use `df.loc[mask, "column"] = value` for conditional changes.
- Indentation is syntax. Select complete indented blocks in RStudio.
- A fresh session needs imports again. Installed packages persist in the environment.
- Python's formula support is package-specific; R's formula conventions do not
  automatically apply to every modeling library.

Further reading: [pandas' official R comparison](https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_r.html).
