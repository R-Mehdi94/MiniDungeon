from enum import IntEnum


class Reward(IntEnum):
    STEP = -5
    WALL = -10
    OUT_OF_MAP = -10
    KEY = 200
    MONSTER = - 50
    DOR_NO_KEY = -20
    DOOR = 300
    GOAL = 100000
