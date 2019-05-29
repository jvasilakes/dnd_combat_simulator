from .base import roll_die


class Player(object):
    """
    A player controls a character.
    This class implements all the actions surrounding the character,
    e.g. their movement and position, rolls, attacking, etc.

    :param Character character: This player's character.
    """

    def __init__(self, character):
        self.character = character
        self.pos = (-1, -1)  # The character position x, y

    def __str__(self):
        return str(self.character)

    def __repr__(self):
        return repr(self.character)
    
    def roll_initiative(self):
        """
        Roll combat initiative.

        :returns: Initiative roll
        :rtype: int
        """
        roll = roll_die(d=20, n=1)
        mod = self.character.ability_modifier["dex"]
        return roll + mod

    def saving_throw(self, ability, advantage=0):
        """
        Make a saving throw for the specified ability.

        :param str ability: The ability to use.
        :param int advantage: 1=advantage, -1=disadvantage, 0=neither
        :returns: saving throw roll
        :rtype: int
        """
        roll = roll_die(d=20, n=1, advantage=advantage)
        mod = self.character.ability_modifier[ability]
        return roll + mod

    def attack_roll(self, attack=None, advantage=0):
        """
        An attack roll for a given attack.

        :param (Attack, str) attack: The attack to use. If None,
                                     use the default attack.
        :param int advantage: 1=advantage, -1=disadvantage, 0=neither.
        :returns: The attack roll and the attack bonus.
        :rtype: (int, int)
        """
        atk = self.character.get_attack(attack)
        roll = roll_die(d=20, n=1, advantage=advantage)
        return (roll, atk.atk_bonus)

    def damage_roll(self, attack=None, crit=False):
        """
        A damage roll for a given attack.

        :param (Attack, str) attack: The attack to use. If None,
                                     use the default attack.
        :param bool crit: Whether to roll critical hit damage (2 * dmg_roll).
        :returns: the damage roll and the damage bonus.
        :rtype: (int, int)
        """
        atk = self.character.get_attack(attack)
        d, n = atk.dmg_roll
        if crit is True:
            n *= 2
        roll = roll_die(d=d, n=n)
        return (roll, atk.dmg_bonus)

    def choose_attack(self, target):
        """
        Choose the best attack for the given target.
        Currently just chooses the default attack.

        :param Character target: The target of the attack.
        :returns: The attack to use.
        :rtype: Attack
        """
        # The main hand attack
        return self.character.get_attack()

    def move_character(self):
        raise NotImplementedError
