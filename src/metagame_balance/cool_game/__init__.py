from enum import IntEnum


class BotType(IntEnum):
    # from https://github.com/Danielhp95/GGJ-2020-cool-game/blob/master/hyperopt_mongo/cool_game_regym_hyperopt.py
    # 0 - sawbot, 1 - torchbot, 2 - nailbot
    SAW = 0
    TORCH = 1
    NAIL = 2
