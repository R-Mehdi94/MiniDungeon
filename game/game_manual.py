import random

import arcade

from environment.environment import Environment
from environment.position.action import Action
from environment.position.position import Position
from game.settings import (
    GLOBAL_SCALING,
    MAP_HEIGHT_TILES,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
    TILE_PIXEL_SIZE,
)
from game.monster.monster import Monster


class GameManual(arcade.Window):

    def __init__(self, env: Environment, maps: list[list[str]]) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.env = env
        self.map_height_tiles = None
        self.map_width_tiles = None
        self.level_completed = False
        self.maps = maps
        self.current_level_index = 0
        self.current_map = self.maps[self.current_level_index]
        self.victory = False

        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.monster_list = arcade.SpriteList()
        self.treasure_list = arcade.SpriteList()
        self.key_pos = None
        self.key_pos = None
        self.door_pos = None
        self.treasure_pos = None
        self.player_sprite = arcade.Sprite(
            ":resources:images/tiles/boxCrate_double.png",
            GLOBAL_SCALING,
        )
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            [],
        )

        # UI / score
        self.key_count = 0
        self.key_text = arcade.Text(
            f"Keys: {self.key_count}",
            10,
            10,
            arcade.color.WHITE,
            18,
        )

        self.action_count = 0

        self.player_move_timer = 0.0

        arcade.set_background_color(arcade.color.DARK_BROWN)

    @property
    def wall_list(self) -> arcade.SpriteList[arcade.Sprite]:
        return self.__wall_list

    @wall_list.setter
    def wall_list(self, wall_list: arcade.SpriteList[arcade.Sprite]) -> None:
        self.__wall_list = wall_list

    @property
    def player_list(self) -> arcade.SpriteList[arcade.Sprite]:
        return self.__player_list

    @player_list.setter
    def player_list(self, player_list: arcade.SpriteList[arcade.Sprite]) -> None:
        self.__player_list = player_list

    @property
    def key_list(self) -> arcade.SpriteList[arcade.Sprite]:
        return self.__key_list

    @key_list.setter
    def key_list(self, key_list: arcade.SpriteList[arcade.Sprite]) -> None:
        self.__key_list = key_list

    @property
    def door_list(self) -> arcade.SpriteList[arcade.Sprite]:
        return self.__door_list

    @door_list.setter
    def door_list(self, door_list: arcade.SpriteList[arcade.Sprite]) -> None:
        self.__door_list = door_list

    @property
    def monster_list(self) -> arcade.SpriteList[Monster]:
        return self.__monster_list

    @monster_list.setter
    def monster_list(self, monster_list: arcade.SpriteList[Monster]) -> None:
        self.__monster_list = monster_list

    @property
    def treasure_list(self) -> arcade.SpriteList[arcade.Sprite]:
        return self.__treasure_list

    @treasure_list.setter
    def treasure_list(self, treasure_list: arcade.SpriteList[arcade.Sprite]) -> None:
        self.__treasure_list = treasure_list

    @property
    def player_sprite(self) -> arcade.Sprite:
        return self.__player_sprite

    @player_sprite.setter
    def player_sprite(self, sprite: arcade.Sprite) -> None:
        self.__player_sprite = sprite

    @property
    def physics_engine(self) -> arcade.PhysicsEngineSimple:
        return self.__physics_engine

    @physics_engine.setter
    def physics_engine(self, engine: arcade.PhysicsEngineSimple) -> None:
        self.__physics_engine = engine

    @property
    def key_count(self) -> int:
        return self.__key_count

    @key_count.setter
    def key_count(self, count: int) -> None:
        self.__key_count = count

    @property
    def key_text(self) -> arcade.Text:
        return self.__key_text

    @key_text.setter
    def key_text(self, text: arcade.Text) -> None:
        self.__key_text = text

    @property
    def player_move_timer(self) -> float:
        return self.__player_move_timer

    @player_move_timer.setter
    def player_move_timer(self, value: float) -> None:
        self.__player_move_timer = value

    @property
    def maps(self) -> list[list[str]]:
        return self.__maps

    @maps.setter
    def maps(self, maps: list[list[str]]) -> None:
        self.__maps = maps

    @property
    def current_level_index(self) -> int:
        return self.__current_level_index

    @current_level_index.setter
    def current_level_index(self, index: int) -> None:
        self.__current_level_index = index

    @property
    def current_map(self) -> list[str]:
        return self.__current_map

    @current_map.setter
    def current_map(self, current_map: list[str]) -> None:
        self.__current_map = current_map

    @property
    def action_count(self) -> int:
        return self.__action_count

    @action_count.setter
    def action_count(self, count: int) -> None:
        self.__action_count = count







    @property
    def victory(self) -> bool:
        return self.__victory

    @victory.setter
    def victory(self, value: bool) -> None:
        self.__victory = value

    def draw_grid(self) -> None:
        width = self.map_width_tiles * TILE_PIXEL_SIZE
        height = self.map_height_tiles * TILE_PIXEL_SIZE

        for x in range(0, width + TILE_PIXEL_SIZE, TILE_PIXEL_SIZE):
            arcade.draw_line(x, 0, x, height, arcade.color.WHITE, 1)

        for y in range(0, height + TILE_PIXEL_SIZE, TILE_PIXEL_SIZE):
            arcade.draw_line(0, y, width, y, arcade.color.WHITE, 1)

    def setup(self) -> None:
        print("\n=== LEVEL LOADING ===")
        env = self.env

        self.key_count = 0
        self.key_text = arcade.Text(
            f"Clés: {self.key_count}",
            10,
            10,
            arcade.color.WHITE,
            18,
        )

        self.map_width_tiles = env.width
        self.map_height_tiles = env.height

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.monster_list = arcade.SpriteList()
        self.treasure_list = arcade.SpriteList()


        screen_width = self.map_width_tiles * TILE_PIXEL_SIZE
        screen_height = self.map_height_tiles * TILE_PIXEL_SIZE

        self.set_size(screen_width, screen_height)

        player_found: bool = False

        for row_index, row in enumerate(self.current_map):

            for col_index, char in enumerate(row):
                x: float = col_index * TILE_PIXEL_SIZE + TILE_PIXEL_SIZE / 2
                y = (
                        (self.map_height_tiles - 1 - row_index)
                        * TILE_PIXEL_SIZE
                        + TILE_PIXEL_SIZE / 2
                )

                if char == "#":
                    wall = arcade.Sprite(
                        ":resources:images/tiles/grassCenter.png",
                        GLOBAL_SCALING,
                    )
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)

                elif char == "P":
                    self.player_sprite = arcade.Sprite(
                        ":resources:/images/animated_characters/female_adventurer/femaleAdventurer_walk0.png",
                        GLOBAL_SCALING,
                    )
                    self.player_sprite.center_x = x
                    self.player_sprite.center_y = y
                    self.player_list.append(self.player_sprite)
                    start_pos = Position(row_index, col_index)
                    player_found = True
                    print(f"PLAYER STARTING POSITION: ({x:.0f}, {y:.0f})")

                elif char == "K":
                    key = arcade.Sprite(
                        ":resources:images/items/keyYellow.png",
                        GLOBAL_SCALING,
                    )
                    key.center_x = x
                    key.center_y = y
                    self.key_list.append(key)

                elif char == "D":
                    door = arcade.Sprite(
                        ":resources:images/tiles/doorClosed_mid.png",
                        GLOBAL_SCALING,
                    )
                    door.center_x = x
                    door.center_y = y

                    self.door_list.append(door)

                elif char == "M":
                    monster = Monster(
                        ":resources:images/animated_characters/"
                        "zombie/zombie_idle.png",
                        GLOBAL_SCALING,
                    )
                    monster.center_x = x
                    monster.center_y = y
                    self.monster_list.append(monster)

                elif char == "T":
                    treasure = arcade.Sprite(
                        ":resources:images/items/gemBlue.png",
                        GLOBAL_SCALING,
                    )
                    treasure.center_x = x
                    treasure.center_y = y
                    self.treasure_list.append(treasure)

        if not player_found:
            print(" ERROR: PLAYER NOT FOUND!")
            return

        else:
            print("DEBUG SETUP: No Door (D) on the map for the Agent to target.")

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            [self.wall_list, self.door_list],
        )

        print(
            f" {len(self.wall_list)} walls, {len(self.key_list)} keys, "
            f"{len(self.monster_list)} monsters, {len(self.door_list)} doors"
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
        self.draw_grid()


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.Z:
            self.player_sprite.change_y = 5
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -5
        elif key == arcade.key.LEFT or key == arcade.key.Q:
            self.player_sprite.change_x = -5
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 5
        if key == arcade.key.R:
            self.restart_game()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.Z:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.Q:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0


    def restart_game(self) -> None:
        self.current_level_index = 0
        self.reset_map()


        self.action_count = 0
        self.key_count = 0

        self.key_text.text = f"Keys: {self.key_count}"

        self.victory = False

        self.setup()

    def on_update(self, delta_time: float) -> None:
        if self.victory:
            return

        self.update_monsters(delta_time)

        current_monster_positions = []

        for monster in self.monster_list:
            col = int(monster.center_x // TILE_PIXEL_SIZE)
            row = self.map_height_tiles - 1 - int(monster.center_y // TILE_PIXEL_SIZE)
            # Avoir la position des monstres en temps réel
            if 0 <= row < MAP_HEIGHT_TILES:
                current_monster_positions.append(Position(row, col))


        self.player_move_timer -= delta_time

        if self.player_move_timer <= 0:
            self.player_move_timer = random.uniform(0.1, 0.1)

            self.action_count += 1

            key_hit_list = arcade.check_for_collision_with_list(
                self.player_sprite,
                self.key_list,
            )

            for key in key_hit_list:
                key.remove_from_sprite_lists()
                self.key_count += 1
                self.key_pos = None
                self.key_text.text = f"Keys: {self.key_count}"
                print(f"KEY COLLECTED! TOTAL: {self.key_count}")

            for door in self.door_list:
                distance = arcade.get_distance_between_sprites(self.player_sprite, door)
                if distance < 47 and self.key_count > 0:
                    self.key_count -= 1
                    self.door_pos = None
                    self.key_text.text = f"Keys: {self.key_count}"
                    door.remove_from_sprite_lists()
                    print("DOOR OPENED!")

                    if self.current_level_index != 2 :
                        self.level_completed = True

                else:
                    pass

        self.physics_engine.update()

        monster_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite,
            self.monster_list,
        )
        if len(monster_hit_list) > 0:
            self.restart_game()

        treasure_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite,
            self.treasure_list,
        )
        if len(treasure_hit_list) > 0:
            self.victory = True
            self.reset_map()
            #self.restart_game()

        if self.level_completed:
            self.level_completed = False
            self.go_to_next_level()

    def reset_map(self):
        self.current_map = self.maps[0]
        self.env = Environment(self.current_map)

    def update_monsters(self, delta_time: float) -> None:
        for monster in self.monster_list:
            monster.move_timer -= delta_time

            if monster.move_timer > 0:
                continue

            monster.move_timer = monster.time_between_moves

            dx: float = 0
            dy: float = 0
            direction: Action = monster.direction

            if direction is Action.LEFT:
                dx = -TILE_PIXEL_SIZE
            elif direction is Action.RIGHT:
                dx = TILE_PIXEL_SIZE
            elif direction is Action.UP:
                dy = TILE_PIXEL_SIZE
            elif direction is Action.DOWN:
                dy = -TILE_PIXEL_SIZE

            monster.center_x += dx
            monster.center_y += dy

            collided_with_wall = arcade.check_for_collision_with_list(
                monster,
                self.wall_list,
            )
            collided_with_door = arcade.check_for_collision_with_list(
                monster,
                self.door_list,
            )

            if collided_with_wall or collided_with_door:
                monster.center_x -= dx
                monster.center_y -= dy
                monster.reverse_direction()

    def go_to_next_level(self) -> None:
        self.current_level_index += 1

        if self.current_level_index >= len(self.maps):
            print(
                "NO MORE LEVELS, EXITING\n"
                f"ACTIONS: {self.action_count}"
            )
            arcade.exit()
            return

        self.current_map = self.maps[self.current_level_index]
        self.env = Environment(self.current_map)
        self.setup()
