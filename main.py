from __future__ import annotations

import arcade
import os.path
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt

from application.train_agent_on_3_maps_use_case import train_agent_on_3_maps_use_case
#from application.train_agent_on_map_4_use_case import train_agent_on_map_4_use_case
from domain.models.environment import Environment
from infrastructure.agent import Agent

from infrastructure.data.map_1 import MAP_1
from infrastructure.data.map_2 import MAP_2

from infrastructure.data.map_4 import MAP_4

from infrastructure.game import Game


FILE_AGENT = 'agent.qtable'


def run_training_on_3_maps_scenario() -> None:
    maps = [MAP_1, MAP_2, MAP_4]
    environment = Environment(MAP_1)
    agent = Agent(environment)


    if os.path.exists(FILE_AGENT):
        agent.load(FILE_AGENT)

    print("=== TRAINING AGENT ON 3 LEVELS (OFFLINE Q-LEARNING) ===")
    #train_agent_on_3_maps_use_case(
    #    agent=agent,
    #    maps=maps,
    #    episode_count=1000,
    #)

    print("=== STARTING ARCADE GAME (MAP 4 SCENARIO) ===")

    window = Game(agent, maps=maps)
    window.setup()
    arcade.run()
    agent.save(FILE_AGENT)
    plt.plot(agent.history)
    plt.show()


def run_training_on_map_4_scenario() -> None:

    maps = [MAP_4]

    environment = Environment(MAP_4)
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
     run_training_on_3_maps_scenario()
   # run_training_on_map_4_scenario()




if __name__ == "__main__":
    main()
