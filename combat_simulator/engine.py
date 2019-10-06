import curses

from .grid import Grid
from .player import Player
from .encounter import Encounter


class Engine(object):

    def __init__(self, *teams):
        self.teams = teams
        self.player = Player()

    def gameloop(self):

        def main(curses_scr):
            grid = Grid()
            for team in self.teams:
                for character in team.members():
                    grid.add_character(character)

            gamewin = GameWindow(grid, (0, 0))
            msgwin = MessageWindow((13, 0))
            enc = Encounter(teams=self.teams, grid=grid)
            while True:
                gamewin.redraw()
                msgwin.redraw(str(enc))
                for team in self.teams:
                    for character in team.members():
                        self.player.move_character(character, grid, pos=None)
                msgwin.getch()

        curses.wrapper(main)

## Run a series of encounters to see who wins.
#enc = Encounter(teams=[team_jake, team_mort], grid=grid)
#print(enc)
#winners = []
#for i in range(10):
#    winner = enc.run_combat(random_seed=i, verbose=0)
#    winners.append(winner)
#    print(f"Round {i+1} winner: {winner}")
#    enc.summary()
#    print("---")
#    input()


class GameWindow(object):

    def __init__(self, grid, pos):
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

    def __init__(self, pos):
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
