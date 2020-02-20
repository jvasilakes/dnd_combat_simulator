[![Build Status](https://api.travis-ci.org/jvasilakes/dnd_combat_simulator.svg?branch=master)](https://travis-ci.org/jvasilakes/dnd_combat_simulator)
[![Coverage Status](https://coveralls.io/repos/github/jvasilakes/dnd_combat_simulator/badge.svg?branch=master)](https://coveralls.io/github/jvasilakes/dnd_combat_simulator?branch=master)

# Dungeons and Dragons Combat Simulator

### Usage

```
python run_scenario.py --scenario_file scenarios/zombie_apocalypse.json --num_encounters 50

100%|███████████████████████████████████████████████████████████████████████████████████| 50/50 [00:14<00:00,  3.39it/s]
Jake (01): DPR (6.97), hit ratio (0.79)
Jake (02): DPR (6.89), hit ratio (0.81)
Zombie (03): DPR (4.11), hit ratio (0.50)
Zombie (04): DPR (4.12), hit ratio (0.50)
Zombie (05): DPR (4.01), hit ratio (0.44)
Zombie (06): DPR (3.84), hit ratio (0.45)
Zombie (07): DPR (4.08), hit ratio (0.50)
Zombie (08): DPR (4.20), hit ratio (0.45)
Wins
Team Jake: 15 / 50 (0.30)
Zombie Patrol: 35 / 50 (0.70)
```


```
python --scenario_file scenarios/zombie_apocalypse.json --visual
```

<p align="center">
  <img width="600" src="https://github.com/jvasilakes/dnd_combat_simulator/blob/master/graphics/battle.svg">
</p>

```
python map_maker.py
```

<p align="center">
  <img width="600" src="https://github.com/jvasilakes/dnd_combat_simulator/blob/master/graphics/map_example.svg">
</p>

Recorded with asciinema and svg-term-cli

```
asciinema rec
~/opt/miniconda3/envs/5e/bin/python3.7 run_scenario.py --scenario_file scenarios/example.json --visual
cat .cat | svg-term --out graphics/battle.svg
```
