from agent.qtable.actions_qualities_for_state import ActionsQualitiesForState
from environment.position.action import Action


class QTable:
    __table: dict[tuple, ActionsQualitiesForState]

    def __init__(self) -> None:
        self.table = {}

    @property
    def table(self) -> dict[tuple, ActionsQualitiesForState]:
        return self.__table

    @table.setter
    def table(self, value: dict[tuple, ActionsQualitiesForState]) -> None:
        self.__table = value





    def __or_create_state(self, state_key: tuple) -> ActionsQualitiesForState:
        if state_key not in self.table:
            self.table[state_key] = ActionsQualitiesForState()
        return self.table[state_key]

    def get_quality(self, state_key: tuple, action: Action) -> float:
        return self.__or_create_state(state_key).get(action)

    def set_quality(self, state_key: tuple, action: Action, quality: float) -> None:
        self.__or_create_state(state_key).set(action, quality)

    def choose_best_action(self, state_key: tuple) -> Action:
        return self.__or_create_state(state_key).choose_best_action()
