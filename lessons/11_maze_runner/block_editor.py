"""Drag-and-drop block editor for Lesson 11 -- one window, map and all.

You don't need to edit this file! It's the window that opens when you
run maze_runner.py. The dungeon map is always visible on the left.
Drag blocks from the BLOCKS palette on the right into YOUR PROGRAM to
build a list of moves, then click RUN and watch Py walk it out right
there on the map -- no separate window to switch to.

Blocks:
    forward()                  -- take one step forward
    turn_left()                 -- turn left in place
    turn_right()                 -- turn right in place
    repeat forward x N            -- take N steps forward (use the - / +
                                    buttons to change N) -- handy for
                                    Dungeon 3's spiral, instead of
                                    dragging in 60+ blocks!
    if blocked: right() else: forward()
                                -- look at the cell ahead first. If it's
                                   a wall, a trap, or a monster, turn
                                   right instead of walking into it.
    repeat (if blocked...) x N -- the block above, repeated N times --
                                   handy in the trap/monster dungeons
                                   where you don't know what's ahead
                                   until you check.

Drag a block out of YOUR PROGRAM and let go anywhere outside that
column to remove it.
"""
import time

import pygame

import dungeon_engine as de

WIN_W, WIN_H = 1180, 680

MAP_X, MAP_Y = 20, 70
MAP_W = 560
STATUS_H = 40
MAP_H = WIN_H - MAP_Y - STATUS_H - 20
CELL = min(MAP_W // de.MAX_DUNGEON_W, MAP_H // de.MAX_DUNGEON_H)

PANEL_X = MAP_X + MAP_W + 30
PANEL_W = WIN_W - PANEL_X - 20

PALETTE_X = PANEL_X
PALETTE_W = 235
TILE_H = 44
TILE_GAP = 10

SCRIPT_X = PALETTE_X + PALETTE_W + 20
SCRIPT_W = PANEL_X + PANEL_W - SCRIPT_X
SCRIPT_Y0 = 70 + 46
SCRIPT_Y1 = WIN_H - 80
BOTTOM_Y = WIN_H - 64

COLOR_BG = (24, 22, 33)
COLOR_PANEL = (36, 33, 48)
COLOR_HEADER = (240, 240, 245)
COLOR_HINT = (150, 145, 165)
COLOR_FORWARD = (66, 133, 244)
COLOR_TURN = (156, 105, 224)
COLOR_REPEAT = (239, 149, 60)
COLOR_COND = (0, 172, 158)
COLOR_COND_REPEAT = (0, 128, 128)
COLOR_TILE_TEXT = (255, 255, 255)
COLOR_DROP_ZONE = (52, 48, 68)
COLOR_RUN = (76, 175, 80)
COLOR_CLEAR = (200, 80, 80)
COLOR_MESSAGE = (255, 224, 130)
COLOR_HIGHLIGHT = (255, 255, 255)

REPEAT_TYPES = {"repeat_forward", "repeat_if_danger"}

PALETTE_TEMPLATES = [
    {"type": "forward", "label": "forward()", "color": COLOR_FORWARD},
    {"type": "left", "label": "turn_left()", "color": COLOR_TURN},
    {"type": "right", "label": "turn_right()", "color": COLOR_TURN},
    {"type": "repeat_forward", "label": "repeat forward x N", "color": COLOR_REPEAT},
    {"type": "if_danger", "label": "if blocked: right() else: fwd()", "color": COLOR_COND},
    {"type": "repeat_if_danger", "label": "repeat (if blocked...) x N", "color": COLOR_COND_REPEAT},
]


def _new_block(block_type):
    if block_type in REPEAT_TYPES:
        return {"type": block_type, "n": 1}
    return {"type": block_type}


def _block_label(block):
    if block["type"] == "repeat_forward":
        return f"repeat forward x {block['n']}"
    if block["type"] == "repeat_if_danger":
        return f"repeat (if blocked...) x {block['n']}"
    for t in PALETTE_TEMPLATES:
        if t["type"] == block["type"]:
            return t["label"]
    return block["type"]


def _block_color(block):
    for t in PALETTE_TEMPLATES:
        if t["type"] == block["type"]:
            return t["color"]
    return COLOR_FORWARD


def compile_commands_with_owners(script):
    """Flatten the block list into "forward"/"left"/"right"/"if_danger"
    strings. `owners[i]` is the index into `script` of the block that
    produced `commands[i]`, so the UI can highlight the block currently
    running.
    """
    commands = []
    owners = []
    for i, block in enumerate(script):
        if block["type"] == "repeat_forward":
            commands += ["forward"] * block["n"]
            owners += [i] * block["n"]
        elif block["type"] == "repeat_if_danger":
            commands += ["if_danger"] * block["n"]
            owners += [i] * block["n"]
        else:
            commands.append(block["type"])
            owners.append(i)
    return commands, owners


def compile_commands(script):
    commands, _owners = compile_commands_with_owners(script)
    return commands


def _in_script_column(x, y):
    return SCRIPT_X <= x <= SCRIPT_X + SCRIPT_W and SCRIPT_Y0 <= y <= SCRIPT_Y1


def _tile_top(i, scroll):
    return SCRIPT_Y0 + i * (TILE_H + TILE_GAP) - scroll


def _max_scroll(script):
    content_h = len(script) * (TILE_H + TILE_GAP)
    return max(0, content_h - (SCRIPT_Y1 - SCRIPT_Y0))


def _insert_index_for_y(script, y, scroll):
    for i, block in enumerate(script):
        if y < _tile_top(i, scroll) + TILE_H / 2:
            return i
    return len(script)


def _scroll_to_reveal(scroll, index, script):
    """Nudge scroll so the block at `index` is fully visible."""
    abs_top = SCRIPT_Y0 + index * (TILE_H + TILE_GAP)
    abs_bottom = abs_top + TILE_H
    if abs_bottom - scroll > SCRIPT_Y1:
        scroll = abs_bottom - SCRIPT_Y1
    if abs_top - scroll < SCRIPT_Y0:
        scroll = abs_top - SCRIPT_Y0
    return max(0, min(scroll, _max_scroll(script)))


def _map_cell_center(col, row, dungeon):
    return de.cell_center(col, row, dungeon, (MAP_X, MAP_Y), CELL)


def run_block_editor():
    """Open the combined map + block editor window. Stays open across
    build <-> run cycles; only closes on window-close or Escape."""
    pygame.init()
    pygame.display.set_caption("Dungeon Runner")
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 26)
    small_font = pygame.font.SysFont(None, 22)

    script = []
    mode = "build"  # or "playing"
    player = None
    dragging = None  # {"from": "palette"/"script", "block", "offset"}
    message = ""
    message_until = 0
    scroll = 0  # pixels scrolled down in the YOUR PROGRAM column

    run_button = pygame.Rect(SCRIPT_X, BOTTOM_Y, 140, 44)
    clear_button = pygame.Rect(SCRIPT_X + 160, BOTTOM_Y, 140, 44)

    running = True
    while running:
        now = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if mode == "playing":
                    mode = "build"
                else:
                    running = False

            elif mode == "build" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                if run_button.collidepoint(mx, my):
                    if script:
                        commands, owners = compile_commands_with_owners(script)
                        player = de.DungeonPlayer(commands, _map_cell_center, owners=owners)
                        mode = "playing"
                    else:
                        message = "Drag some blocks in first!"
                        message_until = now + 1.5
                    continue
                if clear_button.collidepoint(mx, my):
                    script.clear()
                    scroll = 0
                    continue

                # +/- steppers on repeat tiles in the script column
                hit_stepper = False
                for i, block in enumerate(script):
                    if block["type"] not in REPEAT_TYPES:
                        continue
                    tile_top = _tile_top(i, scroll)
                    if not (SCRIPT_Y0 - TILE_H < tile_top < SCRIPT_Y1):
                        continue
                    minus_rect = pygame.Rect(SCRIPT_X + SCRIPT_W - 78, tile_top + 6, 30, TILE_H - 12)
                    plus_rect = pygame.Rect(SCRIPT_X + SCRIPT_W - 40, tile_top + 6, 30, TILE_H - 12)
                    if minus_rect.collidepoint(mx, my):
                        block["n"] = max(1, block["n"] - 1)
                        hit_stepper = True
                        break
                    if plus_rect.collidepoint(mx, my):
                        block["n"] = min(15, block["n"] + 1)
                        hit_stepper = True
                        break
                if hit_stepper:
                    continue

                # start dragging an existing script block
                if _in_script_column(mx, my):
                    for i, block in enumerate(script):
                        tile_top = _tile_top(i, scroll)
                        tile_rect = pygame.Rect(SCRIPT_X, tile_top, SCRIPT_W, TILE_H)
                        if tile_rect.collidepoint(mx, my):
                            dragging = {
                                "from": "script",
                                "block": script.pop(i),
                                "offset": (mx - tile_rect.x, my - tile_rect.y),
                            }
                            break
                if dragging:
                    continue

                # start dragging a new block from the palette
                for i, template in enumerate(PALETTE_TEMPLATES):
                    tile_top = 70 + 46 + i * (TILE_H + TILE_GAP)
                    tile_rect = pygame.Rect(PALETTE_X, tile_top, PALETTE_W, TILE_H)
                    if tile_rect.collidepoint(mx, my):
                        dragging = {
                            "from": "palette",
                            "block": _new_block(template["type"]),
                            "offset": (mx - tile_rect.x, my - tile_rect.y),
                        }
                        break

            elif mode == "build" and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if dragging is not None:
                    mx, my = event.pos
                    if _in_script_column(mx, my):
                        idx = _insert_index_for_y(script, my, scroll)
                        script.insert(idx, dragging["block"])
                        scroll = _scroll_to_reveal(scroll, idx, script)
                    else:
                        scroll = max(0, min(scroll, _max_scroll(script)))
                    dragging = None

            elif mode == "build" and event.type == pygame.MOUSEWHEEL:
                mx, my = pygame.mouse.get_pos()
                if _in_script_column(mx, my):
                    scroll = max(0, min(scroll - event.y * 40, _max_scroll(script)))

        if mode == "playing":
            player.update(now)
            if player.finished or player.victory:
                mode = "build"

        # --- draw ---
        screen.fill(COLOR_BG)

        # map panel (always visible)
        title = font.render("DUNGEON MAP", True, COLOR_HEADER)
        screen.blit(title, (MAP_X, 20))
        dungeon = player.dungeon if player is not None else de.DUNGEONS[0]
        pygame.draw.rect(screen, COLOR_PANEL, pygame.Rect(MAP_X - 10, MAP_Y - 10, MAP_W + 20, MAP_H + STATUS_H + 30))
        de.draw_dungeon(screen, dungeon, (MAP_X, MAP_Y), CELL)
        if player is not None:
            de.draw_player(screen, player.px, player.py, player.facing, CELL)
            dungeon_i, status_message, finished, victory = player.dungeon_i, player.message, player.finished, player.victory
        else:
            start = dungeon["start"]
            sx, sy = _map_cell_center(*start, dungeon)
            de.draw_player(screen, sx, sy, 0, CELL)
            dungeon_i, status_message, finished, victory = 0, "Ready! Drag blocks and press RUN.", False, False

        status_bar = pygame.Rect(MAP_X - 10, MAP_Y + MAP_H + 4, MAP_W + 20, STATUS_H)
        pygame.draw.rect(screen, (14, 13, 20), status_bar)
        if victory:
            status_surf = small_font.render("All dungeons cleared! Badge: Maze Solver", True, de.COLOR_VICTORY)
        else:
            name = f"Dungeon {min(dungeon_i + 1, len(de.DUNGEONS))} of {len(de.DUNGEONS)}"
            shown = status_message
            if finished and not shown:
                shown = "Out of blocks! Add more and press RUN again."
            status_surf = small_font.render(f"{name}   {shown}", True, COLOR_MESSAGE if shown else COLOR_HEADER)
        screen.blit(status_surf, (status_bar.x + 8, status_bar.y + 10))

        # palette panel
        header = font.render("Drag blocks, then press RUN", True, COLOR_HEADER)
        screen.blit(header, (PALETTE_X, 20))
        pygame.draw.rect(screen, COLOR_PANEL, pygame.Rect(PALETTE_X - 10, 70, PALETTE_W + 20, WIN_H - 70 - 20))
        label = small_font.render("BLOCKS", True, COLOR_HINT)
        screen.blit(label, (PALETTE_X, 70 + 12))
        for i, template in enumerate(PALETTE_TEMPLATES):
            tile_top = 70 + 46 + i * (TILE_H + TILE_GAP)
            tile_rect = pygame.Rect(PALETTE_X, tile_top, PALETTE_W, TILE_H)
            pygame.draw.rect(screen, template["color"], tile_rect, border_radius=8)
            text = small_font.render(template["label"], True, COLOR_TILE_TEXT)
            screen.blit(text, (tile_rect.x + 10, tile_rect.y + (TILE_H - text.get_height()) // 2))

        # script panel
        pygame.draw.rect(screen, COLOR_PANEL, pygame.Rect(SCRIPT_X - 10, 70, SCRIPT_W + 20, WIN_H - 70 - 20))
        label = small_font.render("YOUR PROGRAM", True, COLOR_HINT)
        screen.blit(label, (SCRIPT_X, 70 + 12))

        drop_zone = pygame.Rect(SCRIPT_X, SCRIPT_Y0, SCRIPT_W, SCRIPT_Y1 - SCRIPT_Y0)
        pygame.draw.rect(screen, COLOR_DROP_ZONE, drop_zone, border_radius=6)
        if not script:
            hint = small_font.render("(drop blocks here)", True, COLOR_HINT)
            screen.blit(hint, (SCRIPT_X + 14, SCRIPT_Y0 + 14))

        prev_clip = screen.get_clip()
        screen.set_clip(drop_zone)
        for i, block in enumerate(script):
            tile_top = _tile_top(i, scroll)
            if tile_top + TILE_H < SCRIPT_Y0 or tile_top > SCRIPT_Y1:
                continue
            tile_rect = pygame.Rect(SCRIPT_X, tile_top, SCRIPT_W, TILE_H)
            pygame.draw.rect(screen, _block_color(block), tile_rect, border_radius=8)
            if mode == "playing" and player is not None and player.current_owner == i:
                pygame.draw.rect(screen, COLOR_HIGHLIGHT, tile_rect, width=3, border_radius=8)
            text = small_font.render(_block_label(block), True, COLOR_TILE_TEXT)
            screen.blit(text, (tile_rect.x + 10, tile_rect.y + (TILE_H - text.get_height()) // 2))
            if block["type"] in REPEAT_TYPES:
                minus_rect = pygame.Rect(tile_rect.right - 78, tile_rect.y + 6, 30, TILE_H - 12)
                plus_rect = pygame.Rect(tile_rect.right - 40, tile_rect.y + 6, 30, TILE_H - 12)
                pygame.draw.rect(screen, COLOR_BG, minus_rect, border_radius=6)
                pygame.draw.rect(screen, COLOR_BG, plus_rect, border_radius=6)
                minus_text = small_font.render("-", True, COLOR_TILE_TEXT)
                plus_text = small_font.render("+", True, COLOR_TILE_TEXT)
                screen.blit(minus_text, minus_text.get_rect(center=minus_rect.center))
                screen.blit(plus_text, plus_text.get_rect(center=plus_rect.center))
        screen.set_clip(prev_clip)

        max_scroll = _max_scroll(script)
        if max_scroll > 0:
            track_h = SCRIPT_Y1 - SCRIPT_Y0
            thumb_h = max(24, track_h * track_h / (track_h + max_scroll))
            thumb_y = SCRIPT_Y0 + (track_h - thumb_h) * (scroll / max_scroll)
            scrollbar_x = SCRIPT_X + SCRIPT_W - 6
            pygame.draw.rect(screen, COLOR_HINT, pygame.Rect(scrollbar_x, thumb_y, 4, thumb_h), border_radius=2)

        # buttons
        run_color = COLOR_RUN if mode == "build" else (90, 110, 90)
        pygame.draw.rect(screen, run_color, run_button, border_radius=8)
        run_text = font.render("RUN", True, COLOR_TILE_TEXT)
        screen.blit(run_text, run_text.get_rect(center=run_button.center))

        clear_color = COLOR_CLEAR if mode == "build" else (110, 90, 90)
        pygame.draw.rect(screen, clear_color, clear_button, border_radius=8)
        clear_text = font.render("CLEAR", True, COLOR_TILE_TEXT)
        screen.blit(clear_text, clear_text.get_rect(center=clear_button.center))

        if message and now < message_until:
            msg_surf = small_font.render(message, True, COLOR_MESSAGE)
            screen.blit(msg_surf, (SCRIPT_X + 320, BOTTOM_Y + 14))

        if dragging is not None:
            mx, my = pygame.mouse.get_pos()
            ox, oy = dragging["offset"]
            width = SCRIPT_W if dragging["from"] == "script" else PALETTE_W
            ghost_rect = pygame.Rect(mx - ox, my - oy, width, TILE_H)
            ghost = pygame.Surface((ghost_rect.width, ghost_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(ghost, (*_block_color(dragging["block"])[:3], 200), ghost.get_rect(), border_radius=8)
            text = small_font.render(_block_label(dragging["block"]), True, COLOR_TILE_TEXT)
            ghost.blit(text, (10, (TILE_H - text.get_height()) // 2))
            screen.blit(ghost, ghost_rect.topleft)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
