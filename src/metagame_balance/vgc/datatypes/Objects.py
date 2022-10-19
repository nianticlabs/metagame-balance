import random
from abc import ABC, abstractmethod
from copy import deepcopy
from math import isclose
from typing import List, Tuple, Set, Union, Mapping, Text, Dict, Any, Type

import numpy as np

from metagame_balance.vgc.datatypes.Constants import MOVE_MED_PP, MAX_HIT_POINTS
from metagame_balance.vgc.datatypes.Types import PkmType, PkmStatus, N_STATS, N_ENTRY_HAZARD, PkmStat, WeatherCondition, \
    PkmEntryHazard


JSON = Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]

class PkmMove:

    def __init__(self, power: float = 30., acc: float = 1., max_pp: int = MOVE_MED_PP,
                 move_type: PkmType = PkmType.NORMAL, name: str = None, priority: bool = False,
                 prob=0.0, target=1, recover=0.0, status: PkmStatus = PkmStatus.NONE,
                 stat: PkmStat = PkmStat.ATTACK, stage: int = 0, fixed_damage: float = 0.0,
                 weather: WeatherCondition = WeatherCondition.CLEAR, hazard: PkmEntryHazard = PkmEntryHazard.NONE):
        """
        Pokemon move data structure.

        :param power: move power
        :param acc: move accuracy
        :param max_pp: move max power points
        :param move_type: move type
        :param name: move name
        :param priority: move priority
        :param prob: move effect probability (only moves with probability greater than zero perform effects)
        :param target: move effect target, zero for self and 1 for opponent
        :param recover: move recover quantity, how much hit points to recover
        :param status: status the move effect changes
        :param stage: stage the move effect adds/subtracts from the status
        :param fixed_damage: effect fixed_damage to apply, not affected by resistance or weakness (if greater than zero)
        :param weather: effect activates a weather condition
        :param hazard: effect deploys and hazard enter condition on the opponent field
        """
        self.power = power
        self.acc = acc
        self.max_pp = max_pp
        self.pp = max_pp
        self.type = move_type
        self.name = name
        self.priority = priority
        self.prob = prob
        self.target = target
        self.recover = recover
        self.status = status
        self.stat = stat
        self.stage = stage
        self.fixed_damage = fixed_damage
        self.weather = weather
        self.hazard = hazard
        self.public = False
        self.owner = None

    def to_dict(self) -> Mapping[Text, JSON]:
        return {
            "power": self.power,
            "acc": self.acc,
            "max_pp": self.max_pp,
            "type": self.type.name,
            "name": self.name or "unknown_move",
            "priority": self.priority,
            "prob": self.prob,
            "target": self.target,
            "recover": self.recover,
            "status": self.status.name,
            "stage": self.stage,
            "fixed_damage": self.fixed_damage,
            "weather": self.weather.name,
            "hazard": self.hazard.name
        }

    def __eq__(self, other):
        """
        Moves equal if name is equal (use name as id)
        """
        return self.name == other.name

    def __hash__(self):
        """
        Just hash based on name for meta balance!
        """
        if self.name == None:
            print(self)
        return hash(self.name)

    def __str__(self):
        if self.name:
            return self.name
        name = "PkmMove(Power=%f, Acc=%f, PP=%d, Type=%s" % (self.power, self.acc, self.pp, self.type.name)
        if self.priority > 0:
            name += ", Priority=%d" % self.priority
        if self.prob > 0.:
            if self.prob < 1.:
                name += ", Prob=%f" % self.prob
            name += ", Target=Self" if self.target == 0 else ", Target=Opp"
            if self.recover > 0.:
                name += ", Recover=%f" % self.recover
            if self.status != PkmStatus.NONE:
                name += ", Status=%s" % self.status.name
            if self.stage != 0.:
                name += ", Stat=%s, Stage=%d" % (self.stat.name, self.stage)
            if self.fixed_damage > 0.:
                name += ", Fixed=%f" % self.fixed_damage
            if self.weather != self.weather.CLEAR:
                name += ", Weather=%s" % self.weather.name
            if self.hazard != PkmEntryHazard.NONE:
                name += ", Hazard=%s" % self.hazard.name
        return name + ")"

    def set_owner(self, pkm):
        self.owner = pkm

    def reset(self):
        self.pp = self.max_pp

    def effect(self, v):
        self.reveal()
        if random.random() < self.prob:
            v.set_recover(self.recover)
            v.set_fixed_damage(self.fixed_damage)
            if self.stage != 0:
                v.set_stage(self.stat, self.stage, self.target)
            if self.status != self.status.NONE:
                v.set_status(self.status, self.target)
            if self.weather != self.weather.CLEAR:
                v.set_weather(self.weather)
            if self.hazard != PkmEntryHazard.NONE:
                v.set_entry_hazard(self.hazard, self.target)

    def reveal(self):
        self.public = True

    def hide(self):
        self.public = False

    @property
    def revealed(self) -> bool:
        if self.owner is not None:
            return self.owner.revealed and self.public
        return self.public


