from collections import namedtuple
import curses
from utilities import get_random_coords, sleep
from random import randint, choice

star_tick = namedtuple("Star_tick", ["attribute", "time"])

STARS_COUNT = 100
STARS = ["*", ":", "+", ";", "."]

TICK_TEMPLATE = [
    star_tick(curses.A_DIM, 2),
    star_tick(curses.A_NORMAL, 0.3),
    star_tick(curses.A_BOLD, 0.5),
    star_tick(curses.A_NORMAL, 0.3),
]


async def blink(
    canvas: curses.window,
    row: int,
    column: int,
    tick_timeout: float,
    symbol: str = "*",
    start_pause: int = 0,
):
    await sleep(start_pause)
    while True:
        for tick in TICK_TEMPLATE:
            canvas.addch(row, column, symbol, tick.attribute)
            await sleep(int(tick.time / tick_timeout))


def add_stars(canvas: curses.window, coroutines: list, tick_timeout: float):
    for _ in range(STARS_COUNT):
        row, column = get_random_coords(canvas)
        start_pause = randint(1, 20)
        coroutines.append(
            blink(canvas, row, column, tick_timeout, choice(STARS), start_pause)
        )
    return coroutines
