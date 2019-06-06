import json
from combat_simulator import Character, Player, Team, Encounter, Grid


# Create the characters
jake_file = "combat_simulator/character_sheets/jake.json"
mort_file = "combat_simulator/character_sheets/mortimer.json"
jake_data = json.load(open(jake_file, 'r'))
mort_data = json.load(open(mort_file, 'r'))

jakes = [Character(**jake_data) for _ in range(3)]
mortimer = Character(**mort_data)


# Create the teams
team_jake = Team(members=[Player(jake) for jake in jakes],
                 name="JakeTeam")
team_mort = Team(members=[Player(mortimer)], name="TeamMort")

# Create a map and add a character to it.
grid = Grid()
grid.add(mortimer, pos=(0, 0))
grid.add(jakes[0], pos=(5, 5))
print(grid)
# Move the character to a new position.
team_mort.members()[0].move_character(grid)
team_jake.members()[0].move_character(grid)
print(grid)

# Run a series of encounters to see who wins.
enc = Encounter(teams=[team_jake, team_mort], grid=grid)
print(enc)
winners = []
for i in range(10):
    winner = enc.run_combat(random_seed=i, verbose=0)
    winners.append(winner)
    print(f"Round {i+1} winner: {winner}")
    enc.summary()
    print("---")