class MoveView(ABC):

    @property
    @abstractmethod
    def power(self) -> float:
        pass

    @property
    @abstractmethod
    def acc(self) -> float:
        pass

    @property
    @abstractmethod
    def pp(self) -> int:
        pass

    @property
    @abstractmethod
    def max_pp(self) -> int:
        pass

    @property
    @abstractmethod
    def type(self) -> PkmType:
        pass

    @property
    @abstractmethod
    def priority(self) -> int:
        pass

    @property
    @abstractmethod
    def prob(self) -> float:
        pass

    @property
    @abstractmethod
    def target(self) -> int:
        pass

    @property
    @abstractmethod
    def recover(self) -> float:
        pass

    @property
    @abstractmethod
    def status(self) -> PkmStatus:
        pass

    @property
    @abstractmethod
    def stat(self) -> PkmStat:
        pass

    @property
    @abstractmethod
    def stage(self) -> int:
        pass

    @property
    @abstractmethod
    def fixed_damage(self) -> float:
        pass

    @property
    @abstractmethod
    def weather(self) -> WeatherCondition:
        pass

    @property
    @abstractmethod
    def hazard(self) -> PkmEntryHazard:
        pass


def get_move_view(move: PkmMove) -> MoveView:
    class MoveViewImpl(MoveView):

        @property
        def power(self) -> float:
            return move.power

        @property
        def acc(self) -> float:
            return move.acc

        @property
        def pp(self) -> int:
            return move.pp

        @property
        def max_pp(self) -> int:
            return move.max_pp

        @property
        def type(self) -> PkmType:
            return move.type

        @property
        def priority(self) -> int:
            return move.priority

        @property
        def prob(self) -> float:
            return move.prob

        @property
        def target(self) -> int:
            return move.target

        @property
        def recover(self) -> float:
            return move.recover

        @property
        def status(self) -> PkmStatus:
            return move.status

        @property
        def stat(self) -> PkmStat:
            return move.stat

        @property
        def stage(self) -> int:
            return move.stage

        @property
        def fixed_damage(self) -> float:
            return move.fixed_damage

        @property
        def weather(self) -> WeatherCondition:
            return move.weather

        @property
        def hazard(self) -> PkmEntryHazard:
            return move.hazard

        def __eq__(self, other):
            if self.power != other.power:
                return False
            if self.acc != other.acc:
                return False
            if self.max_pp != other.max_pp:
                return False
            if self.type != other.type:
                return False
            if self.priority != other.priority:
                return False
            if self.prob > 0.:
                if self.prob != other.prob:
                    return False
                if self.target != self.target:
                    return False
                if self.recover != self.recover:
                    return False
                if self.status != self.status:
                    return False
                if self.stat != self.stat:
                    return False
                if self.stage != self.stage:
                    return False
                if self.fixed_damage != self.fixed_damage:
                    return False
                if self.weather != self.weather:
                    return False
                if self.hazard != self.hazard:
                    return False
            return True

        def __hash__(self):
            if self.prob == 0.:
                return hash((self.power, self.acc, self.max_pp, self.type, self.priority))
            return hash(
                (self.power, self.acc, self.max_pp, self.type, self.priority, self.prob, self.target, self.recover,
                 self.status, self.stat, self.stage, self.fixed_damage, self.weather, self.hazard))

    return MoveViewImpl()


