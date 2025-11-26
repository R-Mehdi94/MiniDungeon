from random import choice
import random
from domain.models.action import Action
from domain.models.cell_content import CellContent
from domain.models.environment import Environment
from domain.models.radar import Radar
from domain.models.reward import Reward
from infrastructure.q_table import QTable
from domain.models.position import Position


class Agent:
    __environment: Environment
    __q_table: QTable
    __position: Position
    __has_key: bool
    __score: int
    __has_finished_episode: bool
    __reward: int
    __iterations_count: int

    def __init__(self, env: Environment) -> None:
        self.environment = env
        self.q_table = QTable(initial_quality=0.0)
        self.position = self.environment.starting_position
        self.has_key = False
        self.score = 0
        self.has_finished_episode = False
        self.reward = 0
        self.iterations_count = 0

    @property
    def environment(self) -> Environment:
        return self.__environment

    @environment.setter
    def environment(self, value: Environment) -> None:
        self.__environment = value

    @property
    def q_table(self) -> QTable:
        return self.__q_table

    @q_table.setter
    def q_table(self, value: QTable) -> None:
        self.__q_table = value

    @property
    def position(self) -> Position:
        return self.__position

    @position.setter
    def position(self, value: Position) -> None:
        self.__position = value

    @property
    def has_key(self) -> bool:
        return self.__has_key

    @has_key.setter
    def has_key(self, value: bool) -> None:
        self.__has_key = value

    @property
    def score(self) -> int:
        return self.__score

    @score.setter
    def score(self, value: int) -> None:
        self.__score = value

    @property
    def has_finished_episode(self) -> bool:
        return self.__has_finished_episode

    @has_finished_episode.setter
    def has_finished_episode(self, value: bool) -> None:
        self.__has_finished_episode = value

    @property
    def reward(self) -> int:
        return self.__reward

    @reward.setter
    def reward(self, value: int) -> None:
        self.__reward = value

    @property
    def iterations_count(self) -> int:
        return self.__iterations_count

    @iterations_count.setter
    def iterations_count(self, value: int) -> None:
        self.__iterations_count = value

    def reset(self) -> None:
        self.position = self.environment.starting_position
        self.has_key = False
        self.score = 0
        self.has_finished_episode = False
        self.reward = 0
        self.iterations_count = 0

    def scan_area(self) -> Radar:

        def content_at(delta_row: int, delta_col: int) -> CellContent:
            target = Position(
                self.position.row + delta_row,
                self.position.column + delta_col
            )
            return self.environment.get_cell_content(target)

        radar_3x3 = []

        for row in range(3):
            row_data = []
            for col in range(3):
                content = content_at(row, col)
                row_data.append(content)
                radar_3x3.append(row_data)

        return Radar(radar_3x3)

    def execute_action_and_learn_from_reward(
        self,
        action: Action,
        learning_rate: float = 1.0,
        discount_factor: float = 1.0
    ) -> Radar:
        current_position: Position = self.position

        next_position, reward = self.environment.do(current_position, action)

        old_quality: float = self.q_table.get_quality(current_position, action)

        best_next_action: Action = self.q_table.choose_best_action(next_position)
        max_next_quality: float = self.q_table.get_quality(next_position, best_next_action)

        updated_quality: float = old_quality + learning_rate * (reward + discount_factor * max_next_quality - old_quality)

        self.q_table.set_quality(current_position, action, updated_quality)

        self.position = next_position
        self.reward = reward
        self.score += reward
        self.iterations_count += 1

        if reward == Reward.KEY:
            self.has_key = True

        if reward == Reward.GOAL or reward == Reward.MONSTER:
            self.has_finished_episode = True

        radar: Radar = self.scan_area()
        return radar

    def choose_action_from_knowledge_or_random(self, exploration_rate: float) -> Action:
        '''
        Returns a random action or an action from the knowledge according to the exploration rate and a random generated float number between 0.0 and 1.0.

        :param float exploration_rate: The probability of the agent to do a random action to explore the map.
        :rtype: Action
        :return: The next action the agent will perform. It could be a random action or the best action according to the knowledge of the agent.
        '''
        #if random.random() < exploration_rate:
        #    return choice(list(Action))
        return self.choose_best_action()

    def choose_best_action(self) -> Action:
        return self.q_table.choose_best_action(self.position)

    def run_episode(
        self,
        max_steps: int,
        learning_rate: float,
        discount_factor: float,
        exploration_rate: float,
    ) -> int:
        self.reset()
        total_reward: int = 0

        for _ in range(max_steps):
            action: Action = self.choose_action_from_knowledge_or_random(exploration_rate)
            self.execute_action_and_learn_from_reward(action, learning_rate, discount_factor)
            total_reward += self.reward

            if self.has_finished_episode:
                break

        return total_reward
