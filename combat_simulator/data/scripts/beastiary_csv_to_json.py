import argparse
import json
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", type=str, required=True,
                        help="Path to beastiary.csv")
    parser.add_argument("--outfile", type=str, required=True,
                        help="Where to write the JSON lines file.")
    return parser.parse_args()


def atk2json(atk):
    dmg_roll_n = len(atk[3:])
    dmg_roll_die = atk[3]
    dmg_roll_str = f"{dmg_roll_n}d{dmg_roll_die}"
    return {"name": atk[0],
            "type": "melee",  # TODO: get this data
            "range": "5/5",  # TODO: get this data
            "atk_bonus": atk[1],
            "dmg_roll": dmg_roll_str,
            "dmg_bonus": atk[2],
            "dmg_type": "bludgeoning",  # TODO: get this data
            "properties": []}  # TODO: get this data


def row2json(row):
    atks = []
    num_atks = 1

    try:
        raw_atks = json.loads(row["attack_parameters"])
    except json.JSONDecodeError:
        print(row["attack_parameters"])
        input()
        return {}
    except TypeError:
        print(row["attack_parameters"])
        input()
        return {}

    for atk in raw_atks:
        atk_json = atk2json(atk)
        if atk_json not in atks:
            atks.append(atk_json)
        else:
            num_atks += 1

    return {"name": row["name"],
            "icon": row["name"][0].upper(),
            "strength": int(row["Str"]),
            "dexterity": int(row["Dex"]),
            "constitution": int(row["Con"]),
            "intelligence": int(row["Int"]),
            "wisdom": int(row["Wis"]),
            "charisma": int(row["Cha"]),
            "hp": int(row["hp"]),
            "speed": 30,  # TODO: get this data.
            "cr": int(row["CR"]),
            "size": row["size"].lower(),
            "num_attacks": num_atks,
            "attacks": atks}


def main(infile, outfile):
    beastiary = pd.read_csv(infile)

    outjson = {}
    for (i, row) in beastiary.iterrows():
        print(f"{i}/{beastiary.shape[0]}\r", end='')
        entry = row2json(row)
        if entry != {}:
            outjson[entry["name"]] = entry

    with open(outfile, 'w') as outF:
        json.dump(outjson, outF)


if __name__ == "__main__":
    args = parse_args()
    main(args.infile, args.outfile)
