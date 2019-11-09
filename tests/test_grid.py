from .context import combat_simulator


Grid = combat_simulator.grid.Grid


def test_to_adjacency1():
    gold_adjacency = {(0, 0): set([(0, 1), (1, 0)]),
                      (0, 1): set([(0, 0)]),
                      (0, 2): set([(0, 1)]),
                      (1, 0): set([(0, 0), (2, 0)]),
                      (1, 1): set([(0, 1), (1, 0), (2, 1)]),
                      (1, 2): set([(2, 2)]),
                      (2, 0): set([(2, 1), (1, 0)]),
                      (2, 1): set([(2, 0), (2, 2)]),
                      (2, 2): set([(2, 1)])}

    g = Grid((3, 3))
    g._grid[0, 2] = 1
    g._grid[1, 1] = 1
    g._grid[1, 2] = 1
    adj = g.to_adjacency()
    for k, v in gold_adjacency.items():
        assert v == adj[k]


def test_to_adjacency2():
    gold_adjacency = {(0, 0): set([(0, 1), (1, 0)]),
                      (0, 1): set([(0, 2)]),
                      (0, 2): set([(0, 1), (1, 2)]),
                      (1, 0): set([(2, 0)]),
                      (1, 1): set([(0, 1), (1, 0), (1, 2)]),
                      (1, 2): set([(0, 2), (2, 2)]),
                      (2, 0): set([(3, 0), (1, 0)]),
                      (2, 1): set([(2, 0), (2, 2), (3, 1)]),
                      (2, 2): set([(1, 2), (3, 2)]),
                      (3, 0): set([(2, 0), (3, 1)]),
                      (3, 1): set([(3, 0), (3, 2)]),
                      (3, 2): set([(3, 1), (2, 2)])}

    g = Grid((4, 3))
    g._grid[0, 0] = 1
    g._grid[1, 1] = 1
    g._grid[2, 1] = 1
    adj = g.to_adjacency()
    for k, v in gold_adjacency.items():
        assert v == adj[k]


def test_is_traversable():
    g = Grid((2, 2))
    assert g._is_traversable((1, 1)) is True
    assert g._is_traversable((4, 7)) is False


if __name__ == "__main__":
    test_to_adjacency1()
    test_to_adjacency2()
    test_is_traversable()
    print("Passed")
