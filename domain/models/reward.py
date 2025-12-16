from enum import IntEnum


class Reward(IntEnum):
    STEP = -1
    WALL = -25
    OUT_OF_MAP = -10
    MONSTER = -100
    DOR_NO_KEY = -5
    KEY = 50
    DOOR = 150
    GOAL = 1000
