import arcade
from domain.agent import Agent
from domain.environment import Environment
from infrastructure.game import Game

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


TILE_PIXEL_SIZE = int(BASE_TILE_SIZE * TILE_SCALING)
MAP_HEIGHT_TILES = len(map_layout)
MAP_WIDTH_TILES = len(map_layout[0])
SCREEN_WIDTH = MAP_WIDTH_TILES * TILE_PIXEL_SIZE
SCREEN_HEIGHT = MAP_HEIGHT_TILES * TILE_PIXEL_SIZE
SCREEN_TITLE = "MINI DUNGEON"
PLAYER_MOVEMENT_SPEED = 5

print(
    f"=== Donjon {MAP_WIDTH_TILES}x{MAP_HEIGHT_TILES} ({SCREEN_WIDTH}x{SCREEN_HEIGHT}px) ==="
)


def arg_max(table):
    return max(table, key=table.get)


def main():
    env = Environment(map_layout)
    agent = Agent(env)
    window = Game(agent)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
