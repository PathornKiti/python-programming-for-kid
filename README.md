# 🐢 Py's Python Adventure

A friendly, click-and-see way for kids (ages 7–10) to learn real Python —
guided by **Py the Turtle**, who draws every answer on screen instead of
hiding it behind a blinking cursor.

## How it works

* Lessons live in [`lessons/`](lessons/) as **Jupyter notebooks** — pages that
  mix short stories, a little bit of code, and instant pictures.
* Every notebook is *run*, not just read: click a cell, press
  **Shift + Enter**, and see what happens right away.
* A lot of feedback is **click-to-answer** (buttons, not typing), so kids who
  aren't confident typists yet can still play and learn.
* Py draws with **turtle graphics** that appear right inside the notebook —
  no extra windows after the one-time setup.
* Later lessons hand the kid a real **clickable canvas** — freeform pixel
  art, a bubble-popping game — so it's not turtles-and-loops the whole way
  through.
* Finishing a lesson unlocks a badge 🏅 — a small, immediate reward for kids
  who like to see progress.

## Best student journey

A grown-up should do the setup once. After that, the student only needs one
simple start command.

### 1. Grown-up: install Python manually

This project does **not** install Python for you. That keeps the setup safer
and avoids surprising system changes.

1. Download Python 3.10+ from <https://www.python.org/downloads/>.
2. Install it.
3. On Windows, tick **Add python.exe to PATH** on the first installer screen.
4. Close and reopen your terminal after installing Python.

### 2. Grown-up: run the setup command

Open a terminal in this project folder and run the command for your computer:

| Computer | Setup command | What it does |
| --- | --- | --- |
| macOS | `make setup` | Creates `.venv` and installs the lesson tools. |
| Windows with Make | `make setup` | Creates `.venv` and installs the lesson tools. |
| Windows without Make | `setup.bat` | Does the same setup without needing Make. |
| macOS without Make | `./setup.sh` | Checks Python/Make and prints a manual fallback if Make is missing. |

### 3. Student: start the adventure

Use the easiest command for your computer:

| Computer | Start command |
| --- | --- |
| macOS | `make start` |
| Windows with Make | `make start` |
| Windows without Make | `.venv\Scripts\jupyter notebook lessons\00_welcome\00_welcome.ipynb` |

Jupyter opens in the browser at the welcome lesson. Click a code cell, press
**Shift + Enter**, and follow Py.

### Manual setup, no bash required

If the helper scripts feel confusing, do these steps by hand.

**macOS Terminal:**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
.venv/bin/jupyter notebook lessons/00_welcome/00_welcome.ipynb
```

**Windows Command Prompt:**

```bat
py -3 -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\jupyter notebook lessons\00_welcome\00_welcome.ipynb
```

## Helpful Make commands

* `make help` — show the friendly command menu.
* `make setup` — one-time grown-up setup for macOS or Windows with Make.
* `make start` — open the welcome lesson for the student.
* `make journey` — print the learning path.
* `make clean` — remove the local `.venv` toolbox and notebook caches.

More setup notes and troubleshooting are in [`SETUP.md`](SETUP.md).

## Lesson map

See [`lessons/README.md`](lessons/README.md) for the full path from
"what is a cell?" to "build your own turtle art."

## For grown-ups: design notes

This repo is built around a few deliberate choices:

* **Local Jupyter, not a hosted web app.** Kids get *real* Python (the same
  language grown-ups use), not a simplified dialect, while still getting
  instant visual feedback per cell — no build tooling required.
* **`ColabTurtlePlus` instead of the standard library `turtle`.** Classic
  `turtle` pops up a separate OS window, which is confusing for young kids
  and breaks in many notebook setups. `ColabTurtlePlus` draws inline as part
  of the notebook output, so the picture always appears right under the code
  that made it.
* **`ipycanvas` for freeform/click-based lessons.** Turtle graphics are
  relative-movement (forward/turn) and great for shapes, but not for
  freeform drawing or arcade-style clicking games. `ipycanvas` gives a
  pixel canvas with a built-in `on_mouse_down(x, y)` callback, so lessons
  like Pixel Art Studio and Bubble Pop can react to exactly where a kid
  clicked — no separate window, same inline-in-the-notebook feel as
  `ColabTurtlePlus`.
* **[`helpers/kid_tools.py`](helpers/kid_tools.py)** centralizes the "fun"
  parts — celebration cards, click-to-answer quizzes, badges — so every
  lesson gets the same warm, consistent feedback without copy-pasting HTML
  everywhere. Extend this file first if you want new interaction types.
* **One concept per lesson, always ending in something visual.** Each
  notebook introduces one idea (print, variables, turtle basics, loops,
  if/else, …) and immediately uses it to draw or play, rather than stacking
  up abstract exercises.
* **No typed free-text grading for young kids.** Where correctness matters,
  lessons prefer `quiz()` (click a button) over asking a 7-year-old to type
  an exact string. `check_answer()` is still available for lessons where
  typing *is* the point (like lesson 1, printing your own message).

Contributions/new lessons should follow the pattern in an existing notebook
(see `lessons/03_meet_the_turtle` for a turtle-based one, or
`lessons/02_variables_and_numbers` for a non-turtle one).
