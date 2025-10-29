from collections import namedtuple
from random import randint, choice
import time
import curses
import asyncio

Star_tick = namedtuple("Star_tick", ["attribute", "time"])

STARS_COUNT = 100
STARS = ["*", ":", "+", ";", "."]
TICK_TIMEOUT = 0.1
TICK_TEMPLATE = [
    Star_tick(curses.A_DIM, 2),
    Star_tick(curses.A_NORMAL, 0.3),
    Star_tick(curses.A_BOLD, 0.5),
    Star_tick(curses.A_NORMAL, 0.3),
]


def draw_frame(canvas, start_row, start_column, text, negative=False):
    """Draw multiline text fragment on canvas, erase text instead of drawing if negative=True is specified."""

    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            if symbol == " ":
                continue

            # Check that current position it is not in a lower right corner of the window
            # Curses will raise exception in that case. Don`t ask why…
            # https://docs.python.org/3/library/curses.html#curses.window.addch
            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else " "
            canvas.addch(row, column, symbol)


async def animate_spaceship(canvas: curses.window, row: int, column: int, frames: list):
    while True:
        for frame in frames:
            draw_frame(canvas, row, column, frame)
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, frame, negative=True)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), "*")
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), "O")
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), " ")

    row += rows_speed
    column += columns_speed

    symbol = "-" if columns_speed else "|"

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), " ")
        row += rows_speed
        column += columns_speed


async def blink(
    canvas: curses.window,
    row: int,
    column: int,
    symbol: str = "*",
    start_pause: int = 0,
):
    for _ in range(start_pause):
        await asyncio.sleep(0)
    while True:
        for tick in TICK_TEMPLATE:
            canvas.addch(row, column, symbol, tick.attribute)
            for _ in range(int(tick.time / TICK_TIMEOUT)):
                await asyncio.sleep(0)


def get_random_coords(canvas: curses.window):
    max_row, max_col = canvas.getmaxyx()
    return (randint(0, max_row - 1), randint(0, max_col - 1))


def load_ship_frames():
    frames = []
    for i in range(1, 3):
        with open(f"animations/ship{i}.txt", "r") as f:
            frames.append(f.read())
    return frames


def draw(canvas: curses.window):
    ship_frames = load_ship_frames()
    curses.curs_set(0)
    coroutines = []
    for _ in range(STARS_COUNT):
        row, column = get_random_coords(canvas)
        start_pause = randint(1, 20)
        coroutines.append(blink(canvas, row, column, choice(STARS), start_pause))
    coroutines.append(fire(canvas, 10, 10))
    coroutines.append(animate_spaceship(canvas, 10, 10, ship_frames))
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
