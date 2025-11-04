import arcade
import random


map_layout = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                            W",
    "W  P                         W",
    "W                            W",
    "W                            W",
    "W     WWWWWWWWWWWWWWW        W",
    "W     W             W        W",
    "W     W             W        W",
    "W     W    WWWWW    W    M   W",
    "W     W    W   W    W        W",
    "W     W    W   W    W        W",
    "W     W    W T W    WWWWW    W",
    "W     WWWWWW   W    W        W",
    "W              W    W   M    W",
    "W      D       W    W        W",
    "W              W    WWWWW    W",
    "WWWWWWWWW      W             W",
    "W              W             W",
    "W  M           W             W",
    "W     WWWWWWWWWWWWWWW        W",
    "W     W              W       W",
    "W     W     M        W       W",
    "W     W              W M     W",
    "W     WWWWWWW        W       W",
    "W                    W   K   W",
    "W                    W       W",
    "W                            W",
    "W                        M   W",
    "W                            W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

# --- Constantes ---

CHARACTER_SCALING = 0.6
TILE_SCALING = 0.5
ITEM_SCALING = 0.5
DOOR_SCALING = 0.4
BASE_TILE_SIZE = 64
TILE_PIXEL_SIZE = int(BASE_TILE_SIZE * TILE_SCALING)
MAP_HEIGHT_TILES = len(map_layout)
MAP_WIDTH_TILES = len(map_layout[0])
SCREEN_WIDTH = MAP_WIDTH_TILES * TILE_PIXEL_SIZE
SCREEN_HEIGHT = MAP_HEIGHT_TILES * TILE_PIXEL_SIZE
SCREEN_TITLE = "MINI DUNGEON"
PLAYER_MOVEMENT_SPEED = 5

print(f"=== Donjon {MAP_WIDTH_TILES}x{MAP_HEIGHT_TILES} ({SCREEN_WIDTH}x{SCREEN_HEIGHT}px) ===")


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.wall_list = None
        self.player_list = None
        self.key_list = None
        self.door_list = None
        self.monster_list = None
        self.treasure_list = None
        self.player_sprite = None
        self.physics_engine = None
        self.key_count = 0
        self.key_text = None

        # Minuteur pour le mouvement aléatoire du joueur
        self.player_move_timer = 0.0

        arcade.set_background_color(arcade.color.DARK_BROWN)

    def setup(self):
        print("\n=== Chargement du niveau ===")
        self.key_count = 0
        self.key_text = arcade.Text(
            f"Clés : {self.key_count}",
            10, 10,
            arcade.color.WHITE, 18
        )

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.monster_list = arcade.SpriteList()
        self.treasure_list = arcade.SpriteList()

        # Réinitialise le minuteur de mouvement
        self.player_move_timer = 0.0

        player_found = False

        for row_index, row in enumerate(map_layout):
            for col_index, char in enumerate(row):
                x = col_index * TILE_PIXEL_SIZE + TILE_PIXEL_SIZE / 2
                y = (MAP_HEIGHT_TILES - 1 - row_index) * TILE_PIXEL_SIZE + TILE_PIXEL_SIZE / 2

                if char == "W":
                    wall = arcade.Sprite(":resources:images/tiles/grassCenter.png", TILE_SCALING)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)

                elif char == "P":
                    self.player_sprite = arcade.Sprite(
                        ":resources:images/animated_characters/female_person/femalePerson_idle.png",
                        CHARACTER_SCALING
                    )
                    self.player_sprite.center_x = x
                    self.player_sprite.center_y = y
                    self.player_list.append(self.player_sprite)
                    player_found = True
                    print(f"🎮 Joueur placé en ({x:.0f}, {y:.0f})")

                elif char == "K":
                    key = arcade.Sprite(":resources:images/items/keyYellow.png", ITEM_SCALING)
                    key.center_x = x
                    key.center_y = y
                    self.key_list.append(key)

                elif char == "D":
                    door = arcade.Sprite(":resources:images/tiles/doorClosed_mid.png", DOOR_SCALING)
                    door.center_x = x
                    door.center_y = y
                    self.door_list.append(door)

                elif char == "M":
                    monster = arcade.Sprite(
                        ":resources:images/animated_characters/zombie/zombie_idle.png",
                        CHARACTER_SCALING
                    )
                    monster.center_x = x
                    monster.center_y = y
                    self.monster_list.append(monster)

                elif char == "T":
                    treasure = arcade.Sprite(":resources:images/items/gemBlue.png", ITEM_SCALING)
                    treasure.center_x = x
                    treasure.center_y = y
                    self.treasure_list.append(treasure)

        if not player_found:
            print(" ERREUR: Joueur introuvable!")
            return

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            [self.wall_list, self.door_list]
        )

        print(f" {len(self.wall_list)} murs, {len(self.key_list)} clés, "
              f"{len(self.monster_list)} monstres, {len(self.door_list)} portes")

    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.door_list.draw()
        self.key_list.draw()
        self.monster_list.draw()
        self.treasure_list.draw()
        self.player_list.draw()
        self.key_text.draw()

    def on_key_press(self, key, modifiers):
        pass

    def on_key_release(self, key, modifiers):
        pass

    def on_update(self, delta_time):

        self.player_move_timer -= delta_time

        if self.player_move_timer <= 0:
            # Choisit une nouvelle durée aléatoire
            self.player_move_timer = random.uniform(0.1, 0.4)  # secondes

            # Choisit une nouvelle direction aléatoire
            direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

            if direction == "UP":
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
                self.player_sprite.change_x = 0
            elif direction == "DOWN":
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
                self.player_sprite.change_x = 0
            elif direction == "LEFT":
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
                self.player_sprite.change_y = 0
            elif direction == "RIGHT":
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
                self.player_sprite.change_y = 0

        self.physics_engine.update()

        # Ramasser les clés
        key_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.key_list)
        for key in key_hit_list:
            key.remove_from_sprite_lists()
            self.key_count += 1
            self.key_text.text = f"Clés : {self.key_count}"
            print(f" Clé ramassée! Total: {self.key_count}")

        # Ouvrir les portes
        for door in self.door_list:
            distance = arcade.get_distance_between_sprites(self.player_sprite, door)
            if distance < 47 and self.key_count > 0:
                door.remove_from_sprite_lists()
                self.key_count -= 1
                self.key_text.text = f"Clés : {self.key_count}"
                print(f" Porte ouverte! Clés restantes: {self.key_count}")
                self.physics_engine = arcade.PhysicsEngineSimple(
                    self.player_sprite,
                    [self.wall_list, self.door_list]
                )
                break

        # Collision avec monstres
        monster_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.monster_list)
        if len(monster_hit_list) > 0:
            print(" Game Over! Restart...")
            self.setup()  # Le joueur "réapparaît" au début

        # Trésor = victoire
        treasure_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.treasure_list)
        if len(treasure_hit_list) > 0:
            print(" VICTOIRE! Vous avez trouvé le trésor!")
            arcade.exit()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()