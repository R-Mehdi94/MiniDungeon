class Position:
    __abscissa: int
    __ordinate: int

    def get_abscissa(self) -> int:
        return self.__abscissa

    def set_abscissa(self, abscissa: int) -> None:
        if not isinstance(abscissa, int):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError('`abscissa` must be of type `int`.')
        self.__abscissa = abscissa

    def get_ordinate(self) -> int:
        return self.__ordinate

    def set_ordinate(self, ordinate: int) -> None:
        if not isinstance(ordinate, int):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError('`ordinate` must be of type `int`.')
        self.__ordinate = ordinate

    def __init__(self, abscissa: int, ordinate: int) -> None:
        if not isinstance(ordinate, int):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError('`ordinate` must be of type `int`.')
        if not isinstance(ordinate, int):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError('`ordinate` must be of type `int`.')
        self.__abscissa = abscissa
        self.__ordinate = ordinate
