from domain.models.cell_content import CellContent


class Radar:
    view: list[list[CellContent]]

    def __init__(self, view: list[list[CellContent]]) -> None:
        self.__view = view

    @property
    def view(self) -> list[list[CellContent]]:
        return self.__view

    @view.setter
    def view(self, view: list[list[CellContent]]):
        self.__view = view


