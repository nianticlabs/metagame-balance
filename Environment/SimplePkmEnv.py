import gym
from gym import spaces
import random
import numpy as np
from copy import deepcopy

# type codification
NORMAL = 0
FIRE = 1
WATER = 2
ELECTRIC = 3
GRASS = 4
ICE = 5
FIGHT = 6
POISON = 7
GROUND = 8
FLYING = 9
PSYCHIC = 10
BUG = 11
ROCK = 12
GHOST = 13
DRAGON = 14
DARK = 15
STEEL = 16
FAIRY = 17

TYPE_TO_STR = {NORMAL: "NORMAL", FIRE: "FIRE", WATER: "WATER", ELECTRIC: "ELECTRIC", GRASS: "GRASS", ICE: "ICE",
               FIGHT: "FIGHT", POISON: "POISON", GROUND: "GROUND", FLYING: "FLYING", PSYCHIC: "PSYCHIC", BUG: "BUG",
               ROCK: "ROCK", GHOST: "GHOST", DRAGON: "DRAGON", DARK: "DARK", STEEL: "STEEL", FAIRY: "FAIRY"}
TYPE_LIST = [NORMAL, FIRE, WATER, ELECTRIC, GRASS, ICE, FIGHT, POISON, GROUND, FLYING, PSYCHIC, BUG, ROCK, GHOST,
             DRAGON, DARK, STEEL, FAIRY]
N_TYPES = len(TYPE_LIST)

# type chart
TYPE_CHART_MULTIPLIER = [
    [1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., .5, .0, 1., 1., .5, 1.],  # NORMAL
    [1., .5, .5, 1., 2., 2., 1., 1., 1., 1., 1., 2., .5, 1., .5, 1., 2., 1.],  # FIRE
    [1., 2., .5, 1., .5, 1., 1., 1., 2., 1., 1., 1., 2., 1., .5, 1., 1., 1.],  # WATER
    [1., 1., 2., .5, .5, 1., 1., 1., 0., 2., 1., 1., 1., 1., .5, 1., 1., 1.],  # ELECTRIC
    [1., .5, 2., 1., .5, 1., 1., .5, 2., .5, 1., .5, 2., 1., .5, 1., .5, 1.],  # GRASS
    [1., .5, .5, 1., 2., .5, 1., 1., 2., 2., 1., 1., 1., 1., 2., 1., .5, 1.],  # ICE
    [2., 1., 1., 1., 1., 2., 1., .5, 1., .5, .5, .5, 2., 0., 1., 2., 2., .5],  # FIGHTING
    [1., 1., 1., 1., 2., 1., 1., .5, .5, 1., 1., 1., .5, .5, 1., 1., .0, 2.],  # POISON
    [1., 2., 1., 2., .5, 1., 1., 2., 1., 0., 1., .5, 2., 1., 1., 1., 2., 1.],  # GROUND
    [1., 1., 1., .5, 2., 1., 2., 1., 1., 1., 1., 2., .5, 1., 1., 1., .5, 1.],  # FLYING
    [1., 1., 1., 1., 1., 1., 2., 2., 1., 1., .5, 1., 1., 1., 1., 0., .5, 1.],  # PSYCHIC
    [1., .5, 1., 1., 2., 1., .5, .5, 1., .5, 2., 1., 1., .5, 1., 2., .5, .5],  # BUG
    [1., 2., 1., 1., 1., 2., .5, 1., .5, 2., 1., 2., 1., 1., 1., 1., .5, 1.],  # ROCK
    [0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 2., 1., 1., 2., 1., .5, 1., 1.],  # GHOST
    [1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 2., 1., .5, .0],  # DRAGON
    [1., 1., 1., 1., 1., 1., .5, 1., 1., 1., 2., 1., 1., 2., 1., .5, 1., .5],  # DARK
    [1., .5, .5, .5, 1., 2., 1., 1., 1., 1., 1., 1., 2., 1., 1., 1., .5, 2.],  # STEEL
    [1., .5, 1., 1., 1., 1., 2., .5, 1., 1., 1., 1., 1., 1., 2., 2., .5, 1.]  # FAIRY
]

# move power range
POWER_MIN = 50.
POWER_MAX = 100.

# number moves
N_MOVES = 4
SWITCH_ACTION = N_MOVES

# hit Points
HIT_POINTS = POWER_MAX + POWER_MIN + 150.

