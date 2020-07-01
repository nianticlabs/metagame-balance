from Engine.PkmBaseStructures import PkmMove, PkmStatus, PkmStat
from Engine.PkmConstants import N_MOVES
from Trainer.Tabular.Abstract.Agent import *
import PySimpleGUI as sg


class GUIBattleAgent(BattleAgent):

    def __init__(self):
        self.weather = sg.Text('                                                        ')
        self.opponent = sg.Text('                                                         ')
        self.active = sg.Text('                                                        ')
        self.moves = [sg.ReadFormButton('Move 0', bind_return_key=True),
                      sg.ReadFormButton('Move 1', bind_return_key=True),
                      sg.ReadFormButton('Move 2', bind_return_key=True),
                      sg.ReadFormButton('Move 3', bind_return_key=True)]
        self.party = [
            [sg.ReadFormButton('Switch 0', bind_return_key=True), sg.Text('                                      ')],
            [sg.ReadFormButton('Switch 1', bind_return_key=True), sg.Text('                                      ')],
            [sg.ReadFormButton('Switch 2', bind_return_key=True), sg.Text('                                      ')],
            [sg.ReadFormButton('Switch 3', bind_return_key=True), sg.Text('                                      ')],
            [sg.ReadFormButton('Switch 4', bind_return_key=True), sg.Text('                                      ')]]
        layout = [[self.weather], [self.opponent], [self.active], self.moves] + self.party
        self.window = sg.Window('Pokemon Battle Engine', layout)
        self.window.Finalize()

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
            self.moves[i].Update(PkmMove(move_power, move_type, move_name))
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
