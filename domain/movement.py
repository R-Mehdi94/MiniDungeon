from __future__ import annotations
from typing import Optional


class Movement:
    __abscissa: int
    __ordinate: int

    def __init__(self, abscissa: Optional[int], ordinate: Optional[int]) -> None:
        # Autorise 0 comme valeur valide, vérifie uniquement la présence de l'entier
        if abscissa is None:
            raise ValueError('`abscissa` is required in Movement constructor.')
        if ordinate is None:
            raise ValueError('`ordinate` is required in Movement constructor.')
        self.__abscissa = int(abscissa)
        self.__ordinate = int(ordinate)

    def get_abscissa(self) -> int:
        return self.__abscissa

    def set_abscissa(self, abscissa: Optional[int]) -> None:
        if abscissa is None:
            raise ValueError('`abscissa` is required in setter.')
        self.__abscissa = int(abscissa)

    def get_ordinate(self) -> int:
        return self.__ordinate

    def set_ordinate(self, ordinate: Optional[int]) -> None:
        if ordinate is None:
            raise ValueError('`ordinate` is required in setter.')
        self.__ordinate = int(ordinate)

    def as_tuple(self) -> tuple[int, int]:
        return (self.__abscissa, self.__ordinate)

    def __repr__(self) -> str:
        return f"Movement(abscissa={self.__abscissa}, ordinate={self.__ordinate})"
