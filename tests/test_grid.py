from pytest import raises

from .context import combat_simulator


Grid = combat_simulator.grid.Grid
Token = combat_simulator.token.Token


def test_screen_size():
    assert Grid((3, 3)).screen_size == (5, 8)
    assert Grid((3, 1)).screen_size == (5, 4)
    assert Grid((10, 50)).screen_size == (12, 102)


def test_grid_print():
    gold = """┏━━━━━┓
┃· · ·┃
┃· T ·┃
┃· · ·┃
┗━━━━━┛"""
    g = Grid((3, 3))
    g.add_token(Token(name="tok", icon='T'), pos=(1, 1))
    assert str(g) == gold


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


def test_add_get_token():
    g = Grid((2, 2))
    pos = (1, 1)
    t = Token(name="tok")
    g.add_token(t, pos=pos)
    assert g[t] == pos
    assert g.get(t) == pos
    assert g[pos] == t
    assert g.get(pos) == t
    assert g.get((5, 0)) is None
    assert g.get((0, 5)) is None
    with raises(KeyError):
        g[t.copy()]
    with raises(ValueError):
        g.add_token('token')
    with raises(ValueError):
        g[(0, 0, 0)]
    with raises(ValueError):
        g['token']


def test_set_token():
    g = Grid((2, 2))
    t = Token(name="tok")
    new_pos = (1, 1)
    g.add_token(t, pos=(0, 0))
    g[t] = new_pos
    assert g[t] == new_pos
    assert g.get(t) == new_pos
    assert g[new_pos] == t
    assert g.get(new_pos) == t
    with raises(ValueError):
        g['token'] = (0, 0)
    with raises(ValueError):
        g[t] = (0, 0, 0)


def test_rm_token():
    g = Grid((2, 2))
    t = Token(name="tok")
    pos = (0, 0)
    g.add_token(t, pos=pos)
    assert g[t] == pos
    g.rm_token(t)
    assert g.get(t) is None
    assert g[pos] is None
    with raises(KeyError):
        g[t]
    with raises(ValueError):
        g.rm_token('token')


def test_is_traversable():
    g = Grid((2, 2))
    assert g._is_traversable((1, 1)) is True
    assert g._is_traversable((4, 7)) is False


def test_is_adjacent():
    g = Grid((3, 3))
    t1 = Token(name="tok")
    t2 = Token(name="tok")
    t3 = Token(name="tok")
    pos1 = (0, 0)
    pos2 = (1, 0)
    pos3 = (2, 2)
    g.add_token(t1, pos=pos1)
    g.add_token(t2, pos=pos2)
    g.add_token(t3, pos=pos3)
    assert g.is_adjacent(t1, t2) is True
    assert g.is_adjacent(t1, t3) is False
    assert g.is_adjacent(t2, t3) is False
