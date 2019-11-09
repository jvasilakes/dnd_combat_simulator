from .context import combat_simulator

Grid = combat_simulator.grid.Grid
astar = combat_simulator.astar.astar


def test_path1(verbose=False):
    gold_path = [(0, 2),
                 (1, 2),
                 (2, 2),
                 (3, 2),
                 (4, 2),
                 (4, 1)]

    g = Grid((5, 3))
    g._grid[1, 1] = 1
    g._grid[2, 0] = 1
    g._grid[2, 1] = 1
    g._grid[3, 1] = 1
    adj = g.to_adjacency()

    start = (0, 2)
    end = (4, 0)
    g._grid[start] = 3
    g._grid[end] = 4
    if verbose is True:
        print("Goal")
        print(g)
    path = astar(start, end, adj, moves=-1)
    for (i, n) in enumerate(path):
        g._grid[n] = 2
    g._grid[start] = 3
    g._grid[end] = 4
    if verbose is True:
        print("Path")
        print(g)
    assert(path == gold_path)


def test_path1_moves(verbose=False):
    gold_path = [(0, 2),
                 (1, 2),
                 (2, 2),
                 (3, 2),
                 (4, 2),
                 (4, 1)]

    g = Grid((5, 3))
    g._grid[1, 1] = 1
    g._grid[2, 0] = 1
    g._grid[2, 1] = 1
    g._grid[3, 1] = 1
    adj = g.to_adjacency()

    start = (0, 2)
    end = (4, 0)
    g._grid[start] = 3
    g._grid[end] = 4
    if verbose is True:
        print("Goal")
        print(g)
    moves = 3
    path = astar(start, end, adj, moves=moves)
    for (i, n) in enumerate(path):
        g._grid[n] = 2
    g._grid[start] = 3
    g._grid[end] = 4
    if verbose is True:
        print("Path")
        print(g)
    assert(path == gold_path[:moves])

def test_path2(verbose=False):
    gold_path = [(0, 7), (0, 6), (1, 6),
                 (2, 6), (2, 5), (2, 4),
                 (2, 3), (2, 2), (2, 1),
                 (2, 0), (3, 0), (4, 0),
                 (5, 0), (6, 0), (7, 0),
                 (7, 1), (8, 1), (9, 1),
                 (10, 1), (10, 2), (10, 3),
                 (10, 4), (9, 4), (8, 4),
                 (7, 4), (6, 4), (5, 4)]

    g = Grid((12, 8))
    g._grid[0, 2] = 1
    g._grid[1, 2:6] = 1
    g._grid[3, 2:8] = 1
    g._grid[3:7, 1] = 1
    g._grid[3:7, 5] = 1
    g._grid[7, 2:4] = 1
    g._grid[8:10, 2] = 1
    g._grid[11:12, 2] = 1
    adj = g.to_adjacency()

    start = (0, 7)
    end = (4, 4)
    g._grid[start] = 3
    g._grid[end] = 4
    if verbose is True:
        print("Goal")
        print(g)
    path = astar(start, end, adj, moves=-1)
    for (i, n) in enumerate(path):
        g._grid[n] = 2
    g._grid[start] = 3
    g._grid[end] = 4
    if verbose is True:
        print("Path")
        print(g)
    assert(path == gold_path)


if __name__ == "__main__":
    test_path1(verbose=True)
    test_path1_moves(verbose=True)
    test_path2(verbose=True)
    print("Passed")