null_pkm_move = PkmMove()


def get_partial_move_view(move: PkmMove, move_hypothesis: Union[PkmMove, None] = None) -> MoveView:
    if move.revealed:
        return get_move_view(move)
    elif move_hypothesis is not None:
        return get_move_view(move_hypothesis)
    return get_move_view(null_pkm_move)


PkmMoveRoster = Set[PkmMove]


class MoveRosterView(ABC):

    @abstractmethod
    def get_move_view(self, idx: int) -> MoveView:
        pass

    @property
    @abstractmethod
    def n_moves(self) -> int:
        pass


def get_pkm_move_roster_view(move_roster: PkmMoveRoster) -> MoveRosterView:
    class MoveRosterViewImpl(MoveRosterView):

        def get_move_view(self, idx: int) -> MoveView:
            return get_move_view(list(move_roster)[idx])

        @property
        def n_moves(self) -> int:
            return len(move_roster)

        def __eq__(self, other):
            for i in range(len(move_roster)):
                m0, m1 = self.get_move_view(i), other.get_move_view(i)
                if m0 != m1:
                    return False
            return True

        def __hash__(self):
            return hash(move_roster)

    return MoveRosterViewImpl()


class Pkm:

    def __init__(self, p_type: PkmType = PkmType.NORMAL, max_hp: float = MAX_HIT_POINTS,
                 status: PkmStatus = PkmStatus.NONE, move0: PkmMove = PkmMove(), move1: PkmMove = PkmMove(),
                 move2: PkmMove = PkmMove(), move3: PkmMove = PkmMove(), pkm_id=-1):
        """
        In battle Pokemon base data struct.

        :param p_type: pokemon type
        :param max_hp: max hit points
        :param status: current status (PARALYZED, ASLEEP, etc.)
        :param move0: first move
        :param move1: second move
        :param move2: third move
        :param move3: fourth move
        """
        self.type: PkmType = p_type
        self.max_hp: float = max_hp
        self.hp: float = max_hp
        self.status: PkmStatus = status
        self.n_turns_asleep: int = 0
        self.moves: List[PkmMove] = [move0, move1, move2, move3]
        for move in self.moves:
            move.set_owner(self)
        self.public = False
        self.pkm_id = pkm_id

    def __eq__(self, other):
        return self.type == other.type and isclose(self.max_hp, other.max_hp) and set(self.moves) == set(other.moves)

    def __hash__(self):
        return hash((self.type, self.max_hp) + tuple(self.moves))

    def __str__(self):
        s = 'Pkm(Type=%s, HP=%d' % (self.type.name, self.hp)
        if self.status != PkmStatus.NONE:
            s += ', Status=%s' % self.status.name
            if self.status == PkmStatus.SLEEP:
                s += ', Turns Asleep=%d' % self.n_turns_asleep
        s += ', Moves={'
        for move in self.moves:
            s += str(move) + ', '
        return s + '})'

    def reset(self):
        """
        Reset Pkm stats.
        """
        self.hp = self.max_hp
        self.status = PkmStatus.NONE
        self.n_turns_asleep = 0
        for move in self.moves:
            move.reset()

    def fainted(self) -> bool:
        """
        Check if pkm is fainted (hp == 0).

        :return: True if pkm is fainted
        """
        return self.hp == 0

    def paralyzed(self) -> bool:
        """
        Check if pkm is paralyzed this turn and cannot move.

        :return: true if pkm is paralyzed and cannot move
        """
        return self.status == PkmStatus.PARALYZED and np.random.uniform(0, 1) <= 0.25

    def asleep(self) -> bool:
        """
        Check if pkm is asleep this turn and cannot move.

        :return: true if pkm is asleep and cannot move
        """
        return self.status == PkmStatus.SLEEP

    def frozen(self) -> bool:
        """
        Check if pkm is frozen this turn and cannot move.

        :return: true if pkm is frozen and cannot move
        """
        return self.status == PkmStatus.FROZEN

    def reveal(self):
        self.public = True

    def hide_pkm(self):
        self.public = False

    def hide(self):
        self.public = False
        for move in self.moves:
            move.hide()

    @property
    def revealed(self):
        return self.public


