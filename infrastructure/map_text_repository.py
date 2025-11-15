from typing import List


class MapTextRepository:
    __levels: List[str]
    __index: int

    def __init__(self, levels: List[str]) -> None:
        if len(levels) == 0:
            raise ValueError("At least one level required")
        self.__levels = levels
        self.__index = 0

    def current_level(self) -> str:
        return self.__levels[self.__index]

    def next_level(self) -> str:
        if self.__index + 1 < len(self.__levels):
            self.__index += 1
        return self.current_level()
