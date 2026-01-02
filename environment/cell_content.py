from enum import Enum


class CellContent(Enum):
    WALL = '#'
    EMPTY = ' '
    START = 'P'
    KEY = 'K'
    DOOR = 'D'
    MONSTER = 'M'
    TREASURE = 'T'
    OUT_OF_MAP = None
