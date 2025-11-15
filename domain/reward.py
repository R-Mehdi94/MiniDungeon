from enum import IntEnum


class Reward(IntEnum):
    WALL = -10
    DEFAULT = -1
    KEY = 10
    GOAL = 1000
    OUT = -10
    MONSTER = -100