class PkmView(ABC):

    @abstractmethod
    def get_move_view(self, idx: int) -> MoveView:
        pass

    @property
    @abstractmethod
    def type(self) -> PkmType:
        pass

    @property
    @abstractmethod
    def hp(self) -> float:
        pass

    @property
    @abstractmethod
    def status(self) -> PkmStatus:
        pass

    @property
    @abstractmethod
    def n_turns_asleep(self) -> int:
        pass


def get_pkm_view(pkm: Pkm, pkm_hypothesis: Union[Pkm, None] = None, partial=False) -> PkmView:
    class PkmViewImpl(PkmView):

        def get_move_view(self, idx: int) -> MoveView:
            if partial:
                # get opponent pokemon move information with an hypothesis
                if pkm_hypothesis is not None and pkm.moves[idx] is not None:
                    return get_partial_move_view(pkm.moves[idx], pkm_hypothesis.moves[idx])
                # get opponent pokemon move information
                return get_partial_move_view(pkm.moves[idx])
            # get self pokemon move information
            return get_move_view(pkm.moves[idx])

        @property
        def type(self) -> PkmType:
            if pkm_hypothesis is not None:
                return pkm_hypothesis.type
            return pkm.type

        @property
        def hp(self) -> float:
            if pkm_hypothesis is not None:
                return pkm_hypothesis.hp
            return pkm.hp

        @property
        def status(self) -> PkmStatus:
            return pkm.status

        @property
        def n_turns_asleep(self) -> int:
            return pkm.n_turns_asleep

    return PkmViewImpl()


null_pkm = Pkm()


def get_partial_pkm_view(pkm: Pkm, pkm_hypothesis: Pkm = None) -> PkmView:
    if pkm.revealed:
        return get_pkm_view(pkm, pkm_hypothesis, partial=True)
    return get_pkm_view(null_pkm, pkm_hypothesis)


class PkmTemplate:

    def __init__(self, move_roster: PkmMoveRoster, pkm_type: PkmType, max_hp: float, pkm_id: int):
        """
        Pokemon specimen definition data structure.

        :param move_roster: set of available moves for Pokemon of this species
        :param pkm_type: pokemon type
        :param max_hp: pokemon max_hp
        """
        self.move_roster: PkmMoveRoster = move_roster
        self.type: PkmType = pkm_type
        self.max_hp = max_hp
        self.pkm_id = pkm_id

    def __eq__(self, other):
        return self.type == other.type and self.max_hp == other.max_hp and self.move_roster == other.move_roster

    def __hash__(self):
        return hash((self.type, self.max_hp) + tuple(self.move_roster))

    def __str__(self):
        s = 'PkmTemplate(Type=%s, Max_HP=%d, Moves={' % (PkmType(self.type).name, self.max_hp)
        for move in self.move_roster:
            s += str(move) + ', '
        return s + '})'

    def gen_pkm(self, moves: List[int] = None) -> Pkm:
        """
        Given the indexes of the moves generate a pokemon of this species.

        :param moves: index list of moves
        :return: the requested pokemon
        """
        move_list = list(self.move_roster)

        if moves is None:
            return Pkm(p_type=self.type, max_hp=self.max_hp,
                       move0=move_list[0],
                       move1=move_list[1],
                       move2=move_list[2],
                       move3=move_list[3],
                       pkm_id=self.pkm_id)

        return Pkm(p_type=self.type, max_hp=self.max_hp,
                   move0=move_list[moves[0]],
                   move1=move_list[moves[1]],
                   move2=move_list[moves[2]],
                   move3=move_list[moves[3]],
                   pkm_id=self.pkm_id)

    def is_speciman(self, pkm: Pkm) -> bool:
        """
        Check if input pokemon is a speciman of this species

        :param pkm: pokemon
        :return: if pokemon is speciman of this template
        """
        return pkm.type == self.type and pkm.max_hp == self.max_hp and set(pkm.moves).issubset(self.move_roster)

    def to_dict(self) -> Mapping[Text, JSON]:
        return {
            "type": self.type.name,
            "max_hp": self.max_hp,
            "moves": [m.to_dict() for m in self.move_roster],
            "pkm_id": self.pkm_id
        }