# settings
SETTING_RANDOM = 0
SETTING_FULL_DETERMINISTIC = 1
SETTING_HALF_DETERMINISTIC = 2
SETTING_FAIR_IN_ADVANTAGE = 3


class SimpleMove:
    def __init__(self, move_type=None, move_power=None, my_type=None):
        if move_type is None:
            if my_type is None:
                self.type = random.randrange(0, N_TYPES)
            else:
                self.type = random.randrange(0, N_TYPES)
                # Don't pick attacks that are super effective against self or that self is super effective against
                while (TYPE_CHART_MULTIPLIER[self.type][my_type] > 1 or
                       TYPE_CHART_MULTIPLIER[my_type][self.type] > 1):
                    self.type = random.randrange(0, N_TYPES)
        else:
            self.type = move_type
        if move_power is None:
            self.power = random.randrange(POWER_MIN, POWER_MAX) * 1.
        else:
            self.power = move_power
        # STAB
        if my_type == move_type:
            move_power *= 1.5

    def __str__(self):
        return "Move(" + TYPE_TO_STR[self.type] + ", " + str(self.power) + ")"


class SimplePkm:
    def __init__(self, p_type=None, hp=HIT_POINTS,
                 type0=None, type0power=None, type1=None, type1power=None,
                 type2=None, type2power=None, type3=None, type3power=None):
        self.hp = hp
        if p_type is None:
            self.p_type = random.randrange(0, N_TYPES)
            self.moves = [SimpleMove(my_type=self.p_type) for i in range(N_MOVES - 1)] + [
                SimpleMove(move_type=self.p_type)]
        else:
            self.p_type = p_type
            self.moves = [SimpleMove(move_type=type0, move_power=type0power),
                          SimpleMove(move_type=type1, move_power=type1power),
                          SimpleMove(move_type=type2, move_power=type2power),
                          SimpleMove(move_type=type3, move_power=type3power)]

    def __str__(self):
        return 'Pokemon(' + TYPE_TO_STR[self.p_type] + ', HP ' + str(self.hp) + ', ' + str(self.moves[0]) + ', ' + str(
            self.moves[1]) + ', ' + str(self.moves[2]) + ', ' + str(self.moves[3]) + ')'


