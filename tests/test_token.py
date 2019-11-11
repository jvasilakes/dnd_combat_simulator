import os
import re
import json

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
