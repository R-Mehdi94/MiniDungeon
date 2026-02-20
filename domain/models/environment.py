from domain.models.action import Action
from domain.models.cell_content import CellContent
from domain.models.map_constants import *
from domain.models.position import Position
from domain.models.reward import Reward


class Environment:
    def __init__(self, map_layout: list[str]) -> None:
        self.__map = {}
        row: int
        self.__monster_positions = []
        col: int
        row, col = 0, 0
        self.__key = None
        self.__goal = None
        self.__door = None

        for line in map_layout:
            for char in line:
                pos = Position(row, col)

                if char == MAP_MONSTER:
                    self.__map[pos] = MAP_EMPTY
                else:
                    self.__map[pos] = char

                if char == MAP_START:
                    self.__starting_position = pos
                elif char == MAP_KEY:
                    self.__key = pos
                elif char == MAP_DOOR:
                    self.__door = pos
                elif char == MAP_GOAL:
                    self.__goal = pos

                col += 1
            self.__width = col
            row += 1
            col = 0
        self.__height = row

    def update_monster_positions(self, positions: list[Position]) -> None:
        self.__monster_positions = positions

    def get_cell_content(self, position: Position) -> CellContent:

        if position in self.__monster_positions:
            return CellContent.MONSTER

        char = self.__map.get(position)

        if char == MAP_WALL:
            return CellContent.WALL
        if char == MAP_KEY:
            return CellContent.KEY
        if char == MAP_GOAL:
            return CellContent.TREASURE
        if char == MAP_DOOR:
            return CellContent.DOOR
        return CellContent.EMPTY

    def do(self, pos: Position, action: Action, has_key: bool) -> tuple[Position, int]:

        movement = action.to_movement()
        new_pos = pos.calculate_next_position(movement)

        if new_pos not in self.__map:
            return pos, Reward.OUT_OF_MAP

        if new_pos in self.__monster_positions:
            return new_pos, Reward.MONSTER

        cell = self.__map[new_pos]

        if cell == MAP_WALL:
            return pos, Reward.WALL

        if cell == MAP_DOOR:
            if has_key:
                self.__map[new_pos] = MAP_EMPTY
                return new_pos, Reward.DOOR
            else:
                return pos, Reward.DOR_NO_KEY

        if cell == MAP_KEY:
            self.__map[new_pos] = MAP_EMPTY
            return new_pos, Reward.KEY

        if cell == MAP_GOAL:
            return new_pos, Reward.GOAL

        return new_pos, Reward.STEP

    # GETTER / SETTER

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
    def door(self) -> Position | None:
        return self.__door

    @door.setter
    def door(self, door: Position | None) -> None:
        self.__door = door

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
