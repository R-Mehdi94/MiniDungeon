from enum import Enum

from domain.models.movement import Movement


class Action(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def to_movement(self) -> Movement:
        row_delta, col_delta = self.value
        return Movement(row_delta, col_delta)
