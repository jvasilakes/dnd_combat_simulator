import logging
import numpy as np
from collections import defaultdict

from .character import Character

logging.basicConfig(filename="app.log", filemode='w', level=logging.DEBUG)


class Grid(object):

    def __init__(self, shape=(10, 10)):
        self.shape = shape
        self._grid = np.zeros(shape, dtype=int)
        self._grid_map = {}
        self._icon_map = {}

    def __str__(self):
        hline = ''.join(['━'] * ((2 * self._grid.shape[1]) - 1))
        topline = '┏' + hline + '┓'
        bottomline = '┗' + hline + '┛'
        str_grid = self._grid.astype(str)
        str_grid[np.where(str_grid == '0')] = '·'
        for (cid, pos) in self._grid_map.items():
            icon = self._icon_map[cid]
            str_grid[pos] = icon
        lines = [f"┃{' '.join(row)}┃" for row in str_grid]
        lines.insert(0, topline)
        lines.append(bottomline)
        return '\n'.join(lines)

    def __repr__(self):
        return f"{self._grid.shape}"

    @property
    def screen_size(self):
        x = (2 * self._grid.shape[0]) + 2
        y = self.shape[1] + 2
        return x, y

    def _enforce_boundaries(self, pos):
        """
        Make sure the position stays within the boundaries
        of the grid. If the x or y coordinate of the given
        position is outside the grid, put it on the closest
        edge instead.

        :param tuple(int) pos: The (x, y) position.
        """
        xlim = self._grid.shape[0] - 1
        ylim = self._grid.shape[1] - 1
        x, y = pos
        x = max([0, x])
        x = min([xlim, x])
        y = max([0, y])
        y = min([ylim, y])
        return (x, y)

    def __getitem__(self, character_or_pos):
        """
        Get a character's position on the grid.

        :param Character character: The character.
        """
        if isinstance(character_or_pos, Character):
            return self._grid_map[character_or_pos.id]
        elif isinstance(character_or_pos, tuple):
            pos = self._enforce_boundaries(character_or_pos)
            try:
                return self._grid[pos]
            except IndexError:
                return -1

    def get(self, character_or_pos):
        try:
            self[character_or_pos]
        except KeyError:
            return None

    def __setitem__(self, character, pos):
        """
        Move a character to a new position.

        :param Character character: The character.
        :param tuple(int) pos: The new (x, y) position.
        """
        if not isinstance(character, Character):
            raise ValueError(f"character must be of type Character.")
        if not len(pos) == 2 and all([isinstance(p, int) for p in pos]):
            raise ValueError(f"pos must have length 2 and be (int, int).")
        pos = self._enforce_boundaries(pos)
        current_pos = self._grid_map[character.id]
        self._grid[current_pos] = 0
        self._grid[pos] = 1
        self._grid_map[character.id] = pos

    def __delitem__(self, character):
        """
        Remove a character from the grid.

        :param Character character: The character.
        """
        if not isinstance(character, Character):
            raise ValueError(f"character must be of type Character.")
        pos = self._grid_map[character.id]
        self._grid[pos] = 0
        del self._grid_map[character.id]

    def add_character(self, character, pos=None):
        """
        Add a Character instance to the grid. If pos is not specified,
        randomly assign it to an unoccupied position.

        :param Character character: The character to add.
        :param tuple(int) pos: The (x, y) position of the character. Optional.
        """
        if not isinstance(character, Character):
            raise ValueError(f"character must be of type Character.")
        if pos is None:
            idxs = np.where(self._grid == 0)
            x = np.random.choice(idxs[0])
            y = np.random.choice(idxs[1])
            pos = (x, y)
        self._grid[pos] = 1
        self._grid_map[character.id] = pos
        self._icon_map[character.id] = character.icon

    def to_adjacency(self):

        def get_adjacent_indices(x, y, m, n):
            """
            x, y: row and columns positions to check
            m, n: total number of rows and columns in the matrix
            """
            adjacent_indices = []
            if x > 0:
                adjacent_indices.append((x-1, y))
            if x+1 < m:
                adjacent_indices.append((x+1, y))
            if y > 0:
                adjacent_indices.append((x, y-1))
            if y+1 < n:
                adjacent_indices.append((x, y+1))
            return adjacent_indices

        def is_traversable(node):
            try:
                if self._grid[node] == 1:
                    return False
            except IndexError:
                return False
            return True

        adj = defaultdict(set)
        for x in range(self._grid.shape[0]):
            for y in range(self._grid.shape[1]):
                neighbors = get_adjacent_indices(x, y, *self._grid.shape)
                connections = [n for n in neighbors if is_traversable(n)]
                for cnx in connections:
                    adj[(x, y)].add(cnx)
                    if is_traversable((x, y)):
                        adj[cnx].add((x, y))
        return adj
