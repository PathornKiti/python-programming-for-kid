# Setup (for grown-ups)

This is a one-time, ~10 minute setup. After this, your kid can just open
Jupyter and start clicking.

## Easiest way: one command

If you don't want to think about any of the steps below, just run the
bootstrap script from inside this folder. It checks for Python, installs
it if it's missing, sets everything up, and offers to open the lessons.

* **macOS / Linux** — in Terminal:

  ```bash
  ./setup.sh
  ```

* **Windows** — double-click **`setup.bat`**, or run it from Command Prompt:

  ```bat
  setup.bat
  ```

That's the whole setup. Everything below is the same thing done by hand,
in case you'd rather do it step by step or something goes wrong.

> **A note on `make`:** on macOS the script also makes sure `make` is
> available (it comes with Apple's Command Line Tools), so afterwards you
> can start the lessons with `make notebook`. Windows doesn't use `make` —
> `setup.bat` does everything itself and tells you the command to launch.

---

## Doing it by hand

### 1. Install Python

Download Python 3.10+ from [python.org/downloads](https://www.python.org/downloads/)
and install it. On the first screen of the Windows installer, check
**"Add Python to PATH"**.

Check it worked by opening a terminal (macOS: Terminal, Windows: Command
Prompt) and running:

```bash
python3 --version
```

### 2. Install the project's dependencies

From inside this repo folder, run:

```bash
make setup
```

This builds an isolated `.venv` and installs Jupyter, the interactive
widgets, and the inline turtle/canvas graphics libraries used by the
lessons. (No `make`? Use `pip install -r requirements.txt` instead.)

### 3. Launch Jupyter

```bash
make notebook
```

This opens a browser tab file-browser. Navigate into `lessons/00_welcome/`
and open `00_welcome.ipynb`.

### 4. Show your kid how to run a cell

* Click on a gray code cell.
* Press **Shift + Enter** (or click the ▶ Run button) to run it and move to
  the next one.
* Cells run top to bottom — if something looks broken, "Restart & Run All"
  (in the Kernel/Run menu) is a safe fix.

That's it — from here, [`lessons/README.md`](lessons/README.md) has the
suggested order.

## Troubleshooting

* **`pip: command not found`** — try `pip3` instead of `pip`.
* **Turtle drawings don't show up** — make sure the cell that says
  `from ColabTurtlePlus.Turtle import *` ran without a red error first.
* **Buttons in a quiz don't do anything** — run the cell again; some
  Jupyter setups need `jupyter nbextension enable --py widgetsnbextension`
  for older Jupyter Notebook versions (not needed on JupyterLab 4+).
