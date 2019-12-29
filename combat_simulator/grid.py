import numpy as np
from collections import defaultdict

from .token import Token


class Grid(object):
    """
    :param tuple shape: (y, x) size of the grid.
    """

    def __init__(self, shape=(10, 10)):
        self.shape = shape
        self._grid = np.zeros(shape, dtype=int)
        self._tok2pos = {}
        self._pos2tok = {}
        self._icon_map = {}

    def __str__(self):
        hline = ''.join(['━'] * ((2 * self.shape[1]) - 1))
        topline = '┏' + hline + '┓'
        bottomline = '┗' + hline + '┛'
        str_grid = self._grid.astype(str)
        str_grid[np.where(str_grid == '0')] = '·'
        for (tid, pos) in self._tok2pos.items():
            icon = self._icon_map[tid]
            str_grid[pos] = icon
        lines = [f"┃{' '.join(row)}┃" for row in str_grid]
        lines.insert(0, topline)
        lines.append(bottomline)
        return '\n'.join(lines)

    def __repr__(self):
        return f"{self.shape}"

    def change_shape(self, shape):
        self.shape = shape
        self._grid = np.zeros(shape, dtype=int)

    def clear(self):
        for row in range(self._grid.shape[0]):
            for col in range(self._grid.shape[1]):
                try:
                    tok = self._pos2tok[(row, col)]
                except KeyError:
                    continue
                if tok.name != "wall":
                    self._grid[(row, col)] == 0
                    del self._pos2tok[(row, col)]
                    del self._tok2pos[tok]
                    del self._icon_map[tok.id]

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
        pos = self._enforce_boundaries(pos)
        current_pos = self._tok2pos[token.id]
        self._grid[current_pos] = 0
        self._grid[pos] = 1
        self._tok2pos[token.id] = pos
        self._pos2tok[pos] = token

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
        del self._icon_map[token.id]
        self._pos2tok[pos] = None

    def add_token(self, token, pos=None):
        """
        Add a Token instance to the grid. If pos is not specified,
        randomly assign it to an unoccupied position.

        :param Token token: The token to add.
        :param tuple(int) pos: The (y, x) position of the token. Optional.
        """
        if not isinstance(token, Token):
            raise ValueError(f"token must be of type Token.")
        if pos is None:
            idxs = np.where(self._grid == 0)
            chosen = np.random.choice(range(idxs[0].shape[0]))
            y = idxs[0][chosen]
            x = idxs[1][chosen]
            pos = (y, x)
        pos = self._enforce_boundaries(pos)
        self._grid[pos] = 1
        self._tok2pos[token.id] = pos
        self._icon_map[token.id] = token.icon
        self._pos2tok[pos] = token

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
