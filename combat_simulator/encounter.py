import numpy as np
from collections import defaultdict

from .character import Character
from .grid import Grid
from .player import Player


class Team(object):
    """
    A group of players on the same side.

    :param list members: A list of Character instances.
    :param str name: The name of this team.
    """

    def __init__(self, members=[], name=""):
        self._check_params(members)
        self._members = members
        if not name:
            raise ValueError("name cannot be empty.")
        self.name = str(name)

    def _check_params(self, members):
        assert(all([isinstance(m, Character) for m in members]))

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self.__dict__)

    def __len__(self):
        return len(self._members)

    def members(self, alive_only=False):
        """
        Returns the team members.

        :param bool alive_only: Whether to only return alive members.
        :returns: The members of this team.
        :rtype: list(Character)
        """
        if alive_only is True:
            return [m for m in self._members if m.is_alive]
        else:
            return self._members


class Encounter(object):
    """
    A combat encounter between two or more teams of characters.

    :param list teams: A list of Team instances.
    """

    def __init__(self, teams, grid, player):
        self._check_params(teams, grid, player)
        self.teams = teams
        self.combatants = [m for t in self.teams for m in t.members()]
        self._team_lookup = self._get_team_lookup()
        self.grid = grid
        self.player = player
        self.stats = EncounterStats()

    def _check_params(self, teams, grid, player):
        assert(all([isinstance(t, Team) for t in teams]))
        assert(len(teams) >= 2)
        assert(isinstance(grid, Grid))
        assert(isinstance(player, Player))

    def _get_team_lookup(self):
        tm = {}
        for team in self.teams:
            for character in team.members():
                tm[character.id] = team
        return tm

    def __str__(self):
        return ' vs. '.join([t.name for t in self.teams])

    def team(self, player):
        """
        Returns the team of this character.

        :param Character character: The character whose team to get.
        :returns: The team of this character.
        :rtype: Team
        """
        return self._team_lookup[player.character.id]

    def run_combat(self, player, random_seed=None, verbose=0):
        """
        Run simulated combat among all the teams.

        :returns: The winning team.
        :rtype: Team
        """
        # Initialize the battle parameters.
        np.random.seed(random_seed)
        turn_order = self._roll_initiative(player)
        enemy_table = {}
        for team in self.teams:
            enemies = [c for c in self.combatants if self.team(c) != team]
            enemy_table[team.name] = enemies
        while True:
            for player in turn_order:
                char = player.character
                if not char.is_alive:
                    continue
                # Choose an enemy
                team = self.team(player)
                enemy = np.random.choice(enemy_table[team.name])
                # Fight the enemy
                (is_hit, is_crit, dmg) = self._fight(player, enemy)
                self.stats.add_damage_dealt(char, dmg)
                self.stats.add_damage_taken(enemy.character, dmg)
                self.stats.add_hit(char, is_hit)
                if verbose > 0:
                    print(f"{char} --> {enemy.character}: {is_hit}, {is_crit}, {dmg}")  # noqa
                    print(f"{char} ({char.HP})")
                    print(f"{enemy.character} ({enemy.character.HP})")
                    print("---")
                # Check if the battle has been won.
                if not enemy.character.is_alive:
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
        inits = [(character, self.player.roll_initiative(character))
                 for character in self.combatants]
        order = sorted(inits, key=lambda x: x[1], reverse=True)
        return order

    def _fight(self, attacker, victim):

        def _hit(roll, bonus, ac):
            if roll == 20:
                return True
            elif roll + bonus >= ac:
                return True
            else:
                return False

        is_crit = False
        dmg = 0
        atk = attacker.choose_attack(victim)
        roll, bonus = attacker.attack_roll(atk)
        is_hit = _hit(roll, bonus, victim.character.ac)
        if is_hit is True:
            if roll == 20:
                is_crit = True
            dmg = sum(attacker.damage_roll(crit=is_crit))
            victim.character.HP -= dmg
        return (is_hit, is_crit, dmg)

    def summary(self):
        for plyr in self.combatants:
            print(f"{plyr.character}: ", end='')
            self.stats.summary(plyr.character)


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
        print(f"Dealt: {dmg_d:.2f}, Taken: {dmg_t:.2f}, Hit Ratio: {n_hits}/{n_atks} ({hit_ratio:.1f}%)")  # noqa

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
