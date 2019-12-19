import numpy as np

from . import dice


class Attack(object):
    """
    An attack. It's attributes are

    name: The name of the attack. E.g. "Javelin"
    type: The type of attack. E.g. "thrown"
    range: The minimum and maximum range of this attack. E.g. "5/5".
    atk_bonus: How much to add to the attack roll.
    dmg_rolls: The damage roll(s) this attack deals. E.g. ["1d6", "2d4"]
    dmg_bonus: How much additional damage to add. E.g. 4
    dmg_type: The type of damage this attack deals. E.g. "piercing"
    properties: E.g. "Thrown".
    """

    def __init__(self, **attack_data):
        self._parse_attack_data(**attack_data)

    def _parse_attack_data(self, **data):
        self.name = data["name"]
        self.type = data["type"]
        self.range = self._parse_range(data["range"])
        self.atk_bonus = data["atk_bonus"]
        self.dmg_rolls = [dice.parse_die(die_str)
                          for die_str in data["dmg_rolls"]]
        self.dmg_bonus = data["dmg_bonus"]
        self.dmg_type = data["dmg_type"]
        self.properties = data["properties"]

    def __repr__(self):
        return str(list(self.__dict__.values()))

    @staticmethod
    def _parse_range(range_str):
        (low, high) = range_str.split('/')
        return (int(low), int(high))


class Token(object):
    """
    A generic token.
    """

    _id_counter = 0
    _id_format = "{0:02d}"

    def __init__(self, name="token", icon="t"):
        self.id = self._get_id()
        self.name = name
        self.icon = icon

    @classmethod
    def _get_id(cls):
        cls._id_counter += 1
        return cls._id_format.format(cls._id_counter)

    def __str__(self):
        return f"{self.name} ({self.icon})"

    def __repr__(self):
        return f"{self.name}_{self.id}"

    def copy(self):
        return self.__class__(name=self.name, icon=self.icon)


class Character(Token):
    """
    A (non) player character.

    :param dict character_data: Character data loaded from JSON.
    """

    _abilities = ["str", "dex", "con", "int", "wis", "cha"]

    def __init__(self, **character_data):
        super().__init__(name=character_data["name"],
                         icon=character_data["icon"])
        self._orig_char_data = character_data
        try:
            self._parse_character_data(**character_data)
        except Exception as e:
            raise ValueError(f"The following error was raised when parsing the character JSON: {e}")  # noqa
        self.goal = None

    def _parse_character_data(self, **data):
        self.str = int(data["strength"])
        self.dex = int(data["dexterity"])
        self.con = int(data["constitution"])
        self.int = int(data["intelligence"])
        self.wis = int(data["wisdom"])
        self.cha = int(data["charisma"])
        self.ac = int(data["ac"])
        self._hp_max = int(data["hp"])
        self._hp = int(data["hp"])
        self._speed_max = int(data["speed"])
        self._speed = int(data["speed"])
        tmp_atks = [Attack(**atk_data) for atk_data in data["attacks"]]
        self.attacks = dict([(atk.name, atk) for atk in tmp_atks])
        self._main_attack = tmp_atks[0]
        del tmp_atks
        self.num_attacks = int(data["num_attacks"])

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
        # Return the main hand attack by default.
        if attack is None:
            return self._main_attack
        else:
            if isinstance(attack, Attack):
                return attack
            elif isinstance(attack, str):
                try:
                    return self.attacks[attack]
                except KeyError:
                    msg = f"Unknown attack '{attack}:{type(attack)}'."
                    raise ValueError(msg)
            else:
                msg = "Argument to get_attack must be Attack of str."
                raise ValueError(msg)

    def reset(self):
        """
        Reset this character's attributes.
        """
        self._parse_character_data(**self._orig_char_data)
