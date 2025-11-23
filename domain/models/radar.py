from domain.models.cell_content import CellContent


class Radar:
    __north_content: CellContent
    __north_east_content: CellContent
    __east_content: CellContent
    __south_east_content: CellContent
    __south_content: CellContent
    __south_west_content: CellContent
    __west_content: CellContent
    __north_west_content: CellContent

    def __init__(
        self,
        north_content: CellContent,
        north_east_content: CellContent,
        east_content: CellContent,
        south_east_content: CellContent,
        south_content: CellContent,
        south_west_content: CellContent,
        west_content: CellContent,
        north_west_content: CellContent,
    ) -> None:
        self.__north_content = north_content
        self.__north_east_content = north_east_content
        self.__east_content = east_content
        self.__south_east_content = south_east_content
        self.__south_content = south_content
        self.__south_west_content = south_west_content
        self.__west_content = west_content
        self.__north_west_content = north_west_content

    @property
    def north_content(self) -> CellContent:
        return self.__north_content

    @north_content.setter
    def north_content(self, value: CellContent) -> None:
        self.__north_content = value

    @property
    def north_east_content(self) -> CellContent:
        return self.__north_east_content

    @north_east_content.setter
    def north_east_content(self, value: CellContent) -> None:
        self.__north_east_content = value

    @property
    def east_content(self) -> CellContent:
        return self.__east_content

    @east_content.setter
    def east_content(self, value: CellContent) -> None:
        self.__east_content = value

    @property
    def south_east_content(self) -> CellContent:
        return self.__south_east_content

    @south_east_content.setter
    def south_east_content(self, value: CellContent) -> None:
        self.__south_east_content = value

    @property
    def south_content(self) -> CellContent:
        return self.__south_content

    @south_content.setter
    def south_content(self, value: CellContent) -> None:
        self.__south_content = value

    @property
    def south_west_content(self) -> CellContent:
        return self.__south_west_content

    @south_west_content.setter
    def south_west_content(self, value: CellContent) -> None:
        self.__south_west_content = value

    @property
    def west_content(self) -> CellContent:
        return self.__west_content

    @west_content.setter
    def west_content(self, value: CellContent) -> None:
        self.__west_content = value

    @property
    def north_west_content(self) -> CellContent:
        return self.__north_west_content

    @north_west_content.setter
    def north_west_content(self, value: CellContent) -> None:
        self.__north_west_content = value
