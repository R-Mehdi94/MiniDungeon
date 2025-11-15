from typing import Dict, List, Optional, Tuple
from domain.position import Position
from domain.state import State


class InMemoryDungeonEnv(EnvironmentPort):
    __grid: Dict[Tuple[int, int], Tile]
    __width: int
    __height: int
    __start: Position
    __door: Optional[Position]
    __treasure: Optional[Position]
    __key: Optional[Position]
    __monsters: List[Position]
    __player: Position
    __has_key: bool

    def __init__(self, level_text: str) -> None:
        self.__grid = {}
        self.__width = 0
        self.__height = 0
        self.__start = Position(0, 0)
        self.__door = None
        self.__treasure = None
        self.__key = None
        self.__monsters = []
        self.__player = Position(0, 0)
        self.__has_key = False
        self.__parse(level_text)

    def __parse(self, level_text: str) -> None:
        rows = [list(line.rstrip(""))
                for line in level_text.splitlines() if line.strip()]
        if len(rows) == 0:
            raise ValueError("Empty level")
        self.__height = len(rows)
        self.__width = max(len(r) for r in rows)
        for r, row in enumerate(rows):
            for c, ch in enumerate(row):
                tile = Tile(
                    ch) if ch in Tile._value2member_map_ else Tile.EMPTY
                self.__grid[(r, c)] = tile
                if tile is Tile.START:
                    self.__start = Position(r, c)
                elif tile is Tile.KEY:
                    self.__key = Position(r, c)
                elif tile is Tile.DOOR:
                    self.__door = Position(r, c)
                elif tile is Tile.TREASURE:
                    self.__treasure = Position(r, c)
                elif tile is Tile.MONSTER:
                    self.__monsters.append(Position(r, c))
        self.reset()

    def reset(self) -> State:
        self.__player = Position(
            self.__start.get_abscissa(),
            self.__start.get_ordinate()
        )
        self.__has_key = False
        return State(self.__player, self.__has_key)

    def __in_bounds(self, p: Position) -> bool:
        r, c = p.as_tuple()
        return 0 <= r < self.__height and 0 <= c < self.__width

    def __tile_at(self, p: Position) -> Tile:
        return self.__grid.get(p.as_tuple(), Tile.WALL)

    def __can_walk(self, p: Position) -> bool:
        t = self.__tile_at(p)
        return t is not Tile.WALL

    def __move_monsters(self) -> None:
        updated: List[Position] = []
        for m in self.__monsters:
            candidate = m.moved(*choice(list(Action)).delta())
            if self.__in_bounds(candidate) and self.__can_walk(candidate) and candidate != self.__door:
                updated.append(candidate)
            else:
                updated.append(m)
        self.__monsters = updated

    def step(self, state: State, action: Action) -> tuple[State, int, bool]:
        intended = state.get_player().moved(*action.delta())
        reward = Rewards.REWARD_DEFAULT
        done = False
        next_player = state.get_player()
        next_has_key = state.has_key()

        if not self.__in_bounds(intended):
            reward = Rewards.REWARD_OUT
        elif self.__tile_at(intended) is Tile.WALL:
            reward = Rewards.REWARD_WALL
        else:
            next_player = intended
            tile = self.__tile_at(intended)
            if tile is Tile.KEY and not next_has_key:
                next_has_key = True
                reward = Rewards.REWARD_KEY
            elif tile is Tile.DOOR:
                if next_has_key:
                    # ouvrir la porte
                    self.__grid[intended.as_tuple()] = Tile.EMPTY
                    next_has_key = False
                else:
                    reward = Rewards.REWARD_WALL
                    next_player = state.get_player()  # rester sur place
            elif tile is Tile.TREASURE:
                reward = Rewards.REWARD_GOAL
                done = True

        self.__move_monsters()

        for m in self.__monsters:
            if m == next_player:
                reward += Rewards.REWARD_MONSTER
                next_player = Position(
                    self.__start.get_abscissa(), self.__start.get_ordinate())
                next_has_key = False
                break

        new_state = State(next_player, next_has_key)
        self.__player = next_player
        self.__has_key = next_has_key
        return (new_state, reward, done)

    def get_width(self) -> int:
        return self.__width

    def get_height(self) -> int:
        return self.__height

    def get_grid(self) -> Dict[Tuple[int, int], Tile]:
        return dict(self.__grid)

    def get_monsters(self) -> List[Position]:
        return list(self.__monsters)

    def get_start(self) -> Position:
        return Position(self.__start.get_abscissa(), self.__start.get_ordinate())
