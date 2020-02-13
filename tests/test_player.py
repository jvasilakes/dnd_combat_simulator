import os
import json
from .context import combat_simulator


Player = combat_simulator.player.Player
Character = combat_simulator.token.Character
Grid = combat_simulator.grid.Grid

curdir = os.path.dirname(__file__)


def test_create_player():
    player = Player(name="Test")
    assert player is not None


def test_roll_initiative():
    player = Player(name="Test")
    test_data_dir = os.path.join(curdir, "test_data")
    good_char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    good_char_data = json.load(open(good_char_fpath))
    good_char = Character(**good_char_data)
    roll = player.roll_initiative(good_char)
    assert roll > 0
    assert roll <= 20 + good_char.ability_modifier["dex"]


def test_roll_attacks():
    player = Player(name="Test")
    test_data_dir = os.path.join(curdir, "test_data")
    good_char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    good_char_data = json.load(open(good_char_fpath))
    good_char = Character(**good_char_data)
    roll = player.roll_attack(good_char)
    assert roll[0] > 0


def test_roll_damage():
    player = Player(name="Test")
    test_data_dir = os.path.join(curdir, "test_data")
    good_char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    good_char_data = json.load(open(good_char_fpath))
    good_char = Character(**good_char_data)
    roll = player.roll_damage(good_char)
    assert roll[0] > 0
    roll = player.roll_damage(good_char, crit=True)
    assert roll[0] > 0


def test_saving_throw():
    player = Player(name="Test")
    test_data_dir = os.path.join(curdir, "test_data")
    good_char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    good_char_data = json.load(open(good_char_fpath))
    good_char = Character(**good_char_data)
    for ability in ["str", "dex", "con", "wis", "int", "cha"]:
        roll = player.saving_throw(good_char, ability)
        assert roll > 0
        assert roll <= 20 + good_char.ability_modifier[ability]


def test_get_default_attack():
    player = Player(name="Test")
    test_data_dir = os.path.join(curdir, "test_data")
    good_char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    good_char_data = json.load(open(good_char_fpath))
    good_char = Character(**good_char_data)

    atk = player.choose_attack(good_char)
    assert atk == good_char._main_attack


def test_find_best_position():
    player = Player(name="Test")
    test_data_dir = os.path.join(curdir, "test_data")
    good_char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    good_char_data = json.load(open(good_char_fpath))
    good_char = Character(**good_char_data)

    good_char2 = Character(**good_char_data)
    good_char2.name = "Goal"

    grid = Grid((6, 6))
    grid.add_token(good_char, pos=(0, 0))
    grid.add_token(good_char2, pos=(0, 5))
    good_char.goal = good_char2
    new_pos = player._find_best_position(good_char, grid)
    assert new_pos == (0, 4)


def test_move_character():
    player = Player(name="Test")
    test_data_dir = os.path.join(curdir, "test_data")
    good_char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    good_char_data = json.load(open(good_char_fpath))
    good_char = Character(**good_char_data)

    grid = Grid((6, 6))
    grid.add_token(good_char, pos=(0, 0))
    new_pos = player.move_character(good_char, grid, pos=(4, 4))
    assert new_pos == (4, 4)

    # Return None if the character doesn't move.
    new_pos = player.move_character(good_char, grid, pos=grid[good_char])
    assert new_pos is None
