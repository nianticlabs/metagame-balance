from abc import ABC, abstractmethod
from typing import List, Tuple
from framework.behaviour import SelectorPolicy
from framework.DataConstants import MAX_HIT_POINTS, MOVE_POWER_MAX, MOVE_POWER_MIN, MIN_HIT_POINTS, DEFAULT_TEAM_SIZE, \
    DEFAULT_PKM_N_MOVES
from framework.DataObjects import PkmTeam, Pkm, PkmMove, get_team_view
from framework.DataTypes import PkmType
import random

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

    def __init__(self, party_size: int = DEFAULT_TEAM_SIZE - 1):
        self.party_size = party_size

    def get_team(self, t_id: int = 0) -> PkmTeam:
        team: List[Pkm] = []
        for i in range(self.party_size + 1):
            p_type: PkmType = random.choice(LIST_OF_TYPES)
            max_hp: float = round(random.random() * DELTA_HIT_POINTS + MIN_HIT_POINTS)
            moves: List[PkmMove] = []
            for _ in range(DEFAULT_PKM_N_MOVES):
                m_type: PkmType = random.choice(LIST_OF_TYPES)
                m_power: float = round(random.random() * DELTA_MOVE_POWER + MOVE_POWER_MIN)
                moves.append(PkmMove(m_power, 1., m_type))
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

    def __init__(self, team0: PkmTeam, team1: PkmTeam, selector_0: SelectorPolicy, selector_1: SelectorPolicy):
        self.teams = team0, team1
        self.player0_team_views = get_team_view(self.teams[0]), get_team_view(self.teams[1], partial=True)
        self.player1_team_views = get_team_view(self.teams[1]), get_team_view(self.teams[0], partial=True)
        self.team_views = self.player0_team_views, self.player1_team_views
        self.selector: Tuple[SelectorPolicy, SelectorPolicy] = (selector_0, selector_1)

    def get_team(self, t_id: int = 0) -> PkmTeam:
        pkm_ids = self.selector[t_id].get_action(self.team_views[t_id])
        return self.teams[t_id].select_team(pkm_ids)

    def fixed(self) -> bool:
        return False


class FixedTeamSelector(PkmTeamGenerator):

    def __init__(self, team0: PkmTeam, team1: PkmTeam):
        self.teams = team0, team1
        self.player0_team_views = get_team_view(self.teams[0]), get_team_view(self.teams[1], partial=True)
        self.player1_team_views = get_team_view(self.teams[1]), get_team_view(self.teams[0], partial=True)
        self.team_views = self.player0_team_views, self.player1_team_views
        self.selected_teams = PkmTeam(), PkmTeam()

    def set_teams(self, pkm_ids_0: List[int], pkm_ids_1: List[int]):
        self.selected_teams = self.teams[0].select_team(pkm_ids_0), self.teams[1].select_team(pkm_ids_1)

    def get_team(self, t_id: int = 0) -> PkmTeam:
        return self.selected_teams[t_id]

    def fixed(self) -> bool:
        return True
