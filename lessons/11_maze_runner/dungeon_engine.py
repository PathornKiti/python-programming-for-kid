"""Dungeon Runner engine — dungeon data + pygame drawing for Lesson 11.

You don't need to edit this file! Open maze_runner.py instead.

How it works, in short: each dungeon is drawn from a little map of text
rows ('#' = wall, '.' = floor, 'S' = start, 'G' = goal star).
DungeonPlayer plays a command list back one step at a time -- when Py
reaches a dungeon's goal, the SAME command list keeps going straight
into the next dungeon instead of starting over. draw_dungeon() /
draw_player() render one dungeon into any rectangle of a pygame window
you give them, so the same code draws the standalone run_commands()
window AND the combined map-and-blocks window in block_editor.py.
"""
import math
import time

import pygame

CELL = 40
MARGIN = 24
BAR_HEIGHT = 70
MOVE_SECONDS = 0.28
TURN_SECONDS = 0.12
BONK_SECONDS = 0.35
HIT_SECONDS = 0.6
STEP_PAUSE = 0.05
FPS = 60

DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # facing: 0=East 1=South 2=West 3=North

COLOR_BG = (24, 22, 33)
COLOR_FLOOR = (214, 205, 214)
COLOR_FLOOR_ALT = (198, 188, 198)
COLOR_WALL = (58, 48, 72)
COLOR_WALL_EDGE = (38, 31, 48)
COLOR_WALL_BRICK = (46, 38, 58)
COLOR_START = (76, 175, 80)
COLOR_GOAL = (255, 202, 40)
COLOR_PLAYER = (66, 133, 244)
COLOR_PLAYER_TRIM = (220, 230, 250)
COLOR_SKIN = (235, 194, 150)
COLOR_TRAP = (183, 45, 45)
COLOR_TRAP_DARK = (110, 20, 20)
COLOR_MONSTER = (128, 60, 160)
COLOR_MONSTER_DARK = (80, 30, 105)
COLOR_BAR_BG = (14, 13, 20)
COLOR_TEXT = (240, 240, 245)
COLOR_MESSAGE = (255, 224, 130)
COLOR_VICTORY = (129, 230, 148)


def parse_dungeon(name, rows):
    """Turn a list of text rows into a dungeon dict the engine can use.
    '#' wall, '.' floor, 'S' start, 'G' goal, 'T' trap, 'M' monster."""
    walls = set()
    traps = set()
    monsters = set()
    start = goal = None
    for r, line in enumerate(rows):
        for c, ch in enumerate(line):
            if ch == "#":
                walls.add((c, r))
            elif ch == "S":
                start = (c, r)
            elif ch == "G":
                goal = (c, r)
            elif ch == "T":
                traps.add((c, r))
            elif ch == "M":
                monsters.add((c, r))
    return {
        "name": name,
        "walls": walls,
        "traps": traps,
        "monsters": monsters,
        "start": start,
        "goal": goal,
        "width": len(rows[0]),
        "height": len(rows),
    }


def is_hazard_ahead(dungeon, col, row, facing):
    """True if the cell in front of (col, row) is a wall, the edge of the
    dungeon, a trap, or a monster -- anything that's not safe to walk
    into blindly."""
    dc, dr = DIRS[facing]
    nc, nr = col + dc, row + dr
    if not (0 <= nc < dungeon["width"] and 0 <= nr < dungeon["height"]):
        return True
    cell = (nc, nr)
    return cell in dungeon["walls"] or cell in dungeon["traps"] or cell in dungeon["monsters"]


