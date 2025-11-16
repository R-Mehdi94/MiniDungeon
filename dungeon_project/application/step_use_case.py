from __future__ import annotations
from typing import Tuple

from domain.action import Action
from domain.agent import Agent


class StepUseCase:
    def execute(self, agent: Agent) -> Tuple[Action, int, bool]:
        action = agent.best_action()
        _, reward, done = agent.step(action)
        return (action, reward, done)
