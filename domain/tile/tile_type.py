from enum import Enum


class TileType(str, Enum):
    EMPTY = ' '
    WALL = '#'
    START = 'P'
    KEY = 'K'
    DOOR = 'D'
    MONSTER = 'M'
    TREASURE = 'T'
