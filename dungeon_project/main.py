from __future__ import annotations

import arcade
import random
from random import choice
from typing import List
from enum import Enum


class MonsterAxis(Enum):
    HORIZONTAL = 'HORIZONTAL'
    VERTICAL = 'VERTICAL'


class Monster(arcade.Sprite):
    __axis: MonsterAxis
    __direction: Action

    def __init__(
        self,
        texture: str,
        scale: float,
        axis: MonsterAxis | None = None,
    ) -> None:
        super().__init__(texture, scale)

        if axis is None:
            axis = choice(list(MonsterAxis))
        self.__axis = axis

        if self.__axis is MonsterAxis.HORIZONTAL:
            self.__direction = choice([Action.LEFT, Action.RIGHT])
        else:
            self.__direction = choice([Action.UP, Action.DOWN])

    def get_axis(self) -> MonsterAxis:
        return self.__axis

    def set_axis(self, axis: MonsterAxis) -> None:
        self.__axis = axis

    def get_direction(self) -> Action:
        return self.__direction

    def set_direction(self, direction: Action) -> None:
        self.__direction = direction

    def reverse_direction(self) -> None:
        if self.__direction is Action.LEFT:
            self.__direction = Action.RIGHT
        elif self.__direction is Action.RIGHT:
            self.__direction = Action.LEFT
        elif self.__direction is Action.UP:
            self.__direction = Action.DOWN
        elif self.__direction is Action.DOWN:
            self.__direction = Action.UP


class Position:
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

    def calculate_next_position(self, movement: Movement) -> Position:
        return Position(
            self.__row + movement.get_row(),
            self.__column + movement.get_column()
        )

    def __hash__(self) -> int:
        return hash((self.__row, self.__column))

    def __repr__(self) -> str:
        return f'Position({self.__row}, {self.__column})'


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


