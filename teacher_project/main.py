from __future__ import annotations

from random import choice
from typing import Literal, Optional
from collections.abc import Mapping

import arcade
from pyglet.event import EVENT_HANDLE_STATE

from matplotlib import pyplot


class Position:
    __abscissa: int
    __ordinate: int

    def __init__(self, abscissa: int, ordinate: int) -> None:
        if not isinstance(abscissa, int):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError('`abscissa` must be of type `int`.')
        if not isinstance(ordinate, int):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError('`ordinate` must be of type `int`.')
        self.__abscissa = abscissa   # ligne (row)
        self.__ordinate = ordinate   # colonne (col)

    def get_abscissa(self) -> int:
        return self.__abscissa

    def set_abscissa(self, abscissa: int) -> None:
        if not isinstance(abscissa, int):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError('`abscissa` must be of type `int`.')
        self.__abscissa = abscissa

    def get_ordinate(self) -> int:
        return self.__ordinate

    def set_ordinate(self, ordinate: int) -> None:
        if not isinstance(ordinate, int):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError('`ordinate` must be of type `int`.')
        self.__ordinate = ordinate

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):  # pyright: ignore[reportUnnecessaryIsInstance]
            return NotImplemented
        return (
            self.__abscissa == other.__abscissa
            and self.__ordinate == other.__ordinate
        )

    def __hash__(self) -> int:
        return hash((self.__abscissa, self.__ordinate))

    def __repr__(self) -> str:
        return f"Position({self.__abscissa}, {self.__ordinate})"


# ---- Type aliases ----

Action = Literal["UP", "DOWN", "LEFT", "RIGHT"]
ActionDelta = tuple[int, int]
QValues = dict[Action, float]
QTable = dict[Position, QValues]


# ---- Constants ----

SPRITE_SCALE: float = 0.25
SPRITE_SIZE: int = 128

MAZE: str = """
#.###############
#         #     #
######    #     #
#               #
#     #####     #
#        #  ##  #
#        #      #
#            #  #
#            #  #
###############*#
"""

MAP_WALL: str = "#"
MAP_GOAL: str = "*"
MAP_START: str = "."

REWARD_WALL: int = -10
REWARD_DEFAULT: int = -1
REWARD_GOAL: int = 1000
REWARD_OUT: int = -10

ACTION_UP: Action = "UP"
ACTION_DOWN: Action = "DOWN"
ACTION_LEFT: Action = "LEFT"
ACTION_RIGHT: Action = "RIGHT"

ACTIONS: dict[Action, ActionDelta] = {
    ACTION_UP: (-1, 0),
    ACTION_DOWN: (1, 0),
    ACTION_LEFT: (0, -1),
    ACTION_RIGHT: (0, 1),
}


# ---- Helpers ----

def arg_max(table: Mapping[Action, float]) -> Action:
    return max(table, key=lambda a: table[a])

# ---- RL Agent ----


class Agent:
    __environment: Environment
    __position: Position
    __iterationCount: int
    __score: float
    __reward: float
    __qTable: QTable

    def getEnvironment(self) -> Environment:
        return self.__environment

    def setEnvironment(self, environment: Environment) -> None:
        if not isinstance(environment, Environment):  # type: ignore
            raise TypeError('`environment` must be of type `Environment`')
        else:
            self.__environment = environment

    def getPosition(self) -> Position:
        return self.__position

    def setPosition(self, position: Position) -> None:
        if not isinstance(position, Position):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError('`position` must be of type `Position`')
        else:
            self.__position = position

    def getIterationCount(self) -> int:
        return self.__iterationCount

    def setIterationCount(self, iterationCount: int) -> None:
        if not isinstance(iterationCount, int):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError('`iterationCount` must be of type `int`')
        else:
            self.__iterationCount = iterationCount

    def getScore(self) -> float:
        return self.__score

    def setScore(self, score: float) -> None:
        if not isinstance(score, (int, float)):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError('`score` must be of type `float`')
        else:
            self.__score = float(score)

    def getReward(self) -> float:
        return self.__reward

    def setReward(self, reward: float) -> None:
        if not isinstance(reward, (int, float)):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError('`reward` must be of type `float`')
        else:
            self.__reward = float(reward)

    def getQTable(self) -> QTable:
        return self.__qTable

    def setQTable(self, qTable: QTable) -> None:
        if not isinstance(qTable, dict):  # ici on vérifie juste dict
            raise TypeError('`qTable` must be of type `dict[Position, QValues]`')
        else:
            self.__qTable = qTable

    def __init__(self, env: "Environment") -> None:
        self.__environment = env
        self.__qTable = {}
        self.reset()

    def reset(self) -> None:
        self.__position = self.__environment.start
        self.__iterationCount = 0
        self.__score = 0.0
        self.__reward = 0.0

    def do(
        self,
        action: Action,
        learning_rate: float = 1.0,
        discount_factor: float = 1.0,
    ) -> None:
        pos, reward = self.__environment.do(self.__position, action)

        if self.__position not in self.__qTable:
            self.__qTable[self.__position] = {
                ACTION_UP: 0.0,
                ACTION_DOWN: 0.0,
                ACTION_LEFT: 0.0,
                ACTION_RIGHT: 0.0,
            }

        if pos not in self.__qTable:
            self.__qTable[pos] = {
                ACTION_UP: 0.0,
                ACTION_DOWN: 0.0,
                ACTION_LEFT: 0.0,
                ACTION_RIGHT: 0.0,
            }

        # Q(s, a) += alpha * [r + gamma * max Q(s') - Q(s, a)]
        current_q: float = self.__qTable[self.__position][action]
        best_next_q: float = max(self.__qTable[pos].values())
        delta: float = learning_rate * (
            reward + discount_factor * best_next_q - current_q
        )
        self.__qTable[self.__position][action] = current_q + delta

        self.__position = pos
        self.__reward = float(reward)
        self.__score += float(reward)
        self.__iterationCount += 1

    def best_action(self) -> Action:
        if self.__position in self.__qTable:
            return arg_max(self.__qTable[self.__position])
        return choice(list(ACTIONS.keys()))


