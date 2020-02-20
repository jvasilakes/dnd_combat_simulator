import os
import json
import numpy as np
import pytest
from pytest import raises

from .context import combat_simulator


Character = combat_simulator.token.Character
Team = combat_simulator.encounter.Team
Grid = combat_simulator.grid.Grid
Player = combat_simulator.player.Player
Engine = combat_simulator.engine.Engine

curdir = os.path.dirname(__file__)


def test_create_engine():
    test_data_dir = os.path.join(curdir, "test_data")
    char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    char_data = json.load(open(char_fpath))
    team1_chars = [Character(**char_data) for _ in range(3)]
    team1 = Team(team1_chars, name="one")
    team2_chars = [Character(**char_data) for _ in range(3)]
    team2 = Team(team2_chars, name="two")

    with raises(ValueError):
        engine = Engine(team1, team2)

    with raises(AssertionError):
        engine = Engine(team1, team2, grid=np.zeros(shape=(5, 5)))

    grid = Grid((5, 5))
    engine = Engine(team1, team2, grid=grid)
    assert engine is not None


def test_initialize_encounter():
    test_data_dir = os.path.join(curdir, "test_data")
    char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    char_data = json.load(open(char_fpath))
    team1_chars = [Character(**char_data) for _ in range(3)]
    team1 = Team(team1_chars, name="one")
    team2_chars = [Character(**char_data) for _ in range(3)]
    team2 = Team(team2_chars, name="two")
    grid = Grid((5, 5))
    engine = Engine(team1, team2, grid=grid)
    team1_chars[0].HP = 0
    assert team1_chars[0].is_alive is False
    engine.initialize_encounter(visual=False)
    for (i, char) in enumerate(team1.members() + team2.members()):
        assert char.is_alive is True
        # The character was added to the grid.
        assert grid.get(char) is not None
        # Encounter.init_combat() was run.
        assert char.goal is not None
    del engine

    # Make too many characters to fit.
    team2_chars = [Character(**char_data) for _ in range(100)]
    team2 = Team(team2_chars, name="big two")
    engine = Engine(team1, team2, grid=grid)
    engine.initialize_encounter(visual=False)
    assert len(team2.members()) == 22


def test_initialize_encounter_visual():
    test_data_dir = os.path.join(curdir, "test_data")
    char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    char_data = json.load(open(char_fpath))
    team1_chars = [Character(**char_data) for _ in range(3)]
    team1 = Team(team1_chars, name="one")
    team2_chars = [Character(**char_data) for _ in range(3)]
    team2 = Team(team2_chars, name="two")
    grid = Grid((5, 5))
    engine = Engine(team1, team2, grid=grid)
    engine.initialize_encounter(visual=True)
    for char in team1.members() + team2.members():
        # The character was added to the grid.
        assert grid.get(char) is not None
        # Encounter.init_combat() was run.
        assert char.goal is not None
        # Speed is minimized
        assert char.speed == 5


@pytest.mark.xfail
def test_gameloop():
    test_data_dir = os.path.join(curdir, "test_data")
    char_fpath = os.path.join(test_data_dir, "test_character_good.json")
    char_data = json.load(open(char_fpath))
    team1_chars = [Character(**char_data) for _ in range(3)]
    team1 = Team(team1_chars, name="one")
    team2_chars = [Character(**char_data) for _ in range(3)]
    team2 = Team(team2_chars, name="two")
    grid = Grid((5, 5))
    engine = Engine(team1, team2, grid=grid)
    summary = engine.gameloop(visual=False, num_encounters=10)
    assert isinstance(summary, str)
    assert len(summary) > 0
