from enum import IntEnum


class Reward(IntEnum):
    STEP = -1
    WALL = -2
    OUT_OF_MAP = -10
    KEY = 40
    MONSTER = -20
    DOR_NO_KEY = -20
    DOOR = 60
    GOAL = 100
