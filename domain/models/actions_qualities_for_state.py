from domain.models.action import Action


class ActionsQualitiesForState:
    __qualities: dict[Action, float]

    def __init__(self, initial: float = 0.0) -> None:
        self.__qualities = {
            action: initial for action in Action
        }

    def get_qualities(self) -> dict[Action, float]:
        return self.__qualities

    def set_qualities(self, qualities: dict[Action, float]) -> None:
        self.__qualities = qualities

    def get(self, action: Action) -> float:
        return self.__qualities[action]

    def set(self, action: Action, quality: float) -> None:
        self.__qualities[action] = quality

    def choose_best_action(self) -> Action:
        return max(self.__qualities, key=lambda action: self.__qualities[action])
