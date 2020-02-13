import argparse
import curses
import time
import numpy as np

from combat_simulator import Grid, Token


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--load_map", type=str, default=None,
                        help="""Edit an existing map.""")
    return parser.parse_args()


def main(stdscr, grid=None):
    if grid is None:
        grid = Grid((5, 5))

    curses.curs_set(0)
    stdscr.clear()
    rows, cols = stdscr.getmaxyx()
    main_win = curses.newwin(rows - 10, cols)
    msg_win = curses.newwin(9, cols, rows - 9, 0)

    main_win.addstr(str(grid))
    msg_win.addstr("Welcome to the map maker!\n")
    msg_win.addstr("Press any key to get started.")
    main_win.refresh()
    msg_win.refresh()
    msg_win.getch()

    grid = set_grid_shape(grid, main_win, msg_win)
    grid = add_walls(grid, main_win, msg_win)
    msg_win.erase()
    msg_win.addstr("Add team start positions ([y]/n)?\n")
    key = msg_win.getkey()
    if key != 'n':
        grid._start_positions = {}
        grid = set_start_positions(grid, main_win, msg_win)

    msg_win.erase()
    msg_win.addstr("Save this map ([y]/n)?\n")
    key = msg_win.getkey()
    if key != 'n':
        curses.echo()
        msg_win.addstr("Name your map: ")
        map_name = msg_win.getstr()
        map_name = map_name.decode("utf-8").strip()
        map_path = f"maps/{map_name}.npy"
        curses.noecho()
        save_map(map_path, grid)
        msg_win.addstr(f"\nSaved to {map_path}")
        msg_win.refresh()
        time.sleep(2)

    return True


def save_map(filename, grid):
    grid_copy = np.zeros(shape=grid.shape, dtype=str)
    grid_copy[grid._grid == 0] = '.'
    for (pos, tok) in grid._pos2tok.items():
        grid_copy[pos] = tok.icon
    np.save(filename, grid_copy)


def set_grid_shape(grid, main_win, msg_win):
    msg_win.clear()
    msg_win.addstr("Use 'h', 'j', 'k', 'l' to change the shape.\n")
    msg_win.addstr("Press 'q' when finished.")
    msg_win.refresh()

    max_row, max_col = main_win.getmaxyx()
    while True:
        key = main_win.getkey()
        if key == 'q':
            break
        elif key == 'j':
            if grid.screen_size[0] == max_row:
                continue
            new_shape = (grid.shape[0] + 1, grid.shape[1])
        elif key == 'k':
            if grid.shape[0] == 1:
                continue
            new_shape = (grid.shape[0] - 1, grid.shape[1])
        elif key == 'l':
            if grid.screen_size[1] == max_col - 1:
                continue
            new_shape = (grid.shape[0], grid.shape[1] + 1)
        elif key == 'h':
            if grid.shape[1] == 1:
                continue
            new_shape = (grid.shape[0], grid.shape[1] - 1)

        grid.change_shape(new_shape)

        msg_win.erase()
        msg_win.addstr(f"Grid shape: {str(grid.shape)}")
        msg_win.refresh()

        main_win.erase()
        main_win.addstr(str(grid))
        main_win.refresh()

    return grid


def cursor_to_grid(grid, y, x):
    """
    Given the y, x coordinates on the curses screen,
    translate it into grid position.
    """
    def translate_pos(y, x):
        return (y+1, (2*x) + 1)

    min_y, min_x = translate_pos(0, 0)
    max_y, max_x = translate_pos(*grid.shape)
    max_y -= 1
    max_x -= 2
    new_y, new_x = translate_pos(y, x)

    # Adjusted for minimum possible values
    new_y, new_x = (max(new_y, min_y), max(new_x, min_x))
    # Adjusted for maximum possible values
    new_y, new_x = (min(new_y, max_y), min(new_x, max_x))
    return (new_y, new_x)


def add_walls(grid, main_win, msg_win):
    msg_win.clear()
    msg_win.addstr("Move with 'h', 'j', 'k', 'l'.\n")
    msg_win.addstr("Place a wall with 'a'. Delete it with 'd'.\n")
    msg_win.addstr("Press 'q' when finished.")
    msg_win.refresh()

    pos = (0, 0)
    grid_pos = cursor_to_grid(grid, *pos)
    main_win.erase()
    main_win.addstr(str(grid))
    main_win.addstr(*grid_pos, '#')
    main_win.refresh()

    while True:
        key = main_win.getkey()
        if key == 'q':
            break
        elif key == 'a':
            wall = Token(name="wall", icon='#')
            grid.add_token(wall, pos=pos)
            new_pos = pos
        elif key == 'd':
            if grid[pos] is None:
                continue
            grid.rm_token(grid[pos])
        elif key == 'j':
            new_pos = (pos[0] + 1, pos[1])
        elif key == 'k':
            new_pos = (pos[0] - 1, pos[1])
        elif key == 'l':
            new_pos = (pos[0], pos[1] + 1)
        elif key == 'h':
            new_pos = (pos[0], pos[1] - 1)

        new_grid_pos = cursor_to_grid(grid, *new_pos)
        # Check if we hit a boundary.
        if new_grid_pos != grid_pos:
            grid_pos = new_grid_pos
            pos = new_pos

        main_win.erase()
        main_win.addstr(str(grid))
        main_win.addstr(*grid_pos, '#')
        main_win.refresh()

    return grid


def set_start_positions(grid, main_win, msg_win):
    msg_win.clear()
    msg_win.addstr("Move with 'h', 'j', 'k', 'l'.\n")
    msg_win.addstr("Place a starting position with 'a'.\n")
    msg_win.addstr("Press 'q' when finished.")
    msg_win.refresh()

    pos_num = 1
    pos = (0, 0)
    grid_pos = cursor_to_grid(grid, *pos)

    while pos_num <= 2:

        main_win.erase()
        main_win.addstr(str(grid))
        main_win.addstr(*grid_pos, str(pos_num))
        main_win.refresh()

        msg_win.erase()
        msg_win.addstr(f"\nSet start position for team {pos_num}.")
        msg_win.refresh()

        key = main_win.getkey()
        if key == 'q':
            break
        elif key == 'a':
            pos_tok = Token(name="start_pos", icon=str(pos_num))
            grid.add_token(pos_tok, pos=pos)
            new_pos = pos
            pos_num += 1
        elif key == 'j':
            new_pos = (pos[0] + 1, pos[1])
        elif key == 'k':
            new_pos = (pos[0] - 1, pos[1])
        elif key == 'l':
            new_pos = (pos[0], pos[1] + 1)
        elif key == 'h':
            new_pos = (pos[0], pos[1] - 1)

        new_grid_pos = cursor_to_grid(grid, *new_pos)
        # Check if we hit a boundary.
        if new_grid_pos != grid_pos:
            grid_pos = new_grid_pos
            pos = new_pos

    return grid


if __name__ == "__main__":
    args = parse_args()
    grid = None
    if args.load_map is not None:
        map_matrix = np.load(args.load_map)
        grid = Grid.from_map_matrix(map_matrix)
    curses.wrapper(main, grid=grid)
