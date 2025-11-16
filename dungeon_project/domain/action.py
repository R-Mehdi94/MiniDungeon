from enum import Enum
from domain.movement import Movement


class Action(str, Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'

    def get_movement(self) -> Movement:
        if self is Action.UP:
            return Movement(-1, 0)
        if self is Action.DOWN:
            return Movement(1, 0)
        if self is Action.LEFT:
            return Movement(0, -1)
        if self is Action.RIGHT:
            return Movement(0, 1)
        else:
            raise ValueError('The action has no value.')
