from Engine.PkmBaseStructures import PkmTeam
from Engine.PkmConstants import DEFAULT_SELECTION_SIZE
from Trainer.Tabular.Abstract.Agent import *
import PySimpleGUI as sg


class GUISelectionAgent(SelectionAgent):

    def __init__(self, selected_team_size: int = DEFAULT_SELECTION_SIZE):
        self.selected_team_size = selected_team_size
        self.opp_title = sg.Text('Opponent Team:')
        self.opp = [[sg.Text('                                      ')],
                    [sg.Text('                                      ')],
                    [sg.Text('                                      ')],
                    [sg.Text('                                      ')],
                    [sg.Text('                                      ')],
                    [sg.Text('                                      ')]]
        self.team_title = sg.Text('Your Team:')
        self.team = [
            [sg.Text('                                      '),
             sg.Checkbox('Pkm 0', size=(10, 1), default=False, enable_events=True)],
            [sg.Text('                                      '),
             sg.Checkbox('Pkm 1', size=(10, 1), default=False, enable_events=True)],
            [sg.Text('                                      '),
             sg.Checkbox('Pkm 2', size=(10, 1), default=False, enable_events=True)],
            [sg.Text('                                      '),
             sg.Checkbox('Pkm 3', size=(10, 1), default=False, enable_events=True)],
            [sg.Text('                                      '),
             sg.Checkbox('Pkm 4', size=(10, 1), default=False, enable_events=True)],
            [sg.Text('                                      '),
             sg.Checkbox('Pkm 5', size=(10, 1), default=False, enable_events=True)]]
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
        selected = []
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
