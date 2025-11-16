from domain.agent import Agent


class ResetUseCase:
    def execute(self, agent: Agent) -> None:
        agent.reset()