DUNGEON_MAPS = [
    (
        "Dungeon 1: The Long Hall",
        [
            "#######",
            "#S....#",
            "#.#####",
            "#....G#",
            "#######",
        ],
    ),
    (
        "Dungeon 2: The Crossroads",
        [
            "#########",
            "#S..#...#",
            "###.#.###",
            "#...#...#",
            "#.#####.#",
            "#.......#",
            "#######G#",
            "#########",
        ],
    ),
    (
        "Dungeon 3: The Spiral Vault",
        [
            "#############",
            "#S..........#",
            "#.#########.#",
            "#.#.......#.#",
            "#.#.#####.#.#",
            "#.#.#...#.#.#",
            "#.#.#.#G#.#.#",
            "#.#.#.###.#.#",
            "#.#.#.....#.#",
            "#.#.#######.#",
            "#.#.........#",
            "#.###########",
            "#............",
            "#############",
        ],
    ),
    (
        "Dungeon 4: The Trap Hall",
        [
            "#############",
            "#S.T..T.....#",
            "#.......T..G#",
            "#############",
        ],
    ),
    (
        "Dungeon 5: The Monster Crypt",
        [
            "#############",
            "#S..M.......#",
            "#.......M...#",
            "######..#####",
            "######T.#####",
            "######..#####",
            "######.T#####",
            "######..#####",
            "######T.#####",
            "######..#####",
            "######..#####",
            "#####...G####",
            "#############",
        ],
    ),
]

DUNGEONS = [parse_dungeon(name, rows) for name, rows in DUNGEON_MAPS]
MAX_DUNGEON_W = max(d["width"] for d in DUNGEONS)
MAX_DUNGEON_H = max(d["height"] for d in DUNGEONS)


def _star_points(cx, cy, outer, inner, points=5):
    pts = []
    step = math.pi / points
    angle = -math.pi / 2
    for i in range(points * 2):
        r = outer if i % 2 == 0 else inner
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        angle += step
    return pts


def dungeon_offset(dungeon, origin, cell, max_w=MAX_DUNGEON_W, max_h=MAX_DUNGEON_H):
    """Top-left pixel of a dungeon's grid, centering it within the
    max_w x max_h bounding box so every dungeon lines up at the same
    scale no matter its own size."""
    ox, oy = origin
    off_x = ox + (max_w - dungeon["width"]) * cell / 2
    off_y = oy + (max_h - dungeon["height"]) * cell / 2
    return off_x, off_y


def cell_center(col, row, dungeon, origin, cell, max_w=MAX_DUNGEON_W, max_h=MAX_DUNGEON_H):
    off_x, off_y = dungeon_offset(dungeon, origin, cell, max_w, max_h)
    return off_x + col * cell + cell / 2, off_y + row * cell + cell / 2


def _draw_trap(screen, cx, cy, cell):
    r = cell * 0.32
    for i in range(4):
        angle = -math.pi / 2 + i * math.pi / 2
        tip = (cx + r * math.cos(angle), cy + r * math.sin(angle))
        pygame.draw.polygon(
            screen,
            COLOR_TRAP,
            [tip, (cx + cell * 0.06, cy + cell * 0.06), (cx - cell * 0.06, cy - cell * 0.06)],
        )
    pygame.draw.circle(screen, COLOR_TRAP_DARK, (cx, cy), cell * 0.1)


def _draw_monster(screen, cx, cy, cell):
    body = pygame.Rect(0, 0, cell * 0.6, cell * 0.5)
    body.center = (cx, cy + cell * 0.04)
    pygame.draw.ellipse(screen, COLOR_MONSTER, body)
    for i in range(3):
        spike_x = body.left + body.width * (i + 0.5) / 3
        pygame.draw.polygon(
            screen,
            COLOR_MONSTER_DARK,
            [(spike_x - cell * 0.06, body.top + 2), (spike_x + cell * 0.06, body.top + 2), (spike_x, body.top - cell * 0.14)],
        )
    eye_y = cy
    for dx in (-cell * 0.14, cell * 0.14):
        pygame.draw.circle(screen, (250, 250, 250), (cx + dx, eye_y), cell * 0.08)
        pygame.draw.circle(screen, (20, 10, 20), (cx + dx, eye_y), cell * 0.04)


