from typing import Set, Tuple
from framework.DataObjects import GameStateView, PkmTeamView
from framework.behaviour import SelectorPolicy
from framework.DataConstants import DEFAULT_TEAM_SIZE, MAX_TEAM_SIZE
import PySimpleGUI as sg
import random


class GUISelectorPolicy(SelectorPolicy):

    def __init__(self, selected_team_size: int = DEFAULT_TEAM_SIZE, full_team_size: int = MAX_TEAM_SIZE):
        self.selected_team_size = selected_team_size
        self.opp_title = sg.Text('Opponent Team:')
        self.opp = [[sg.Text('                                      ')] for _ in range(full_team_size)]
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

    def requires_encode(self) -> bool:
        return False

    def get_action(self, team_views: Tuple[PkmTeamView, PkmTeamView]) -> Set[int]:
        """

        :param team_views: (self, opponent)
        :return: idx list of selected pokemons
        """
        selected = []
        for item in self.team:
            item[1].Update(value=False)
        # opponent active
        opp_team = team_views[1]
        opp_active = opp_team.active_pkm_view
        opp_active_type = opp_active.type
        opp_active_hp = opp_active.hp
        opp_text = opp_active_type.name + ' ' + str(opp_active_hp) + ' HP'
        self.opp[0][0].Update(opp_text)
        # opponent party
        opp_party = [opp_team.get_party_pkm_view(0), opp_team.get_party_pkm_view(1)]
        for i, pkm in enumerate(opp_party):
            party_type = pkm.type
            party_hp = pkm.hp
            party_text = party_type.name + ' ' + str(party_hp) + ' HP'
            self.opp[i + 1][0].Update(party_text)
        # active
        my_team = team_views[0]
        my_active = my_team.active_pkm_view
        my_active_type = my_active.type
        my_active_hp = my_active.hp
        active_text = my_active_type.name + ' ' + str(my_active_hp) + ' HP'
        self.team[0][0].Update(active_text)
        # party
        my_party = [my_team.get_party_pkm_view(0), my_team.get_party_pkm_view(1)]
        for i, pkm in enumerate(my_party):
            party_type = pkm.type
            party_hp = pkm.hp
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
        return set(selected)

    def close(self):
        self.window.close()


class RandomSelectorPolicy(SelectorPolicy):

    def __init__(self, teams_size: int = MAX_TEAM_SIZE, selection_size: int = DEFAULT_TEAM_SIZE):
        self.teams_size = teams_size
        self.selection_size = selection_size

    def requires_encode(self) -> bool:
        return False

    def get_action(self, team_views: Tuple[PkmTeamView, PkmTeamView]) -> Set[int]:
        ids = [i for i in range(self.teams_size)]
        random.shuffle(ids)
        return set(ids[:self.selection_size])

    def close(self):
        pass
