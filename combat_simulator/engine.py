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

    # TODO: Check if the first team(s) will fill up the grid.
    # If this happens then the last team will not be added at all.
    def initialize_encounter(self, visual=False):
        # Initialize the grid and add the players
        # to random positions.
        self.grid.clear_tokens()
        for (i, team) in enumerate(self.teams):
            for character in team.members():
                if visual is True:
                    # Makes for nicer visualization.
                    character.speed = 5
                if not character.is_alive:
                    character.reset()
                added = self.grid.add_token(character, team=i+1)
                # This happens when the Grid runs out of room for
                # more tokens.
                if added is False:
                    team.rm_member(character)

        # Start the encounter
        enc = Encounter(teams=self.teams, grid=self.grid,
                        player=self.player)
        enc.init_combat()
        return enc

    def initialize_windows(self):
        gamewin = GameWindow(self.grid, pos=(0, 0))
        gamewin.redraw()
        msgwin_size = (30, 50)
        msgwin_pos = (gamewin.shape[0] + 2, 0)
        msgwin = MessageWindow(size=msgwin_size, pos=msgwin_pos)
        return gamewin, msgwin

    def gameloop(self, visual=True, num_encounters=10, speed=0.3):

        def main(curses_scr=None):
            if visual is True:
                curses.curs_set(0)
                num_encounters = 1
            if num_encounters == 1:
                enc_loop = range(num_encounters)
            else:
                enc_loop = trange(num_encounters)

            log = None
            winners = defaultdict(int)
            for _ in enc_loop:
                enc = self.initialize_encounter(visual=visual)
                gamewin, msgwin = self.initialize_windows()
                msgwin.redraw(str(enc))
                msgwin.getch()
                for round in enc.run_combat():
                    if visual is True:
                        gamewin.redraw()
                        time.sleep(speed)
                msgwin.redraw(f"Winner: {str(enc.winner)}")
                msgwin.getch()
                winners[enc.winner.name] += 1
                log = pd.concat([log, enc.log])
                del enc
            return log, winners

        if visual is True:
            log, winners = curses.wrapper(main)
        else:
            log, winners = main()

        outstr = ""
        for ((name, cid), group) in log.groupby(["attacker_name", "attacker_id"]):  # noqa
            dpr = group[group["hit"] == True]["dmg"].mean()  # noqa
            hit_ratio = group["hit"].sum() / group.shape[0]
            outstr += f"{name} ({cid}): DPR ({dpr:.2f}), hit ratio ({hit_ratio:.2f})\n"  # noqa
        outstr += "Wins\n"
        for team in self.teams:
            percentage = winners[team.name] / num_encounters
            outstr += f"{team.name}: {winners[team.name]} / {num_encounters} ({percentage:.2f})\n"  # noqa
        return outstr


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
        self.win.scrollok(True)

    def redraw(self, msg):
        self.win.erase()
        self.win.addstr(msg)
        self.win.refresh()

    def getch(self):
        self.win.getch()
