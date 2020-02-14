import os
import json
import pandas as pd
from pytest import raises

from .context import combat_simulator

Character = combat_simulator.token.Character
Team = combat_simulator.encounter.Team
Grid = combat_simulator.grid.Grid
Player = combat_simulator.player.Player
Encounter = combat_simulator.encounter.Encounter

curdir = os.path.dirname(__file__)


############################
#  Team tests
############################

def test_create_team():
    test_data_dir = os.path.join(curdir, "test_data")
    good_char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    good_char_data = json.load(open(good_char_fpath))
    team_chars = [Character(**good_char_data) for _ in range(3)]
    team = Team(team_chars, name="team")
    assert team is not None

    with raises(ValueError):
        team = Team(team_chars)


def test_team_len():
    test_data_dir = os.path.join(curdir, "test_data")
    good_char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    good_char_data = json.load(open(good_char_fpath))
    team_chars = [Character(**good_char_data) for _ in range(3)]
    team = Team(team_chars, name="team")
    assert len(team) == 3


def test_get_members():
    test_data_dir = os.path.join(curdir, "test_data")
    good_char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    good_char_data = json.load(open(good_char_fpath))
    team_chars = [Character(**good_char_data) for _ in range(3)]
    team = Team(team_chars, name="team")
    team_chars[0].HP = 0
    assert team.members() == team_chars
    assert team.members(alive_only=True) == team_chars[1:]


def test_rm_member():
    test_data_dir = os.path.join(curdir, "test_data")
    good_char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    good_char_data = json.load(open(good_char_fpath))
    team_chars = [Character(**good_char_data) for _ in range(3)]
    team = Team(team_chars, name="team")
    team.rm_member(team_chars[0])
    assert team.members() == team_chars[1:]


############################
#  Encounter tests
############################

def test_create_encounter():
    test_data_dir = os.path.join(curdir, "test_data")
    good_char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    good_char_data = json.load(open(good_char_fpath))
    team1_chars = [Character(**good_char_data) for _ in range(3)]
    team1 = Team(team1_chars, name="team1")
    team2_chars = [Character(**good_char_data) for _ in range(3)]
    team2 = Team(team2_chars, name="team2")

    grid = Grid((5, 5))
    player = Player(name="test_player")
    encounter = Encounter(teams=[team1, team2], grid=grid, player=player)
    assert encounter is not None

    assert encounter._team_lookup[team1_chars[0].id] == team1
    assert encounter._team_lookup[team2_chars[2].id] == team2
    assert encounter._enemy_lookup[team1.name] == team2_chars
    assert encounter._enemy_lookup[team2.name] == team1_chars


def test_init_combat():
    test_data_dir = os.path.join(curdir, "test_data")
    good_char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    good_char_data = json.load(open(good_char_fpath))
    team1_chars = [Character(**good_char_data)]
    team1 = Team(team1_chars, name="team1")
    team2_chars = [Character(**good_char_data)]
    team2 = Team(team2_chars, name="team2")

    grid = Grid((5, 5))
    for c in team1_chars + team2_chars:
        grid.add_token(c)
    player = Player(name="test_player")
    encounter = Encounter(teams=[team1, team2], grid=grid, player=player)
    encounter.init_combat()
    assert team1_chars[0].goal == team2_chars[0]
    assert team2_chars[0].goal == team1_chars[0]


def test_fight():
    test_data_dir = os.path.join(curdir, "test_data")
    good_char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    good_char_data = json.load(open(good_char_fpath))
    team1_chars = [Character(**good_char_data)]
    team1 = Team(team1_chars, name="team1")
    team2_chars = [Character(**good_char_data)]
    team2 = Team(team2_chars, name="team2")

    grid = Grid((5, 5))
    for c in team1_chars + team2_chars:
        grid.add_token(c)
    player = Player(name="test_player")
    encounter = Encounter(teams=[team1, team2], grid=grid, player=player)
    encounter.init_combat()

    seen = set()
    while True:
        start_hp = team2_chars[0].HP
        hit, crit, dmg = encounter._fight(team1_chars[0], team2_chars[0])
        seen.add((hit, crit))
        with open("log.log", 'a') as outF:
            outF.write(str((hit, crit)) + '\n')
        assert isinstance(hit, bool)
        assert isinstance(crit, bool)
        assert dmg >= 0
        assert team2_chars[0].HP == start_hp - dmg
        if seen == {(False, False), (True, False), (True, True)}:
            break


def test_run_combat():
    test_data_dir = os.path.join(curdir, "test_data")
    good_char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    good_char_data = json.load(open(good_char_fpath))
    team1_chars = [Character(**good_char_data) for _ in range(3)]
    team1 = Team(team1_chars, name="team1")
    team2_chars = [Character(**good_char_data) for _ in range(3)]
    team2 = Team(team2_chars, name="team2")

    grid = Grid((5, 5))
    for c in team1_chars + team2_chars:
        grid.add_token(c)
    player = Player(name="test_player")
    encounter = Encounter(teams=[team1, team2], grid=grid, player=player)
    encounter.init_combat()
    rounds = list(encounter.run_combat())
    assert encounter.winner is not None
    assert len(encounter.winner.members(alive_only=True)) > 0

    assert isinstance(encounter.log, pd.DataFrame)
    assert encounter.log.shape[0] >= len(rounds)
