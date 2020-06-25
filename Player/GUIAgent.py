from Engine.PkmBaseStructures import PkmMove, PkmStatus
from Trainer.Tabular.Abstract.Agent import *
import PySimpleGUI as sg


class GUIAgent(Agent):

    def __init__(self):
        self.active = sg.Text('                                      ')
        self.moves = [sg.ReadFormButton('Move 0', bind_return_key=True),
                      sg.ReadFormButton('Move 1', bind_return_key=True),
                      sg.ReadFormButton('Move 2', bind_return_key=True),
                      sg.ReadFormButton('Move 3', bind_return_key=True)]
        layout = [[self.active], self.moves]
        self.window = sg.Window('Pokemon Battle Engine', layout)
        self.window.Finalize()

    def get_action(self, s):
        """

        :param s: state
        :return: action
        """
        active_type, active_hp, active_status, active_confused = s.get_active()
        active_text = active_type.name + ' ' + str(active_hp) + ' HP' + ('' if active_status == PkmStatus.NONE else active_status.name)
        self.active.Update(active_text)
        for i in range(s.get_n_moves()):
            move_power, move_type, move_name = s.get_active_move(i)
            self.moves[i].Update(PkmMove(move_power, move_type, move_name))
        event, values = self.window.read()
        return self.__event_to_action(event)

    def __event_to_action(self, event):
        for i in range(len(self.moves)):
            if event == self.moves[i].get_text():
                return i
        return -1

    def close(self):
        self.window.close()
