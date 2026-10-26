# Python for an R user

A first, one-hour **hands-on analysis lesson**, written for someone who already
works in R. Your knowledge of data frames, model formulas, study design, and
statistical interpretation transfers. The new work is learning Python's syntax,
pandas' data operations, and how Python environments work. No previous Python is assumed.

**Start here:** [setup](SETUP.md), then [the guided lesson](lessons/01_intro.md).
Open [the companion Python script](lessons/01_intro.py) alongside the guide in RStudio.

## What you will do

Use a small, explicitly simulated seedling dataset to read a CSV, inspect and
clean data, filter/select/mutate/group, summarize one variable, run a one-sample
t-test, fit and interpret a linear model, make figures, and export tables and figures.
One dataset carries through the whole workflow. All analysis runs offline after setup.

| Time | Activity |
|---|---|
| Before the hour | Download repo, open project, install Python and packages via reticulate |
| 0–10 min | Imports, objects, lists, indexing, functions, indentation |
| 10–25 min | Read, inspect, clean, and wrangle data |
| 25–35 min | Univariate summaries and one-sample t-test |
| 35–48 min | Linear model and interpretation |
| 48–56 min | Figures and exported results |
| 56–60 min | Small independent exercise |

The hour is a first guided pass, not mastery. Installation/downloads can add
10–30 minutes or more; if you have only one hour total, do setup and sections
1–3 first and finish modeling/export next time. Optional material is clearly marked.

## Stay in RStudio?

Yes, for this lesson. RStudio can run `.py` selections through the R package
`reticulate`. You can keep familiar editing habits while writing ordinary Python.
There is no requirement to translate every analysis through R. A different editor
can wait until your team's workflow or later image-classification work calls for it.
See [Posit's Python guide](https://docs.posit.co/ide/user/ide/guide/environments/py/python.html).

## Contents

- [SETUP.md](SETUP.md): exact RStudio setup; optional terminal route; troubleshooting.
- [lessons/01_intro.md](lessons/01_intro.md): explanations, checkpoints, interpretation.
- [lessons/01_intro.py](lessons/01_intro.py): runnable, commented analysis, in lesson order.
- [lessons/01_solutions.py](lessons/01_solutions.py): exercise answers; try first.
- [reference/r_to_python.md](reference/r_to_python.md): R/Python translation and vocabulary.
- [data/README.md](data/README.md): data dictionary and simulation details.
- [data/seedlings.csv](data/seedlings.csv): bundled teaching data, including three missing values.
- [scripts/make_data.py](scripts/make_data.py): deterministic dataset generator; optional.
- [outputs/README.md](outputs/README.md): files your analysis creates.
- [VALIDATION.md](VALIDATION.md): how the materials were checked and expected results.

## After lesson 1

Suggested next steps: (2) joins, reshaping, functions, and project organization;
(3) categorical predictors, interactions, diagnostics, GLMs, and repeated measures;
(4) loading images, arrays, labels, and reproducible train/validation/test splits.
The first lesson deliberately leaves classes, deep learning, and deployment for later.

Teaching materials prepared October 26, 2026. Package versions are pinned for this
lesson; use your colleagues' agreed environment for production project work.
