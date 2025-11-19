from __future__ import annotations
from abc import ABC, abstractmethod


class AgentKnowledge(ABC):
    @abstractmethod
    def save(self, knowledge: AgentKnowledge) -> None:
        ...
