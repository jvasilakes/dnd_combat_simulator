import argparse
import os
import json

from combat_simulator import Character, Team, Engine, Grid


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario_file", type=str, required=True,
                        help="""Path to JSON file specifying
                                the scenario to run.""")
    parser.add_argument("--visual", action="store_true", default=False,
                        help="""Visualize a single combat encounter.""")
    parser.add_argument("--num_encounters", type=int, default=1000,
                        help="""The number of encounters to run.""")
    parser.add_argument("--speed", type=float, default=0.3,
                        help="""How many second to wait between refreshing the
                                visualization.""")
    parser.add_argument("--grid_shape", nargs=2, type=int, default=[20, 20],
                        help="""Width and height of the battle grid.""")
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

    team1 = scenario_data["team1"]
    team_1_members = []
    for mem in team1["members"]:
        (source, name) = mem.split('.')
        if source == "character":
            char_data = chars_by_name[name.lower()]
        elif source == "monster":
            char_data = monsters_by_name[name.lower()]
        else:
            raise ValueError(f"Unsupported character source '{source}'.")
        team_1_members.append(Character(**char_data))
    team1 = Team(members=team_1_members, name=team1["name"])

    team2 = scenario_data["team2"]
    team_2_members = []
    for mem in team2["members"]:
        (source, name) = mem.split('.')
        if source == "character":
            char_data = chars_by_name[name.lower()]
        elif source == "monster":
            char_data = monsters_by_name[name.lower()]
        else:
            raise ValueError(f"Unsupported character source '{source}'.")
        team_2_members.append(Character(**char_data))
    team2 = Team(members=team_2_members, name=team2["name"])

    engine = Engine(team1, team2, grid=grid)
    engine.gameloop(num_encounters=num_encounters, visual=visual, speed=speed)


if __name__ == "__main__":
    args = parse_args()
    grid = Grid(shape=args.grid_shape)
    run(args.scenario_file, args.num_encounters, args.visual,
        args.speed, grid)
