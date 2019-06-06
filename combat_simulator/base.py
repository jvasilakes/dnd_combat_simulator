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
    n = (n, 1)
    if advantage in [1, -1]:
        n = (n, 2)  # rolls x advantage
    # Sum over the rolls.
    rolls = np.random.randint(1, d, size=n).sum(axis=0)
    # Then take (dis)advantage into account.
    if advantage == 1:
        return np.max(rolls)
    elif advantage == -1:
        return np.min(rolls)
    else:
        return rolls[0]


class Attack(object):
    """
    An attack. It's attributes are

    name: The name of the attack. E.g. "Javelin"
    type: The type of attack. E.g. "thrown"
    dmg_roll: The damage roll this attack deals. E.g. "1d6"
    dmg_bonus: How much additional damage to add. E.g. 4
    dmg_type: The type of damage this attack deals. E.g. "piercing"
    """

    def __init__(self, **attack_data):
        self._parse_attack_data(**attack_data)

    def _parse_attack_data(self, **data):
        self.name = data["name"]
        self.type = data["type"]
        self.range = self._parse_range(data["range"])
        self.atk_bonus = data["atk_bonus"]
        self.dmg_roll = parse_die(data["dmg_roll"])
        self.dmg_bonus = data["dmg_bonus"]
        self.dmg_type = data["dmg_type"]
        self.properties = data["properties"]

    def __repr__(self):
        return str(list(self.__dict__.values()))

    @staticmethod
    def _parse_range(range_str):
        (low, high) = range_str.split('/')
        return (int(low), int(high))


class Character(object):

    _id_counter = 0
    _id_format = "{0:02d}"
    _abilities = ["str", "dex", "con", "int", "wis", "cha"]

    def __init__(self, **character_data):
        self.id = self.get_id()
        self._parse_character_data(**character_data)

    @classmethod
    def get_id(cls):
        cls._id_counter += 1
        return cls._id_format.format(cls._id_counter)

    def _parse_character_data(self, **data):
        self.name = data["name"]
        self.icon = data["icon"]
        self.str = data["strength"]
        self.dex = data["dexterity"]
        self.con = data["constitution"]
        self.int = data["intelligence"]
        self.wis = data["wisdom"]
        self.cha = data["charisma"]
        self.ac = data["ac"]
        self._hp_max = data["hp"]
        self._hp = data["hp"]
        self._speed_max = data["speed"]
        self._speed = data["speed"]
        tmp_atks = [Attack(**atk_data) for atk_data in data["attacks"]]
        self.attacks = dict([(atk.name, atk) for atk in tmp_atks])
        self._main_attack = tmp_atks[0]
        del tmp_atks
        self.num_attacks = data["num_attacks"]

    def __str__(self):
        return f"{self.name} ({self.icon})"

    def __repr__(self):
        return f"{self.name}_{self.id}"

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
        if value > self._hp_max:
            msg = f"HP cannot be above HP maximum: {self._hp_max}"
            raise ValueError(msg)
        self._hp = value

    @property
    def is_alive(self):
        """
        Whether or not this character is alive.
        """
        return self.HP > 0

    @property
    def speed(self):
        """
        The speed getter.
        """
        return self._speed

    @speed.setter
    def speed(self, value):
        """
        The speed setter.

        :param int value: The new speed value.
        """
        if value < 0:
            raise ValueError("speed cannot be below 0")
        if value > self._speed_max:
            msg = f"speed cannot be above speed maximum: {self._speed_max}"
            raise ValueError(msg)
        self._speed = value

    def get_attack(self, attack=None):
        """
        Interface to the character's attacks.

        :param (None, str, Attack) attack: The attack to get.
        :returns: Attack instance
        :rtype: Attack
        """
        if attack is None:
            return self._main_attack
        else:
            if isinstance(attack, Attack):
                return attack
            elif isinstance(attack, str):
                return self.attacks[attack]
            else:
                raise ValueError(f"Unknown attack '{attack}:{type(attack)}'.")

    def reset(self):
        """
        Reset this character's attributes.
        """
        self.HP = self._hp_max
        self.speed = self._speed_max


class Player(object):
    """
    A player controls a character.
    This class implements all the actions surrounding the character,
    e.g. their movement and position, rolls, attacking, etc.

    :param Character character: This player's character.
    """

    def __init__(self, character):
        self.character = character

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

    # TODO: Make this smarter.
    def _find_best_position(self, grid):
        pos = grid[self.character]
        return (pos[0] + 1, pos[1] + 1)

    def move_character(self, grid, pos=None):
        """
        Move the character to a new position on the grid.

        :param Grid grid: The grid.
        :param tuple(int) pos: The new (x, y) position. Optional.
                               If None, use heuristics to find the
                               new pos.
        """
        if pos is None:
            pos = self._find_best_position(grid)
        grid[self.character] = pos
