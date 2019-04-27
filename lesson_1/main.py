import asyncio
import curses
import time
from random import randint

from curses_tools import MIN_ROW, MIN_COL
from curses_tools import read_frame_from_file, get_rocket_position, draw_frame, get_frame_size, \
    get_random_blink_params, read_controls

TIC_TIMEOUT = 0.025
MAX_STARS = 120


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot. Direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    borders_size = 2
    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - borders_size, columns - borders_size

    curses.beep()

    while MIN_ROW < row < max_row and MIN_COL < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def blink(canvas, row, column, offset_tics, symbol='*'):
    """Display animation of star blink."""

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(offset_tics):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)


async def animate_spaceship(canvas, row, column):
    """Display animation and controls spaceship."""

    frame_1 = read_frame_from_file('frames/rocket_frame_1.txt')
    frame_2 = read_frame_from_file('frames/rocket_frame_2.txt')

    while True:
        for _ in range(randint(3, 5)):
            row, column = get_rocket_position(canvas, row, column, controls, frame_1)
            draw_frame(canvas, row, column, frame_1)

            await asyncio.sleep(0)

            draw_frame(canvas, row, column, frame_1, negative=True)

        for _ in range(randint(3, 5)):
            row, column = get_rocket_position(canvas, row, column, controls, frame_2)
            draw_frame(canvas, row, column, frame_2)

            await asyncio.sleep(0)

            draw_frame(canvas, row, column, frame_2, negative=True)


def draw(canvas):
    global controls

    curses.curs_set(False)
    canvas.border()
    canvas.nodelay(True)

    borders_size = 1
    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - borders_size, columns - borders_size

    spaceship_rows, spaceship_columns = get_frame_size(read_frame_from_file('frames/rocket_frame_1.txt'))
    canvas_column_center = max_column // 2

    spaceship_row = max_row - spaceship_rows
    spaceship_column = canvas_column_center - spaceship_columns // 2

    coroutines = [blink(canvas, *get_random_blink_params(canvas)) for _ in range(MAX_STARS)]
    coroutines.append(animate_spaceship(canvas, spaceship_row, spaceship_column))
    coroutines.append(fire(canvas, spaceship_row, canvas_column_center))

    while True:
        controls = read_controls(canvas)

        for coroutine in coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
