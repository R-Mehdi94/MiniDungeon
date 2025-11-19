from domain.models.action import Action
from domain.models.actions_qualities_for_state import ActionsQualitiesForState
from domain.models.position import Position


class QTable:
    __table: dict[Position, ActionsQualitiesForState]
    __initial_quality: float

    def __init__(self, initial_quality: float = 0.0) -> None:
        self.__table = {}
        self.__initial_quality = initial_quality

    def get_table(self) -> dict[Position, ActionsQualitiesForState]:
        return self.__table

    def set_table(self, table: dict[Position, ActionsQualitiesForState]) -> None:
        self.__table = table

    def get_initial_quality(self) -> float:
        return self.__initial_quality

    def set_initial_quality(self, value: float) -> None:
        self.__initial_quality = value

    def __get_or_create_state(self, position: Position) -> ActionsQualitiesForState:
        if position not in self.__table:
            self.__table[position] = ActionsQualitiesForState(self.__initial_quality)
        return self.__table[position]

    def get_quality(self, position: Position, action: Action) -> float:
        return self.__get_or_create_state(position).get(action)

    def set_quality(self, position: Position, action: Action, quality: float) -> None:
        self.__get_or_create_state(position).set(action, quality)

    def choose_best_action(self, position: Position) -> Action:
        return self.__get_or_create_state(position).choose_best_action()

    def get_state_qualities(self, position: Position) -> ActionsQualitiesForState:
        return self.__get_or_create_state(position)
