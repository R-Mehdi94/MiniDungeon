from __future__ import annotations

import arcade
import os.path

from matplotlib import pyplot as plt

from application.train_agent_on_3_maps_use_case import train_agent_on_3_maps_use_case
#from application.train_agent_on_map_4_use_case import train_agent_on_map_4_use_case
from domain.models.environment import Environment
from infrastructure.agent import Agent
from infrastructure.arcade.settings import (
    MAP_HEIGHT_TILES,
    MAP_WIDTH_TILES,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from infrastructure.data.map_1 import MAP_1
from infrastructure.data.map_2 import MAP_2
from infrastructure.data.map_3 import MAP_3
from infrastructure.data.map_5 import MAP_TRAINING_2
from infrastructure.game import Game


print(
    f"=== DUNGEON {MAP_WIDTH_TILES}x{MAP_HEIGHT_TILES} "
    f"({SCREEN_WIDTH}x{SCREEN_HEIGHT}px) ==="
)

FILE_AGENT = 'agent.qtable'


def run_training_on_3_maps_scenario() -> None:
    maps = [MAP_1, MAP_2, MAP_3]
    environment = Environment(MAP_1)
    agent = Agent(environment)

    print("=== TRAINING AGENT ON 3 LEVELS (OFFLINE Q-LEARNING) ===")
    #train_agent_on_3_maps_use_case(
    #    agent=agent,
    #    maps=maps,
    #    episode_count=1000,
    #)

    print("=== STARTING ARCADE GAME (3 MAPS SCENARIO) ===")
    window = Game(agent, maps=maps)
    window.setup()
    arcade.run()


def run_training_on_map_4_scenario() -> None:

    maps = [MAP_TRAINING_2]

    environment = Environment(MAP_TRAINING_2)
    agent = Agent(environment)

    if os.path.exists(FILE_AGENT):
        agent.load(FILE_AGENT)


    print("=== TRAINING AGENT ON MAP 4 (OFFLINE Q-LEARNING) ===")
    #train_agent_on_map_4_use_case(
    #    agent=agent,
    #    episode_count=1000,
    #)

    print("=== STARTING ARCADE GAME (MAP 4 SCENARIO) ===")
    window = Game(agent, maps=maps)
    window.setup()
    arcade.run()
    agent.save(FILE_AGENT)
    plt.plot(agent.history)
    plt.show()

def main() -> None:
    # run_training_on_3_maps_scenario()
    run_training_on_map_4_scenario()




if __name__ == "__main__":
    main()
