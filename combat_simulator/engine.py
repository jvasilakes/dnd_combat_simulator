import curses
import time

from .grid import Grid
from .player import Player
from .encounter import Encounter


class Engine(object):

    def __init__(self, *teams):
        self.teams = teams
        self.player = Player()

    def gameloop(self):

        # Initialize the grid and add the players
        # to random positions.
        grid = Grid()
        for team in self.teams:
            for character in team.members():
                grid.add_character(character)

        def main(curses_scr):
            gamewin = GameWindow(grid, pos=(0, 0))
            msgwin = MessageWindow(pos=(13, 0))
            enc = Encounter(teams=self.teams, grid=grid, player=self.player)
            inits = enc._roll_initiative()
            init_str = ["Initiative"] + inits
            msgwin.redraw('\n'.join([str(init) for init in init_str]))
            msgwin.getch()
            msgwin.redraw(str(enc))
            while True:
                for team in self.teams:
                    for character in team.members():
                        new_pos = self.player.move_character(character,
                                                             grid, pos=None)
                        if new_pos is None:
                            continue
                        gamewin.redraw()
                        time.sleep(0.2)

        curses.wrapper(main)


class GameWindow(object):

    def __init__(self, grid, pos=(0, 0)):
        self._check_params(grid)
        self.pos = pos
        self.grid = grid
        self._create_window()

    def _check_params(self, grid):
        assert(isinstance(grid, Grid))

    def _create_window(self):
        # Curses uses (y,x) coordinates
        y = self.grid.screen_size[1]
        x = self.grid.screen_size[0]
        self.win = curses.newwin(y, x, *self.pos)

    def redraw(self):
        self.win.erase()
        self.win.addstr(str(self.grid))
        self.win.refresh()

    def getch(self):
        self.win.getch()


class MessageWindow(object):

    def __init__(self, pos=(0, 0)):
        self.pos = pos
        self._create_window()

    def _create_window(self):
        self.win = curses.newwin(10, 30, *self.pos)

    def redraw(self, msg):
        self.win.erase()
        self.win.addstr(msg)
        self.win.refresh()

    def getch(self):
        self.win.getch()
