import random
from random import choice

import arcade

from domain.models.action import Action
from domain.models.environment import Environment
from domain.models.reward import Reward
from infrastructure.agent import Agent
from infrastructure.arcade.settings import (
    GLOBAL_SCALING,
    MAP_HEIGHT_TILES,
    MONSTER_MOVEMENT_SPEED,
    PLAYER_MOVEMENT_SPEED,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
    TILE_PIXEL_SIZE,
)
from infrastructure.monster import Monster


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

    __score_text: arcade.Text
    __action_count: int
    __actions_text: arcade.Text
    __exploration_text: arcade.Text
    __qtable_text: arcade.SpriteList[arcade.Sprite]

    __maps: list[list[str]]
    __current_level_index: int
    __current_map: list[str]
    __victory: bool

    def __init__(self, agent: Agent, maps: list[list[str]]) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.agent = agent
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
        self.score_text = arcade.Text(
            f"Score: {self.agent.score}",
            10,
            40,
            arcade.color.WHITE,
            18,
        )
        self.actions_text = arcade.Text(
            f"Actions: {self.action_count}",
            10,
            70,
            arcade.color.WHITE,
            18,
        )

        self.exploration_text = arcade.Text(
            f"Exploration: {self.agent.exploration}",
            10,
            100,
            arcade.color.WHITE,
            18,
        )

        self.qtable_text = arcade.Text(
            f"Q-Table Size: 0",
            10,
            130,  # Position Y (au-dessus de Exploration qui est à 100)
            arcade.color.WHITE,
            18,
        )
        self.player_move_timer = 0.0

        arcade.set_background_color(arcade.color.DARK_BROWN)

    @property
    def agent(self) -> Agent:
        return self.__agent

    @agent.setter
    def agent(self, agent: Agent) -> None:
        self.__agent = agent

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
    def score_text(self) -> arcade.Text:
        return self.__score_text

    @score_text.setter
    def score_text(self, text: arcade.Text) -> None:
        self.__score_text = text

    @property
    def actions_text(self) -> arcade.Text:
        return self.__actions_text

    @actions_text.setter
    def actions_text(self, text: arcade.Text) -> None:
        self.__actions_text = text

    @property
    def exploration_text(self) -> arcade.Text:
        return self.__exploration_text

    @exploration_text.setter
    def exploration_text(self, text: arcade.Text) -> None:
        self.__exploration_text = text

    @property
    def victory(self) -> bool:
        return self.__victory

    @victory.setter
    def victory(self, value: bool) -> None:
        self.__victory = value



    @property
    def qtable_text(self) -> arcade.Text:
        return self.__qtable_text

    @qtable_text.setter
    def qtable_text(self, text: arcade.Text) -> None:
        self.__qtable_text = text

    def setup(self) -> None:
        print("\n=== LEVEL LOADING ===")
        self.key_count = 0
        self.key_text = arcade.Text(
            f"Clés: {self.key_count}",
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

        self.player_move_timer = 0.0

        player_found: bool = False

        for row_index, row in enumerate(self.current_map):
            for col_index, char in enumerate(row):
                x: float = col_index * TILE_PIXEL_SIZE + TILE_PIXEL_SIZE / 2
                y: float = (
                    (MAP_HEIGHT_TILES - 1 - row_index) * TILE_PIXEL_SIZE
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
                        ":resources:images/animated_characters/"
                        "female_person/femalePerson_idle.png",
                        GLOBAL_SCALING,
                    )
                    self.player_sprite.center_x = x
                    self.player_sprite.center_y = y
                    self.player_list.append(self.player_sprite)
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
        self.score_text.draw()
        self.actions_text.draw()
        self.exploration_text.draw()
        self.qtable_text.draw()
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.R:
            self.restart_game()
        if symbol == arcade.key.E:
            self.agent.exploration += 0.2



    def restart_game(self) -> None:
        self.current_level_index = 0
        self.current_map = self.maps[0]

        new_env = Environment(self.current_map)
        self.agent.environment = new_env
        self.agent.reset()

        self.action_count = 0
        self.key_count = 0
        self.score_text.text = f"Score: {self.agent.score}"
        self.actions_text.text = f"Actions: {self.action_count}"
        self.key_text.text = f"Keys: {self.key_count}"
        self.exploration_text = f"Exploration: {self.agent.exploration}"
        #self.qtable_text = f"Qtable:  {self.agent.q_table.}"

        self.victory = False

        self.setup()

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        pass

    def on_update(self, delta_time: float) -> None:
        if self.victory:
            return

        self.player_move_timer -= delta_time

        if self.player_move_timer <= 0:
            self.player_move_timer = random.uniform(0.0, 0.01)

            direction: Action = self.agent.choose_action_from_knowledge_or_random()

            self.agent.execute_action_and_learn_from_reward(direction)

            self.action_count += 1
            self.agent.score += Reward.STEP
            self.score_text.text = f"Score: {self.agent.score}"
            self.actions_text.text = f"Actions: {self.action_count}"
            self.exploration_text.text = f"Exploration: {self.agent.exploration:.2f}"
            q_table_size = len(self.agent.q_table.table)
            self.qtable_text.text = f"States: {q_table_size}"

            if direction is Action.UP:
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
                self.player_sprite.change_x = 0
            elif direction is Action.DOWN:
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
                self.player_sprite.change_x = 0
            elif direction is Action.LEFT:
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
                self.player_sprite.change_y = 0
            elif direction is Action.RIGHT:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
                self.player_sprite.change_y = 0

        self.physics_engine.update()
        self.update_monsters()

        key_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite,
            self.key_list,
        )
        for key in key_hit_list:
            key.remove_from_sprite_lists()
            self.key_count += 1
            self.agent.score += Reward.KEY
            self.key_text.text = f"Keys: {self.key_count}"
            self.score_text.text = f"Score: {self.agent.score}"
            print(f"KEY COLLECTED! TOTAL: {self.key_count}")

        for door in self.door_list:

            distance = arcade.get_distance_between_sprites(self.player_sprite, door)
            if distance < 47:
                if self.key_count > 0:
                    print("DOOR REACHED WITH A KEY -> NEXT LEVEL")
                    self.key_count -= 1
                    self.agent.score += Reward.DOOR
                    self.go_to_next_level()
                    return
                else:
                    self.agent.score += Reward.DOR_NO_KEY
        monster_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite,
            self.monster_list,
        )
        if len(monster_hit_list) > 0:
            self.agent.score += Reward.MONSTER
            self.score_text.text = f"Score: {self.agent.score}"
            print(
                f"GAME OVER - SCORE: {self.agent.score} - "
                f"ACTIONS: {self.action_count}"
            )
            self.setup()

        treasure_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite,
            self.treasure_list,
        )
        if len(treasure_hit_list) > 0:
            self.agent.score += Reward.GOAL
            self.score_text.text = f"Score: {self.agent.score}"
            print(
                "VICTORY YOU HAVE FOUND THE TREASURE!\n"
                f"FINAL SCORE: {self.agent.score} - "
                f"ACTIONS: {self.action_count}\n"
                "PRESS R TO RESTART"
            )
            self.victory = True
            return

    def update_monsters(self) -> None:
        for monster in self.monster_list:
            dx: float = 0.0
            dy: float = 0.0
            direction: Action = monster.direction

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
                f"FINAL SCORE: {self.agent.score} - "
                f"ACTIONS: {self.action_count}"
            )
            arcade.exit()
            return

        self.current_map = self.maps[self.current_level_index]

        new_env = Environment(self.current_map)
        self.agent.environment = new_env
        self.agent.reset()

        self.setup()
