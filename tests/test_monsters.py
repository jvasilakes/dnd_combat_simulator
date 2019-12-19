import os
import json

from .context import combat_simulator


Player = combat_simulator.player.Player
Character = combat_simulator.token.Character
curdir = os.path.dirname(__file__)


def test_load_monsters():
    monster_file = os.path.join(curdir, "../assets/5e_SRD_monsters.jsonl")
    monster_data = [json.loads(line) for line in open(monster_file)]
    for md in monster_data:
        monster = Character(**md)
        assert monster is not None


def test_attack_damage():
    player = Player(name="Test")
    monster_file = os.path.join(curdir, "../assets/5e_SRD_monsters.jsonl")
    monster_data = [json.loads(line) for line in open(monster_file)]
    for md in monster_data:
        monster = Character(**md)
        atk_roll = player.attack_roll(monster)
        assert atk_roll is not None
        dmg_roll = player.damage_roll(monster)
        assert atk_roll is not None
