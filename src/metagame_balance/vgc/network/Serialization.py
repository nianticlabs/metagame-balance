from metagame_balance.vgc.datatypes.Objects import GameStateView, PkmTeamView, PkmView, MoveView, PkmRosterView, PkmTemplateView, \
    MoveRosterView, PkmFullTeamView
from metagame_balance.vgc.datatypes.Types import WeatherCondition, PkmEntryHazard, PkmStat, N_ENTRY_HAZARD, N_STATS, PkmStatus, \
    PkmType


class SerializedMove(MoveView):

    def __init__(self, mv: MoveView):
        self._power = mv.power
        self._acc = mv.acc
        self._pp = mv.pp
        self._max_pp = mv.max_pp
        self._type = mv.type
        self._priority = mv.priority
        self._prob = mv.prob
        self._target = mv.target
        self._recover = mv.recover
        self._status = mv.status
        self._stat = mv.stat
        self._stage = mv.stage
        self._stage = mv.stage
        self._fixed_damage = mv.fixed_damage
        self._weather = mv.weather
        self._hazard = mv.hazard

    @property
    def power(self) -> float:
        return self._power

    @property
    def acc(self) -> float:
        return self._acc

    @property
    def pp(self) -> int:
        return self._pp

    @property
    def max_pp(self) -> int:
        return self._max_pp

    @property
    def type(self) -> PkmType:
        return self._type

    @property
    def priority(self) -> int:
        return self._priority

    @property
    def prob(self) -> float:
        return self._prob

    @property
    def target(self) -> int:
        return self._target

    @property
    def recover(self) -> float:
        return self._recover

    @property
    def status(self) -> PkmStatus:
        return self._status

    @property
    def stat(self) -> PkmStat:
        return self._stat

    @property
    def stage(self) -> int:
        return self._stage

    @property
    def fixed_damage(self) -> float:
        return self._fixed_damage

    @property
    def weather(self) -> WeatherCondition:
        return self._weather

    @property
    def hazard(self) -> PkmEntryHazard:
        return self._hazard


class SerializedPkm(PkmView):

    def __init__(self, pv: PkmView):
        self._move_view = [SerializedMove(pv.get_move_view(i)) for i in range(4)]
        self._type = pv.type
        self._hp = pv.hp
        self._status = pv.status
        self._n_turns_asleep = pv.n_turns_asleep

    def get_move_view(self, idx: int) -> MoveView:
        return self._move_view[idx]

    @property
    def type(self) -> PkmType:
        return self._type

    @property
    def hp(self) -> float:
        return self._hp

    @property
    def status(self) -> PkmStatus:
        return self._status

    @property
    def n_turns_asleep(self) -> int:
        return self._n_turns_asleep


class SerializedPkmTeam(PkmTeamView):

    def __init__(self, ptv: PkmTeamView):
        self._active_pkm_view = SerializedPkm(ptv.active_pkm_view)
        self._party_pkm_view = [SerializedPkm(ptv.get_party_pkm_view(0)), SerializedPkm(ptv.get_party_pkm_view(1))]
        self._stage = [0] * N_STATS
        self._stage[PkmStat.ATTACK] = ptv.get_stage(PkmStat.ATTACK)
        self._stage[PkmStat.DEFENSE] = ptv.get_stage(PkmStat.DEFENSE)
        self._stage[PkmStat.SPEED] = ptv.get_stage(PkmStat.SPEED)
        self._confused = ptv.confused
        self._n_turns_confused = ptv.n_turns_confused
        self._entry_hazard = [0] * N_ENTRY_HAZARD
        self._entry_hazard[PkmEntryHazard.SPIKES] = ptv.get_entry_hazard(PkmEntryHazard.SPIKES)

    @property
    def active_pkm_view(self) -> PkmView:
        return self._active_pkm_view

    def get_party_pkm_view(self, idx: int) -> PkmView:
        return self._party_pkm_view[idx]

    def get_stage(self, stat: PkmStat) -> int:
        return self._stage[stat]

    @property
    def confused(self) -> bool:
        return self._confused

    @property
    def n_turns_confused(self) -> int:
        return self._n_turns_confused

    def get_entry_hazard(self, hazard: PkmEntryHazard) -> int:
        return self._entry_hazard[hazard]


class SerializedGameState(GameStateView):

    def __init__(self, gsv: GameStateView):
        self._team_views = [SerializedPkmTeam(gsv.get_team_view(0)), SerializedPkmTeam(gsv.get_team_view(1))]
        self._weather_condition = gsv.weather_condition
        self._n_turns_no_clear = gsv.n_turns_no_clear

    def get_team_view(self, idx: int) -> PkmTeamView:
        return self._team_views[idx]

    @property
    def weather_condition(self) -> WeatherCondition:
        return self._weather_condition

    @property
    def n_turns_no_clear(self) -> int:
        return self._n_turns_no_clear


class SerializedMoveRoster(MoveRosterView):

    def __init__(self, mrv: MoveRosterView):
        self._move_view = [SerializedMove(mrv.get_move_view(i)) for i in range(mrv.n_moves)]
        self._n_moves = mrv.n_moves

    def get_move_view(self, idx: int) -> MoveView:
        return self._move_view[idx]

    @property
    def n_moves(self) -> int:
        return self._n_moves


class SerializedPkmTemplate(PkmTemplateView):

    def __init__(self, ptv: PkmTemplateView):
        self._move_roster_view = SerializedMoveRoster(ptv.get_move_roster_view())
        self._pkm_type = ptv.pkm_type
        self._max_hp = ptv.max_hp
        self._pkm_id = ptv.pkm_id

    def get_move_roster_view(self) -> MoveRosterView:
        return self._move_roster_view

    @property
    def pkm_type(self) -> PkmType:
        return self._pkm_type

    @property
    def max_hp(self) -> float:
        return self._max_hp

    @property
    def pkm_id(self) -> int:
        return self._pkm_id


class SerializedPkmRoster(PkmRosterView):

    def __init__(self, prv: PkmRosterView):
        self._pkm_template_view = [SerializedPkmTemplate(prv.get_pkm_template_view(i)) for i in range(prv.n_pkms)]
        self._n_pkms = prv.n_pkms

    def get_pkm_template_view(self, idx: int) -> PkmTemplateView:
        return self._pkm_template_view[idx]

    @property
    def n_pkms(self) -> int:
        return self._n_pkms


class SerializedPkmFullTeam(PkmFullTeamView):

    def __init__(self, pftv: PkmFullTeamView):
        self._pkm_view = [SerializedPkm(pftv.get_pkm_view(i)) for i in range(pftv.n_pkms)]
        self._n_pkms = pftv.n_pkms

    def get_pkm_view(self, idx: int) -> PkmView:
        return self._pkm_view[idx]

    @property
    def n_pkms(self) -> int:
        return self._n_pkms
