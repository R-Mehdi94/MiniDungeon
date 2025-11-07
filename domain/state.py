from __future__ import annotations
from typing import Optional, Tuple
from .position import Position


class State:
    """État MDP minimal pour Q-learning.
    On encode (position joueur, possession de clé (0/1)).
    Les monstres sont modélisés par la stochasticité de l'environnement.
    """
    __player: Position
    __has_key: bool

    def __init__(self, player: Position, has_key: bool) -> None:
        self.__player = player
        self.__has_key = has_key

    def get_player(self) -> Position:
        return self.__player

    def set_player(self, player: Optional[Position]) -> None:
        if player is None:
            raise ValueError("player required")
        self.__player = player

    def has_key(self) -> bool:
        return self.__has_key

    def set_has_key(self, has_key: Optional[bool]) -> None:
        if has_key is None:
            raise ValueError("has_key required")
        self.__has_key = has_key

        def as_tuple(self) -> Tuple[int, int, int]:

        p = self.__player.as_tuple()
        return (p[0], p[1], 1 if self.__has_key else 0)

    def __hash__(self) -> int:
        return hash(self.as_tuple())

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.as_tuple() == other.as_tuple()
