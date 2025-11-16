from __future__ import annotations
from typing import Tuple

from domain.agent import Agent


class RunEpisodeUseCase:
    def __init__(self, max_steps: int = 500) -> None:
        self.__max_steps = max_steps

    def execute(self, agent: Agent) -> Tuple[int, int]:
        agent.reset()
        total_reward: int = 0
        steps: int = 0
        for _ in range(self.__max_steps):
            _, reward, is_done = agent.step(agent.best_action())
            total_reward += reward
            steps += 1
            if is_done:
                break
        return total_reward, steps