def draw_dungeon(screen, dungeon, origin, cell, max_w=MAX_DUNGEON_W, max_h=MAX_DUNGEON_H):
    off_x, off_y = dungeon_offset(dungeon, origin, cell, max_w, max_h)
    for row in range(dungeon["height"]):
        for col in range(dungeon["width"]):
            rect = pygame.Rect(off_x + col * cell, off_y + row * cell, cell, cell)
            if (col, row) in dungeon["walls"]:
                pygame.draw.rect(screen, COLOR_WALL, rect)
                mid_y = rect.top + rect.height // 2
                pygame.draw.line(screen, COLOR_WALL_BRICK, (rect.left, mid_y), (rect.right, mid_y), 1)
                offset = rect.width // 2 if row % 2 == 0 else 0
                mid_x = rect.left + offset
                if rect.left < mid_x < rect.right:
                    pygame.draw.line(screen, COLOR_WALL_BRICK, (mid_x, rect.top), (mid_x, mid_y), 1)
                pygame.draw.rect(screen, COLOR_WALL_EDGE, rect, 2)
            else:
                shade = COLOR_FLOOR if (col + row) % 2 == 0 else COLOR_FLOOR_ALT
                pygame.draw.rect(screen, shade, rect)
                pygame.draw.rect(screen, COLOR_BG, rect, 1)

    sx, sy = cell_center(*dungeon["start"], dungeon, origin, cell, max_w, max_h)
    pygame.draw.circle(screen, COLOR_START, (sx, sy), cell * 0.28)
    pygame.draw.circle(screen, COLOR_BG, (sx, sy), cell * 0.28, 2)

    for tc, tr in dungeon["traps"]:
        cx, cy = cell_center(tc, tr, dungeon, origin, cell, max_w, max_h)
        _draw_trap(screen, cx, cy, cell)

    for mc, mr in dungeon["monsters"]:
        cx, cy = cell_center(mc, mr, dungeon, origin, cell, max_w, max_h)
        _draw_monster(screen, cx, cy, cell)

    gx, gy = cell_center(*dungeon["goal"], dungeon, origin, cell, max_w, max_h)
    pygame.draw.polygon(screen, (255, 235, 160), _star_points(gx, gy, cell * 0.42, cell * 0.18))
    pygame.draw.polygon(screen, COLOR_GOAL, _star_points(gx, gy, cell * 0.32, cell * 0.14))


def draw_player(screen, px, py, facing, cell):
    """A little knight, facing whichever of the 4 directions Py is
    walking -- shown by the nose bump on the helmet and the sword."""
    dx, dy = DIRS[facing]
    perp = (-dy, dx)

    shadow = pygame.Rect(0, 0, cell * 0.5, cell * 0.16)
    shadow.center = (px, py + cell * 0.32)
    pygame.draw.ellipse(screen, (30, 28, 40), shadow)

    leg_w, leg_h = cell * 0.12, cell * 0.18
    for side in (-1, 1):
        leg = pygame.Rect(0, 0, leg_w, leg_h)
        leg.center = (px + side * cell * 0.1, py + cell * 0.22)
        pygame.draw.rect(screen, COLOR_WALL_EDGE, leg, border_radius=3)

    torso = pygame.Rect(0, 0, cell * 0.52, cell * 0.4)
    torso.center = (px, py + cell * 0.02)
    pygame.draw.rect(screen, COLOR_PLAYER, torso, border_radius=8)
    pygame.draw.rect(screen, COLOR_PLAYER_TRIM, torso, width=2, border_radius=8)

    head_center = (px, py - cell * 0.22)
    pygame.draw.circle(screen, COLOR_SKIN, head_center, cell * 0.16)

    helmet_rect = pygame.Rect(0, 0, cell * 0.38, cell * 0.3)
    helmet_rect.center = (px, py - cell * 0.26)
    pygame.draw.arc(screen, COLOR_WALL_EDGE, helmet_rect, math.pi, 2 * math.pi, max(2, int(cell * 0.09)))

    nose = (head_center[0] + dx * cell * 0.14, head_center[1] + dy * cell * 0.14)
    pygame.draw.circle(screen, COLOR_WALL_EDGE, nose, cell * 0.05)

    sword_base = (px + dx * cell * 0.22, py + dy * cell * 0.22)
    sword_tip = (px + dx * cell * 0.5, py + dy * cell * 0.5)
    pygame.draw.line(screen, COLOR_PLAYER_TRIM, sword_base, sword_tip, max(2, int(cell * 0.07)))
    hilt_a = (sword_base[0] + perp[0] * cell * 0.08, sword_base[1] + perp[1] * cell * 0.08)
    hilt_b = (sword_base[0] - perp[0] * cell * 0.08, sword_base[1] - perp[1] * cell * 0.08)
    pygame.draw.line(screen, (110, 84, 58), hilt_a, hilt_b, max(2, int(cell * 0.06)))