class SimplePkmEnv(gym.Env):
    def __init__(self, setting=SETTING_RANDOM, debug=False):
        self.numberOfActions = N_MOVES + 1
        self.a_pkm = [SimplePkm(), SimplePkm()]  # active pokemons
        self.p_pkm = [SimplePkm(), SimplePkm()]  # party pokemons
        self.setting = setting
        self.action_space = spaces.Discrete(N_MOVES + 1)
        self.observation_space = spaces.Discrete(len(encode(self._state_trainer(0))))
        self.first = None
        self.second = None
        # debug
        self.debug = debug
        self.debug_message = ['', '']
        self.switched = [False, False]
        self.has_fainted = False

    def step(self, actions):
        self.has_fainted = False
        self.switched = [False, False]
        r = [0., 0.]
        # switch pokemon
        if actions[0] == SWITCH_ACTION:
            if not SimplePkmEnv._fainted_pkm(self.p_pkm[0]):
                self._switch_pkm(0)
        if actions[1] == SWITCH_ACTION:
            if not SimplePkmEnv._fainted_pkm(self.p_pkm[1]):
                self._switch_pkm(1)

        # pokemon attacks
        order = [0, 1]
        # random attack order
        np.random.shuffle(order)
        self.first = order[0]
        self.second = order[1]

        terminal = False
        can_player2_attack = True

        # first attack
        dmg_dealt1 = 0
        dmg_dealt2 = 0

        if actions[self.first] != SWITCH_ACTION:
            r[self.first], terminal, can_player2_attack, dmg_dealt1 = self._battle_pkm(actions[self.first], self.first)

        if can_player2_attack and actions[self.second] != SWITCH_ACTION:
            r[self.second], terminal, _, dmg_dealt2 = self._battle_pkm(actions[self.second], self.second)
        elif self.debug:
            self.debug_message[self.second] = 'can\'t perform any action'

        r[self.first] -= dmg_dealt2 / HIT_POINTS
        r[self.second] -= dmg_dealt1 / HIT_POINTS

        return [encode(self._state_trainer(0)), encode(self._state_trainer(1))], r, terminal, None

    def reset(self):
        if self.debug:
            self.debug_message = ['', '']
        if self.setting == SETTING_RANDOM:
            self.a_pkm = [SimplePkm(), SimplePkm()]  # active pokemons
            self.p_pkm = [SimplePkm(), SimplePkm()]  # party pokemons
        elif self.setting == SETTING_FULL_DETERMINISTIC:
            self.a_pkm = [SimplePkm(GRASS, HIT_POINTS, GRASS, 90, FIRE, 90, GRASS, 90, FIRE, 90),
                          SimplePkm(FIRE, HIT_POINTS, FIRE, 90, FIRE, 90, FIRE, 90, FIRE, 90)]  # active pokemons
            self.p_pkm = [SimplePkm(WATER, HIT_POINTS, FIGHT, 90, NORMAL, 90, NORMAL, 90, WATER, 90),
                          SimplePkm(NORMAL, HIT_POINTS, NORMAL, 90, NORMAL, 90, NORMAL, 90, NORMAL,
                                    90)]  # party pokemons
        elif self.setting == SETTING_HALF_DETERMINISTIC:
            if random.uniform(0, 1) <= 0.2:
                type1 = random.randrange(0, N_TYPES - 1)
                type2 = get_super_effective_move(type1)
                self.a_pkm = [SimplePkm(type1, HIT_POINTS, type1, 90, type2, 90, type1, 90, type2, 90),
                              SimplePkm(type2, HIT_POINTS, type2, 90, type2, 90, type2, 90, type2,
                                        90)]  # active pokemons
            else:
                self.a_pkm = [SimplePkm(), SimplePkm()]  # active pokemons
            self.p_pkm = [SimplePkm(), SimplePkm()]  # party pokemons
        elif self.setting == SETTING_FAIR_IN_ADVANTAGE:
            type1 = random.randrange(0, N_TYPES - 1)
            type2 = get_super_effective_move(type1)
            self.a_pkm = [
                SimplePkm(type1, get_non_very_effective_move(type2), 90, get_non_very_effective_move(type2), 90,
                          get_normal_effective_move(type2), 90, type1, 90),
                SimplePkm(type2, get_super_effective_move(type1), 90, get_non_very_effective_move(type1), 90,
                          get_normal_effective_move(type1), 90, type2, 90)]  # active pokemons
            self.p_pkm = [SimplePkm(), SimplePkm()]  # party pokemons
        return [encode(self._state_trainer(0)), encode(self._state_trainer(1))]

    def render(self, mode='human'):
        if self.debug:
            if self.debug_message[0] != '' and self.debug_message[1] != '':
                if self.switched[0]:
                    if self.has_fainted:
                        print('Trainer 1', self.debug_message[1])
                        print('Trainer 0', self.debug_message[0])
                    else:
                        print('Trainer 0', self.debug_message[0])
                        print('Trainer 1', self.debug_message[1])
                elif self.switched[1]:
                    if self.has_fainted:
                        print('Trainer 0', self.debug_message[0])
                        print('Trainer 1', self.debug_message[1])
                    else:
                        print('Trainer 1', self.debug_message[1])
                        print('Trainer 0', self.debug_message[0])
                elif self.first == 0:
                    print('Trainer 0', self.debug_message[0])
                    print('Trainer 1', self.debug_message[1])
                else:
                    print('Trainer 1', self.debug_message[1])
                    print('Trainer 0', self.debug_message[0])
            print()
        print('Trainer 0')
        print('Active', self.a_pkm[0])
        print('Party', self.p_pkm[0])
        print('Trainer 1')
        print('Active', self.a_pkm[1])
        if mode != 'player':
            print('Party', self.p_pkm[1])
        print()

    def change_setting(self, setting):
        self.setting = setting

    def _state_trainer(self, t_id):
        return [self.a_pkm[t_id].p_type, self.a_pkm[t_id].hp,
                self.p_pkm[t_id].p_type, self.p_pkm[t_id].hp,
                self.a_pkm[not t_id].p_type, self.a_pkm[not t_id].hp,
                self.a_pkm[t_id].moves[0].type, self.a_pkm[t_id].moves[0].power,
                self.a_pkm[t_id].moves[1].type, self.a_pkm[t_id].moves[1].power,
                self.a_pkm[t_id].moves[2].type, self.a_pkm[t_id].moves[2].power,
                self.a_pkm[t_id].moves[3].type, self.a_pkm[t_id].moves[3].power,
                self.p_pkm[not t_id].hp]

    def _switch_pkm(self, t_id):
        if self.p_pkm[t_id].hp != 0:
            temp = self.a_pkm[t_id]
            self.a_pkm[t_id] = self.p_pkm[t_id]
            self.p_pkm[t_id] = temp
            if self.debug:
                self.debug_message[t_id] = "SWITCH"
            self.switched[t_id] = True
        elif self.debug:
            self.debug_message[t_id] = "FAILED SWITCH"

    def _attack_pkm(self, t_id, m_id):
        move = self.a_pkm[t_id].moves[m_id]
        opponent_pkm = self.a_pkm[not t_id]
        before_pkm = deepcopy(opponent_pkm)
        opponent_pkm.hp -= TYPE_CHART_MULTIPLIER[move.type][opponent_pkm.p_type] * move.power
        if opponent_pkm.hp <= 0.:
            opponent_pkm.hp = 0.
        damage = before_pkm.hp - opponent_pkm.hp
        if self.debug:
            self.debug_message[t_id] = "ATTACK with " + str(move) + " to type " + TYPE_TO_STR[
                opponent_pkm.p_type] + " multiplier=" + str(
                TYPE_CHART_MULTIPLIER[move.type][opponent_pkm.p_type]) + " causing " + str(
                damage) + " damage, leaving opponent hp " + str(opponent_pkm.hp) + ''
        return damage

    def _battle_pkm(self, a, t_id):
        """

        :param a: attack
        :param t_id: trainer id
        :return: reward, terminal, and whether target survived and can attack
        """
        opponent = not t_id
        terminal = False
        next_player_can_attack = True
        damage_dealt = self._attack_pkm(t_id, a)
        reward = damage_dealt / HIT_POINTS
        if self._fainted_pkm(self.a_pkm[opponent]):
            self.has_fainted = True
            reward += 1
            next_player_can_attack = False
            if self._fainted_pkm(self.p_pkm[opponent]):
                terminal = True
            else:
                self._switch_pkm(opponent)
                if self.debug:
                    self.debug_message[opponent] += " FAINTED"
        return reward, terminal, next_player_can_attack, damage_dealt

    @staticmethod
    def _fainted_pkm(pkm):
        return pkm.hp == 0


