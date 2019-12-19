import numpy as np


def parse_die(die_roll):
    """
    Parse a standard die roll representation into
    the die and the number of rolls. E.g.
    2d8 -> d=8, n=2

    :param str die_roll: The die roll.
    :returns: The die and the roll.
    :rtype: (int, int)
    """
    (n, d) = die_roll.lower().split('d')
    return (int(d), int(n))


def roll_die(d=20, n=1, advantage=0):
    """
    Roll a die n number of times.

    :param int d: The die. E.g. 20 for a d20
    :param int n: The number of times to roll.
    :param int advantage: 1=advantage, -1=disadvantage, 0=regular roll
    :returns: The result of the roll.
    :rtype: int
    """
    if d == 1:
        return 1
    if advantage in [1, -1]:
        n = (n, 2)
    else:
        n = (n, 1)
    # Sum over the rolls.
    rolls = np.random.randint(1, d, size=n).sum(axis=0)
    # Then take (dis)advantage into account.
    if advantage == 1:
        return np.max(rolls)
    elif advantage == -1:
        return np.min(rolls)
    else:
        return rolls[0]
