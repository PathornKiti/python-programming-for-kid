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
  no extra windows, no setup beyond the first install.
* Later lessons hand the kid a real **clickable canvas** — freeform pixel
  art, a bubble-popping game — so it's not turtles-and-loops the whole way
  through.
* Finishing a lesson unlocks a badge 🏅 — a small, immediate reward for kids
  who like to see progress.

## Getting started

A grown-up does the one-time setup. The quickest way, from inside this
folder:

* **macOS / Linux:** `./setup.sh`
* **Windows:** double-click `setup.bat`

That checks for Python (installing it if needed), sets everything up, and
offers to open the lessons. Full details and a manual path are in
[`SETUP.md`](SETUP.md).

After that, kids can just:

1. Run `make notebook` (or open **Jupyter**).
2. Open `lessons/00_welcome/00_welcome.ipynb`.
3. Click "Run" and follow Py!

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
