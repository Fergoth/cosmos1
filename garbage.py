from utilities import draw_frame
import asyncio
from random import randint


def load_garbage_frames():
    """Load garbage frames from file."""
    filenames = ["duck", "hubble", "lamp", "trash_large", "trash_small", "trash_xl"]
    frames = []
    for filename in filenames:
        with open(f"animations/{filename}.txt", "r") as f:
            frames.append(f.read())
    return frames


async def fill_orbit_with_garbage(coroutines, frame, canvas):
    """Fill orbit with garbage."""
    while True:
        coroutines.append(
            fly_garbage(canvas, column=randint(0, 100), garbage_frame=frame)
        )
        for i in range(3):
            await asyncio.sleep(0)


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
