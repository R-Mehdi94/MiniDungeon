from enum import IntEnum


class Reward(IntEnum):
    STEP = -1
    WALL = -10
    OUT_OF_MAP = -10
    KEY = 10
    MONSTER = -100
    GOAL = 1000
