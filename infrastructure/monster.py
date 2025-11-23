import arcade
from domain.models.action import Action
from domain.models.monster_axis import MonsterAxis
from random import choice


class Monster(arcade.Sprite):
    __axis: MonsterAxis
    __direction: Action

    def __init__(
        self,
        texture: str,
        scale: float,
        axis: MonsterAxis | None = None,
    ) -> None:
        super().__init__(texture, scale)

        if axis is None:
            axis = choice(list(MonsterAxis))
        self.axis = axis

        if self.axis is MonsterAxis.HORIZONTAL:
            self.direction = choice([Action.LEFT, Action.RIGHT])
        else:
            self.direction = choice([Action.UP, Action.DOWN])

    @property
    def axis(self) -> MonsterAxis:
        return self.__axis

    @axis.setter
    def axis(self, axis: MonsterAxis) -> None:
        self.__axis = axis

    @property
    def direction(self) -> Action:
        return self.__direction

    @direction.setter
    def direction(self, direction: Action) -> None:
        self.__direction = direction

    def reverse_direction(self) -> None:
        if self.direction is Action.LEFT:
            self.direction = Action.RIGHT
        elif self.direction is Action.RIGHT:
            self.direction = Action.LEFT
        elif self.direction is Action.UP:
            self.direction = Action.DOWN
        elif self.direction is Action.DOWN:
            self.direction = Action.UP
