import argparse
import json

from combat_simulator import Character, Team, Engine


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--visual", action="store_true", default=False,
                        help="""Visualize a single combat encounter.""")
    parser.add_argument("--num_encounters", type=int, default=1000,
                        help="""The number of encounters to run.""")
    parser.add_argument("--speed", type=float, default=0.3,
                        help="""How many second to wait between refreshing the
                                visualization.""")
    return parser.parse_args()


def main(visual, num_encounters, speed):
    # Create the characters
    jake_file = "combat_simulator/character_sheets/jake.json"
    mort_file = "combat_simulator/character_sheets/mortimer.json"
    commoner_file = "combat_simulator/character_sheets/commoner.json"
    orc_file = "combat_simulator/character_sheets/orc.json"
    zombie_file = "combat_simulator/character_sheets/zombie.json"
    jake_data = json.load(open(jake_file, 'r'))
    mortimer_data = json.load(open(mort_file, 'r'))
    commoner_data = json.load(open(commoner_file, 'r'))
    orc_data = json.load(open(orc_file, 'r'))
    zombie_data = json.load(open(zombie_file, 'r'))

    jakes = [Character(**jake_data) for _ in range(1)]
    mortimers = [Character(**mortimer_data) for _ in range(1)]
    commoners = [Character(**commoner_data) for _ in range(8)]
    orcs = [Character(**orc_data) for _ in range(5)]
    zombies = [Character(**zombie_data) for _ in range(7)]

    # Create the teams
    team_jake = Team(members=jakes, name="Team of Jakes")
    team_mortimer = Team(members=mortimers, name="Team Mortimer")
    team_commoner = Team(members=commoners, name="Average Joes")
    team_orc = Team(members=orcs, name="ORC BRIGADE")
    team_zombie = Team(members=zombies, name="Zombie Patrol")

    engine = Engine(team_jake, team_commoner)
    engine.gameloop(visual=visual, num_encounters=num_encounters, speed=speed)


if __name__ == "__main__":
    args = parse_args()
    main(args.visual, args.num_encounters, args.speed)
