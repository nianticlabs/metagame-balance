from abc import ABC, abstractmethod
from typing import List, Tuple

import random

from Engine.PkmBaseStructures import PkmTeam, Pkm, PkmType, PkmMove
from Engine.PkmConstants import N_MAX_PARTY, MAX_HIT_POINTS, MIN_HIT_POINTS, N_MOVES, MOVE_POWER_MAX, MOVE_POWER_MIN
from Player.Abstract.Agent import SelectorAgent

LIST_OF_TYPES: List[PkmType] = list(PkmType)
DELTA_HIT_POINTS = MAX_HIT_POINTS - MIN_HIT_POINTS
DELTA_MOVE_POWER = MOVE_POWER_MAX - MOVE_POWER_MIN


class PkmTeamGenerator(ABC):

    @abstractmethod
    def get_team(self, t_id: int = 0) -> PkmTeam:
        pass

    @abstractmethod
    def fixed(self) -> bool:
        pass


# Example generators
class RandomGenerator(PkmTeamGenerator):

    def __init__(self, party_size: int = N_MAX_PARTY):
        self.party_size = party_size

    def get_team(self, t_id: int = 0) -> PkmTeam:
        team: List[Pkm] = []
        for i in range(self.party_size + 1):
            p_type: PkmType = random.choice(LIST_OF_TYPES)
            max_hp: float = round(random.random() * DELTA_HIT_POINTS + MIN_HIT_POINTS)
            moves: List[PkmMove] = []
            for _ in range(N_MOVES):
                m_type: PkmType = random.choice(LIST_OF_TYPES)
                m_power: float = round(random.random() * DELTA_MOVE_POWER + MOVE_POWER_MIN)
                moves.append(PkmMove(m_power, .1, m_type))
            moves[0].type = p_type
            random.shuffle(moves)
            team.append(Pkm(p_type, max_hp, move0=moves[0], move1=moves[1], move2=moves[2], move3=moves[3]))
        return PkmTeam(team)

    def fixed(self) -> bool:
        return False


class FixedGenerator(PkmTeamGenerator):

    def __init__(self, gen: PkmTeamGenerator):
        self.gen: PkmTeamGenerator = gen
        self.team = [gen.get_team(0), gen.get_team(1)]

    def get_team(self, t_id: int = 0) -> PkmTeam:
        return self.team[t_id]

    def fixed(self) -> bool:
        return True


class TeamSelector(PkmTeamGenerator):

    def __init__(self, team0: PkmTeam, team1: PkmTeam, selector_0: SelectorAgent, selector_1: SelectorAgent):
        self.teams = team0, team1
        team_view_0 = self.teams[0].create_team_view()
        team_view_1 = self.teams[1].create_team_view()
        self.team_views = (team_view_1[0], team_view_0[1]), (team_view_0[0], team_view_1[1])
        self.selector: Tuple[SelectorAgent, SelectorAgent] = (selector_0, selector_1)

    def get_team(self, t_id: int = 0) -> PkmTeam:
        pkm_ids = self.selector[t_id].get_action(self.team_views[t_id])
        return self.teams[t_id].select_team(pkm_ids)

    def fixed(self) -> bool:
        return False


class FixedTeamSelector(PkmTeamGenerator):

    def __init__(self, team0: PkmTeam, team1: PkmTeam):
        self.teams = team0, team1
        team_view_0 = self.teams[0].create_team_view()
        team_view_1 = self.teams[1].create_team_view()
        self.team_views = (team_view_1[0], team_view_0[1]), (team_view_0[0], team_view_1[1])
        self.selected_teams = PkmTeam(), PkmTeam()

    def set_teams(self, pkm_ids_0: List[int], pkm_ids_1: List[int]):
        self.selected_teams = self.teams[0].select_team(pkm_ids_0), self.teams[1].select_team(pkm_ids_1)

    def get_team(self, t_id: int = 0) -> PkmTeam:
        return self.selected_teams[t_id]

    def fixed(self) -> bool:
        return True
