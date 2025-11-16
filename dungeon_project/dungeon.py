from __future__ import annotations

import arcade
import random
from random import choice
from typing import List, TypeAlias, Literal
from collections.abc import Mapping


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
        return f"Position({self.__row}, {self.__column})"


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
        return f"Movement(row={self.__row}, column={self.__column})"


maze_1: List[str] = [
    '########################################',
    '# P                                    #',
    '#                                      #',
    '#                                      #',
    '#       ##########                     #',
    '#       #        #                     #',
    '#         M         #####              #',
    '#                        T             #',
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

Action: TypeAlias = Literal['UP', 'DOWN', 'LEFT', 'RIGHT']
ActionDelta: TypeAlias = tuple[int, int]
QValues: TypeAlias = dict[Action, float]
QTable: TypeAlias = dict[Position, QValues]

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

ACTION_UP: Action = 'UP'
ACTION_DOWN: Action = 'DOWN'
ACTION_LEFT: Action = 'LEFT'
ACTION_RIGHT: Action = 'RIGHT'

ACTIONS: dict[Action, ActionDelta] = {
    ACTION_UP: (-1, 0),
    ACTION_DOWN: (1, 0),
    ACTION_LEFT: (0, -1),
    ACTION_RIGHT: (0, 1),
}

TEXTURE_SIZE: int = 128
TILE_PIXEL_SIZE: int = 32

GLOBAL_SCALING: float = TILE_PIXEL_SIZE / TEXTURE_SIZE

CHARACTER_SCALING: float = GLOBAL_SCALING
TILE_SCALING: float = GLOBAL_SCALING
ITEM_SCALING: float = GLOBAL_SCALING
DOOR_SCALING: float = GLOBAL_SCALING

MAP_HEIGHT_TILES: int = len(maze_1)
MAP_WIDTH_TILES: int = len(maze_1[0])

SCREEN_WIDTH: int = MAP_WIDTH_TILES * TILE_PIXEL_SIZE
SCREEN_HEIGHT: int = MAP_HEIGHT_TILES * TILE_PIXEL_SIZE
SCREEN_TITLE: str = 'MINI DUNGEON'
PLAYER_MOVEMENT_SPEED: int = 30

print(
    f'=== DUNGEON {MAP_WIDTH_TILES}x{MAP_HEIGHT_TILES} '
    f'({SCREEN_WIDTH}x{SCREEN_HEIGHT}px) ==='
)


def choose_best_action(table: Mapping[Action, float]) -> Action:
    return max(table, key=lambda action: table[action])


class Agent:
    env: Environment
    qtable: QTable
    pos: Position
    has_key: bool
    score: int
    done: bool
    reward: int
    iterations: int

    def __init__(self, env: Environment) -> None:
        self.env = env
        self.qtable = {}
        self.reset()

    def reset(self) -> None:
        self.pos = self.env.start
        self.has_key = False
        self.score = 0
        self.done = False
        self.reward = 0
        self.iterations = 0

    def get_radar(self, pos: Position) -> dict[Action, str | None]:
        radar: dict[Action, str | None] = {}
        for direction, (dr, dc) in ACTIONS.items():
            check_pos: Position = Position(pos.get_row() + dr, pos.get_column() + dc)
            if check_pos in self.env.map:
                radar[direction] = self.env.map[check_pos]
            else:
                radar[direction] = None  # en dehors de la map
        return radar

    def do(
        self,
        action: Action,
        learning_rate: float = 1.0,
        discount_factor: float = 1.0,
    ) -> None:
        pos, reward = self.env.do(self.pos, action)

        if self.pos not in self.qtable:
            self.qtable[self.pos] = {
                ACTION_UP: 0.0,
                ACTION_DOWN: 0.0,
                ACTION_LEFT: 0.0,
                ACTION_RIGHT: 0.0,
            }
        if pos not in self.qtable:
            self.qtable[pos] = {
                ACTION_UP: 0.0,
                ACTION_DOWN: 0.0,
                ACTION_LEFT: 0.0,
                ACTION_RIGHT: 0.0,
            }

        delta: float = learning_rate * (
            reward
            + discount_factor * max(self.qtable[pos].values())
            - self.qtable[self.pos][action]
        )
        self.qtable[self.pos][action] += delta

        self.pos = pos
        self.reward = reward
        self.score += reward
        self.iterations += 1

    def best_action(self) -> Action:
        if self.pos in self.qtable:
            return choose_best_action(self.qtable[self.pos])
        return choice(list(ACTIONS.keys()))


class Environment:
    map: dict[Position, str]
    start: Position
    key: Position
    goal: Position
    width: int
    height: int

    def __init__(self, map_layout: list[str]) -> None:
        self.map = {}
        row: int
        col: int
        row, col = 0, 0

        for line in map_layout:
            for char in line:
                pos = Position(row, col)
                self.map[pos] = char
                if char == MAP_START:
                    self.start = pos
                elif char == MAP_KEY:
                    self.key = pos
                elif char == MAP_GOAL:
                    self.goal = pos

                col += 1
            self.width = col
            row += 1
            col = 0
        self.height = row

    def do(self, pos: Position, action: Action) -> tuple[Position, int]:
        move: ActionDelta = ACTIONS[action]
        new_pos = Position(pos.get_row() + move[0], pos.get_column() + move[1])

        reward: int
        if new_pos in self.map:
            if self.map[new_pos] == MAP_WALL:
                reward = REWARD_WALL
            else:
                pos = new_pos
                if self.map[new_pos] == MAP_KEY:
                    reward = REWARD_KEY
                elif self.map[new_pos] == MAP_GOAL:
                    reward = REWARD_GOAL
                else:
                    reward = REWARD_DEFAULT
        else:
            reward = REWARD_OUT

        return pos, reward


class MyGame(arcade.Window):
    agent: Agent
    wall_list: arcade.SpriteList[arcade.Sprite]
    player_list: arcade.SpriteList[arcade.Sprite]
    key_list: arcade.SpriteList[arcade.Sprite]
    door_list: arcade.SpriteList[arcade.Sprite]
    monster_list: arcade.SpriteList[arcade.Sprite]
    treasure_list: arcade.SpriteList[arcade.Sprite]
    player_sprite: arcade.Sprite
    physics_engine: arcade.PhysicsEngineSimple
    key_count: int
    key_text: arcade.Text
    player_move_timer: float

    def __init__(self, agent: Agent) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.agent = agent

        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.monster_list = arcade.SpriteList()
        self.treasure_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite(
            ':resources:images/tiles/boxCrate_double.png',
            TILE_SCALING,
        )
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            [],
        )
        self.key_count = 0
        self.key_text = arcade.Text(
            f'Clés : {self.key_count}',
            10,
            10,
            arcade.color.WHITE,
            18,
        )

        # Minuteur pour le mouvement aléatoire du joueur
        self.player_move_timer = 0.0

        arcade.set_background_color(arcade.color.DARK_BROWN)

    def setup(self) -> None:
        print('\n=== LEVEL LOADING... ===')
        self.key_count = 0
        self.key_text = arcade.Text(
            f'Keys: {self.key_count}',
            10,
            10,
            arcade.color.WHITE,
            18,
        )

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.monster_list = arcade.SpriteList()
        self.treasure_list = arcade.SpriteList()

        # Réinitialise le minuteur de mouvement
        self.player_move_timer = 0.0

        player_found: bool = False

        for row_index, row in enumerate(maze_1):
            for col_index, char in enumerate(row):
                x: float = (
                    col_index * TILE_PIXEL_SIZE + TILE_PIXEL_SIZE / 2
                )
                y: float = (
                    (MAP_HEIGHT_TILES - 1 - row_index) * TILE_PIXEL_SIZE
                    + TILE_PIXEL_SIZE / 2
                )

                if char == '#':
                    wall = arcade.Sprite(
                        ':resources:images/tiles/grassCenter.png',
                        TILE_SCALING,
                    )
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)

                elif char == 'P':
                    self.player_sprite = arcade.Sprite(
                        ':resources:images/animated_characters/'
                        'female_person/femalePerson_idle.png',
                        CHARACTER_SCALING,
                    )
                    self.player_sprite.center_x = x
                    self.player_sprite.center_y = y
                    self.player_list.append(self.player_sprite)
                    player_found = True
                    print(f'🎮 Joueur placé en ({x:.0f}, {y:.0f})')

                elif char == 'K':
                    key = arcade.Sprite(
                        ':resources:images/items/keyYellow.png',
                        ITEM_SCALING,
                    )
                    key.center_x = x
                    key.center_y = y
                    self.key_list.append(key)

                elif char == 'D':
                    door = arcade.Sprite(
                        ':resources:images/tiles/doorClosed_mid.png',
                        DOOR_SCALING,
                    )
                    door.center_x = x
                    door.center_y = y
                    self.door_list.append(door)

                elif char == 'M':
                    monster = arcade.Sprite(
                        ':resources:images/animated_characters/'
                        'zombie/zombie_idle.png',
                        CHARACTER_SCALING,
                    )
                    monster.center_x = x
                    monster.center_y = y
                    self.monster_list.append(monster)

                elif char == 'T':
                    treasure = arcade.Sprite(
                        ':resources:images/items/gemBlue.png',
                        ITEM_SCALING,
                    )
                    treasure.center_x = x
                    treasure.center_y = y
                    self.treasure_list.append(treasure)

        if not player_found:
            print(' ERROR: PLAYER NOT FOUND!')
            return

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            [self.wall_list, self.door_list],
        )

        print(
            f' {len(self.wall_list)} walls, {len(self.key_list)} keys, '
            f'{len(self.monster_list)} monsters, {len(self.door_list)} doors'
        )

    def on_draw(self) -> None:
        self.clear()
        self.wall_list.draw()
        self.door_list.draw()
        self.key_list.draw()
        self.monster_list.draw()
        self.treasure_list.draw()
        self.player_list.draw()
        self.key_text.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        pass

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        pass

    def on_update(self, delta_time: float) -> None:
        self.player_move_timer -= delta_time

        if self.player_move_timer <= 0:
            # Choisit une nouvelle durée aléatoire
            self.player_move_timer = random.uniform(0.1, 0.4)

            # Choisit une nouvelle direction aléatoire
            direction: Action = random.choice(
                ['UP', 'DOWN', 'LEFT', 'RIGHT']
            )  # type: ignore[assignment]

            if direction == 'UP':
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
                self.player_sprite.change_x = 0
            elif direction == 'DOWN':
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
                self.player_sprite.change_x = 0
            elif direction == 'LEFT':
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
                self.player_sprite.change_y = 0
            elif direction == 'RIGHT':
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
                self.player_sprite.change_y = 0

        self.physics_engine.update()

        # Ramasser les clés
        key_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite,
            self.key_list,
        )
        for key in key_hit_list:
            key.remove_from_sprite_lists()
            self.key_count += 1
            self.key_text.text = f'KEY: {self.key_count}'
            print(f'KEY COLLECTED! TOTAL: {self.key_count}')

        # Ouvrir les portes
        for door in self.door_list:
            distance: float = arcade.get_distance_between_sprites(
                self.player_sprite,
                door,
            )
            if distance < 47 and self.key_count > 0:
                door.remove_from_sprite_lists()
                self.key_count -= 1
                self.key_text.text = f'KEYS: {self.key_count}'
                print(
                    f'DOOR OPEN! KEYS REMAINING: {self.key_count}'
                )
                self.physics_engine = arcade.PhysicsEngineSimple(
                    self.player_sprite,
                    [self.wall_list, self.door_list],
                )
                break

        # Collision avec monstres
        monster_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite,
            self.monster_list,
        )
        if len(monster_hit_list) > 0:
            print('GAME OVER')
            self.setup()

        # Trésor = victoire
        treasure_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite,
            self.treasure_list,
        )
        if len(treasure_hit_list) > 0:
            print('VICTORY YOU HAVE FOUND THE TREASURE!')
            arcade.exit()


def main() -> None:
    env = Environment(maze_1)
    agent = Agent(env)

    window = MyGame(agent)
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
