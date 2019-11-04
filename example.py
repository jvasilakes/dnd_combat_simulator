import json

from combat_simulator import Character, Team, Engine


# Create the characters
jake_file = "combat_simulator/character_sheets/jake.json"
mort_file = "combat_simulator/character_sheets/mortimer.json"
commoner_file = "combat_simulator/character_sheets/commoner.json"
orc_file = "combat_simulator/character_sheets/orc.json"
jake_data = json.load(open(jake_file, 'r'))
mort_data = json.load(open(mort_file, 'r'))
comm_data = json.load(open(commoner_file, 'r'))
orc_data = json.load(open(orc_file, 'r'))

jakes = [Character(**jake_data) for _ in range(1)]
mortimers = [Character(**mort_data) for _ in range(1)]
commoners = [Character(**comm_data) for _ in range(8)]
orcs = [Character(**orc_data) for _ in range(4)]

# Create the teams
team_jake = Team(members=jakes, name="Jake")
team_mort = Team(members=mortimers, name="Team Mortimer")
team_comm = Team(members=commoners, name="Average Joes")
team_orc = Team(members=orcs, name="ORC BRIGADE")

engine = Engine(team_jake, team_comm)
engine.gameloop()