class DungeonPlayer:
    """Plays a "forward"/"left"/"right" command list back one step at a
    time, walking through DUNGEONS in order. `cell_center_fn(col, row,
    dungeon)` maps a grid cell to a pixel position -- callers supply it
    so the same class can draw into a full window or a small panel.

    `owners`, if given, is a list the same length as `commands` saying
    which "owner" (e.g. a block index) produced each command; the
    currently-executing owner is exposed as `.current_owner` so a UI
    can highlight it.
    """

    def __init__(self, commands, cell_center_fn, owners=None, start_delay=0.6):
        self.commands = commands
        self.cell_center_fn = cell_center_fn
        self.owners = owners
        self.dungeon_i = 0
        self.cmd_i = 0
        self.dungeon = DUNGEONS[0]
        self.col, self.row = self.dungeon["start"]
        self.facing = 0
        self.px, self.py = cell_center_fn(self.col, self.row, self.dungeon)
        self.anim = None  # (from_xy, to_xy, start_time)
        self.message = f"{self.dungeon['name']} -- go!"
        self.finished = False
        self.victory = False
        self.current_owner = None
        self.next_action_time = time.time() + start_delay

    def _enter_dungeon(self, dungeon, now):
        self.dungeon = dungeon
        self.col, self.row = dungeon["start"]
        self.facing = 0
        self.px, self.py = self.cell_center_fn(self.col, self.row, dungeon)
        self.message = f"{dungeon['name']} -- go!"
        self.next_action_time = now + STEP_PAUSE

    def update(self, now):
        if self.anim is not None:
            t = (now - self.anim[2]) / MOVE_SECONDS
            if t >= 1:
                self.px, self.py = self.anim[1]
                self.anim = None
            else:
                fx, fy = self.anim[0]
                tx, ty = self.anim[1]
                self.px = fx + (tx - fx) * t
                self.py = fy + (ty - fy) * t
            return

        if self.victory or self.finished or now < self.next_action_time:
            return

        here = (self.col, self.row)
        if here in self.dungeon["traps"] or here in self.dungeon["monsters"]:
            if here in self.dungeon["traps"]:
                self.message = "Ouch! A trap! Back to the start of this dungeon."
            else:
                self.message = "A monster got you! Back to the start of this dungeon."
            self.col, self.row = self.dungeon["start"]
            self.facing = 0
            self.px, self.py = self.cell_center_fn(self.col, self.row, self.dungeon)
            self.next_action_time = now + HIT_SECONDS
            return

        if (self.col, self.row) == self.dungeon["goal"]:
            self.dungeon_i += 1
            if self.dungeon_i >= len(DUNGEONS):
                self.victory = True
                print("All dungeons cleared! Badge unlocked: Maze Solver")
            else:
                self._enter_dungeon(DUNGEONS[self.dungeon_i], now)
                print(f"Entering {self.dungeon['name']}")
            return

        if self.cmd_i >= len(self.commands):
            self.finished = True
            self.message = ""
            print("Out of commands before reaching the goal. Add more moves!")
            return

        cmd = self.commands[self.cmd_i]
        if self.owners is not None:
            self.current_owner = self.owners[self.cmd_i]
        self.cmd_i += 1

        if cmd == "forward":
            dc, dr = DIRS[self.facing]
            nc, nr = self.col + dc, self.row + dr
            blocked = (nc, nr) in self.dungeon["walls"] or not (
                0 <= nc < self.dungeon["width"] and 0 <= nr < self.dungeon["height"]
            )
            if blocked:
                self.message = "Bonk! There's a wall there."
                self.next_action_time = now + BONK_SECONDS
            else:
                self.anim = ((self.px, self.py), self.cell_center_fn(nc, nr, self.dungeon), now)
                self.col, self.row = nc, nr
                self.message = ""
        elif cmd == "left":
            self.facing = (self.facing - 1) % 4
            self.message = ""
            self.next_action_time = now + TURN_SECONDS
        elif cmd == "right":
            self.facing = (self.facing + 1) % 4
            self.message = ""
            self.next_action_time = now + TURN_SECONDS
        elif cmd == "if_danger":
            if is_hazard_ahead(self.dungeon, self.col, self.row, self.facing):
                self.facing = (self.facing + 1) % 4
                self.message = ""
                self.next_action_time = now + TURN_SECONDS
            else:
                dc, dr = DIRS[self.facing]
                nc, nr = self.col + dc, self.row + dr
                self.anim = ((self.px, self.py), self.cell_center_fn(nc, nr, self.dungeon), now)
                self.col, self.row = nc, nr
                self.message = ""
        else:
            self.message = f"Unknown command: {cmd!r} (try 'forward', 'left', 'right', or 'if_danger')"
            self.next_action_time = now + 0.3