# ---- Environment ----

class Environment:
    map: dict[Position, str]
    start: Position
    goal: Position
    width: int
    height: int

    def __init__(self, maze: str) -> None:
        self.map = {}
        row: int = 0
        col: int = 0

        for line in maze.strip().split("\n"):
            for char in line:
                pos: Position = Position(row, col)
                self.map[pos] = char
                if char == MAP_START:
                    self.start = pos
                elif char == MAP_GOAL:
                    self.goal = pos
                col += 1
            self.width = col
            row += 1
            col = 0

        self.height = row

    def do(self, pos: Position, action: Action) -> tuple[Position, int]:
        move: ActionDelta = ACTIONS[action]

        new_pos: Position = Position(
            pos.get_abscissa() + move[0],
            pos.get_ordinate() + move[1],
        )

        reward: int
        if new_pos in self.map:
            tile: str = self.map[new_pos]
            if tile == MAP_WALL:
                reward = REWARD_WALL
            else:
                pos = new_pos
                if tile == MAP_GOAL:
                    reward = REWARD_GOAL
                else:
                    reward = REWARD_DEFAULT
        else:
            reward = REWARD_OUT

        return pos, reward


# ---- Rendering ----

class MazeWindow(arcade.Window):
    sprite_agent: Optional[arcade.Sprite]
    sprite_goal: Optional[arcade.Sprite]
    walls: Optional[arcade.SpriteList[arcade.Sprite]]
    info: Optional[arcade.Text]
    history: list[float]

    def __init__(self, agent: Agent) -> None:
        width: int = int(SPRITE_SIZE * SPRITE_SCALE *
                         agent.getEnvironment().width)
        height: int = int(SPRITE_SIZE * SPRITE_SCALE *
                          agent.getEnvironment().height)
        super().__init__(width, height, "Escape from ESGI")

        self.background_color = arcade.csscolor.BLACK
        self.agent = agent
        self.env = agent.getEnvironment()

        self.sprite_agent = None
        self.sprite_goal = None
        self.walls = None
        self.info = None
        self.history = []

    def pos_to_xy(self, pos: Position, sprite: arcade.Sprite) -> tuple[float, float]:
        x: float = (pos.get_ordinate() + 0.5) * sprite.width
        y: float = (self.env.height - pos.get_abscissa() - 0.5) * sprite.height
        return x, y

    def setup(self) -> None:
        resource_agent = arcade.load_texture(
            ":resources:/images/enemies/bee.png")
        self.sprite_agent = arcade.Sprite(resource_agent, SPRITE_SCALE)
        self.sprite_agent.center_x, self.sprite_agent.center_y = self.pos_to_xy(
            self.agent.getPosition(), self.sprite_agent
        )

        resource_goal = arcade.load_texture(
            ":resources:/images/tiles/cactus.png")
        self.sprite_goal = arcade.Sprite(resource_goal, SPRITE_SCALE)
        self.sprite_goal.center_x, self.sprite_goal.center_y = self.pos_to_xy(
            self.env.goal, self.sprite_goal
        )

        self.walls = arcade.SpriteList()
        for pos, value in self.env.map.items():
            if value == MAP_WALL:
                resource_wall = arcade.load_texture(
                    ":resources:/images/tiles/brickBrown.png"
                )
                wall_sprite = arcade.Sprite(resource_wall, SPRITE_SCALE)
                wall_sprite.center_x, wall_sprite.center_y = self.pos_to_xy(
                    pos, wall_sprite
                )
                self.walls.append(wall_sprite)

        self.info = arcade.Text(
            f"{self.agent.getIterationCount()}",
            10,
            10,
            color=arcade.csscolor.BLACK,
            font_size=20,
        )

    def on_draw(self) -> None:
        self.clear()
        if self.walls is not None:
            self.walls.draw()
        if self.sprite_goal is not None:
            arcade.draw_sprite(self.sprite_goal)
        if self.sprite_agent is not None:
            arcade.draw_sprite(self.sprite_agent)
        if self.info is not None:
            self.info.draw()

    def on_update(self, delta_time: float) -> bool | None:
        _ = delta_time  # unused but kept for signature compatibility
        if self.info is not None:
            self.info.text = f"#{self.agent.getIterationCount()} Score: {self.agent.getScore()}"

        if self.agent.getPosition() != self.env.goal:
            action: Action = self.agent.best_action()
            self.agent.do(action)

            if self.sprite_agent is not None:
                self.sprite_agent.center_x, self.sprite_agent.center_y = (
                    self.pos_to_xy(self.agent.getPosition(), self.sprite_agent)
                )
        return None

    def on_key_press(self, symbol: int, modifiers: int) -> EVENT_HANDLE_STATE:
        _ = modifiers  # unused

        if symbol == arcade.key.R:
            self.history.append(self.agent.getScore())
            self.agent.reset()
        if symbol == arcade.key.Q:
            self.close()
        # EVENT_HANDLED / EVENT_UNHANDLED are ints; type is EVENT_HANDLE_STATE
        return EVENT_HANDLE_STATE  # type: ignore[return-value]


# ---- Main ----

if __name__ == "__main__":
    env: Environment = Environment(MAZE)
    agent: Agent = Agent(env)

    window: MazeWindow = MazeWindow(agent)
    window.setup()
    arcade.run()

    pyplot.plot(window.history)  # type: ignore
    pyplot.show()  # type: ignore
