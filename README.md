# Dungeons and Dragons Combat Simulator

### Usage
```python
>>> from combat_simulator import Character, Team, Encounter
>>> import json
>>> jake_data = json.load(open("combat_simulator/character_sheets/jake.json", 'r'))
>>> jake1 = Character(**jake_data)
>>> jake2 = Character(**jake_data)
>>> team1 = Team(members=[jake1], name="Team Jake 1")
>>> team2 = Team(members=[jake2], name="Team Jake 2")
>>> enc = Encounter(teams=[team1, team2])
>>> enc.run(random_seed=0)
{'_members': [Jake_01], 'name': 'Team Jake 1'}
>>> enc.stats.summary(jake1)
Dealt: 3.36, Taken: 0.86, Hits: 12/25 (48.0%)
```
