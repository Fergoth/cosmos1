import asyncio
from random import randint
from typing import List

from obstacles import Obstacle
from utilities import draw_frame, get_frame_size, sleep
from explode import explode

OBSTACLES: List[Obstacle] = []
OBSTACLES_IN_LAST_COLLISION: List[Obstacle] = []


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
        row_size, column_size = get_frame_size(frame)
        column = randint(0, 100)
        new_obstacle = Obstacle(0, column, rows_size=row_size, columns_size=column_size)
        coroutines.append(fly_garbage(canvas, column, frame, new_obstacle))
        OBSTACLES.append(new_obstacle)
        await sleep(randint(5, 7))


async def fly_garbage(canvas, column, garbage_frame, obstacle, speed=0.5):
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
        obstacle.row = row
        if obstacle in OBSTACLES_IN_LAST_COLLISION:
            OBSTACLES_IN_LAST_COLLISION.remove(obstacle)
            OBSTACLES.remove(obstacle)
            await explode(canvas, row, column)
            return
    OBSTACLES.remove(obstacle)
