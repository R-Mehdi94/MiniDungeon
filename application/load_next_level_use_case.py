class LoadNextLevelUseCase:
    def __init__(self, env: EnvironmentPort) -> None:
        self.__env = env


    def execute(self) -> None:
        self.__env.reset()