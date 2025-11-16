from __future__ import annotations
from typing import Dict
from .action import Action
from .state import State


class QTable:
    __table: Dict[State, Dict[Action, float]]

    def __init__(self) -> None:
        self.__table = {}

    def get_actions(self, state: State) -> Dict[Action, float]:
        if state not in self.__table:
            self.__table[state] = {a: 0.0 for a in Action}
        return self.__table[state]

    def update(self, state: State, action: Action, reward: float, next_state: State, alpha: float, gamma: float) -> None:
        actions = self.get_actions(state)
        next_actions = self.get_actions(next_state)
        best_next = max(next_actions.values())
        old = actions[action]
        actions[action] = old + alpha * (reward + gamma * best_next - old)

    def as_dict(self) -> Dict[str, Dict[str, float]]:
        out: Dict[str, Dict[str, float]] = {}
        for s, acts in self.__table.items():
            out[str(s.as_tuple())] = {a.value: float(v)
                                      for a, v in acts.items()}
        return out
