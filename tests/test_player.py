import os
import json
from .context import combat_simulator


Player = combat_simulator.player.Player
Character = combat_simulator.token.Character

curdir = os.path.dirname(__file__)


def test_create_player():
    player = Player(name="Test")
    assert player is not None


def test_damage_roll():
    test_data_dir = os.path.join(curdir, "test_data")
    good_char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    good_char_data = json.load(open(good_char_fpath))
    good_char = Character(**good_char_data)
    player = Player(name="Test")
    roll = player.damage_roll(good_char)
    assert roll[0] > 0
