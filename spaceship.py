import asyncio
import curses
from itertools import cycle
from utilities import draw_frame, read_controls, get_frame_size, duplicate_frames
from physics import update_speed

SPACE_SHIP_TICK_RATE = 0.1


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


def load_ship_frames():
    frames = []
    for i in range(1, 3):
        with open(f"animations/ship{i}.txt", "r") as f:
            frames.append(f.read())
    return frames


async def animate_spaceship(
    canvas: curses.window,
    start_row: int,
    start_col: int,
    frames: list,
    tick_timeout: float,
    coroutines: list,
):
    row_speed = col_speed = 0
    col = start_col
    row = start_row
    frame_rate = int(SPACE_SHIP_TICK_RATE / tick_timeout)
    for frame in cycle(duplicate_frames(frame_rate, frames)):
        draw_frame(canvas, row, col, frame)
        await asyncio.sleep(0)
        row_dir, col_dir, space_pressed = read_controls(canvas)
        if space_pressed:
            coroutines.append(fire(canvas, row, col+2))
        draw_frame(canvas, row, col, frame, negative=True)
        row_speed, col_speed = update_speed(row_speed, col_speed, row_dir, col_dir)
        row += row_speed
        col += col_speed
        max_row, max_col = canvas.getmaxyx()
        frame_rows, frame_cols = get_frame_size(frame)
        row = max(0, min(row, max_row - frame_rows))
        col = max(0, min(col, max_col - frame_cols))
