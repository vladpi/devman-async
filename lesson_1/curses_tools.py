from random import randint, choice

SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258


def read_controls(canvas):
    """Read keys pressed and returns tuple witl controls state."""

    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            # https://docs.python.org/3/library/curses.html#curses.window.getch
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -1

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True

    return rows_direction, columns_direction, space_pressed


def draw_frame(canvas, start_row, start_column, text, negative=False):
    """Draw multiline text fragment on canvas. Erase text instead of drawing if negative=True is specified."""

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

            if symbol == ' ':
                continue

            # Check that current position it is not in a lower right corner of the window
            # Curses will raise exception in that case. Don`t ask why…
            # https://docs.python.org/3/library/curses.html#curses.window.addch
            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


def get_frame_size(text):
    """Calculate size of multiline text fragment. Returns pair (rows number, columns number)"""

    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns


def read_frame_from_file(file_path):
    """Read frame from txt file. Return plain string."""

    with open(file_path, 'r') as file:
        output_string = file.read()

    return output_string


def get_rocket_position(canvas, current_row, current_column, controls, frame):
    """
        Calculate position of rocket by frame size and current controls values. 
        Returns pairs (row value, column value)
    """

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    frame_rows, frame_columns = get_frame_size(frame)

    controls_row, controls_column, _ = controls

    row, column = current_row + controls_row, current_column + controls_column

    row = max(1, min(row, max_row - frame_rows))
    column = max(1, min(column, max_column - frame_columns))

    return row, column


def get_random_blink_params(canvas):
    """
        Generate random params (row, column, symbol) for blink star.
        Returns row value, column value, symbol.
    """

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 2, columns - 2

    row = randint(1, max_row)
    column = randint(1, max_column)
    symbol = choice('+*.:')

    return row, column, symbol
