import time
import curses
from stars.stars import add_stars
from spaceship.spaceship import load_ship_frames, animate_spaceship
from spaceship.fire import fire


TICK_TIMEOUT = 0.1


def draw(canvas: curses.window):
    canvas.nodelay(True)
    ship_frames = load_ship_frames()
    curses.curs_set(0)
    coroutines = []
    coroutines = add_stars(canvas, coroutines, TICK_TIMEOUT)
    coroutines.append(fire(canvas, 10, 10))
    coroutines.append(animate_spaceship(canvas, 10, 10, ship_frames, TICK_TIMEOUT))
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
