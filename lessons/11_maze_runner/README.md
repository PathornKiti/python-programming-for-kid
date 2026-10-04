# 🧩 Lesson 11: Maze Runner — Dungeon Crawler

This lesson is different from the others: instead of a notebook, a
little knight named Py crawls through **ten dungeons** in its own
**pygame** window with a drag-and-drop block editor.

## How to run it

From the project folder, with the setup already done (`make setup`):

```bash
make maze
```

Or run it directly:

```bash
.venv/bin/python lessons/11_maze_runner/maze_runner.py
```

(Windows: `.venv\Scripts\python lessons\11_maze_runner\maze_runner.py`)

## Build your program

One window, three panels, all visible at once:

* **DUNGEON MAP** (left) — always on screen, so you can see exactly
  where Py is while you build and while it runs.
* **BLOCKS** (middle) — drag one of these into **YOUR PROGRAM**:
  * `forward()` — take one step in the direction Py is facing
  * `turn_left()` / `turn_right()` — turn in place (no step)
  * `repeat forward x N` — take N steps forward; click `-` / `+` to
    change N
  * `if blocked: right() else: forward()` — **look before stepping.**
    Checks the cell right in front of Py. If it's a wall, a trap, or a
    monster, Py turns right instead of walking into it; otherwise it
    steps forward like normal.
  * `repeat (if blocked...) x N` — the block above, repeated N times,
    for when you need to check-and-step over and over.
* **YOUR PROGRAM** (right) — the blocks you've dragged in, top to
  bottom. Drag a block out and drop it outside this column to remove
  it. Longer programs scroll — use the mouse wheel over the column, or
  just keep dragging new blocks to the bottom and it scrolls to follow.

Click **RUN** and watch Py play out your program right there on the
map — the block currently running lights up with a white outline so
you can follow along. Py starts each dungeon facing **East**, at the
green dot. Get Py to the **gold star** and the dungeon is cleared: your
program is wiped clean and the next dungeon appears, ready for a fresh
program.

If Py bonks into a wall, steps on a **trap** 🔺, or runs into a
**monster** 👾, the window doesn't close — you're dropped right back
into building mode. Drag in more blocks and click **RUN** again; your
program (and Py's spot on the map) is still there.

## Why "if blocked... else..." matters

Walking into a wall just bonks Py in place — no harm done, try again.
But a **trap** or a **monster** is worse: if Py steps onto one, it gets
sent all the way back to the start of *that* dungeon, and your program
keeps consuming commands from there. A blind `forward()` can't tell the
difference between safe floor and a trap until it's too late.

That's what the `if blocked: right() else: forward()` block is for —
it senses what's ahead *before* committing to the step, the same way
you used `if` / `else` back in Lesson 5 to make a decision instead of
guessing. Dungeons 4 and 5 are built so a plain `forward()` walks
straight into trouble somewhere along the way; the conditional block
is what gets Py through safely.

## Your task

1. **Dungeon 1 (The Long Hall):** a short warm-up — get Py from the
   green dot to the star with just `forward()` and turn blocks.
2. **Dungeon 2 (The Crossroads):** trickier. Run your program, watch
   where Py bonks or stalls, then drag in more blocks and try again.
3. **Dungeon 3 (The Spiral Vault):** this one is a perfect spiral —
   dragging in 60+ `forward()` blocks by hand would take forever. Use
   ten `repeat forward x N` blocks instead, with N counting *down*
   (10, 9, 8, ... 1), each followed by a `turn_right()` block.
4. **Dungeon 4 (The Trap Hall):** a wide, open hall with 🔺 traps
   scattered across it. There's always a clear lane past each one — use
   `if blocked: right() else: forward()` at the risky spots instead of
   guessing which lane is safe.
5. **Dungeon 5 (The Monster Crypt):** the final dungeon — a long, bendy
   corridor patrolled by 👾 monsters as well as traps. Combine
   everything: `forward()`/turn blocks for the parts you know, and the
   conditional block for the parts you don't.
6. **Dungeon 6 (The Zigzag):** alternating left and right turns.
7. **Dungeon 7 (The Counter-Spiral):** a spiral that only ever turns
   *left*. Try the new `if blocked: left() else: forward()` blocks!
8. **Dungeon 8 (The Trap Garden):** a wall of traps with one gap — find it.
9. **Dungeon 9 (The Monster Maze):** monsters everywhere; weave between them.
10. **Dungeon 10 (The Final Gauntlet):** twisty corridors, traps and
    monsters together. Some routes are decoys!

Clear all ten dungeons to unlock the **🧩 Maze Solver** badge (printed
in the terminal, and shown in the window).

## Stuck? Peek at working solutions

<details>
<summary>Dungeon 2</summary>

```
forward(), forward(), turn_right(),
forward(), forward(), turn_right(),
forward(), forward(), turn_left(),
forward(), forward(), turn_left(),
repeat forward x 6,
turn_right(), forward()
```

</details>

<details>
<summary>Dungeon 4</summary>

```
forward(), turn_right(), forward(), turn_left(),
repeat forward x 5,
turn_left(), forward(), turn_right(),
repeat forward x 4,
turn_right(), forward()
```

(Or swap any of those `forward()` runs for
`if blocked: right() else: forward()` blocks — since the path really is
clear there, the conditional block just steps forward anyway.)

</details>

## For advanced kids: skip the blocks, write real Python

The block editor is just a friendly front end — under the hood every
block turns into one of four strings: `"forward"`, `"left"`,
`"right"`, or `"if_danger"`. If you'd rather write the list directly in
code (like earlier lessons), open a Python file in this folder and
call the engine yourself:

```python
from dungeon_engine import run_commands

commands = ["right", "forward", "forward", "left",
            "forward", "forward", "forward", "forward"]
run_commands(commands)
```
