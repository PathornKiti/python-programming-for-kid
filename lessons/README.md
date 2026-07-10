# 🗺️ Lesson map

Work through these in order — each one builds on the last.

| # | Lesson | Teaches | Badge | Status |
|---|--------|---------|-------|--------|
| 00 | [Welcome](00_welcome/00_welcome.ipynb) | How notebooks & cells work | 🧭 Explorer | ✅ |
| 01 | [Hello, Python](01_hello_python/01_hello_python.ipynb) | `print()`, strings | 💬 Chatterbox | ✅ |
| 02 | [Variables & Numbers](02_variables_and_numbers/02_variables_and_numbers.ipynb) | variables, math operators | 🔢 Number Wizard | ✅ |
| 03 | [Meet the Turtle](03_meet_the_turtle/03_meet_the_turtle.ipynb) | turtle moves, color | 🐢 Turtle Trainer | ✅ |
| 04 | [Loops Make Shapes](04_loops_make_shapes/04_loops_make_shapes.ipynb) | `for` loops, `range()` | 🔁 Loop Master | ✅ |
| 05 | [If This, Then That](05_decisions_if_else/05_decisions_if_else.ipynb) | `if` / `else`, comparisons | 🤔 Decision Maker | ✅ |
| 06 | Functions as Spells | `def`, reusing code | 🪄 Spellcaster | 🚧 planned |
| 07 | Lists & the Treasure Chest | lists, indexing, `for` over a list | 📦 Collector | 🚧 planned |
| 08 | Catch the Star | combining loops + if + turtle into a mini game | ⭐ Game Maker | 🚧 planned |
| 09 | Final Project: Draw Your Own World | free-form turtle art using everything so far | 🎨 Python Artist | 🚧 planned |

## Design pattern for new lessons

Every notebook follows the same shape:

1. A short, friendly markdown intro from Py.
2. The standard setup cell (`from helpers.kid_tools import ...`).
3. One new idea at a time, demonstrated in a runnable cell.
4. A "your turn" cell the kid edits directly.
5. A `quiz(...)` or `check_answer(...)` for a quick win.
6. A closing `badge(...)` call.

See [`helpers/kid_tools.py`](../helpers/kid_tools.py) for the available
building blocks (`celebrate`, `try_again`, `check_answer`, `quiz`, `badge`).
