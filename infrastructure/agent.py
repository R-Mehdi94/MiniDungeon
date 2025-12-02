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


def get_direction_sign(val: int) -> int:
    """
    1  = C'est positif (vers le Bas ou la Droite)
    -1 = C'est négatif (vers le Haut ou la Gauche)
    0  = C'est nul (on est aligné)
    """
    if val > 0: return 1
    if val < 0: return -1
    return 0


class Agent:


    def __init__(self, env: Environment) -> None:
        self.environment = env
        self.q_table = QTable(initial_quality=0.0)
        self.position = self.environment.starting_position

        # États du jeu
        self.has_key = False
        self.has_door = False
        self.score = 0
        self.has_finished_episode = False
        self.key_pos = None
        self.door_pos = None
        self.treasure_pos = None

        # Apprentissage
        self.reward = 0
        self.iterations_count = 0
        self.exploration = 0.0  # Float
        self.history = []
        self.radar = None

        # Mémoire pour l'algo RL
        self.previous_state = None
        self.previous_action = None

    def reset(self) -> None:
        if self.score is not None:
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

    def get_state(self):
        if self.key_pos:
            delta_key_pos_row = get_direction_sign(self.key_pos.row - self.position.row)
            delta_key_pos_col = get_direction_sign(self.key_pos.column - self.position.column)
        else:
            delta_key_pos_row = 0
            delta_key_pos_col = 0
        if self.treasure_pos:
            delta_door_pos_row = get_direction_sign(self.door_pos.row - self.position.row)
            delta_door_pos_col = get_direction_sign(self.door_pos.column  - self.position.column)
        else:
            delta_door_pos_row = 0
            delta_door_pos_col = 0
        if self.treasure_pos:
            delta_treasure_pos_row = get_direction_sign(self.treasure_pos.row - self.position.row)
            delta_treasure_pos_col = get_direction_sign(self.treasure_pos.column  - self.position.column)
        else:
            delta_treasure_pos_row = 0
            delta_treasure_pos_col = 0

        return (delta_key_pos_row, delta_key_pos_col), (delta_door_pos_row, delta_door_pos_col), (delta_treasure_pos_row, delta_treasure_pos_col)



    def get_state_key(self) -> tuple:

        radar = self.scan_surroundings()

        state = self.get_state()

        test = radar,state,self.has_key
        print(test)

        return test

    def execute_action_and_learn_from_reward(
            self,
            action: Action,
            learning_rate: float = 0.6,
            discount_factor: float = 0.9
    ) -> None:

        current_state_key = self.get_state_key()

        #self.__previous_state = current_state_key
        #self.__previous_action = action

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
        if random.random() < self.exploration:
            return choice(list(Action))
        self.exploration *= .99
        return self.choose_best_action()

    def run_episode(
            self,
            max_steps: int,
            learning_rate: float,
            discount_factor: float,
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
            # noinspection PyTypeChecker
            pickle.dump((self.q_table, self.history), file)



    def load(self, filename):
        with open(filename, 'rb') as file:
            self.q_table, self.history = pickle.load(file)