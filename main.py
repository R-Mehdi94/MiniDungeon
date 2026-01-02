from __future__ import annotations

import arcade
import os.path
#import matplotlib
#matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt
from environment.environment import Environment
from agent.agent import Agent
from game.map.map import MAP_1, MAP_3, MAP_2

from game.game import Game


FILE_AGENT = 'agent.qtable'



def main() -> None:
    maps = [MAP_1, MAP_2, MAP_3]
    environment = Environment(MAP_1)
    agent = Agent(environment)

    if os.path.exists(FILE_AGENT):
        agent.load(FILE_AGENT)

    window = Game(agent, maps=maps)
    window.setup()
    arcade.run()
    agent.save(FILE_AGENT)
    plt.plot(agent.history)
    plt.show()


if __name__ == "__main__":
    main()
