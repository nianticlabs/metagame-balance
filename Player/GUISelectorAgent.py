from typing import List

from Engine.PkmBaseStructures import PkmTeam
from Engine.PkmConstants import DEFAULT_SELECTION_SIZE, MAX_TEAM_SIZE
import PySimpleGUI as sg

from Player.Abstract.Agent import SelectorAgent


class GUISelectorAgent(SelectorAgent):

    def __init__(self, selected_team_size: int = DEFAULT_SELECTION_SIZE, full_team_size: int = MAX_TEAM_SIZE):
        self.selected_team_size = selected_team_size
        self.opp_title = sg.Text('Opponent Team:')
        self.opp = [[sg.Text('                                      ')] for i in range(full_team_size)]
        self.team_title = sg.Text('Your Team:')
        self.team = [
            [sg.Text('                                      '),
             sg.Checkbox('Pkm ' + str(i), size=(10, 1), default=False, enable_events=True)] for i in
            range(full_team_size)]
        self.select = sg.ReadFormButton('Select', bind_return_key=True)
        layout = [[self.opp_title]] + self.opp + [[self.team_title]] + self.team + [[self.select]]
        self.window = sg.Window('Pokemon Battle Engine', layout)
        self.window.Finalize()
        self.select.Update(disabled=True)

    def get_action(self, s) -> List[int]:
        """

        :param s: state
        :return: action
        """
        selected = []
        for item in self.team:
            item[1].Update(value=False)
        opp: PkmTeam.OpponentView = s[0]
        team: PkmTeam.View = s[1]
        # opponent active
        opp_type, opp_hp = opp.get_active()
        opp_text = opp_type.name + ' ' + str(opp_hp) + ' HP'
        self.opp[0][0].Update(opp_text)
        # opponent party
        for i in range(opp.get_n_party()):
            party_type, party_hp = opp.get_party(i)
            party_text = party_type.name + ' ' + str(party_hp) + ' HP'
            self.opp[i + 1][0].Update(party_text)
        # active
        active_type, active_hp = team.get_active()
        active_text = active_type.name + ' ' + str(active_hp) + ' HP'
        self.team[0][0].Update(active_text)
        # party
        for i in range(opp.get_n_party()):
            party_type, party_hp = team.get_party(i)
            party_text = party_type.name + ' ' + str(party_hp) + ' HP'
            self.team[i + 1][0].Update(party_text)
        event, values = self.window.read()
        while event != self.select.get_text():
            if event not in selected:
                selected.append(event)
            else:
                selected.remove(event)
            self.select.Update(disabled=self.selected_team_size != len(selected))
            event, values = self.window.read()
        return selected

    def close(self):
        self.window.close()