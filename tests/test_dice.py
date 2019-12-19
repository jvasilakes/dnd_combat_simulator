import numpy as np

from .context import combat_simulator


dice = combat_simulator.dice


def test_parse_die():
    assert dice.parse_die("1d8") == (8, 1)
    assert dice.parse_die("12d3") == (3, 12)
    assert dice.parse_die(" 12d3 ") == (3, 12)


def test_roll():
    d = 20
    n = 1
    np.random.seed(0)
    reg = dice.roll_die(d=d, n=n, advantage=0)
    adv = dice.roll_die(d=d, n=n, advantage=1)
    dis = dice.roll_die(d=d, n=n, advantage=-1)
    print(type(reg))
    assert isinstance(reg, np.int64)
    assert isinstance(adv, np.int64)
    assert isinstance(dis, np.int64)
    assert adv > reg
    assert dis < reg