def _draw_bar(screen, font, big_font, win_w, dungeon_i, message, finished, victory):
    bar_rect = pygame.Rect(0, 0, win_w, BAR_HEIGHT)
    pygame.draw.rect(screen, COLOR_BAR_BG, bar_rect)

    if victory:
        text = big_font.render("All dungeons cleared! Badge unlocked: Maze Solver", True, COLOR_VICTORY)
        screen.blit(text, (16, 20))
        return

    title = f"Dungeon {min(dungeon_i + 1, len(DUNGEONS))} of {len(DUNGEONS)}"
    title_surf = font.render(title, True, COLOR_TEXT)
    screen.blit(title_surf, (16, 10))

    shown = message
    if finished and not message:
        shown = "Out of commands! Add more moves to the list and run again."
    if shown:
        msg_surf = font.render(shown, True, COLOR_MESSAGE)
        screen.blit(msg_surf, (16, 38))


def run_commands(commands):
    """Play back a list of "forward" / "left" / "right" commands in a
    standalone window (no block editor). Handy if you'd rather write
    the list directly in Python -- see the README's "advanced kids"
    section. Close the window (or press Escape) to stop.
    """
    pygame.init()
    pygame.display.set_caption("Dungeon Runner")

    win_w = MAX_DUNGEON_W * CELL + 2 * MARGIN
    win_h = MAX_DUNGEON_H * CELL + 2 * MARGIN + BAR_HEIGHT
    screen = pygame.display.set_mode((win_w, win_h))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    big_font = pygame.font.SysFont(None, 28)

    origin = (MARGIN, MARGIN + BAR_HEIGHT)
    player = DungeonPlayer(commands, lambda c, r, d: cell_center(c, r, d, origin, CELL))

    print(f"Dungeon Runner started: {player.dungeon['name']}")

    running = True
    while running:
        now = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        player.update(now)

        screen.fill(COLOR_BG)
        draw_dungeon(screen, player.dungeon, origin, CELL)
        draw_player(screen, player.px, player.py, player.facing, CELL)
        _draw_bar(screen, font, big_font, win_w, player.dungeon_i, player.message, player.finished, player.victory)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
