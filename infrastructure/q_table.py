from domain.models.action import Action
from domain.models.actions_qualities_for_state import ActionsQualitiesForState


class QTable:
    __table: dict[tuple, ActionsQualitiesForState]
    __initial_quality: float

    def __init__(self, initial_quality: float = 0.0) -> None:
        self.table = {}
        self.initial_quality = initial_quality

    @property
    def table(self) -> dict[tuple, ActionsQualitiesForState]:
        return self.__table

    @table.setter
    def table(self, value: dict[tuple, ActionsQualitiesForState]) -> None:
        self.__table = value

    @property
    def initial_quality(self) -> float:
        return self.__initial_quality

    @initial_quality.setter
    def initial_quality(self, value: float) -> None:
        self.__initial_quality = value

    def __or_create_state(self, state_key: tuple) -> ActionsQualitiesForState:
        if state_key not in self.table:
            self.table[state_key] = ActionsQualitiesForState(self.initial_quality)
        return self.table[state_key]

    def get_quality(self, state_key: tuple, action: Action) -> float:
        return self.__or_create_state(state_key).get(action)

    def set_quality(self, state_key: tuple, action: Action, quality: float) -> None:
        self.__or_create_state(state_key).set(action, quality)

    def choose_best_action(self, state_key: tuple) -> Action:
        return self.__or_create_state(state_key).choose_best_action()

    def state_qualities(self, state_key: tuple) -> ActionsQualitiesForState:
        return self.__or_create_state(state_key)