class PkmTemplateView(ABC):

    @abstractmethod
    def get_move_roster_view(self) -> MoveRosterView:
        pass

    @property
    @abstractmethod
    def pkm_type(self) -> PkmType:
        pass

    @property
    @abstractmethod
    def max_hp(self) -> float:
        pass

    @property
    @abstractmethod
    def pkm_id(self) -> int:
        pass


def get_pkm_template_view(template: PkmTemplate) -> PkmTemplateView:
    class PkmTemplateViewImpl(PkmTemplateView):

        def get_move_roster_view(self) -> MoveRosterView:
            return get_pkm_move_roster_view(template.move_roster)

        @property
        def pkm_type(self) -> PkmType:
            return template.type

        @property
        def max_hp(self) -> float:
            return template.max_hp

        @property
        def pkm_id(self) -> int:
            return template.pkm_id

        def __eq__(self, other):
            return self.pkm_type == other.pkm_type and self.max_hp == other.max_hp and self.get_move_roster_view() == \
                   other.get_move_roster_view()

        def __hash__(self):
            return hash((template.type, template.max_hp) + tuple(template.move_roster))

    return PkmTemplateViewImpl()


PkmRoster = Set[PkmTemplate]


class PkmRosterView(ABC):

    @abstractmethod
    def get_pkm_template_view(self, idx: int) -> PkmTemplateView:
        pass

    @property
    @abstractmethod
    def n_pkms(self) -> int:
        pass


def get_pkm_roster_view(pkm_roster: PkmRoster) -> PkmRosterView:
    class PkmRosterViewImpl(PkmRosterView):

        def get_pkm_template_view(self, idx: int) -> PkmTemplateView:
            return get_pkm_template_view(list(pkm_roster)[idx])

        @property
        def n_pkms(self) -> int:
            return len(pkm_roster)

    return PkmRosterViewImpl()


