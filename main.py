import curses
import time

import obstacles
from garbage import OBSTACLES, fill_orbit_with_garbage, load_garbage_frames
from spaceship import animate_spaceship, load_ship_frames
from stars import add_stars

TICK_TIMEOUT = 0.1


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
    coroutines.append(fill_orbit_with_garbage(coroutines, garbage_frames[0], canvas))
    # uncomment below to show obstacles
    # coroutines.append(obstacles.show_obstacles(canvas, OBSTACLES))
    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(TICK_TIMEOUT)


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
