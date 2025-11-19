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
        self.__axis = axis

        if self.__axis is MonsterAxis.HORIZONTAL:
            self.__direction = choice([Action.LEFT, Action.RIGHT])
        else:
            self.__direction = choice([Action.UP, Action.DOWN])

    def get_axis(self) -> MonsterAxis:
        return self.__axis

    def set_axis(self, axis: MonsterAxis) -> None:
        self.__axis = axis

    def get_direction(self) -> Action:
        return self.__direction

    def set_direction(self, direction: Action) -> None:
        self.__direction = direction

    def reverse_direction(self) -> None:
        if self.__direction is Action.LEFT:
            self.__direction = Action.RIGHT
        elif self.__direction is Action.RIGHT:
            self.__direction = Action.LEFT
        elif self.__direction is Action.UP:
            self.__direction = Action.DOWN
        elif self.__direction is Action.DOWN:
            self.__direction = Action.UP
