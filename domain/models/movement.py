class Movement:
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

    def as_tuple(self) -> tuple[int, int]:
        return (self.__row, self.__column)

    def __repr__(self) -> str:
        return f'Movement(row={self.__row}, column={self.__column})'
