"""
Lesson 11: Maze Runner -- Dungeon Crawler
==========================================

A little knight named Py just dropped into the first of five dungeons!
Run this file:

    python maze_runner.py

One window, three panels, all visible together:

  * DUNGEON MAP (left)   -- always on screen, so you can watch Py while
                            you build and while it runs.
  * BLOCKS (middle)       -- drag one of these into YOUR PROGRAM:
        forward()             take one step in the direction Py is facing
        turn_left()            turn left in place (no step)
        turn_right()            turn right in place (no step)
        repeat forward x N       take N steps forward -- use the - / +
                                 buttons on the block to change N
        if blocked: right() else: forward()
                                 look at the cell ahead first. If it's a
                                 wall, a trap, or a monster, turn right
                                 instead of walking into it.
        repeat (if blocked...) x N
                                 the block above, repeated N times.

  * YOUR PROGRAM (right) -- the blocks you've dragged in, top to bottom.
    Drag a block out and drop it outside this column to remove it.
    Long programs scroll -- use the mouse wheel over the column.

Click RUN to watch Py play out your program right there on the map (the
block that's currently running lights up). If Py reaches the gold
star, the SAME program keeps going straight into the next dungeon --
you don't start over! Walking into a wall just bonks Py in place, but
stepping on a trap or into a monster sends Py back to the start of
THAT dungeon -- and your program keeps consuming commands from there.
The window never closes on its own: it just drops you back into
building mode so you can drag in more blocks and click RUN again.

--------------------------------------------------------------------
Dungeon 1 (The Long Hall) just needs a handful of forward/turn blocks.
Dungeon 2 (The Crossroads) takes some trial and error -- watch where
Py bonks and adjust. Dungeon 3 (The Spiral Vault) is a perfect spiral:
ten "repeat forward x N" blocks (N = 10, 9, 8, ... 1), each followed by
a turn_right() block, will walk Py all the way to the center.

Dungeon 4 (The Trap Hall) and Dungeon 5 (The Monster Crypt) hide traps
and monsters right on the path -- a blind forward() will walk straight
into one sooner or later. That's what "if blocked: right() else:
forward()" is for: it senses what's ahead before committing to the
step, the same way `if` / `else` let you make a decision back in
Lesson 5 instead of guessing.
--------------------------------------------------------------------
"""
from block_editor import run_block_editor

run_block_editor()
