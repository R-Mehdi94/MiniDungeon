from domain.models.action import Action
import random


class ActionsQualitiesForState:
    __qualities: dict[Action, float]

    def __init__(self, initial: float = 0.0) -> None:
        self.__qualities = {
            action: initial for action in Action
        }

    @property
    def qualities(self) -> dict[Action, float]:
        return self.__qualities

    @qualities.setter
    def qualities(self, qualities: dict[Action, float]) -> None:
        self.__qualities = qualities

    def get(self, action: Action) -> float:
        return self.__qualities[action]

    def set(self, action: Action, quality: float) -> None:
        self.__qualities[action] = quality

    def choose_best_action(self) -> Action:
        max_q = max(self.__qualities.values())
        best_actions = [action for action, q in self.__qualities.items() if q == max_q]
        return random.choice(best_actions)
