from __future__ import annotations

import arcade
import os.path
from matplotlib import pyplot as plt
from environment.environment import Environment
from agent.agent import Agent
from game.game_manual import GameManual
from game.map.map import MAP_1, MAP_3, MAP_2

from game.game_agent import GameAgent

FILE_AGENT = 'agent.qtable'


def main() -> None:
    text = input("Choice your mode [1: Manual mode] [2: Agent mode] : ")

    maps = [MAP_1, MAP_2, MAP_3]
    environment = Environment(MAP_1)


    if text == '1':
        window = GameManual(environment, maps=maps)
    else:
        agent = Agent(environment)
        if os.path.exists(FILE_AGENT):
            agent.load(FILE_AGENT)
        window = GameAgent(agent, maps=maps)

    window.setup()
    arcade.run()

    if text == '2':
        agent.save(FILE_AGENT)
        plt.plot(agent.history)
        plt.show()


if __name__ == "__main__":
    main()
