from typing import List

from Engine.PkmBaseStructures import PkmType, WeatherCondition, PkmStat
from Engine.PkmBattleEngine import TYPE_CHART_MULTIPLIER, PkmBattleEngine
from Engine.PkmConstants import N_MOVES
import numpy as np

from Player.Abstract.Agent import BattleAgent


class HeuristicBattleAgent(BattleAgent):

    def close(self):
        pass

    def get_action(self, s: PkmBattleEngine.TrainerView) -> int:
        """

        :param s: state
        :return: action
        """
        active_type, active_hp, active_status, active_confused = s.get_active()
        opp_type, opp_hp, opp_status, opp_confused = s.get_opponent()
        party = [s.get_party(i) for i in range(s.get_n_party())]
        attack_stage = s.get_stage()
        defense_stage = s.get_stage(PkmStat.DEFENSE)
        speed_stage = s.get_stage(PkmStat.SPEED)
        opp_attack_stage = s.get_stage(t_id=1)
        opp_defense_stage = s.get_stage(PkmStat.DEFENSE, 1)
        opp_speed_stage = s.get_stage(PkmStat.SPEED, 1)
        active_moves = [s.get_active_move(i) for i in range(s.get_n_moves())]
        spikes = s.get_entry_hazard()
        weather = s.get_weather()

        # get best move
        estimated_damage: List[float] = []
        for i in range(s.get_n_moves()):
            move_power, move_type, _ = active_moves[i]
            estimated_damage.append(HeuristicBattleAgent.estimate_move_damage(move_type, active_type, move_power, opp_type,
                                                                              attack_stage, defense_stage, weather))
        move_id: int = np.argmax(estimated_damage)

        # switch decision
        best_pkm = 0
        if opp_hp > estimated_damage[move_id]:
            effectiveness_to_stay = TYPE_CHART_MULTIPLIER[active_type][opp_type]
            for i in range(s.get_n_party()):
                party_type, _, _ = party[i]
                effectiveness_party = TYPE_CHART_MULTIPLIER[party_type][opp_type]
                if effectiveness_party > effectiveness_to_stay:
                    effectiveness_to_stay = effectiveness_party
                    best_pkm = i + 1
        if best_pkm > 0:
            move_id = N_MOVES + best_pkm - 1

        return move_id

    @staticmethod
    def estimate_move_damage(move_type: PkmType, pkm_type: PkmType, move_power: float, opp_pkm_type: PkmType,
                             attack_stage: int, defense_stage: int, weather: WeatherCondition) -> float:
        stab = 1.5 if move_type == pkm_type else 1.
        if (move_type == PkmType.WATER and weather == WeatherCondition.RAIN) or (
                move_type == PkmType.FIRE and weather == WeatherCondition.SUNNY):
            weather = 1.5
        elif (move_type == PkmType.WATER and weather == WeatherCondition.SUNNY) or (
                move_type == PkmType.FIRE and weather == WeatherCondition.RAIN):
            weather = .5
        else:
            weather = 1.
        stage_level = attack_stage - defense_stage
        stage = (stage_level + 2.) / 2 if stage_level >= 0. else 2. / (np.abs(stage_level) + 2.)
        damage = TYPE_CHART_MULTIPLIER[move_type][opp_pkm_type] * stab * weather * stage * move_power
        return damage