class PkmTeam:

    def __init__(self, pkms: List[Pkm] = None):
        """
        In battle Pkm team.

        :param pkms: Chosen pokemon. The first stays the active pokemon.
        """
        if pkms is None or pkms == []:
            pkms = [Pkm(), Pkm(), Pkm()]
        self.active: Pkm = pkms.pop(0)
        self.active.reveal()
        self.party: List[Pkm] = pkms
        self.stage: List[int] = [0] * N_STATS
        self.confused: bool = False
        self.n_turns_confused: int = 0
        self.entry_hazard: List[int] = [0] * N_ENTRY_HAZARD

    def __eq__(self, other):
        eq = self.active == other.active and self.stage == other.stage and self.confused == other.confused and \
             self.n_turns_confused == other.n_turns_confused
        if not eq:
            return False
        for i, p in enumerate(self.party):
            if p != other.party[i]:
                return False
        for i, h in enumerate(self.entry_hazard):
            if h != other.entry_hazard[i]:
                return False
        return True

    def __str__(self):
        party = ''
        for i in range(0, len(self.party)):
            party += str(self.party[i]) + '\n'
        return 'Active:\n%s\nParty:\n%s' % (str(self.active), party)

    def reset(self):
        """
        Reset all pkm status from team and active pkm conditions.
        """
        self.active.reset()
        for pkm in self.party:
            pkm.reset()
        for i in range(len(self.stage)):
            self.stage[i] = 0
        self.confused = False
        self.n_turns_confused = 0
        for i in range(len(self.entry_hazard)):
            self.entry_hazard[i] = 0

    def reset_team_members(self, pkms: List[Pkm] = None):
        """
        Reset team members

        :param pkms: list of pkm members
        """
        if pkms is None:
            pkms = [Pkm()]
        self.active = pkms.pop(0)
        self.party = pkms
        self.reset()

    def size(self) -> int:
        """
        Get team size.

        :return: Team size. Number of party pkm plus 1
        """
        return len(self.party) + 1

    def fainted(self) -> bool:
        """
        Check if team is fainted

        :return: True if entire team is fainted
        """
        for i in range(len(self.party)):
            if not self.party[i].fainted():
                return False
        return self.active.fainted()

    def get_not_fainted(self) -> List[int]:
        """
        Check which pokemon are not fainted in party.

        :return: a list of positions of not fainted pkm in party.
        """
        not_fainted = []
        for i, p in enumerate(self.party):
            if not p.fainted():
                not_fainted.append(i)
        return not_fainted

    def switch(self, pos: int) -> Tuple[Pkm, Pkm, int]:
        """
        Switch active pkm with party pkm on pos.
        Random party pkm if s_pos = -1

        :param pos: to be switch pokemon party position
        :returns: new active pkm, old active pkm, pos
        """
        if len(self.party) == 0:
            return self.active, self.active, -1

        # identify fainted pkm
        not_fainted_pkm = self.get_not_fainted()
        all_party_fainted = not not_fainted_pkm
        all_fainted = all_party_fainted and self.active.fainted()

        if not all_fainted:
            # select random party pkm to switch if needed
            if not all_party_fainted:
                if pos == -1:
                    np.random.shuffle(not_fainted_pkm)
                    pos = not_fainted_pkm[0]

                # switch party and bench pkm
                active = self.active
                self.active = self.party[pos]
                self.party[pos] = active

                # clear
                self.stage = [0] * N_STATS
                self.confused = False

                self.active.reveal()

        return self.active, self.party[pos], pos

    def get_pkm_list(self):
        return [self.active] + self.party


class PkmTeamView(ABC):

    @property
    @abstractmethod
    def active_pkm_view(self) -> PkmView:
        pass

    @abstractmethod
    def get_party_pkm_view(self, idx: int) -> PkmView:
        pass

    @abstractmethod
    def get_stage(self, stat: PkmStat) -> int:
        pass

    @property
    @abstractmethod
    def confused(self) -> bool:
        pass

    @property
    @abstractmethod
    def n_turns_confused(self) -> int:
        pass

    @property
    @abstractmethod
    def party_size(self) -> int:
        pass

    @abstractmethod
    def get_entry_hazard(self, hazard: PkmEntryHazard) -> int:
        pass


class PkmTeamPrediction:

    def __init__(self, team_view: PkmTeamView = None):
        self.team_view = team_view
        self.active: Union[Pkm, None] = None
        self.party: List[Union[Pkm, None]] = []


def get_team_view(team: PkmTeam, team_prediction: PkmTeamPrediction = None, partial: bool = False) -> PkmTeamView:
    class PkmTeamViewImpl(PkmTeamView):

        @property
        def active_pkm_view(self) -> PkmView:
            if partial:
                if team_prediction is None:
                    # get partial information without any hypothesis
                    return get_partial_pkm_view(team.active)
                # get partial information with  hypothesis
                return get_partial_pkm_view(team.active, team_prediction.active)
            # get self active pkm information
            return get_pkm_view(team.active)

        def get_party_pkm_view(self, idx: int) -> PkmView:
            if partial:
                if team_prediction is None:
                    # get partial information without any hypothesis
                    return get_partial_pkm_view(team.party[idx])
                # get partial information with a hypothesis
                return get_partial_pkm_view(team.party[idx], team_prediction.party[idx])
            # get self party pkm information
            return get_pkm_view(team.party[idx])

        def get_stage(self, stat: PkmStat) -> int:
            return team.stage[stat]

        @property
        def confused(self) -> bool:
            return team.confused

        @property
        def n_turns_confused(self) -> int:
            return team.n_turns_confused

        def get_entry_hazard(self, hazard: PkmEntryHazard) -> int:
            return team.entry_hazard[hazard]

        @property
        def party_size(self) -> int:
            return team.size() - 1

    return PkmTeamViewImpl()


