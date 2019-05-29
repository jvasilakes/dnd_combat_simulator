import json
from combat_simulator import Character, Player, Team, Encounter


# Create the characters
jake_data = json.load(open("combat_simulator/character_sheets/jake.json", 'r'))
mort_data = json.load(open("combat_simulator/character_sheets/mortimer.json", 'r'))

jake1 = Character(**jake_data)
jake2 = Character(**jake_data)
jake3 = Character(**jake_data)
mortimer = Character(**mort_data)

# Assign each a player
p1 = Player(jake1)
p2 = Player(jake2)
p3 = Player(jake3)
p4 = Player(mortimer)

# Create the teams
team_jake = Team(members=[p1, p2, p3], name="JakeTeam")
team_mort = Team(members=[p4], name="TeamMort")

# Run a series of encounters to see who wins.
enc = Encounter(teams=[team_jake, team_mort])
print(enc)
winners = []
for i in range(10):
    winner = enc.run(random_seed=i)
    winners.append(winner)
print(f"WINNERS: {[w.name for w in winners]}")
