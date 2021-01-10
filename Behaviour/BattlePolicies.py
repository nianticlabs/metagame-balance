from typing import List
from Behaviour import BattlePolicy
from Framework.DataConstants import TYPE_CHART_MULTIPLIER, N_MOVES, N_DEFAULT_PARTY, N_SWITCHES
from Framework.DataObjects import PkmMove
from Framework.DataTypes import PkmStat, PkmType, WeatherCondition, PkmStatus
from Framework.Process.BattleEngine import PkmBattleEnv

import numpy as np
import PySimpleGUI as sg


class HeuristicBattlePolicy(BattlePolicy):

    def close(self):
        pass

    def requires_encode(self) -> bool:
        return False

    def get_action(self, s: PkmBattleEnv.TrainerView) -> int:
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
            estimated_damage.append(HeuristicBattlePolicy.estimate_move_damage(move_type, active_type, move_power,
                                                                               opp_type, attack_stage, defense_stage,
                                                                               weather))
        move_id: int = np.argmax(estimated_damage)[0]

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


class GUIBattlePolicy(BattlePolicy):

    def __init__(self, n_party: int = N_DEFAULT_PARTY, n_moves: int = N_MOVES):
        print(n_party)
        self.weather = sg.Text('                                                        ')
        self.opponent = sg.Text('                                                         ')
        self.active = sg.Text('                                                        ')
        self.moves = [sg.ReadFormButton('Move ' + str(i), bind_return_key=True) for i in range(n_moves)]
        self.party = [
            [sg.ReadFormButton('Switch ' + str(i), bind_return_key=True),
             sg.Text('                                      ')] for i in range(n_party)]
        layout = [[self.weather], [self.opponent], [self.active], self.moves] + self.party
        self.window = sg.Window('Pokemon Battle Engine', layout)
        self.window.Finalize()

    def requires_encode(self) -> bool:
        return False

    def get_action(self, s) -> int:
        """

        :param s: state
        :return: action
        """
        # weather
        self.weather.Update('Weather: ' + s.get_weather().name)
        # opponent
        opp_type, op_hp, opp_status, opp_confused = s.get_opponent()
        opp_text = 'Opp: ' + opp_type.name + ' ' + str(op_hp) + ' HP' + (
            '' if opp_status == PkmStatus.NONE else opp_status.name)
        opp_attack_stage = s.get_stage(t_id=1)
        if opp_attack_stage != 0:
            opp_text += ' ATK ' + str(opp_attack_stage)
        opp_defense_stage = s.get_stage(PkmStat.DEFENSE, 1)
        if opp_defense_stage != 0:
            opp_text += ' DEF ' + str(opp_defense_stage)
        opp_speed_stage = s.get_stage(PkmStat.SPEED, 1)
        if opp_speed_stage != 0:
            opp_text += ' SPD ' + str(opp_speed_stage)
        self.opponent.Update(opp_text)
        # active
        active_type, active_hp, active_status, active_confused = s.get_active()
        active_text = 'You: ' + active_type.name + ' ' + str(active_hp) + ' HP' + (
            '' if active_status == PkmStatus.NONE else active_status.name)
        active_attack_stage = s.get_stage(t_id=0)
        if active_attack_stage != 0:
            active_text += ' ATK ' + str(active_attack_stage)
        active_defense_stage = s.get_stage(PkmStat.DEFENSE, 0)
        if active_defense_stage != 0:
            active_text += ' DEF ' + str(active_defense_stage)
        active_speed_stage = s.get_stage(PkmStat.SPEED, 0)
        if active_speed_stage != 0:
            active_text += ' SPD ' + str(active_speed_stage)
        self.active.Update(active_text)
        # party
        for i in range(s.get_n_party()):
            party_type, party_hp, party_status = s.get_party(i)
            party_text = party_type.name + ' ' + str(party_hp) + ' HP' + (
                '' if party_status == PkmStatus.NONE else party_status.name) + ' '
            self.party[i][1].Update(party_text)
            self.party[i][0].Update(disabled=(party_hp == 0.0))
        # moves
        for i in range(s.get_n_moves()):
            move_power, move_type, move_name = s.get_active_move(i)
            self.moves[i].Update(str(PkmMove(power=move_power, move_type=move_type, name=move_name)))
        event, values = self.window.read()
        return self.__event_to_action(event)

    def __event_to_action(self, event):
        for i in range(len(self.moves)):
            if event == self.moves[i].get_text():
                return i
        for i in range(len(self.party)):
            if event == self.party[i][0].get_text():
                return i + N_MOVES
        return -1

    def close(self):
        self.window.close()


SWITCH_PROBABILITY = .15


class RandomBattlePolicy(BattlePolicy):

    def __init__(self, switch_probability: float = SWITCH_PROBABILITY, n_moves: int = N_MOVES,
                 n_switches: int = N_SWITCHES):
        super().__init__()
        self.n_actions: int = n_moves + n_switches
        self.pi: List[float] = ([(1. - switch_probability) / n_moves] * n_moves) + (
                [switch_probability / n_switches] * n_switches)

    def requires_encode(self) -> bool:
        return False

    def get_action(self, s) -> int:
        """

        :param s: state
        :return: action
        """
        return np.random.choice(self.n_actions, p=self.pi)

    def close(self):
        pass