class Action(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def to_movement(self) -> Movement:
        row_delta, col_delta = self.value
        return Movement(row_delta, col_delta)


class CardinalDirection(Enum):
    NORTH = 'NORTH'
    NORTH_EAST = 'NORTH EAST'
    EAST = 'EAST'
    SOUTH_EAST = 'SOUTH EAST'
    SOUTH = 'SOUTH'
    SOUTH_WEST = 'SOUTH WEST'
    WEST = 'WEST'
    NORTH_WEST = 'NORTH WEST'


class CellContent(Enum):
    WALL = '#'
    EMPTY = ' '
    START = 'P'
    KEY = 'K'
    DOOR = 'D'
    MONSTER = 'M'
    TREASURE = 'T'
    OUT_OF_MAP = None


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


maze_1: List[str] = [
    '########################################',
    '# P                                    #',
    '#                                      #',
    '#       ##########                     #',
    '#       #        #                     #',
    '#         M         #####              #',
    '#                                      #',
    '##########        D                    #',
    '#     M                       M        #',
    '#           #####   #                  #',
    '#                   ######             #',
    '#   M                         K        #',
    '#         #                            #',
    '#         ############                 #',
    '#         #                 M          #',
    '#         #                            #',
    '#         #                            #',
    '########################################',
]

maze_2: List[str] = [
    '########################################',
    '# P                         M          #',
    '#                                      #',
    '#       ##########                     #',
    '#       #        #                     #',
    '#             K     #####              #',
    '#                                      #',
    '##########                    D        #',
    '#     M                                #',
    '#           #####   #                  #',
    '#                   ######             #',
    '#                                M     #',
    '#         #                            #',
    '#         ############                 #',
    '#         #                            #',
    '#         #                            #',
    '#         #                            #',
    '########################################',
]

maze_3: List[str] = [
    '########################################',
    '# P                                    #',
    '#                                      #',
    '#       ##########                     #',
    '#       #        #                     #',
    '#         M         #####              #',
    '#                        T             #',
    '##########                             #',
    '#     M                                #',
    '#           #####   #                  #',
    '#                   ######             #',
    '#   M                                  #',
    '#         #                            #',
    '#         ############                 #',
    '#         #                 M          #',
    '#         #                            #',
    '#         #                            #',
    '########################################',
]


class QTable:
    __table: dict[Position, ActionsQualitiesForState]
    __initial_quality: float

    def __init__(self, initial_quality: float = 0.0) -> None:
        self.__table = {}
        self.__initial_quality = initial_quality

    def get_table(self) -> dict[Position, ActionsQualitiesForState]:
        return self.__table

    def set_table(self, table: dict[Position, ActionsQualitiesForState]) -> None:
        self.__table = table

    def get_initial_quality(self) -> float:
        return self.__initial_quality

    def set_initial_quality(self, value: float) -> None:
        self.__initial_quality = value

    def __get_or_create_state(self, position: Position) -> ActionsQualitiesForState:
        if position not in self.__table:
            self.__table[position] = ActionsQualitiesForState(self.__initial_quality)
        return self.__table[position]

    def get_quality(self, position: Position, action: Action) -> float:
        return self.__get_or_create_state(position).get(action)

    def set_quality(self, position: Position, action: Action, quality: float) -> None:
        self.__get_or_create_state(position).set(action, quality)

    def choose_best_action(self, position: Position) -> Action:
        return self.__get_or_create_state(position).choose_best_action()

    def get_state_qualities(self, position: Position) -> ActionsQualitiesForState:
        return self.__get_or_create_state(position)


class ActionsQualitiesForState:
    __qualities: dict[Action, float]

    def __init__(self, initial: float = 0.0) -> None:
        self.__qualities = {
            action: initial for action in Action
        }

    def get_qualities(self) -> dict[Action, float]:
        return self.__qualities

    def set_qualities(self, qualities: dict[Action, float]) -> None:
        self.__qualities = qualities

    def get(self, action: Action) -> float:
        return self.__qualities[action]

    def set(self, action: Action, quality: float) -> None:
        self.__qualities[action] = quality

    def choose_best_action(self) -> Action:
        return max(self.__qualities, key=lambda action: self.__qualities[action])


BASE_TILE_SIZE: int = 128
MAP_WALL: str = '#'
MAP_GOAL: str = 'T'
MAP_START: str = 'P'
MAP_KEY: str = 'K'

REWARD_WALL: int = -10
REWARD_DEFAULT: int = -1
REWARD_KEY: int = 10
REWARD_GOAL: int = 1000
REWARD_OUT: int = -10

TEXTURE_SIZE: int = 128
TILE_PIXEL_SIZE: int = 32

GLOBAL_SCALING: float = TILE_PIXEL_SIZE / TEXTURE_SIZE

MAP_HEIGHT_TILES: int = len(maze_1)
MAP_WIDTH_TILES: int = len(maze_1[0])

SCREEN_WIDTH: int = MAP_WIDTH_TILES * TILE_PIXEL_SIZE
SCREEN_HEIGHT: int = MAP_HEIGHT_TILES * TILE_PIXEL_SIZE
SCREEN_TITLE: str = 'MINI DUNGEON'
PLAYER_MOVEMENT_SPEED: int = 30
MONSTER_MOVEMENT_SPEED: int = 5

print(
    f'=== DUNGEON {MAP_WIDTH_TILES}x{MAP_HEIGHT_TILES} '
    f'({SCREEN_WIDTH}x{SCREEN_HEIGHT}px) ==='
)


class Agent:
    __env: Environment
    __qtable: QTable
    __pos: Position
    __has_key: bool
    __score: int
    __done: bool
    __reward: int
    __iterations: int

    def __init__(self, env: Environment) -> None:
        self.__env = env
        self.__qtable = QTable(initial_quality=0.0)
        self.reset()

    def get_env(self) -> Environment:
        return self.__env

    def set_env(self, env: Environment) -> None:
        self.__env = env

    def get_qtable(self) -> QTable:
        return self.__qtable

    def set_qtable(self, qtable: QTable) -> None:
        self.__qtable = qtable

    def get_pos(self) -> Position:
        return self.__pos

    def set_pos(self, pos: Position) -> None:
        self.__pos = pos

    def get_has_key(self) -> bool:
        return self.__has_key

    def set_has_key(self, has_key: bool) -> None:
        self.__has_key = has_key

    def get_score(self) -> int:
        return self.__score

    def set_score(self, score: int) -> None:
        self.__score = score

    def get_done(self) -> bool:
        return self.__done

    def set_done(self, done: bool) -> None:
        self.__done = done

    def get_reward(self) -> int:
        return self.__reward

    def set_reward(self, reward: int) -> None:
        self.__reward = reward

    def get_iterations(self) -> int:
        return self.__iterations

    def set_iterations(self, iterations: int) -> None:
        self.__iterations = iterations

    def reset(self) -> None:
        self.__pos = self.__env.get_start()
        self.__has_key = False
        self.__score = 0
        self.__done = False
        self.__reward = 0
        self.__iterations = 0

    def get_radar(self, pos: Position) -> dict[Action, str | None]:
        radar: dict[Action, str | None] = {}
        env_map = self.__env.get_map()
        for action in Action:
            movement: Movement = action.to_movement()
            check_pos: Position = pos.calculate_next_position(movement)
            if check_pos in env_map:
                radar[action] = env_map[check_pos]
            else:
                radar[action] = None
        return radar

    def do(
        self,
        action: Action,
        learning_rate: float = 1.0,
        discount_factor: float = 1.0,
    ) -> None:
        current_pos: Position = self.__pos

        next_pos, reward = self.__env.do(current_pos, action)

        old_quality: float = self.__qtable.get_quality(current_pos, action)

        best_next_action: Action = self.__qtable.choose_best_action(next_pos)
        max_next_quality: float = self.__qtable.get_quality(next_pos, best_next_action)

        updated_quality: float = old_quality + learning_rate * (
            reward + discount_factor * max_next_quality - old_quality
        )

        self.__qtable.set_quality(current_pos, action, updated_quality)

        self.__pos = next_pos
        self.__reward = reward
        self.__score += reward
        self.__iterations += 1

    def choose_best_action(self) -> Action:
        return self.__qtable.choose_best_action(self.__pos)


class Environment:
    __map: dict[Position, str]
    __start: Position
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
                    self.__start = pos
                elif char == MAP_KEY:
                    self.__key = pos
                elif char == MAP_GOAL:
                    self.__goal = pos

                col += 1
            self.__width = col
            row += 1
            col = 0
        self.__height = row

    def get_map(self) -> dict[Position, str]:
        return self.__map

    def set_map(self, new_map: dict[Position, str]) -> None:
        self.__map = new_map

    def get_start(self) -> Position:
        return self.__start

    def set_start(self, start: Position) -> None:
        self.__start = start

    def get_key(self) -> Position | None:
        return self.__key

    def set_key(self, key: Position | None) -> None:
        self.__key = key

    def get_goal(self) -> Position | None:
        return self.__goal

    def set_goal(self, goal: Position | None) -> None:
        self.__goal = goal

    def get_width(self) -> int:
        return self.__width

    def set_width(self, width: int) -> None:
        self.__width = width

    def get_height(self) -> int:
        return self.__height

    def set_height(self, height: int) -> None:
        self.__height = height

    def do(self, pos: Position, action: Action) -> tuple[Position, int]:
        movement: Movement = action.to_movement()
        new_pos: Position = pos.calculate_next_position(movement)

        reward: int
        if new_pos in self.__map:
            if self.__map[new_pos] == MAP_WALL:
                reward = REWARD_WALL
            else:
                pos = new_pos
                if self.__map[new_pos] == MAP_KEY:
                    reward = REWARD_KEY
                elif self.__map[new_pos] == MAP_GOAL:
                    reward = REWARD_GOAL
                else:
                    reward = REWARD_DEFAULT
        else:
            reward = REWARD_OUT

        return pos, reward


class Game(arcade.Window):
    __agent: Agent
    __wall_list: arcade.SpriteList[arcade.Sprite]
    __player_list: arcade.SpriteList[arcade.Sprite]
    __key_list: arcade.SpriteList[arcade.Sprite]
    __door_list: arcade.SpriteList[arcade.Sprite]
    __monster_list: arcade.SpriteList[Monster]
    __treasure_list: arcade.SpriteList[arcade.Sprite]
    __player_sprite: arcade.Sprite
    __physics_engine: arcade.PhysicsEngineSimple
    __key_count: int
    __key_text: arcade.Text
    __player_move_timer: float

    __maps: list[list[str]]
    __current_level_index: int
    __current_map: list[str]

    def __init__(self, agent: Agent) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.__agent = agent

        self.__maps = [maze_1, maze_2, maze_3]
        self.__current_level_index = 0
        self.__current_map = self.__maps[self.__current_level_index]

        self.__wall_list = arcade.SpriteList()
        self.__player_list = arcade.SpriteList()
        self.__key_list = arcade.SpriteList()
        self.__door_list = arcade.SpriteList()
        self.__monster_list = arcade.SpriteList()
        self.__treasure_list = arcade.SpriteList()

        self.__player_sprite = arcade.Sprite(
            ':resources:images/tiles/boxCrate_double.png',
            GLOBAL_SCALING,
        )
        self.__physics_engine = arcade.PhysicsEngineSimple(
            self.__player_sprite,
            [],
        )
        self.__key_count = 0
        self.__key_text = arcade.Text(
            f'Clés : {self.__key_count}',
            10,
            10,
            arcade.color.WHITE,
            18,
        )

        self.__player_move_timer = 0.0

        arcade.set_background_color(arcade.color.DARK_BROWN)

    def get_agent(self) -> Agent:
        return self.__agent

    def set_agent(self, agent: Agent) -> None:
        self.__agent = agent

    def get_wall_list(self) -> arcade.SpriteList[arcade.Sprite]:
        return self.__wall_list

    def set_wall_list(self, wall_list: arcade.SpriteList[arcade.Sprite]) -> None:
        self.__wall_list = wall_list

    def get_player_list(self) -> arcade.SpriteList[arcade.Sprite]:
        return self.__player_list

    def set_player_list(self, player_list: arcade.SpriteList[arcade.Sprite]) -> None:
        self.__player_list = player_list

    def get_key_list(self) -> arcade.SpriteList[arcade.Sprite]:
        return self.__key_list

    def set_key_list(self, key_list: arcade.SpriteList[arcade.Sprite]) -> None:
        self.__key_list = key_list

    def get_door_list(self) -> arcade.SpriteList[arcade.Sprite]:
        return self.__door_list

    def set_door_list(self, door_list: arcade.SpriteList[arcade.Sprite]) -> None:
        self.__door_list = door_list

    def get_monster_list(self) -> arcade.SpriteList[Monster]:
        return self.__monster_list

    def set_monster_list(self, monster_list: arcade.SpriteList[Monster]) -> None:
        self.__monster_list = monster_list

    def get_treasure_list(self) -> arcade.SpriteList[arcade.Sprite]:
        return self.__treasure_list

    def set_treasure_list(self, treasure_list: arcade.SpriteList[arcade.Sprite]) -> None:
        self.__treasure_list = treasure_list

    def get_player_sprite(self) -> arcade.Sprite:
        return self.__player_sprite

    def set_player_sprite(self, sprite: arcade.Sprite) -> None:
        self.__player_sprite = sprite

    def get_physics_engine(self) -> arcade.PhysicsEngineSimple:
        return self.__physics_engine

    def set_physics_engine(self, engine: arcade.PhysicsEngineSimple) -> None:
        self.__physics_engine = engine

    def get_key_count(self) -> int:
        return self.__key_count

    def set_key_count(self, count: int) -> None:
        self.__key_count = count

    def get_key_text(self) -> arcade.Text:
        return self.__key_text

    def set_key_text(self, text: arcade.Text) -> None:
        self.__key_text = text

    def get_player_move_timer(self) -> float:
        return self.__player_move_timer

    def set_player_move_timer(self, value: float) -> None:
        self.__player_move_timer = value

    def get_maps(self) -> list[list[str]]:
        return self.__maps

    def set_maps(self, maps: list[list[str]]) -> None:
        self.__maps = maps

    def get_current_level_index(self) -> int:
        return self.__current_level_index

    def set_current_level_index(self, index: int) -> None:
        self.__current_level_index = index

    def get_current_map(self) -> list[str]:
        return self.__current_map

    def set_current_map(self, current_map: list[str]) -> None:
        self.__current_map = current_map

    def setup(self) -> None:
        print('\n=== LEVEL LOADING ===')
        self.__key_count = 0
        self.__key_text = arcade.Text(
            f'Keys: {self.__key_count}',
            10,
            10,
            arcade.color.WHITE,
            18,
        )

        self.__player_list = arcade.SpriteList()
        self.__wall_list = arcade.SpriteList()
        self.__key_list = arcade.SpriteList()
        self.__door_list = arcade.SpriteList()
        self.__monster_list = arcade.SpriteList()
        self.__treasure_list = arcade.SpriteList()

        self.__player_move_timer = 0.0

        player_found: bool = False

        for row_index, row in enumerate(self.__current_map):
            for col_index, char in enumerate(row):
                x: float = (col_index * TILE_PIXEL_SIZE + TILE_PIXEL_SIZE / 2)
                y: float = (
                    (MAP_HEIGHT_TILES - 1 - row_index) * TILE_PIXEL_SIZE
                    + TILE_PIXEL_SIZE / 2
                )

                if char == '#':
                    wall = arcade.Sprite(
                        ':resources:images/tiles/grassCenter.png',
                        GLOBAL_SCALING,
                    )
                    wall.center_x = x
                    wall.center_y = y
                    self.__wall_list.append(wall)

                elif char == 'P':
                    self.__player_sprite = arcade.Sprite(
                        ':resources:images/animated_characters/'
                        'female_person/femalePerson_idle.png',
                        GLOBAL_SCALING,
                    )
                    self.__player_sprite.center_x = x
                    self.__player_sprite.center_y = y
                    self.__player_list.append(self.__player_sprite)
                    player_found = True
                    print(f'PLAYER STARTING POSITION: ({x:.0f}, {y:.0f})')

                elif char == 'K':
                    key = arcade.Sprite(
                        ':resources:images/items/keyYellow.png',
                        GLOBAL_SCALING,
                    )
                    key.center_x = x
                    key.center_y = y
                    self.__key_list.append(key)

                elif char == 'D':
                    door = arcade.Sprite(
                        ':resources:images/tiles/doorClosed_mid.png',
                        GLOBAL_SCALING,
                    )
                    door.center_x = x
                    door.center_y = y
                    self.__door_list.append(door)

                elif char == 'M':
                    monster = Monster(
                        ':resources:images/animated_characters/'
                        'zombie/zombie_idle.png',
                        GLOBAL_SCALING,
                    )
                    monster.center_x = x
                    monster.center_y = y
                    self.__monster_list.append(monster)

                elif char == 'T':
                    treasure = arcade.Sprite(
                        ':resources:images/items/gemBlue.png',
                        GLOBAL_SCALING,
                    )
                    treasure.center_x = x
                    treasure.center_y = y
                    self.__treasure_list.append(treasure)

        if not player_found:
            print(' ERROR: PLAYER NOT FOUND!')
            return

        self.__physics_engine = arcade.PhysicsEngineSimple(
            self.__player_sprite,
            [self.__wall_list, self.__door_list],
        )

        print(
            f' {len(self.__wall_list)} walls, {len(self.__key_list)} keys, '
            f'{len(self.__monster_list)} monsters, {len(self.__door_list)} doors'
        )

    def on_draw(self) -> None:
        self.clear()
        self.__wall_list.draw()
        self.__door_list.draw()
        self.__key_list.draw()
        self.__monster_list.draw()
        self.__treasure_list.draw()
        self.__player_list.draw()
        self.__key_text.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        pass

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        pass

    def on_update(self, delta_time: float) -> None:
        self.__player_move_timer -= delta_time

        if self.__player_move_timer <= 0:
            self.__player_move_timer = random.uniform(0.1, 0.4)

            direction: Action = choice(list(Action))

            if direction is Action.UP:
                self.__player_sprite.change_y = PLAYER_MOVEMENT_SPEED
                self.__player_sprite.change_x = 0
            elif direction is Action.DOWN:
                self.__player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
                self.__player_sprite.change_x = 0
            elif direction is Action.LEFT:
                self.__player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
                self.__player_sprite.change_y = 0
            elif direction is Action.RIGHT:
                self.__player_sprite.change_x = PLAYER_MOVEMENT_SPEED
                self.__player_sprite.change_y = 0

        self.__physics_engine.update()
        self.update_monsters()

        key_hit_list = arcade.check_for_collision_with_list(
            self.__player_sprite,
            self.__key_list,
        )
        for key in key_hit_list:
            key.remove_from_sprite_lists()
            self.__key_count += 1
            self.__key_text.text = f'KEY: {self.__key_count}'
            print(f'KEY COLLECTED! TOTAL: {self.__key_count}')

        for door in self.__door_list:
            distance: float = arcade.get_distance_between_sprites(
                self.__player_sprite,
                door,
            )
            if distance < 47 and self.__key_count > 0:
                print('DOOR REACHED WITH A KEY -> NEXT LEVEL')
                self.__key_count -= 1
                self.go_to_next_level()
                return

        monster_hit_list = arcade.check_for_collision_with_list(
            self.__player_sprite,
            self.__monster_list,
        )
        if len(monster_hit_list) > 0:
            print('GAME OVER')
            self.setup()

        treasure_hit_list = arcade.check_for_collision_with_list(
            self.__player_sprite,
            self.__treasure_list,
        )
        if len(treasure_hit_list) > 0:
            print('VICTORY YOU HAVE FOUND THE TREASURE!')
            arcade.exit()

    def update_monsters(self) -> None:
        for monster in self.__monster_list:
            dx: float = 0.0
            dy: float = 0.0
            direction: Action = monster.get_direction()

            if direction is Action.LEFT:
                dx = -MONSTER_MOVEMENT_SPEED
            elif direction is Action.RIGHT:
                dx = MONSTER_MOVEMENT_SPEED
            elif direction is Action.UP:
                dy = MONSTER_MOVEMENT_SPEED
            elif direction is Action.DOWN:
                dy = -MONSTER_MOVEMENT_SPEED

            monster.center_x += dx
            monster.center_y += dy

            collided_with_wall = arcade.check_for_collision_with_list(
                monster,
                self.__wall_list,
            )
            collided_with_door = arcade.check_for_collision_with_list(
                monster,
                self.__door_list,
            )

            if collided_with_wall or collided_with_door:
                monster.center_x -= dx
                monster.center_y -= dy
                monster.reverse_direction()

    def go_to_next_level(self) -> None:
        self.__current_level_index += 1

        if self.__current_level_index >= len(self.__maps):
            print('NO MORE LEVELS, EXITING')
            arcade.exit()
            return

        self.__current_map = self.__maps[self.__current_level_index]

        new_env = Environment(self.__current_map)
        self.__agent.set_env(new_env)
        self.__agent.reset()

        self.setup()


def main() -> None:
    env = Environment(maze_1)
    agent = Agent(env)

    window = Game(agent)
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
