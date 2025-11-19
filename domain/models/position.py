from __future__ import annotations
from domain.models.movement import Movement


class Position:
    __row: int
    __column: int

    def __init__(self, row: int, column: int) -> None:
        self.__row = row
        self.__column = column

    def get_row(self) -> int:
        return self.__row

    def set_row(self, row: int) -> None:
        self.__row = row

    def get_column(self) -> int:
        return self.__column

    def set_column(self, column: int) -> None:
        self.__column = column

    def calculate_next_position(self, movement: Movement) -> Position:
        return Position(
            self.__row + movement.get_row(),
            self.__column + movement.get_column()
        )

    def __hash__(self) -> int:
        return hash((self.__row, self.__column))

    def __repr__(self) -> str:
        return f'Position({self.__row}, {self.__column})'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):
            return NotImplemented
        return (
            self.__row == other.get_row()
            and self.__column == other.get_column()
        )
