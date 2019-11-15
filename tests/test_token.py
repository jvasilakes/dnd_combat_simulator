import os
import re
import json
import copy

from pytest import raises

from .context import combat_simulator

Token = combat_simulator.token.Token
Character = combat_simulator.token.Character

curdir = os.path.dirname(__file__)


def test_create_token():
    tok = Token(name="Jake", icon="J")
    assert tok is not None
    assert isinstance(tok, Token)
    tok = Token()
    assert tok.name == "token"
    assert tok.icon == "t"
    assert str(tok) == "token (t)"
    assert re.match(r"token_[0-9]{2}", repr(tok))


def test_create_character():
    test_data_dir = os.path.join(curdir, "test_data")
    good_char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    good_char_data = json.load(open(good_char_fpath))
    good_char = Character(**good_char_data)
    assert good_char is not None
    assert good_char.str == good_char_data["strength"]
    assert good_char.dex == good_char_data["dexterity"]
    assert good_char.con == good_char_data["constitution"]
    assert good_char.int == good_char_data["intelligence"]
    assert good_char.wis == good_char_data["wisdom"]
    assert good_char.cha == good_char_data["charisma"]
    assert good_char.ac == good_char_data["ac"]
    assert good_char.HP == good_char_data["hp"]
    assert good_char._speed == good_char_data["speed"]
    assert good_char.num_attacks == good_char_data["num_attacks"]
    # TODO check attacks are correct

    bad_char_fpath = os.path.join(test_data_dir,
                                  "test_character_bad_dtype.json")
    bad_char_data = json.load(open(bad_char_fpath))
    with raises(ValueError):
        Character(**bad_char_data)

    bad_char_fpath = os.path.join(test_data_dir,
                                  "test_character_bad_key.json")
    bad_char_data = json.load(open(bad_char_fpath))
    with raises(ValueError):
        Character(**bad_char_data)


def test_modifier():
    test_data_dir = os.path.join(curdir, "test_data")
    char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    char_data = json.load(open(char_fpath))
    char = Character(**char_data)

    gold_mods = [-5, -4, -4, -3, -3, -2, -2, -1, -1,
                 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5,
                 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]

    for score in range(1, 31):
        computed_mod = char._compute_modifier(score)
        assert computed_mod == gold_mods[score - 1]

    for ability in ["str", "dex", "con", "int", "wis", "cha"]:
        score = getattr(char, ability)
        assert gold_mods[score - 1] == char.ability_modifier[ability]


def test_hp():
    test_data_dir = os.path.join(curdir, "test_data")
    char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    char_data = json.load(open(char_fpath))
    char = Character(**char_data)

    # Test the setter
    char.HP = 10
    assert char.HP == 10
    with raises(ValueError):
        char.HP = char._hp_max + 1

    # Test is_alive
    char.HP = 0
    assert char.is_alive is False


def test_speed():
    test_data_dir = os.path.join(curdir, "test_data")
    char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    char_data = json.load(open(char_fpath))
    char = Character(**char_data)

    # Test the setter
    char.speed = 10
    assert char.speed == 10
    with raises(ValueError):
        char.speed = -1
    with raises(ValueError):
        char.speed = char._speed_max + 1


def test_attack():
    test_data_dir = os.path.join(curdir, "test_data")
    char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    char_data = json.load(open(char_fpath))
    char = Character(**char_data)

    # Default return value is main hand
    atk = char.get_attack()
    assert atk == char._main_attack

    # get_attack using Attack instance
    atk = char.get_attack(char._main_attack)
    assert atk == char._main_attack

    # get_attack using attack name
    atk = char.get_attack("Punch")
    assert atk == char._main_attack

    # Unknown attack
    with raises(ValueError):
        char.get_attack("Kick")

    # Unknown attack type
    with raises(ValueError):
        char.get_attack(10)


def test_reset():
    test_data_dir = os.path.join(curdir, "test_data")
    char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    char_data = json.load(open(char_fpath))
    char = Character(**char_data)
    orig_char = copy.deepcopy(char)

    for ability in ["str", "dex", "con", "int", "wis", "cha"]:
        setattr(char, ability, 1)
    char.HP -= 5
    char.speed -= 10

    char.reset()
    assert char is not None
    assert char.str == orig_char.str
    assert char.dex == orig_char.dex
    assert char.con == orig_char.con
    assert char.int == orig_char.int
    assert char.wis == orig_char.wis
    assert char.cha == orig_char.cha
    assert char.HP == orig_char.HP
    assert char._speed == orig_char.speed
