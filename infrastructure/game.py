import random
import arcade
from domain.models.action import Action
from domain.models.environment import Environment
from domain.models.reward import Reward
from infrastructure.agent import Agent
from infrastructure.arcade.settings import GLOBAL_SCALING, MAP_HEIGHT_TILES, MONSTER_MOVEMENT_SPEED, PLAYER_MOVEMENT_SPEED, SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH, TILE_PIXEL_SIZE
from infrastructure.data.map_1 import MAP_1
from infrastructure.data.map_2 import MAP_2
from infrastructure.data.map_3 import MAP_3
from infrastructure.monster import Monster
from random import choice


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

    __score: int
    __score_text: arcade.Text
    __action_count: int
    __actions_text: arcade.Text

    __maps: list[list[str]]
    __current_level_index: int
    __current_map: list[str]
    __victory: bool

    def __init__(self, agent: Agent) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.__agent = agent
        self.__victory = False
        self.__maps = [MAP_1, MAP_2, MAP_3]
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
            f'Keys: {self.__key_count}',
            10,
            10,
            arcade.color.WHITE,
            18,
        )

        self.__score = 0
        self.__action_count = 0
        self.__score_text = arcade.Text(
            f'Score: {self.__score}',
            10,
            40,
            arcade.color.WHITE,
            18,
        )
        self.__actions_text = arcade.Text(
            f'Actions: {self.__action_count}',
            10,
            70,
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

    def get_score(self) -> int:
        return self.__score

    def set_score(self, score: int) -> None:
        self.__score = score

    def get_action_count(self) -> int:
        return self.__action_count

    def set_action_count(self, count: int) -> None:
        self.__action_count = count

    def get_score_text(self) -> arcade.Text:
        return self.__score_text

    def set_score_text(self, text: arcade.Text) -> None:
        self.__score_text = text

    def get_actions_text(self) -> arcade.Text:
        return self.__actions_text

    def set_actions_text(self, text: arcade.Text) -> None:
        self.__actions_text = text

    def setup(self) -> None:
        print('\n=== LEVEL LOADING ===')
        self.__key_count = 0
        self.__key_text = arcade.Text(
            f'Clés: {self.__key_count}',
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
        self.__score_text.draw()
        self.__actions_text.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.R:
            self.restart_game()

    def restart_game(self) -> None:
        self.__current_level_index = 0
        self.__current_map = self.__maps[0]

        new_env = Environment(self.__current_map)
        self.__agent.set_env(new_env)
        self.__agent.reset()

        self.__score = 0
        self.__action_count = 0
        self.__key_count = 0
        self.__score_text.text = f'Score: {self.__score}'
        self.__actions_text.text = f'Actions: {self.__action_count}'
        self.__key_text.text = f'Keys: {self.__key_count}'

        self.__victory = False

        self.setup()

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        pass

    def on_update(self, delta_time: float) -> None:
        if self.__victory:
            return
        self.__player_move_timer -= delta_time

        if self.__player_move_timer <= 0:
            self.__player_move_timer = random.uniform(0.1, 0.4)

            direction: Action = choice(list(Action))

            self.__action_count += 1
            self.__score += Reward.STEP
            self.__score_text.text = f'Score: {self.__score}'
            self.__actions_text.text = f'Actions: {self.__action_count}'

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
            self.__score += Reward.KEY
            self.__key_text.text = f'Keys: {self.__key_count}'
            self.__score_text.text = f'Score: {self.__score}'
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
            self.__score += Reward.MONSTER
            self.__score_text.text = f'Score: {self.__score}'
            print(
                f'GAME OVER - SCORE: {self.__score} - '
                f'ACTIONS: {self.__action_count}'
            )
            self.setup()

        treasure_hit_list = arcade.check_for_collision_with_list(
            self.__player_sprite,
            self.__treasure_list,
        )
        if len(treasure_hit_list) > 0:
            self.__score += Reward.GOAL
            self.__score_text.text = f'Score: {self.__score}'
            print(
                'VICTORY YOU HAVE FOUND THE TREASURE!\n'
                f'FINAL SCORE: {self.__score} - '
                f'ACTIONS: {self.__action_count}\n'
                'PRESS R TO RESTART'
            )
            self.__victory = True
            return

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
            print(
                'NO MORE LEVELS, EXITING\n'
                f'FINAL SCORE: {self.__score} - '
                f'ACTIONS: {self.__action_count}'
            )
            arcade.exit()
            return

        self.__current_map = self.__maps[self.__current_level_index]

        new_env = Environment(self.__current_map)
        self.__agent.set_env(new_env)
        self.__agent.reset()

        self.setup()
