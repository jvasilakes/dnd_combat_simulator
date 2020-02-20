import argparse
import os
import json
import numpy as np

from combat_simulator import Character, Team, Engine, Grid
from combat_simulator.logger import log


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario_file", type=str, required=True,
                        help="""Path to JSON file specifying
                                the scenario to run.""")
    parser.add_argument("--visual", action="store_true", default=False,
                        help="""Visualize a single combat encounter.""")
    parser.add_argument("--num_encounters", type=int, default=1000,
                        help="""The number of encounters to run.""")
    parser.add_argument("--speed", type=float, default=0.4,
                        help="""How many second to wait between refreshing the
                                visualization.""")
    parser.add_argument("--grid_shape", nargs=2, type=int, default=[20, 20],
                        help="""Width and height of the battle grid.""")
    parser.add_argument("--map", type=str, default=None,
                        help="""Path to saved map file.""")
    return parser.parse_args()


def load_character_sheets(indir):
    chars_by_name = {}
    for fname in os.listdir(indir):
        if fname == "template.json":
            continue
        char_data = json.load(open(os.path.join(indir, fname)))
        chars_by_name[char_data["name"].lower()] = char_data
    return chars_by_name


def load_monsters(infile):
    monsters_data = (json.loads(line) for line in open(infile))
    monsters_by_name = {m["name"].lower(): m for m in monsters_data}
    return monsters_by_name


def run(scenario_file, num_encounters, visual, speed, grid):
    curdir = os.path.dirname(__file__)
    char_sheets_dir = os.path.join(curdir, "assets/character_sheets")
    chars_by_name = load_character_sheets(char_sheets_dir)
    monsters_file = os.path.join(curdir,
                                 "assets/5e_SRD_monsters_formatted.jsonl")
    monsters_by_name = load_monsters(monsters_file)

    scenario_data = json.load(open(scenario_file))

    teams = []
    for team_id in ["team1", "team2"]:
        team_data = scenario_data[team_id]
        team_members = []
        for char_type, num in team_data["members"]:
            (source, name) = char_type.split('.')
            if source == "character":
                data_dict = chars_by_name
            elif source == "monster":
                data_dict = monsters_by_name
            else:
                raise ValueError(f"Unsupported character source '{source}'.")
            for i in range(num):
                char_data = data_dict[name.lower()]
                team_members.append(Character(**char_data))
        team = Team(members=team_members, name=team_data["name"])
        teams.append(team)

    log.debug(" vs. ".join([str(t) for t in teams]))
    engine = Engine(*teams, grid=grid)
    summary = engine.gameloop(num_encounters=num_encounters,
                              visual=visual, speed=speed)
    print(summary)


if __name__ == "__main__":
    args = parse_args()
    if args.map is not None:
        map_matrix = np.load(args.map, allow_pickle=True)
        grid = Grid.from_map_matrix(map_matrix)
    else:
        grid = Grid(shape=args.grid_shape)
    run(args.scenario_file, args.num_encounters, args.visual,
        args.speed, grid)