class PkmFullTeam:

    def __init__(self, pkm_list: List[Pkm] = None):
        if pkm_list is None:
            pkm_list = [deepcopy(null_pkm) for _ in range(6)]
        self.pkm_list = pkm_list[:6]

    def __str__(self):
        team = ''
        for i in range(0, len(self.pkm_list)):
            team += str(self.pkm_list[i]) + '\n'
        return 'Team:\n%s' % team

    def get_battle_team(self, idx: List[int]) -> PkmTeam:
        return PkmTeam([self.pkm_list[i] for i in idx])

    def reset(self):
        for pkm in self.pkm_list:
            pkm.reset()

    def hide(self):
        for pkm in self.pkm_list:
            pkm.hide()

    def hide_pkms(self):
        for pkm in self.pkm_list:
            pkm.hide_pkm()

    def reveal(self):
        for pkm in self.pkm_list:
            pkm.reveal()

    def get_copy(self):
        return PkmFullTeam(self.pkm_list)

    def __len__(self):
        return len(self.pkm_list)

    def __getitem__(self, index):
        return self.pkm_list[index]

class PkmFullTeamView(ABC):

    @abstractmethod
    def get_pkm_view(self, idx: int) -> PkmView:
        pass

    @property
    @abstractmethod
    def n_pkms(self) -> int:
        pass


def get_full_team_view(full_team: PkmFullTeam, team_prediction: PkmTeamPrediction = None,
                       partial: bool = False) -> PkmFullTeamView:
    class PkmFullTeamViewImpl(PkmFullTeamView):

        def get_pkm_view(self, idx: int) -> PkmView:
            pkm = full_team.pkm_list[idx]
            if partial:
                if team_prediction is None:
                    # get partial information without any hypothesis
                    return get_partial_pkm_view(pkm)
                # get partial information with a hypothesis
                return get_partial_pkm_view(pkm, team_prediction.active)
            # get self active pkm information
            return get_pkm_view(pkm)

        @property
        def n_pkms(self) -> int:
            return len(full_team.pkm_list)

    return PkmFullTeamViewImpl()


class Weather:

    def __init__(self):
        self.condition: WeatherCondition = WeatherCondition.CLEAR
        self.n_turns_no_clear: int = 0


class GameState:

    def __init__(self, teams: List[PkmTeam], weather: Weather):
        self.teams = teams
        self.weather = weather

    def __eq__(self, other):
        for i, team in enumerate(self.teams):
            if team != other.teams[i]:
                return False
        return self.weather.condition == other.weather.condition and self.weather.n_turns_no_clear == other.weather.n_turns_no_clear


class GameStateView(ABC):

    @abstractmethod
    def get_team_view(self, idx: int) -> PkmTeamView:
        pass

    @property
    @abstractmethod
    def weather_condition(self) -> WeatherCondition:
        pass

    @property
    @abstractmethod
    def n_turns_no_clear(self) -> int:
        pass


def get_game_state_view(game_state: GameState, team_prediction: PkmTeamPrediction = None) -> GameStateView:
    class GameStateViewImpl(GameStateView):

        def __init__(self):
            self._teams = [get_team_view(game_state.teams[0]),
                           get_team_view(game_state.teams[1], team_prediction, partial=True)]

        def get_team_view(self, idx: int) -> PkmTeamView:
            return self._teams[idx]

        @property
        def weather_condition(self) -> WeatherCondition:
            return game_state.weather.condition

        @property
        def n_turns_no_clear(self) -> int:
            return game_state.weather.n_turns_no_clear

    return GameStateViewImpl()
