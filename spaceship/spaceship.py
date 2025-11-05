import asyncio
import curses
from itertools import cycle
from utilities import draw_frame, read_controls, get_frame_size, duplicate_frames
from physics import update_speed

SPACE_SHIP_TICK_RATE = 0.1


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
):
    row_speed = col_speed = 0
    col = start_col
    row = start_row
    frame_rate = int(SPACE_SHIP_TICK_RATE / tick_timeout)
    for frame in cycle(duplicate_frames(frame_rate, frames)):
        draw_frame(canvas, row, col, frame)
        await asyncio.sleep(0)
        row_dir, col_dir, _ = read_controls(canvas)
        draw_frame(canvas, row, col, frame, negative=True)
        row_speed, col_speed = update_speed(row_speed, col_speed, row_dir, col_dir)
        row += row_speed
        col += col_speed
        max_row, max_col = canvas.getmaxyx()
        frame_rows, frame_cols = get_frame_size(frame)
        row = max(0, min(row, max_row - frame_rows))
        col = max(0, min(col, max_col - frame_cols))
