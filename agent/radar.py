class Radar:

    __view: tuple[int, ...]

    def __init__(self, view: tuple[int, ...]) -> None:
        self.__view = view

    @property
    def view(self) -> tuple[int, ...]:
        return self.__view

    @view.setter
    def view(self, view: tuple[int, ...]):
        self.__view = view

    @property
    def top(self) -> int:
        return self.__view[0]

    @property
    def bottom(self) -> int:
        return self.__view[1]

    @property
    def left(self) -> int:
        return self.__view[2]

    @property
    def right(self) -> int:
        return self.__view[3]
