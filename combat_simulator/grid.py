import numpy as np
from collections import defaultdict

from .token import Token


class Grid(object):
    """
    :param tuple shape: (y, x) size of the grid.
    :param numpy.ndarray map_matrix: Numpy matrix specifying
        the map with obstacles and start positions.
    """

    def __init__(self, shape=(10, 10)):
        self.shape = shape
        self._grid = np.zeros(shape, dtype=int)
        self._tok2pos = {}  # Token.id: (y, x)
        self._pos2tok = {}  # (y, x): Token
        self._start_positions = {}  # team number: list(tuple) of positions

    def __str__(self):
        hline = ''.join(['━'] * ((2 * self.shape[1]) - 1))
        topline = '┏' + hline + '┓'
        bottomline = '┗' + hline + '┛'
        str_grid = self._grid.astype(str)
        str_grid[np.where(str_grid == '0')] = '·'
        for (pos, tok) in self._pos2tok.items():
            str_grid[pos] = tok.icon
        lines = [f"┃{' '.join(row)}┃" for row in str_grid]
        lines.insert(0, topline)
        lines.append(bottomline)
        return '\n'.join(lines)

    def __repr__(self):
        return f"{self.shape}"

    @classmethod
    def from_map_matrix(cls, map_matrix):
        """
        Instantiate the Grid from a given matrix
        (specifically a numpy.ndarray) representing a
        grid/map as constructed by map_maker.py,

        :param numpy.ndarray map_matrix: grid matrix
        :returns: Grid from the specified matrix
        :rtype: Grid
        """
        grid = cls(map_matrix.shape)
        WALL = '#'
        START_POS = ['1', '2']
        # [(pos, team_number)]
        start_positions = []
        for col in range(map_matrix.shape[0]):
            for row in range(map_matrix.shape[1]):
                icon = map_matrix[(col, row)]
                if icon == '.':
                    continue
                elif icon in START_POS:
                    start_positions.append(((col, row), int(icon)))
                    continue
                elif icon == WALL:
                    name = "wall"
                else:
                    name = "unk"
                t = Token(name=name, icon=icon)
                grid.add_token(t, pos=(col, row))

        for (pos, team) in start_positions:
            grid._set_start_positions(pos, team=team)
        return grid

    def change_shape(self, shape):
        self.shape = shape
        self._grid = np.zeros(shape, dtype=int)

    def clear_tokens(self):
        """
        Remove all non-wall tokens from this grid.
        """
        for row in range(self._grid.shape[0]):
            for col in range(self._grid.shape[1]):
                try:
                    tok = self._pos2tok[(row, col)]
                except KeyError:
                    continue
                if tok.name != "wall":
                    self._grid[(row, col)] = 0
                    del self._pos2tok[(row, col)]
                    del self._tok2pos[tok.id]

    def _set_start_positions(self, pos, team=1):
        """
        The start positions are those non-occupied
        positions within a 10ft radius of pos.

        :param tuple pos: The center of positions area.
        """
        area = set()
        for adj1 in self._get_adjacent_indices(pos):
            if self._is_traversable(adj1):
                area.add(adj1)
            for adj2 in self._get_adjacent_indices(adj1):
                if self._is_traversable(adj2):
                    area.add(adj2)
        self._start_positions[team] = list(area)

    @property
    def screen_size(self):
        y = self.shape[0] + 2
        x = (2 * self._grid.shape[1]) + 2
        return y, x

    def _is_valid(self, pos):
        """
        Check if the given position is within the boundaries
        of the grid.

        :param tuple(int) pos: The (y, x) position.
        """
        ylim = self._grid.shape[0] - 1
        xlim = self._grid.shape[1] - 1
        y, x = pos
        if y < 0 or y > ylim:
            return False
        if x < 0 or x > xlim:
            return False
        return True

    def _enforce_boundaries(self, pos):
        """
        Make sure the position stays within the boundaries
        of the grid. If the x or y coordinate of the given
        position is outside the grid, put it on the closest
        edge instead.

        :param tuple(int) pos: The (y, x) position.
        """
        if self._is_valid(pos):
            return pos
        ylim = self._grid.shape[0] - 1
        xlim = self._grid.shape[1] - 1
        y, x = pos
        y = max([0, y])
        y = min([ylim, y])
        x = max([0, x])
        x = min([xlim, x])
        return (y, x)

    def __getitem__(self, token_or_pos):
        """
        Get a token's position on the grid.
        Or the token at the given position on the grid.

        :param token_or_pos: The token or position to get.
        """
        if isinstance(token_or_pos, Token):
            token = token_or_pos
            try:
                return self._tok2pos[token.id]
            except KeyError:
                msg = f"Token {token} not in grid."
                raise KeyError(msg)
        elif isinstance(token_or_pos, tuple):
            pos = token_or_pos
            if not len(pos) == 2 and all([isinstance(p, int) for p in pos]):
                raise ValueError(f"pos must have length 2 and be (int, int).")
            if self._is_valid(pos) is False:
                msg = f"Position {pos} invalid for grid of shape {self.shape}"
                raise KeyError(msg)
            # Yes this will return None. This is desired functionality so that
            # pos is an empty cell, grid[pos] will return None.
            return self._pos2tok.get(pos)
        else:
            raise ValueError(f"Unsupported key type {type(token_or_pos)}")

    def get(self, token_or_pos):
        try:
            return self[token_or_pos]
        except KeyError:
            return None

    def __setitem__(self, token, pos):
        """
        Move a token to a new position.

        :param Token token: The token to move.
        :param tuple(int) pos: The new (y, x) position.
        """
        if not isinstance(token, Token):
            raise ValueError(f"token must be of type Token.")
        if not len(pos) == 2 and all([isinstance(p, int) for p in pos]):
            raise ValueError(f"pos must have length 2 and be (int, int).")
        new_pos = self._enforce_boundaries(pos)
        old_pos = self._tok2pos[token.id]
        # Token didn't actually move after enforcing boundaries.
        if new_pos == old_pos:
            return
        self._grid[old_pos] = 0
        self._grid[new_pos] = 1
        self._tok2pos[token.id] = new_pos
        self._pos2tok[new_pos] = token
        try:
            del self._pos2tok[old_pos]
        except KeyError:
            raise KeyError(f"{old_pos},  {token}{token.id}, {token.is_alive}\n{self._pos2tok}\n{self._tok2pos}")  # noqa

    def rm_token(self, token):
        """
        Remove a token from the grid.

        :param Token token: The token to remove.
        """
        if not isinstance(token, Token):
            raise ValueError(f"token must be of type Token.")
        pos = self._tok2pos[token.id]
        self._grid[pos] = 0
        del self._tok2pos[token.id]
        del self._pos2tok[pos]

    # TODO
    def add_team(self, team, pos=None):
        """
        Add a team of characters to the grid. If pos is not None,
        add them centered around pos. If pos is None, one of two
        things may happen:
          * If this grid contains team start positions for this team,
            they will be used.
          * An available position will be randomly assigned.
        """
        raise NotImplementedError("Grid.add_team() is planned functionality.")

    def add_token(self, token, pos=None, team=None):
        """
        Add a Token instance to the grid. If pos is not specified,
        randomly assign it to an unoccupied position.

        :param Token token: The token to add.
        :param tuple(int) pos: The (y, x) position of the token. Optional.
        :param int team: (Optional) The number of the team to which this
            token belongs.
        """
        if not isinstance(token, Token):
            raise ValueError(f"token must be of type Token.")
        # We filled up the grid!
        if self._grid.sum() == self._grid.ravel().shape[0]:
            return False
        if pos is None:
            if team is not None and self._start_positions != []:
                idxs = [i for i in self._start_positions[team]
                        if self._is_traversable(self._enforce_boundaries(i))]
                i = 0
                while idxs == []:
                    search_from = self._start_positions[team][i]
                    adjacents = self._get_adjacent_indices(search_from)
                    idxs = [i for i in adjacents
                            if self._is_traversable(self._enforce_boundaries(i))]  # noqa
                    self._start_positions[team].extend(idxs)
                    i += 1
            else:
                idxs = list(zip(*np.where(self._grid == 0)))
            chosen = np.random.choice(len(idxs))
            pos = idxs[chosen]
        pos = self._enforce_boundaries(pos)
        if not self._is_traversable(pos):
            return False
        self._grid[pos] = 1
        self._tok2pos[token.id] = pos
        self._pos2tok[pos] = token
        return True

    def _get_adjacent_indices(self, pos):
        """
        :param tuple(int) pos: The (y, x) position of the token. Optional.
        """
        m, n = self._grid.shape
        adjacent_indices = []
        y, x = pos
        if y > 0:
            adjacent_indices.append((y-1, x))
        if y+1 < m:
            adjacent_indices.append((y+1, x))
        if x > 0:
            adjacent_indices.append((y, x-1))
        if x+1 < n:
            adjacent_indices.append((y, x+1))
        return adjacent_indices

    def _is_traversable(self, node):
        try:
            if self._grid[node] == 1:
                return False
        except IndexError:
            return False
        return True

    def to_adjacency(self):
        adj = defaultdict(set)
        for y in range(self._grid.shape[0]):
            for x in range(self._grid.shape[1]):
                neighbors = self._get_adjacent_indices((y, x))
                connections = [n for n in neighbors if self._is_traversable(n)]
                for cnx in connections:
                    adj[(y, x)].add(cnx)
                    if self._is_traversable((y, x)):
                        adj[cnx].add((y, x))
        return adj

    def is_adjacent(self, token1, token2):
        """
        Test if token1 is next to token2.
        """
        token1_idxs = self[token1]
        token2_idxs = self[token2]
        adj_idxs = self._get_adjacent_indices(token1_idxs)
        if token2_idxs in adj_idxs:
            return True
        return False
