from __future__ import annotations
import arcade
from application.train_agent_on_3_maps_use_case import train_agent_on_3_maps_use_case
from domain.models.environment import Environment
from infrastructure.agent import Agent
from infrastructure.arcade.settings import MAP_HEIGHT_TILES, MAP_WIDTH_TILES, SCREEN_HEIGHT, SCREEN_WIDTH
from infrastructure.data.map_1 import MAP_1
from infrastructure.data.map_2 import MAP_2
from infrastructure.data.map_3 import MAP_3
from infrastructure.game import Game


print(
    f'=== DUNGEON {MAP_WIDTH_TILES}x{MAP_HEIGHT_TILES} '
    f'({SCREEN_WIDTH}x{SCREEN_HEIGHT}px) ==='
)


def main() -> None:
    env = Environment(MAP_1)
    agent = Agent(env)

    print('=== TRAINING AGENT ON 3 LEVELS (OFFLINE Q-LEARNING) ===')
    train_agent_on_3_maps_use_case(agent, [MAP_1, MAP_2, MAP_3], episodes=1000)

    print('=== STARTING ARCADE GAME (mouvements encore aléatoires) ===')
    window = Game(agent)
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
