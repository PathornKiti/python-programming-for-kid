# Setup (for grown-ups)

This is a one-time setup. After this, your kid can open Jupyter and start
clicking through Py's Python Adventure.

## Important: Python is manual

The project helpers do **not** install Python, Homebrew, winget, or other
system tools. A grown-up installs Python first so nothing surprising changes
on the computer.

1. Download Python 3.10+ from <https://www.python.org/downloads/>.
2. Install it.
3. On Windows, tick **Add python.exe to PATH** on the first installer screen.
4. Close and reopen your terminal.

## Easiest setup

From inside this folder:

* **macOS or Windows with Make:**

  ```bash
  make setup
  ```

* **Windows without Make:** double-click **`setup.bat`**, or run:

  ```bat
  setup.bat
  ```

* **macOS helper check:**

  ```bash
  ./setup.sh
  ```

The setup creates a local `.venv` toolbox and installs Jupyter, widgets,
inline turtle graphics, and canvas tools from `requirements.txt`.

## Start the lessons

* **macOS or Windows with Make:**

  ```bash
  make start
  ```

* **Windows without Make:**

  ```bat
  .venv\Scripts\jupyter notebook lessons
  ```

* **macOS manual start:**

  ```bash
  .venv/bin/jupyter notebook lessons
  ```

## Manual setup, step by step

### macOS Terminal

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
.venv/bin/jupyter notebook lessons
```

### Windows Command Prompt

```bat
py -3 -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\jupyter notebook lessons
```

## Show your kid how to run a cell

* In Jupyter, open the `00_welcome` folder, then open `00_welcome.ipynb`.
* Click on a gray code cell.
* Press **Shift + Enter** or click the ▶ Run button.
* Run cells from top to bottom.
* If something looks broken, use **Restart & Run All** from Jupyter's menu.

## Troubleshooting

* **`python3: command not found` on macOS** — install Python from
  <https://www.python.org/downloads/>, then reopen Terminal.
* **`py` is not recognized on Windows** — reinstall Python and tick
  **Add python.exe to PATH**, then reopen Command Prompt.
* **`make` is not recognized on Windows** — use `setup.bat` and the Windows
  manual start command instead.
* **Turtle drawings don't show up** — make sure the cell that says
  `from ColabTurtlePlus.Turtle import *` ran without a red error first.
* **Buttons in a quiz don't do anything** — run the cell again; older
  Jupyter Notebook installs may need widgets enabled, but JupyterLab 4+
  usually works without extra steps.
