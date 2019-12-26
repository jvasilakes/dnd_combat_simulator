import argparse
import json
import re


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", type=str, required=True,
                        help="JSON file containing SRD data.")
    parser.add_argument("--outfile", type=str, required=True,
                        help="Where to save the formatted JSON.")
    return parser.parse_args()


def main(infile, outfile):
    indata = json.load(open(infile))

    out = []
    for (i, monster) in enumerate(indata):
        if "name" not in monster.keys():
            continue
        try:
            formatted = {"name": monster["name"],
                         "icon": monster["name"][0].upper(),
                         "strength": monster["strength"],
                         "dexterity": monster["dexterity"],
                         "constitution": monster["constitution"],
                         "intelligence": monster["intelligence"],
                         "wisdom": monster["wisdom"],
                         "charisma": monster["charisma"],
                         "hp": monster["hit_points"],
                         "ac": monster["armor_class"],
                         "speed": parse_speed(monster),
                         "num_attacks": parse_multiattack(monster),
                         "attacks": get_attacks(monster)}
        except Exception as e:
            print(monster["name"])
            raise(e)
        out.append(formatted)

    with open(outfile, 'w') as outF:
        for line in out:
            json.dump(line, outF)
            outF.write('\n')


def parse_speed(monster_data):
    speeds = re.findall(r'\s?([0-9]+)\s?ft\.', monster_data["speed"])
    return int(speeds[0])


# TODO: Implement this.
def parse_multiattack(monster_data):
    return 1


# TODO implement all attacks
def get_attacks(monster_data):
    if "actions" not in monster_data.keys():
        return []
    attacks = []
    for action in monster_data["actions"]:
        if "damage_dice" not in action.keys():
            continue
        if "damage_bonus" in action.keys():
            damage_bonus = action["damage_bonus"]
        else:
            damage_bonus = 0
        if '+' in action["damage_dice"]:
            dmg_rolls = [roll.strip() for roll
                         in action["damage_dice"].split('+')]
        else:
            dmg_rolls = [action["damage_dice"]]
        # TODO: Parse type, range, and damage
        attack = {"name": action["name"],
                  "type": "melee",
                  "range": "5/5",
                  "atk_bonus": action["attack_bonus"],
                  "dmg_rolls": dmg_rolls,
                  "dmg_bonus": damage_bonus,
                  "dmg_type": "bludgeoning",
                  "properties": []}
        attacks.append(attack)
    return attacks


if __name__ == "__main__":
    args = parse_args()
    main(args.infile, args.outfile)
