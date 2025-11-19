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
    __env: Environment
    __q_table: QTable
    __pos: Position
    __has_key: bool
    __score: int
    __done: bool
    __reward: int
    __iterations: int

    def __init__(self, env: Environment) -> None:
        self.__env = env
        self.__q_table = QTable(initial_quality=0.0)
        self.reset()

    def get_env(self) -> Environment:
        return self.__env

    def set_env(self, env: Environment) -> None:
        self.__env = env

    def get_q_table(self) -> QTable:
        return self.__q_table

    def set_q_table(self, q_table: QTable) -> None:
        self.__q_table = q_table

    def get_pos(self) -> Position:
        return self.__pos

    def set_pos(self, pos: Position) -> None:
        self.__pos = pos

    def get_has_key(self) -> bool:
        return self.__has_key

    def set_has_key(self, has_key: bool) -> None:
        self.__has_key = has_key

    def get_score(self) -> int:
        return self.__score

    def set_score(self, score: int) -> None:
        self.__score = score

    def get_done(self) -> bool:
        return self.__done

    def set_done(self, done: bool) -> None:
        self.__done = done

    def get_reward(self) -> int:
        return self.__reward

    def set_reward(self, reward: int) -> None:
        self.__reward = reward

    def get_iterations(self) -> int:
        return self.__iterations

    def set_iterations(self, iterations: int) -> None:
        self.__iterations = iterations

    def is_done(self) -> bool:
        return self.__done

    def reset(self) -> None:
        self.__pos = self.__env.get_start()
        self.__has_key = False
        self.__score = 0
        self.__done = False
        self.__reward = 0
        self.__iterations = 0

    def get_radar(self) -> Radar:
        env = self.__env
        pos = self.__pos

        def content_at(delta_row: int, delta_col: int) -> CellContent:
            target = Position(pos.get_row() + delta_row, pos.get_column() + delta_col)
            return env.get_cell_content(target)

        north = content_at(-1, 0)
        north_east = content_at(-1, 1)
        east = content_at(0, 1)
        south_east = content_at(1, 1)
        south = content_at(1, 0)
        south_west = content_at(1, -1)
        west = content_at(0, -1)
        north_west = content_at(-1, -1)

        return Radar(
            north=north,
            north_east=north_east,
            east=east,
            south_east=south_east,
            south=south,
            south_west=south_west,
            west=west,
            north_west=north_west,
        )

    def do(
        self,
        action: Action,
        learning_rate: float = 1.0,
        discount_factor: float = 1.0,
    ) -> Radar:
        current_pos: Position = self.__pos

        next_pos, reward = self.__env.do(current_pos, action)

        old_quality: float = self.__q_table.get_quality(current_pos, action)

        best_next_action: Action = self.__q_table.choose_best_action(next_pos)
        max_next_quality: float = self.__q_table.get_quality(next_pos, best_next_action)

        updated_quality: float = old_quality + learning_rate * (
            reward + discount_factor * max_next_quality - old_quality
        )

        self.__q_table.set_quality(current_pos, action, updated_quality)

        self.__pos = next_pos
        self.__reward = reward
        self.__score += reward
        self.__iterations += 1

        if reward == Reward.KEY:
            self.__has_key = True

        if reward == Reward.GOAL or reward == Reward.MONSTER:
            self.__done = True

        radar: Radar = self.get_radar()
        return radar

    def choose_action_epsilon_greedy(self, epsilon: float) -> Action:
        if random.random() < epsilon:
            return choice(list(Action))
        return self.choose_best_action()

    def choose_best_action(self) -> Action:
        return self.__q_table.choose_best_action(self.__pos)

    def run_episode(
        self,
        max_steps: int,
        learning_rate: float,
        discount_factor: float,
        epsilon: float,
    ) -> int:
        self.reset()
        total_reward: int = 0

        for _ in range(max_steps):
            action: Action = self.choose_action_epsilon_greedy(epsilon)
            self.do(action, learning_rate, discount_factor)
            total_reward += self.__reward

            if self.__done:
                break

        return total_reward
