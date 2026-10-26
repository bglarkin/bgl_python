# Setup: RStudio first

Setup happens **before** the one-hour practice session. You need internet here,
but the lesson's data are bundled, so analysis itself needs no downloads.

## 1. Get the files and open an RStudio project

In RStudio, choose **File > New Project > Version Control > Git**, use
`https://github.com/bglarkin/bgl_python.git`, and choose a parent folder.
If Git is not configured, GitHub's **Code > Download ZIP** is fine: unzip it,
then open `bgl_python.Rproj`. Do one route only.

The project folder should contain `requirements.txt`, `data/`, and `lessons/`.
In the **R console** (`>`), run:

```r
getwd()
file.exists("data/seedlings.csv")  # must be TRUE
install.packages("reticulate")    # one-time installation/update from CRAN
```

After installation, choose **Session > Restart R**. We need reticulate >= 1.41.
Do not launch Python or run Python code before the next step.

## 2. Let reticulate obtain Python and packages

In the **R console**, run:

```r
source("setup_rstudio.R")
```

This requests Python 3.12 and the package versions in `requirements.txt`.
Reticulate obtains Python and resolves packages into its managed, cached environment.
Approve any download prompt it presents. You do **not** need a separate Python
installer, Anaconda, or a global `pip install` for this route.
The first run can take several minutes. `py_config()` prints the chosen Python
path/version so you can see what you are actually using.

Run `source("setup_rstudio.R")` after each R-session restart, before Python starts.
It declares this session's requirements; cached downloads can be reused.
The script intentionally selects managed Python for this session. It does not
edit your global RStudio interpreter preference or install packages into another project.

This follows reticulate's current [package setup](https://rstudio.github.io/reticulate/articles/python_packages.html)
and [py_require reference](https://rstudio.github.io/reticulate/reference/py_require.html).
The managed environment belongs to reticulate; it is separate from a `.venv` you
might create with the optional terminal route below.

## 3. Run ordinary Python in RStudio

Open `lessons/01_intro.py` using **File > Open File**. Select the first block
and press **Cmd+Enter** (Mac) or **Ctrl+Enter** (Windows/Linux). Continue top to
bottom with the guide. Select an entire indented `if`, `for`, or `def` block,
including its header; do not send just its first line.

The console may show `>>>` instead of `>`: you are now talking to Python.
`...` means Python is waiting for the remainder of a block. Send the complete
block, or press Escape to cancel and try again. Type `exit` in reticulate's Python
console to return to R. Use the file's **Run** controls for Python selections.

Explicit `print()` calls make output appear when the whole script runs too.
Plots appear in the available graphics display; the saved files in `outputs/`
are the reliable result if your plot pane does not show them.

## Troubleshooting

| Symptom | What to do |
|---|---|
| `could not find function "py_require"` | Update reticulate, restart R, source setup again. |
| Wrong Python path/version | Restart R, then source setup **before** any Python. Python cannot be swapped after initialization. |
| `ModuleNotFoundError` | Use the setup script in a fresh session; a package installed in another Python is not available here. |
| `FileNotFoundError` | Open `bgl_python.Rproj`; in Python run `print(Path.cwd())`. The working folder must contain `data/`. |
| `NameError: pd is not defined` | Run the import block first, then run sections in order. |
| `SyntaxError` on `<-` or `library(...)` | You sent R to Python. Check the console language and file extension. |
| Download/proxy/certificate failure | Check network access to CRAN/Python package downloads; use your institution's approved proxy/mirror or ask IT. Do not disable certificate verification. |

## Optional: run without RStudio

Skip this for the first lesson. If a colleague already uses terminal Python,
install **Python 3.12** using [python.org](https://www.python.org/downloads/),
then open a terminal **inside this repository folder**. Do not type these commands
in the R or Python console.

macOS/Linux:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python lessons/01_intro.py
```

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe lessons/01_intro.py
```

Using the environment's executable avoids activation and makes it explicit which
Python receives packages. `python -m pip` means “run pip using this Python.”
See the [Python environment tutorial](https://docs.python.org/3/tutorial/venv.html).
For a complete package snapshot from the author's tested environment see
`requirements-tested.txt`; `requirements.txt` pins the five directly used packages.
