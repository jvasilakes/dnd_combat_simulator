from .context import combat_simulator

Token = combat_simulator.token.Token
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
    g.add_token(Token(name="obs", icon='#'), pos=(1, 1))
    g.add_token(Token(name="obs", icon='#'), pos=(2, 0))
    g.add_token(Token(name="obs", icon='#'), pos=(2, 1))
    g.add_token(Token(name="obs", icon='#'), pos=(3, 1))
    adj = g.to_adjacency()

    start = (0, 2)
    end = (4, 0)
    g.add_token(Token(name="start", icon='S'), pos=start)
    g.add_token(Token(name="end", icon='E'), pos=end)
    if verbose is True:
        print("Goal")
        print(g)
    path = astar(start, end, adj, moves=-1)
    for (i, n) in enumerate(path[1:]):
        g.add_token(Token(name="path", icon='+'), pos=n)
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
    g.add_token(Token(name="obs", icon='#'), pos=(1, 1))
    g.add_token(Token(name="obs", icon='#'), pos=(2, 0))
    g.add_token(Token(name="obs", icon='#'), pos=(2, 1))
    g.add_token(Token(name="obs", icon='#'), pos=(3, 1))
    adj = g.to_adjacency()

    start = (0, 2)
    end = (4, 0)
    g.add_token(Token(name="start", icon='S'), pos=start)
    g.add_token(Token(name="end", icon='E'), pos=start)
    if verbose is True:
        print("Goal")
        print(g)
    moves = 3
    path = astar(start, end, adj, moves=moves)
    for (i, n) in enumerate(path[1:]):
        g.add_token(Token(name="path", icon='+'), pos=n)
    if verbose is True:
        print("Path")
        print(g)
    assert(path == gold_path[:moves+1])


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
    obs = Token(name="obs", icon='#')
    g.add_token(obs.copy(), pos=(0, 2))
    for y in range(2, 6):
        g.add_token(obs.copy(), pos=(1, y))
    for y in range(2, 8):
        g.add_token(obs.copy(), pos=(3, y))
    for x in range(3, 7):
        g.add_token(obs.copy(), pos=(x, 1))
    for x in range(3, 7):
        g.add_token(obs.copy(), pos=(x, 5))
    for y in range(2, 4):
        g.add_token(obs.copy(), pos=(7, y))
    for x in range(8, 10):
        g.add_token(obs.copy(), pos=(x, 2))
    for x in range(11, 12):
        g.add_token(obs.copy(), pos=(x, 2))
    adj = g.to_adjacency()

    start = (0, 7)
    end = (4, 4)
    g.add_token(Token(name="start", icon='S'), pos=start)
    g.add_token(Token(name="end", icon='E'), pos=end)
    if verbose is True:
        print("Goal")
        print(g)
    path = astar(start, end, adj, moves=-1)
    for (i, n) in enumerate(path[1:]):
        g.add_token(Token(name="path", icon='+'), pos=n)
    if verbose is True:
        print("Path")
        print(g)
    assert(path == gold_path)


if __name__ == "__main__":
    test_path1(verbose=True)
    test_path1_moves(verbose=True)
    test_path2(verbose=True)
    print("Passed")
