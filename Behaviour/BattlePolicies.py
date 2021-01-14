from typing import List
from Behaviour import BattlePolicy
from Framework.Competition.Config import PARTY_SIZE
from Framework.DataConstants import TYPE_CHART_MULTIPLIER, N_MOVES, N_DEFAULT_PARTY
from Framework.DataObjects import PkmMove
from Framework.DataTypes import PkmStat, PkmType, WeatherCondition, PkmStatus
import numpy as np
import PySimpleGUI as sg


def estimate_damage(move_type: PkmType, pkm_type: PkmType, move_power: float, opp_pkm_type: PkmType,
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


class SimpleBattlePolicy(BattlePolicy):

    def close(self):
        pass

    def requires_encode(self) -> bool:
        return False

    def get_action(self, g) -> int:
        """
        Decision step.

        :param g: game state
        :return: action
        """
        # check weather condition
        weather = g.get_weather_condition()

        # get my team
        my_team = g.get_team_view(0)
        my_active = my_team.get_active_pkm_view()
        my_active_type = my_active.get_type()
        my_party = [my_team.get_party_pkm_view(0), my_team.get_party_pkm_view(1)]
        my_active_moves = [my_active.get_move_view(i) for i in range(N_MOVES)]
        my_attack_stage = my_team.get_stage(PkmStat.ATTACK)

        # get opp team
        opp_team = g.get_team_view(1)
        opp_active = opp_team.get_active_pkm_view()
        opp_active_type = opp_active.get_type()
        opp_active_hp = opp_active.get_hp()
        opp_defense_stage = opp_team.get_stage(PkmStat.DEFENSE)

        # get best move
        damage: List[float] = []
        for move in my_active_moves:
            move_power = move.get_power()
            move_type = move.get_type()
            damage.append(
                estimate_damage(move_type, my_active_type, move_power, opp_active_type, my_attack_stage,
                                opp_defense_stage, weather))
        move_id = int(np.argmax(damage))

        # switch decision
        best_pkm = 0
        if opp_active_hp > damage[move_id]:
            effectiveness_to_stay = TYPE_CHART_MULTIPLIER[my_active_type][opp_active_type]
            for i, pkm in enumerate(my_party):
                party_type = pkm.get_type()
                party_hp = pkm.get_hp()
                effectiveness_party = TYPE_CHART_MULTIPLIER[party_type][opp_active_type]
                if effectiveness_party > effectiveness_to_stay and party_hp != 0.0:
                    effectiveness_to_stay = effectiveness_party
                    best_pkm = i
        if best_pkm > 0:
            move_id = N_MOVES + best_pkm

        return move_id


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

    def get_action(self, g) -> int:
        """
        Decision step.

        :param g: game state
        :return: action
        """
        # weather
        self.weather.Update('Weather: ' + g.get_weather_condition().name)

        # get opp team
        opp_team = g.get_team_view(1)
        opp_active = opp_team.get_active_pkm_view()
        opp_active_type = opp_active.get_type()
        opp_active_hp = opp_active.get_hp()
        print(opp_active_hp)
        opp_status = opp_active.get_status()
        opp_text = 'Opp: ' + opp_active_type.name + ' ' + str(opp_active_hp) + ' HP' + (
            '' if opp_status == PkmStatus.NONE else opp_status.name)
        opp_attack_stage = opp_team.get_stage(PkmStat.ATTACK)
        if opp_attack_stage != 0:
            opp_text += ' ATK ' + str(opp_attack_stage)
        opp_defense_stage = opp_team.get_stage(PkmStat.DEFENSE)
        if opp_defense_stage != 0:
            opp_text += ' DEF ' + str(opp_defense_stage)
        opp_speed_stage = opp_team.get_stage(PkmStat.SPEED)
        if opp_speed_stage != 0:
            opp_text += ' SPD ' + str(opp_speed_stage)
        self.opponent.Update(opp_text)

        # active
        my_team = g.get_team_view(0)
        my_active = my_team.get_active_pkm_view()
        my_active_type = my_active.get_type()
        my_active_hp = my_active.get_hp()
        my_status = my_active.get_status()
        active_text = 'You: ' + my_active_type.name + ' ' + str(my_active_hp) + ' HP' + (
            '' if my_status == PkmStatus.NONE else my_status.name)
        active_attack_stage = my_team.get_stage(PkmStat.ATTACK)
        if active_attack_stage != 0:
            active_text += ' ATK ' + str(active_attack_stage)
        active_defense_stage = my_team.get_stage(PkmStat.DEFENSE)
        if active_defense_stage != 0:
            active_text += ' DEF ' + str(active_defense_stage)
        active_speed_stage = my_team.get_stage(PkmStat.SPEED)
        if active_speed_stage != 0:
            active_text += ' SPD ' + str(active_speed_stage)
        self.active.Update(active_text)

        # party
        my_party = [my_team.get_party_pkm_view(0), my_team.get_party_pkm_view(1)]
        for i, pkm in enumerate(my_party):
            party_type = pkm.get_type()
            party_hp = pkm.get_hp()
            party_status = pkm.get_status()
            party_text = party_type.name + ' ' + str(party_hp) + ' HP' + (
                '' if party_status == PkmStatus.NONE else party_status.name) + ' '
            self.party[i][1].Update(party_text)
            self.party[i][0].Update(disabled=(party_hp == 0.0))
        # moves
        my_active_moves = [my_active.get_move_view(i) for i in range(N_MOVES)]
        for i, move in enumerate(my_active_moves):
            move_power = move.get_power()
            move_type = move.get_type()
            self.moves[i].Update(str(PkmMove(power=move_power, move_type=move_type)))
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
                 n_switches: int = PARTY_SIZE):
        super().__init__()
        self.n_actions: int = n_moves + n_switches
        self.pi: List[float] = ([(1. - switch_probability) / n_moves] * n_moves) + (
                [switch_probability / n_switches] * n_switches)

    def requires_encode(self) -> bool:
        return False

    def get_action(self, g) -> int:
        """
        Decision step.

        :param g: game state
        :return: action
        """
        return np.random.choice(self.n_actions, p=self.pi)

    def close(self):
        pass