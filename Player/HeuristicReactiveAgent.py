from Environment.PkmBattleEnv import N_MOVES, N_SWITCHES, Pkm, WATER, RAIN, FIRE, SUNNY, TYPE_CHART_MULTIPLIER
from Trainer.Tabular.Abstract.Agent import *
import numpy as np

SWITCH_PROBABILITY = .15


class HeuristicReactiveAgent(Agent):

    def __init__(self, switch_probability=SWITCH_PROBABILITY):
        super().__init__()
        self.n_actions = N_MOVES + N_SWITCHES
        self.pi = ([(1. - switch_probability) / N_MOVES] * N_MOVES) + ([switch_probability / N_SWITCHES] * N_SWITCHES)

    def get_action(self, s):
        """

        :param s: state
        :return: action
        """
        a_pkm = Pkm(p_type=s[0], hp=s[1], status=s[2], type0=s[21], type0power=s[22], type1=s[23], type1power=s[24],
                    type2=s[25], type2power=s[26], type3=s[27], type3power=s[28])
        opp_a_pkm = Pkm(p_type=s[3], hp=s[4], status=s[5])
        p_pkm = [Pkm(p_type=s[6], hp=s[7], status=s[8]), Pkm(p_type=s[9], hp=s[10], status=s[11]),
                 Pkm(p_type=s[12], hp=s[13], status=s[14]), Pkm(p_type=s[15], hp=s[16], status=s[17]),
                 Pkm(p_type=s[18], hp=s[19], status=s[20])]
        attack_stage = [s[29], s[30]]
        defense_stage = [s[31], s[32]]
        speed_stage = [s[33], s[34]]
        spikes = [s[35], s[36]]
        n_turns_asleep = [s[37], s[38]]
        confused = [s[39], s[40]]
        weather = s[41]

        # TODO

        return np.random.choice(self.n_actions, p=self.pi)

    @staticmethod
    def _estimate_move_damage(move_id, pkm, opp_pkm, attack_stage, defense_stage, weather):
        move = pkm.moves[move_id]
        stab = 1.5 if move.type == pkm.p_type else 1.
        if (move.type == WATER and weather == RAIN) or (move.type == FIRE and weather == SUNNY):
            weather = 1.5
        elif (move.type == WATER and weather == SUNNY) or (move.type == FIRE and weather == RAIN):
            weather = .5
        else:
            weather = 1.
        stage_level = attack_stage[0] - defense_stage[1]
        stage = (stage_level + 2.) / 2 if stage_level >= 0. else 2. / (np.abs(stage_level) + 2.)
        damage = TYPE_CHART_MULTIPLIER[move.type][opp_pkm.p_type] * stab * weather * stage * move.power
        return damage
