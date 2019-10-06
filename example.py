import json

from combat_simulator import Character, Team, Engine


# Create the characters
jake_file = "combat_simulator/character_sheets/jake.json"
mort_file = "combat_simulator/character_sheets/mortimer.json"
jake_data = json.load(open(jake_file, 'r'))
mort_data = json.load(open(mort_file, 'r'))

jakes = [Character(**jake_data) for _ in range(3)]
mortimer = Character(**mort_data)

# Create the teams
team_jake = Team(members=jakes, name="JakeTeam")
team_mort = Team(members=[mortimer], name="TeamMort")

engine = Engine(team_jake, team_mort)
engine.gameloop()

## Run a series of encounters to see who wins.
#enc = Encounter(teams=[team_jake, team_mort], grid=grid)
#print(enc)
#winners = []
#for i in range(10):
#    winner = enc.run_combat(random_seed=i, verbose=0)
#    winners.append(winner)
#    print(f"Round {i+1} winner: {winner}")
#    enc.summary()
#    print("---")
#    input()
