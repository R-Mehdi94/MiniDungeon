from __future__ import annotations

from random import choice
from typing import Literal, Optional
from collections.abc import Mapping

import arcade
from pyglet.event import EVENT_HANDLE_STATE

from matplotlib import pyplot

# ---- Type aliases ----

Position = tuple[int, int]
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
    env: Environment
    pos: Position
    iterations: int
    score: float
    reward: float
    qtable: QTable

    def __init__(self, env: "Environment") -> None:
        self.env = env
        self.qtable = {}
        self.reset()

    def reset(self) -> None:
        self.pos = self.env.start
        self.iterations = 0
        self.score = 0.0
        self.reward = 0.0

    def do(
        self,
        action: Action,
        learning_rate: float = 1.0,
        discount_factor: float = 1.0,
    ) -> None:
        pos, reward = self.env.do(self.pos, action)

        if self.pos not in self.qtable:
            self.qtable[self.pos] = {
                ACTION_UP: 0.0,
                ACTION_DOWN: 0.0,
                ACTION_LEFT: 0.0,
                ACTION_RIGHT: 0.0,
            }

        if pos not in self.qtable:
            self.qtable[pos] = {
                ACTION_UP: 0.0,
                ACTION_DOWN: 0.0,
                ACTION_LEFT: 0.0,
                ACTION_RIGHT: 0.0,
            }

        # Q(s, a) += alpha * [r + gamma * max Q(s') - Q(s, a)]
        current_q: float = self.qtable[self.pos][action]
        best_next_q: float = max(self.qtable[pos].values())
        delta: float = learning_rate * (
            reward + discount_factor * best_next_q - current_q
        )
        self.qtable[self.pos][action] = current_q + delta

        self.pos = pos
        self.reward = float(reward)
        self.score += float(reward)
        self.iterations += 1

    def best_action(self) -> Action:
        if self.pos in self.qtable:
            return arg_max(self.qtable[self.pos])
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
                pos: Position = (row, col)
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
        new_pos: Position = (pos[0] + move[0], pos[1] + move[1])

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
        width: int = int(SPRITE_SIZE * SPRITE_SCALE * agent.env.width)
        height: int = int(SPRITE_SIZE * SPRITE_SCALE * agent.env.height)
        super().__init__(width, height, "Escape from ESGI")

        self.background_color = arcade.csscolor.BLACK
        self.agent = agent
        self.env = agent.env

        self.sprite_agent = None
        self.sprite_goal = None
        self.walls = None
        self.info = None
        self.history = []

    def pos_to_xy(self, pos: Position, sprite: arcade.Sprite) -> tuple[float, float]:
        x: float = (pos[1] + 0.5) * sprite.width
        y: float = (self.env.height - pos[0] - 0.5) * sprite.height
        return x, y

    def setup(self) -> None:
        resource_agent = arcade.load_texture(
            ":resources:/images/enemies/bee.png")
        self.sprite_agent = arcade.Sprite(resource_agent, SPRITE_SCALE)
        self.sprite_agent.center_x, self.sprite_agent.center_y = self.pos_to_xy(
            self.agent.pos, self.sprite_agent
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
            f"{self.agent.iterations}",
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
            self.info.text = f"#{self.agent.iterations} Score: {self.agent.score}"

        if self.agent.pos != self.env.goal:
            action: Action = self.agent.best_action()
            self.agent.do(action)

            if self.sprite_agent is not None:
                self.sprite_agent.center_x, self.sprite_agent.center_y = (
                    self.pos_to_xy(self.agent.pos, self.sprite_agent)
                )
        return None

    def on_key_press(self, symbol: int, modifiers: int) -> EVENT_HANDLE_STATE:
        _ = modifiers  # unused

        if symbol == arcade.key.R:
            self.history.append(self.agent.score)
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

    # score = 0
    # iterations = 0
    #
    # while agent.pos != env.goal:
    #     random_action: Action = choice(list(ACTIONS.keys()))
    #     agent.do(random_action)
    #     score += agent.reward
    #     iterations += 1
    #
    # print(iterations)
