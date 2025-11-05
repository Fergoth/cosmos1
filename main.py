import curses
import time
import asyncio

import obstacles
from garbage import OBSTACLES, fill_orbit_with_garbage, load_garbage_frames
from spaceship import animate_spaceship, load_ship_frames
from stars import add_stars
from game_scenario import game_state

TICK_TIMEOUT = 0.1
TICK_PER_YEAR = 15


async def draw_year(canvas: curses.window):
    while True:
        await asyncio.sleep(0)
        canvas.addstr(0, 0, f"Year: {game_state.year}")


async def draw_phrase(canvas: curses.window):
    while True:
        await asyncio.sleep(0)
        if game_state.year in game_state.phrase:
            canvas.clear()
            canvas.addstr(0, 0, game_state.phrase[game_state.year])
        canvas.refresh()


def draw(canvas: curses.window):
    canvas.nodelay(True)
    ship_frames = load_ship_frames()
    garbage_frames = load_garbage_frames()
    curses.curs_set(0)
    coroutines = []
    coroutines = add_stars(canvas, coroutines, TICK_TIMEOUT)
    coroutines.append(
        animate_spaceship(canvas, 10, 10, ship_frames, TICK_TIMEOUT, coroutines)
    )
    coroutines.append(fill_orbit_with_garbage(coroutines, garbage_frames, canvas))
    coroutines.append(draw_year(canvas))
    # uncomment below to show obstacles
    # coroutines.append(obstacles.show_obstacles(canvas, OBSTACLES))
    total_ticks = 0
    max_row, max_col = canvas.getmaxyx()

    canvas_for_phrase = canvas.derwin(1, 60, max_row - 1, max_col - 60)
    canvas_for_phrase.nodelay(True)

    coroutines.append(draw_phrase(canvas_for_phrase))
    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(TICK_TIMEOUT)
        total_ticks += 1
        if total_ticks % TICK_PER_YEAR == 0:
            game_state.year += 1


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
