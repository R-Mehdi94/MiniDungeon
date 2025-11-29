import pickle
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
    __has_door: bool
    __score: int
    __has_finished_episode: bool
    __reward: int
    __iterations_count: int
    __exploration: float
    __history: list
    __radar: Radar

    def __init__(self, env: Environment) -> None:

        self.environment = env
        self.q_table = QTable(initial_quality=0.0)
        self.position = self.environment.starting_position
        self.has_key = False
        self.has_door = False
        self.score = 0
        self.has_finished_episode = False
        self.reward = 0
        self.iterations_count = 0
        self.exploration = 0
        self.history = []
        self.radar = Radar([])

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
    def has_door(self) -> bool:
        return self.__has_door

    @has_door.setter
    def has_door(self, value: bool) -> None:
        self.__has_door = value

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

    @property
    def exploration(self) -> float:
        return self.__exploration

    @exploration.setter
    def exploration(self, value: float) -> None:
        self.__exploration = value

    @property
    def history(self) -> list:
        return self.__history

    @history.setter
    def history(self, value: list) -> None:
        self.__history = value

    @property
    def radar(self) -> Radar:
        return self.__radar

    @radar.setter
    def radar(self, value: Radar) -> None:
        self.__radar = value

    @iterations_count.setter
    def iterations_count(self, value: int) -> None:
        self.__iterations_count = value

    def reset(self) -> None:
        if self.score != None:
            self.history.append(self.score)
        self.position = self.environment.starting_position
        self.has_key = False
        self.has_door = False
        self.score = 0
        self.has_finished_episode = False
        self.reward = 0
        self.iterations_count = 0

    def scan_area(self) -> Radar:

        surroundings_tuple = self.scan_surroundings()

        return Radar(surroundings_tuple)

    def calcule_distance(self, but: Position, pos: Position) -> tuple[int, int]:
        row = but.row - pos.row
        col = but.column - pos.column

        return (row, col)



    def dynamic_goal(self) -> Position:
        if self.has_key and self.has_door is False:

            return self.environment.door

        elif self.has_door:
            return self.environment.goal

        else:
            return self.environment.key

    def get_cell_type(self, row_offset: int, col_offset: int) -> int:
        """
        Analyse une case voisine et renvoie son code simplifié :
        0 = Libre (Vide, Clé, Goal, Porte ouverte)
        1 = Bloqué (Mur, Porte fermée)
        2 = Danger (Monstre)
        """
        target = Position(
            self.position.row + row_offset,
            self.position.column + col_offset
        )
        content = self.environment.get_cell_content(target)

        if content == CellContent.MONSTER:
            return 2

        if content == CellContent.WALL:
            return 1
        if content == CellContent.DOOR and not self.has_key:
            return 1

        return 0

    def scan_surroundings(self) -> tuple:
        surroundings = []

        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for d_row, d_col in offsets:
            cell_code = self.get_cell_type(d_row, d_col)
            surroundings.append(cell_code)

        return tuple(surroundings)


    def get_direction_sign(self, val: int) -> int:
        """
        1  = C'est positif (vers le Bas ou la Droite)
        -1 = C'est négatif (vers le Haut ou la Gauche)
        0  = C'est nul (on est aligné)
        """
        if val > 0: return 1
        if val < 0: return -1
        return 0

    def get_state_key(self) -> tuple:

        goal_pos = self.dynamic_goal()

        d_row = self.get_direction_sign(goal_pos.row - self.position.row)

        d_col = self.get_direction_sign(goal_pos.column - self.position.column)

        radar = self.scan_surroundings()

        return (
            d_row,
            d_col,
            radar,
            self.has_key
        )

    def execute_action_and_learn_from_reward(
            self,
            action: Action,
            learning_rate: float = 0.6,
            discount_factor: float = 0.9
    ) -> None:

        current_state_key = self.get_state_key()

        self.radar = self.scan_area()

        next_position, reward = self.environment.do(self.position, action, self.has_key)

        self.position = next_position
        self.reward = reward
        self.score += reward
        self.iterations_count += 1

        if reward == Reward.KEY:
            self.has_key = True
        elif reward == Reward.DOOR:
            self.has_key = False
            self.has_door = True

        if reward == Reward.GOAL or reward == Reward.MONSTER:
            self.has_finished_episode = True

        next_state_key = self.get_state_key()

        old_quality: float = self.q_table.get_quality(current_state_key, action)

        best_next_action: Action = self.q_table.choose_best_action(next_state_key)
        max_next_quality: float = self.q_table.get_quality(next_state_key, best_next_action)

        updated_quality: float = old_quality + learning_rate * (
                reward + discount_factor * max_next_quality - old_quality
        )

        self.q_table.set_quality(current_state_key, action, updated_quality)

    def choose_best_action(self) -> Action:
        current_state_key = self.get_state_key()

        self.radar = self.scan_area()

        return self.q_table.choose_best_action(current_state_key)

    def choose_action_from_knowledge_or_random(self) -> Action:
        '''
        Returns a random action or an action from the knowledge according to the exploration rate and a random generated float number between 0.0 and 1.0.

        :param float exploration_rate: The probability of the agent to do a random action to explore the map.
        :rtype: Action
        :return: The next action the agent will perform. It could be a random action or the best action according to the knowledge of the agent.
        '''
        if random.random() < self.exploration:
            return choice(list(Action))
        self.exploration *= .99
        return self.choose_best_action()



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
            action: Action = self.choose_action_from_knowledge_or_random()
            self.execute_action_and_learn_from_reward(action, learning_rate, discount_factor)
            total_reward += self.reward

            if self.has_finished_episode:
                break

        return total_reward

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump((self.q_table, self.history), file)

    def load(self, filename):
        with open(filename, 'rb') as file:
            self.q_table, self.history = pickle.load(file)