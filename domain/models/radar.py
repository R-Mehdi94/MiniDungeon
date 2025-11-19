from domain.models.cell_content import CellContent


class Radar:
    __north: CellContent
    __north_east: CellContent
    __east: CellContent
    __south_east: CellContent
    __south: CellContent
    __south_west: CellContent
    __west: CellContent
    __north_west: CellContent

    def __init__(
        self,
        north: CellContent,
        north_east: CellContent,
        east: CellContent,
        south_east: CellContent,
        south: CellContent,
        south_west: CellContent,
        west: CellContent,
        north_west: CellContent,
    ) -> None:
        self.__north = north
        self.__north_east = north_east
        self.__east = east
        self.__south_east = south_east
        self.__south = south
        self.__south_west = south_west
        self.__west = west
        self.__north_west = north_west

    def get_north(self) -> CellContent:
        return self.__north

    def set_north(self, value: CellContent) -> None:
        self.__north = value

    def get_north_east(self) -> CellContent:
        return self.__north_east

    def set_north_east(self, value: CellContent) -> None:
        self.__north_east = value

    def get_east(self) -> CellContent:
        return self.__east

    def set_east(self, value: CellContent) -> None:
        self.__east = value

    def get_south_east(self) -> CellContent:
        return self.__south_east

    def set_south_east(self, value: CellContent) -> None:
        self.__south_east = value

    def get_south(self) -> CellContent:
        return self.__south

    def set_south(self, value: CellContent) -> None:
        self.__south = value

    def get_south_west(self) -> CellContent:
        return self.__south_west

    def set_south_west(self, value: CellContent) -> None:
        self.__south_west = value

    def get_west(self) -> CellContent:
        return self.__west

    def set_west(self, value: CellContent) -> None:
        self.__west = value

    def get_north_west(self) -> CellContent:
        return self.__north_west

    def set_north_west(self, value: CellContent) -> None:
        self.__north_west = value
