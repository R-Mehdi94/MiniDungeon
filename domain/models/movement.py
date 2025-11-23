class Movement:
    __row: int
    __column: int

    def __init__(self, row: int, column: int) -> None:
        self.__row = row
        self.__column = column

    @property
    def row(self) -> int:
        return self.__row

    @row.setter
    def row(self, row: int) -> None:
        self.__row = row

    @property
    def column(self) -> int:
        return self.__column

    @column.setter
    def column(self, column: int) -> None:
        self.__column = column

    def as_tuple(self) -> tuple[int, int]:
        return (self.__row, self.__column)

    def __repr__(self) -> str:
        return f'Movement(row={self.__row}, column={self.__column})'