def encode(s):
    """
    Encode Game state.
    :param s: game state
    :return: encoded game state in one hot vector
    """
    e = []
    for i in range(0, len(s) - 1):
        if i % 2 == 0:
            b = [0] * N_TYPES
            b[s[i]] = 1
            e += b
        else:
            e += [(s[i] / HIT_POINTS)]
    e += [(s[-1] / HIT_POINTS)]
    return e


def decode(e):
    """
    Decode game state.
    :param e: encoded game state in one hot vector
    :return: game state
    """
    s = []
    index_e = 0
    for i in range(0, 7):
        for j in range(index_e, index_e + N_TYPES):
            if e[j] == 1:
                s.append(j % (N_TYPES + 1))
        index_e += N_TYPES
        s.append(e[index_e] * HIT_POINTS)
        index_e += 1
    s.append(e[index_e] * HIT_POINTS)
    return s


def get_super_effective_move(t):
    """
    :param t: pokemon type
    :return: a random type that is super effective against pokemon type t
    """
    _t = [t_[t] for t_ in TYPE_CHART_MULTIPLIER]
    s = [index for index, value in enumerate(_t) if value == 2]
    if not s:
        print('Warning: Empty List!')
        return random.randrange(N_TYPES)
    return random.choice(s)


def get_non_very_effective_move(t):
    """
    :param t: pokemon type
    :return: a random type that is not very effective against pokemon type t
    """
    _t = [t_[t] for t_ in TYPE_CHART_MULTIPLIER]
    s = [index for index, value in enumerate(_t) if value == 1 / 2]
    if not s:
        print('Warning: Empty List!')
        return random.randrange(N_TYPES)
    return random.choice(s)


def get_normal_effective_move(t):
    """
    :param t: pokemon type
    :return: a random type that is not very effective against pokemon type t
    """
    _t = [t_[t] for t_ in TYPE_CHART_MULTIPLIER]
    s = [index for index, value in enumerate(_t) if value == 1]
    if not s:
        print('Warning: Empty List!')
        return random.randrange(N_TYPES)
    return random.choice(s)
