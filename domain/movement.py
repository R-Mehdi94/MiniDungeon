from typing import Optional


class Movement:
    __abscissa: int
    __ordinate: int

    def get_abscissa(self) -> int:
        return self.__abscissa

    def set_abscissa(self, abscissa: Optional[int]) -> None:
        if abscissa is None:
            raise ValueError('`abscissa` is required in setter.')
        self.__abscissa = abscissa

    def get_ordinate(self) -> int:
        return self.__ordinate

    def set_ordinate(self, ordinate: Optional[int]) -> None:
        if ordinate is None:
            raise ValueError('`ordinate` is required in setter.')
        self.__ordinate = ordinate

    def __init__(self, abscissa: Optional[int], ordinate: Optional[int]) -> None:
        if not abscissa:
            raise ValueError('`abscissa` is required in Movement constructor.')
        if not ordinate:
            raise ValueError('`ordinate` is required in Movement constructor.')
        self.__abscissa = abscissa
        self.__ordinate = ordinate
