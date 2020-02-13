import numpy as np
import pandas as pd

from .token import Character
from .grid import Grid
from .player import Player
from .astar import distance


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

    def rm_member(self, character):
        """
        Remove a team member.

        :param Character character: The team member to remove.
        """
        self._members = [m for m in self._members if m != character]

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

    _id_counter = 0

    def __init__(self, teams, grid, player):
        self._check_params(teams, grid, player)
        self._log = []
        self.id = self._get_id()
        self.teams = teams
        self.grid = grid
        self.player = player
        self.combatants = [m for t in self.teams for m in t.members()]
        self.winner = None
        self._team_lookup = self._get_team_lookup()
        self._enemy_lookup = self._get_enemy_lookup()

    def _check_params(self, teams, grid, player):
        assert(all([isinstance(t, Team) for t in teams]))
        assert(len(teams) >= 2)
        assert(isinstance(grid, Grid))
        assert(isinstance(player, Player))

    @classmethod
    def _get_id(cls):
        cls._id_counter += 1
        return f"ENC{cls._id_counter:015d}"

    def __str__(self):
        return ' vs. '.join([t.name for t in self.teams])

    def _get_team_lookup(self):
        tm = {}
        for team in self.teams:
            for character in team.members():
                tm[character.id] = team
        return tm

    def _get_enemy_lookup(self):
        enemy_lookup = {}
        for team in self.teams:
            enemies = [c for c in self.combatants if self.get_team(c) != team]
            enemy_lookup[team.name] = enemies
        return enemy_lookup

    def _set_combatants_goals(self):
        for c in self.combatants:
            if not c.is_alive:
                continue
            team = self._team_lookup[c.id]
            enemies = self._enemy_lookup[team.name]
            # Choose an enemy to attack.
            distances = [distance(self.grid[c], self.grid[e])
                         for e in enemies]
            c.goal = enemies[np.argmin(distances)]

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
        atk = self.player.choose_attack(attacker, target=victim)
        roll, bonus = self.player.roll_attack(attacker, atk)
        is_hit = _hit(roll, bonus, victim.ac)
        if is_hit is True:
            if roll == 20:
                is_crit = True
            dmg = sum(self.player.roll_damage(attacker, atk, crit=is_crit))
            victim.HP -= dmg
        return (is_hit, is_crit, dmg)

    def get_team(self, character):
        """
        Returns the team of this character.

        :param Character character: The character whose team to get.
        :returns: The team of this character.
        :rtype: Team
        """
        return self._team_lookup[character.id]

    def init_combat(self):
        # Who will attack who.
        self._set_combatants_goals()
        self.turn_order = self._roll_initiative()

    def run_combat(self, random_seed=None, verbose=0):
        """
        Run simulated combat among all the teams.

        :returns: The winning team.
        :rtype: Team
        """
        rounds = 0
        won = False
        while won is False:
            for (character, _) in self.turn_order:
                if not character.is_alive:
                    continue
                new_pos = self.player.move_character(character, self.grid)  # noqa
                enemy = character.goal
                if self.grid.is_adjacent(character, enemy):
                    is_hit, is_crit, dmg = self._fight(character, enemy)
                    atk = {"encounter_id": self.id,
                           "attacker_id": character.id,
                           "attacker_name": character.name,
                           "victim_id": enemy.id,
                           "victim_name": enemy.name,
                           "hit": is_hit,
                           "dmg": dmg}
                    self._log.append(atk)
                team = self._team_lookup[character.id]
                if not enemy.is_alive:
                    self._enemy_lookup[team.name].remove(enemy)
                    self.grid.rm_token(enemy)
                    if self._enemy_lookup[team.name] == []:
                        self.winner = team
                        won = True
                        break
                    self._set_combatants_goals()
            rounds += 1
            yield rounds

    @property
    def log(self):
        return pd.DataFrame(self._log)

    def summary(self):
        for ((name, cid), group) in self.log.groupby(["attacker_name", "attacker_id"]):  # noqa
            dpr = group[group["hit"] == True]["dmg"].mean()  # noqa
            hit_ratio = group["hit"].sum() / group.shape[0]
            print(f"{name} ({cid}): DPR ({dpr:.2f}), hit ratio ({hit_ratio:.2f})")  # noqa
