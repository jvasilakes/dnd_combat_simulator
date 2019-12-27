import curses
import time
import pandas as pd
from tqdm import trange
from collections import defaultdict

from .grid import Grid
from .player import Player
from .encounter import Encounter


class Engine(object):

    def __init__(self, *teams, grid=None):
        if grid is None:
            raise ValueError("grid must be specified.")
        self.teams = teams
        self.player = Player()
        assert(isinstance(grid, Grid))
        self.grid = grid

    def gameloop(self, visual=True, num_encounters=1000, speed=0.3):

        def initialize_encounter():
            # Initialize the grid and add the players
            # to random positions.
            for team in self.teams:
                for character in team.members():
                    if not character.is_alive:
                        character.reset()
                    self.grid.add_token(character)

            # Start the encounter
            enc = Encounter(teams=self.teams, grid=self.grid,
                            player=self.player)
            enc.init_combat()
            return enc

        def main_visual(curses_scr):
            enc = initialize_encounter()
            gamewin = GameWindow(self.grid, pos=(0, 0))
            gamewin.redraw()
            msg_size = (30, 50)
            msg_pos = (gamewin.shape[0] + 2, 0)
            msgwin = MessageWindow(size=msg_size, pos=msg_pos)

            init_str = ["Initiative Order"] + enc.turn_order
            msgwin.redraw('\n'.join([str(init) for init in init_str]))
            msgwin.getch()
            msgwin.redraw(str(enc))
            for rnd in enc.run_combat():
                gamewin.redraw()
                time.sleep(speed)
            msgwin.redraw(f"Winner: {str(enc.winner)}")
            msgwin.getch()
            return enc

        def main_background():
            log = None
            winners = defaultdict(int)
            for _ in trange(num_encounters):
                enc = initialize_encounter()
                list(enc.run_combat())
                winners[enc.winner.name] += 1
                log = pd.concat([log, enc.log])
                del enc
            return log, winners

        if visual is True:
            enc = curses.wrapper(main_visual)
            enc.summary()
        else:
            results, winners = main_background()
            for ((name, cid), group) in results.groupby(["attacker_name", "attacker_id"]):  # noqa
                dpr = group[group["hit"] == True]["dmg"].mean()  # noqa
                hit_ratio = group["hit"].sum() / group.shape[0]
                print(f"{name} ({cid}): DPR ({dpr:.2f}), hit ratio ({hit_ratio:.2f})")  # noqa
            print("Wins")
            for team in self.teams:
                percentage = winners[team.name] / num_encounters
                print(f"{team.name}: {winners[team.name]} / {num_encounters} ({percentage:.2f})")  # noqa


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
        y = self.grid.screen_size[0]
        x = self.grid.screen_size[1]
        self.shape = (y, x)
        self.win = curses.newwin(y, x, *self.pos)

    def redraw(self):
        self.win.erase()
        self.win.addstr(str(self.grid))
        self.win.refresh()

    def getch(self):
        self.win.getch()


class MessageWindow(object):

    def __init__(self, size=(10, 30), pos=(0, 0)):
        self.pos = pos
        self.size = size
        self._create_window()

    def _create_window(self):
        y = self.size[0]
        x = self.size[1]
        self.win = curses.newwin(y, x, *self.pos)

    def redraw(self, msg):
        self.win.erase()
        self.win.addstr(msg)
        self.win.refresh()

    def getch(self):
        self.win.getch()
