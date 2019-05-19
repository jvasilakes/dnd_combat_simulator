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


def roll_die(d=20, n=1):
    """
    Roll a die n number of times.

    :param int d: The die. E.g. 20 for a d20
    :param int n: The number of times to roll.
    :returns: The result of the roll.
    :rtype: int
    """
    return np.random.randint(1, d, size=n).sum()


class Weapon(object):
    """
    A weapon. It's attributes are

    name: The name of the weapon. E.g. "Javelin"
    type: The type of weapon. E.g. "thrown"
    dmg_roll: The damage roll this weapon deals. E.g. "1d6"
    dmg_bonus: How much additional damage to add. E.g. 4
    dmg_type: The type of damage this weapon deals. E.g. "piercing"
    """

    def __init__(self, **weapon_data):
        self._parse_weapon_data(**weapon_data)

    def _parse_weapon_data(self, **data):
        self.name = data["name"]
        self.type = data["type"]
        self.dmg_roll = data["dmg_roll"]
        self.dmg_bonus = data["dmg_bonus"]
        self.dmg_type = data["dmg_type"]


class Character(object):

    _abilities = ["str", "dex", "con", "int", "wis", "cha"]

    def __init__(self, **character_data):
        self._parse_character_data(**character_data)

    def _parse_character_data(self, **data):
        self.name = data["name"]
        self.str = data["strength"]
        self.dex = data["dexterity"]
        self.con = data["constitution"]
        self.int = data["intelligence"]
        self.wis = data["wisdom"]
        self.cha = data["charisma"]
        self._hp_max = data["hp"]
        self._hp = data["hp"]
        self.ac = data["ac"]
        self.speed = data["speed"]
        self.prof = data["proficiency_bonus"]
        tmp_wpns = [Weapon(**wpn_data) for wpn_data in data["weapons"]]
        self.weapons = dict([(wpn.name, wpn) for wpn in tmp_wpns])

    @staticmethod
    def _compute_modifier(ability_score):
        """
        Calculates the modifier for the given ability score.

        :param int ability_score: The ability score.
        :returns: the ability score modifier
        :rtype: int
        """
        return int(np.floor((ability_score - 10) / 2))

    @property
    def ability_modifier(self):
        """
        A dictionary from abilities to modifiers.
        Keys are "str", "dex", "con", "int", "wis", "cha"
        """
        mods = {}
        for ab in self._abilities:
            score = self.__dict__.get(ab)
            mods[ab] = self._compute_modifier(score)
        return mods

    @property
    def attack_bonus(self):
        """
        A dictionary from weapon names to attack bonuses.
        Computed according to the 5e ruleset.
        """
        bonuses = {}
        for wpn_name in self.weapons.keys():
            stat = "str"  # TODO: Make this follow the rules.
            bonus = self.prof + self.ability_modifier[stat]
            bonuses[wpn_name] = bonus
        return bonuses

    @property
    def HP(self):
        """
        The hit points getter.
        """
        return self._hp

    @HP.setter
    def HP(self, value):
        """
        The hit points setter.

        :param int value: The new HP value.
        """
        if value < 0:
            raise ValueError("HP cannot be below 0")
        if value > self._hp_max:
            msg = f"HP cannot be above HP maximum: {self._hp_max}"
            raise ValueError(msg)
        self._hp = value

    def attack(self, weapon):
        """
        An attack roll.

        :param str weapon: The name of the weapon to attack with.
        :returns: The attack roll and attack bonus.
        :rtype: (int, int)
        """
        weapon = self.weapons[weapon]
        atk_bonus = self.attack_bonus[weapon.name]
        roll = np.sum(roll_die(d=20, n=1))
        return (roll, atk_bonus)

    def damage(self, weapon, crit=False):
        """
        A damage roll.

        :param str weapon: The name of the weapon.
        :returns: The damage roll.
        :rtype: int
        """
        weapon = self.weapons[weapon]
        d, n = parse_die(weapon.dmg_roll)
        roll = roll_die(d=d, n=n)
        return roll + weapon.dmg_bonus
