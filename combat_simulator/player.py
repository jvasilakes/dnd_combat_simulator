from .dice import roll_die
from .astar import astar


class Player(object):
    """
    A player controls a character.
    This class implements all the actions surrounding the character,
    e.g. their movement and position, rolls, attacking, etc.

    :param Character character: This player's character.
    """

    def __init__(self, name="Default"):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def roll_initiative(self, character):
        """
        Roll combat initiative.

        :param Character character: The character to control.
        :returns: Initiative roll
        :rtype: int
        """
        roll = roll_die(d=20, n=1)
        mod = character.ability_modifier["dex"]
        return roll + mod

    def saving_throw(self, character, ability, advantage=0):
        """
        Make a saving throw for the specified ability.

        :param Character character: The character to control.
        :param str ability: The ability to use.
        :param int advantage: 1=advantage, -1=disadvantage, 0=neither
        :returns: saving throw roll
        :rtype: int
        """
        roll = roll_die(d=20, n=1, advantage=advantage)
        mod = character.ability_modifier[ability]
        return roll + mod

    def roll_attack(self, character, attack=None, advantage=0):
        """
        An attack roll for a given attack.

        :param Character character: The character to control.
        :param (Attack, str) attack: The attack to use. If None,
                                     use the default attack.
        :param int advantage: 1=advantage, -1=disadvantage, 0=neither.
        :returns: The attack roll and the attack bonus.
        :rtype: (int, int)
        """
        atk = character.get_attack(attack)
        if atk is None:
            return (0, 0)
        roll = roll_die(d=20, n=1, advantage=advantage)
        return (roll, atk.atk_bonus)

    def roll_damage(self, character, attack=None, crit=False):
        """
        A damage roll for a given attack.

        :param Character character: The character to control.
        :param (Attack, str) attack: The attack to use. If None,
                                     use the default attack.
        :param bool crit: Whether to roll critical hit damage (2 * dmg_roll).
        :returns: the damage roll and the damage bonus.
        :rtype: (int, int)
        """
        atk = character.get_attack(attack)
        if atk is None:
            return (0, 0)
        total_roll = 0
        for (d, n) in atk.dmg_rolls:
            if crit is True:
                n *= 2
            total_roll += roll_die(d=d, n=n)
        return (total_roll, atk.dmg_bonus)

    def choose_attack(self, character, target=None):
        """
        Choose the best attack for the given target.
        Currently just chooses the default attack.

        :param Character character: The character to control.
        :param Character target: The target of the attack.
        :returns: The attack to use.
        :rtype: Attack
        """
        # The main hand attack
        return character.get_attack()

    def _find_best_position(self, character, grid):
        """
        Move the character to the "best" position on the grid.

        :param Character character: The character to control.
        :param Grid grid: The grid.
        :returns: The new (x,y) position of the character on the grid.
        :rtype: tuple
        """
        pos = grid[character]
        goal_pos = grid[character.goal]
        adj = grid.to_adjacency()
        num_moves = character.speed // 5
        # Minimum 5ft of movement.
        if num_moves == 0:
            num_moves = 1
        path = astar(pos, goal_pos, adj, moves=num_moves)
        new_pos = path[-1]
        return new_pos

    def move_character(self, character, grid, pos=None):
        """
        Move the character to a new position on the grid.

        :param Character character: The character to control.
        :param Grid grid: The grid.
        :param tuple(int) pos: The new (x, y) position. Optional.
                               If None, use heuristics to find the
                               new pos.
        :returns: The new position or None if the character didn't move.
        """
        current_pos = grid[character]
        if pos is None:
            pos = self._find_best_position(character, grid)
        if pos != current_pos:
            grid[character] = pos
            return grid[character]
        else:
            return None
