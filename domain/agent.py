from __future__ import annotations
from domain.action import Action
from domain.q_table import QTable
from domain.state import State


class Agent:
    __env: EnvironmentPort
    __qtable: QTable
    __policy: EpsilonGreedyPolicy
    __alpha: float
    __gamma: float
    __state: State
    __score: float

    def __init__(self, env: EnvironmentPort, alpha: float = 1.0, gamma: float = 0.95, epsilon: float = 0.1) -> None:
        self.__env = env
        self.__qtable = QTable()
        self.__policy = EpsilonGreedyPolicy(epsilon)
        self.__alpha = alpha
        self.__gamma = gamma
        self.__state = env.reset()
        self.__score = 0.0

    def get_score(self) -> float:
        return self.__score

    def get_qtable(self) -> QTable:
        return self.__qtable

    def get_state(self) -> State:
        return self.__state

    def get_alpha(self) -> float:
        return self.__alpha

    def set_alpha(self, alpha: Optional[float]) -> None:
        if alpha is None:
            raise ValueError("alpha required")
        self.__alpha = alpha

    def get_gamma(self) -> float:
        return self.__gamma

    def set_gamma(self, gamma: Optional[float]) -> None:
        if gamma is None:
            raise ValueError("gamma required")
        self.__gamma = gamma

    def reset(self) -> None:
        self.__state = self.__env.reset()
        self.__score = 0.0

    def best_action(self) -> Action:
        q = self.__qtable.get_actions(self.__state)
        return self.__policy.choose(q)

    def step(self, action: Action) -> tuple[State, int, bool]:
        next_state, reward, done = self.__env.step(self.__state, action)
        self.__qtable.update(
            self.__state, action,
            reward,
            next_state,
            self.__alpha, self.__gamma
        )
        self.__state = next_state
        self.__score += reward
        return (next_state, reward, done)
