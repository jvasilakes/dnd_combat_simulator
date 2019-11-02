from combat_simulator.grid import Grid


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
print(g)
adj = g.to_adjacency()
for k, v in gold_adjacency.items():
    try:
        assert(v == adj[k])
    except AssertionError as e:
        print(k, v, adj[k])
        raise e


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
print(g)
adj = g.to_adjacency()
for k, v in gold_adjacency.items():
    try:
        assert(v == adj[k])
    except AssertionError as e:
        print(k, v, adj[k])
        raise e
