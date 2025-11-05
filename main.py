import time
import curses
from stars import add_stars
from spaceship.spaceship import load_ship_frames, animate_spaceship
from spaceship.fire import fire
from garbage import load_garbage_frames, fly_garbage
from random import choice

TICK_TIMEOUT = 0.1


def draw(canvas: curses.window):
    canvas.nodelay(True)
    ship_frames = load_ship_frames()
    garbage_frames = load_garbage_frames()
    curses.curs_set(0)
    coroutines = []
    coroutines = add_stars(canvas, coroutines, TICK_TIMEOUT)
    coroutines.append(fire(canvas, 10, 10))
    coroutines.append(animate_spaceship(canvas, 10, 10, ship_frames, TICK_TIMEOUT))
    coroutines.append(
        fly_garbage(canvas, column=10, garbage_frame=choice(garbage_frames))
    )
    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        canvas.refresh()
        time.sleep(TICK_TIMEOUT)


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
