from domain.models.action import Action
from domain.models.cell_content import CellContent
from domain.models.map_constants import MAP_GOAL, MAP_KEY, MAP_START, MAP_WALL
from domain.models.movement import Movement
from domain.models.position import Position
from domain.models.reward import Reward


class Environment:
    __map: dict[Position, str]
    __starting_position: Position
    __key: Position | None
    __goal: Position | None
    __width: int
    __height: int

    def __init__(self, map_layout: list[str]) -> None:
        self.__map = {}
        row: int
        col: int
        row, col = 0, 0
        self.__key = None
        self.__goal = None

        for line in map_layout:
            for char in line:
                pos = Position(row, col)
                self.__map[pos] = char
                if char == MAP_START:
                    self.__starting_position = pos
                elif char == MAP_KEY:
                    self.__key = pos
                elif char == MAP_GOAL:
                    self.__goal = pos

                col += 1
            self.__width = col
            row += 1
            col = 0
        self.__height = row

    @property
    def map(self) -> dict[Position, str]:
        return self.__map

    @map.setter
    def map(self, new_map: dict[Position, str]) -> None:
        self.__map = new_map

    @property
    def starting_position(self) -> Position:
        return self.__starting_position

    @starting_position.setter
    def starting_position(self, start: Position) -> None:
        self.__starting_position = start

    @property
    def key(self) -> Position | None:
        return self.__key

    @key.setter
    def key(self, key: Position | None) -> None:
        self.__key = key

    @property
    def goal(self) -> Position | None:
        return self.__goal

    @goal.setter
    def goal(self, goal: Position | None) -> None:
        self.__goal = goal

    @property
    def width(self) -> int:
        return self.__width

    @width.setter
    def width(self, width: int) -> None:
        self.__width = width

    @property
    def height(self) -> int:
        return self.__height

    @height.setter
    def height(self, height: int) -> None:
        self.__height = height

    def get_cell_content(self, position: Position) -> CellContent:
        char = self.__map.get(position)
        if char is None:
            return CellContent.OUT_OF_MAP
        if char == MAP_WALL:
            return CellContent.WALL
        if char == MAP_START:
            return CellContent.START
        if char == MAP_KEY:
            return CellContent.KEY
        if char == MAP_GOAL:
            return CellContent.TREASURE
        if char == 'D':
            return CellContent.DOOR
        if char == 'M':
            return CellContent.MONSTER
        return CellContent.EMPTY

    def do(self, pos: Position, action: Action) -> tuple[Position, int]:
        movement: Movement = action.to_movement()
        new_pos: Position = pos.calculate_next_position(movement)

        reward: int
        if new_pos in self.__map:
            cell: str = self.__map[new_pos]
            if cell == MAP_WALL:
                reward = Reward.WALL
            else:
                pos = new_pos
                if cell == MAP_KEY:
                    reward = Reward.KEY
                elif cell == MAP_GOAL:
                    reward = Reward.GOAL
                elif cell == 'M':
                    reward = Reward.MONSTER
                else:
                    reward = Reward.STEP
        else:
            reward = Reward.OUT_OF_MAP

        return pos, reward
