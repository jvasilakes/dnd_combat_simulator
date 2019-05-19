import numpy as np
from collections import defaultdict

from .base import roll_die


class Team(object):
    """
    A group of characters on the same side.

    :param list members: A list of Character instances.
    :param str name: The name of this team.
    """

    def __init__(self, members=[], name=""):
        self._members = members
        if not name:
            raise ValueError("name cannot be empty.")
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self.__dict__)

    def members(self, alive_only=False):
        """
        Returns the team members.

        :param bool alive_only: Whether to only return alive members.
        :returns: The members of this team.
        :rtype: list(Character)
        """
        if alive_only is True:
            return [c for c in self._members if c.is_alive]
        else:
            return self._members


class EncounterStats(object):
    """
    Holds statistics for each combatant in an encounter.
    """

    def __init__(self):
        self.damage_dealt = defaultdict(list)
        self.damage_taken = defaultdict(list)
        self.hits = defaultdict(list)

    def add_damage_dealt(self, character, value):
        """
        Update the damage dealt by this character.

        :param Character character: The character whose data to update.
        :param int value: The amount of damage dealt.
        """
        self.damage_dealt[character.id].append(value)

    def add_damage_taken(self, character, value):
        """
        Update the damage taken by this character.

        :param Character character: The character whose data to update.
        :param int value: The amount of damage taken.
        """
        self.damage_taken[character.id].append(value)

    def add_hit(self, character, value):
        """
        Add a hit value for this character.

        :param Character character: The character whose data to update.
        :param bool value: Whether the character hit or not.
        """
        self.hits[character.id].append(value)

    def summary(self, character):
        """
        Summarize the stats of this character.

        :param Character character: The character whose data to summarize.
        """
        dmg_d = self.average_damage_dealt(character)
        dmg_t = self.average_damage_taken(character)
        n_hits = self.n_hits(character)
        n_atks = self.n_attacks(character)
        hit_ratio = 100 * (n_hits / n_atks)
        print(f"Dealt: {dmg_d:.2f}, Taken: {dmg_t:.2f}, Hits: {n_hits}/{n_atks} ({hit_ratio:.1f}%)")  # noqa

    def average_damage_dealt(self, character):
        """
        Compute the average damage dealt by this character.

        :param Character character: The character whose data to average.
        """
        return np.mean(self.damage_dealt[character.id])

    def average_damage_taken(self, character):
        """
        Compute the average damage taken by this character.

        :param Character character: The character whose data to average.
        """
        return np.mean(self.damage_taken[character.id])

    def n_attacks(self, character):
        """
        The number of attacks this character attempted.

        :param Character character: The character whose data to return.
        """
        return len(self.hits[character.id])

    def n_hits(self, character):
        """
        The number of hits this character achieved.

        :param Character character: The character whose data to return.
        """
        return np.sum(self.hits[character.id])


class Encounter(object):
    """
    A combat encounter between two or more teams of characters.

    :param list teams: A list of Team instances.
    """

    def __init__(self, teams=[]):
        if len(teams) < 2:
            raise ValueError("An encounter must have >1 teams.")
        self.teams = teams
        self.combatants = [c for t in self.teams for c in t.members()]
        self._team_map = self._get_team_map()
        self.stats = EncounterStats()

    def _get_team_map(self):
        tm = {}
        for team in self.teams:
            for char in team.members():
                tm[char.id] = team
        return tm

    def __str__(self):
        return ' vs. '.join([t.name for t in self.teams])

    def team(self, character):
        """
        Returns the team of this character.

        :param Character character: The character whose team to get.
        :returns: The team of this character.
        :rtype: Team
        """
        return self._team_map[character.id]

    def run(self, random_seed=None, verbose=0):
        """
        Run simulated combat among all the teams.

        :returns: The winning team.
        :rtype: Team
        """
        # Initialize the battle parameters.
        np.random.seed(random_seed)
        turn_order = self._roll_initiative()
        enemy_table = {}
        for team in self.teams:
            enemies = [c for c in self.combatants if self.team(c) != team]
            enemy_table[team.name] = enemies
        while True:
            for character in turn_order:
                if not character.is_alive:
                    continue
                # Choose an enemy
                team = self.team(character)
                enemy = np.random.choice(enemy_table[team.name])
                # Fight the enemy
                (h, c, dmg) = self._fight(character, enemy)
                self.stats.add_damage_dealt(character, dmg)
                self.stats.add_damage_taken(enemy, dmg)
                self.stats.add_hit(character, h)
                if verbose > 0:
                    print(f"{character} --> {enemy}: {h}, {c}, {dmg}")
                    print(f"{character} ({character.HP})")
                    print(f"{enemy} ({enemy.HP})")
                    print("---")
                # Check if the battle has been won.
                if not enemy.is_alive:
                    enemy_table[team.name].remove(enemy)
                    if verbose > 0:
                        print("===")
                        print(enemy_table[team.name])
                        print("===")
                    if enemy_table[team.name] == []:
                        winner = team
                        return winner

    def _roll_initiative(self):
        """
        Rolls initiative for each character in each team and
        returns them in the order in which they take their turns.
        """
        inits = []
        for char in self.combatants:
            roll = roll_die(d=20, n=1)
            init = roll + char.ability_modifier["dex"]
            inits.append((char, init))
        order = sorted(inits, key=lambda x: x[1], reverse=True)
        return [char for (char, init) in order]

    def _fight(self, attacker, victim):

        def _hit(roll, bonus, ac):
            if roll == 20:
                return True
            elif roll + bonus >= ac:
                return True
            else:
                return False

        crit = False
        dmg = 0
        atk = attacker.choose_attack(victim)
        roll, bonus = attacker.attack(atk)
        hit = _hit(roll, bonus, victim.ac)
        if hit is True:
            if roll == 20:
                crit = True
            dmg = sum(attacker.damage(crit=crit))
            victim.HP -= dmg
        return (hit, crit, dmg)
