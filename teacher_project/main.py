from random import choice
from typing import Literal
from typing import Optional

import arcade
from pyglet.event import EVENT_HANDLE_STATE

import matplotlib.pyplot as plt

SPRITE_SCALE = .25

SPRITE_SIZE = 128

MAZE = """
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

MAP_WALL = "#"
MAP_GOAL = "*"
MAP_START = '.'

REWARD_WALL = -10
REWARD_DEFAULT = -1
REWARD_GOAL = 1000
REWARD_OUT = -10

ACTION_UP = 'UP'
ACTION_DOWN = 'DOWN'
ACTION_LEFT = 'LEFT'
ACTION_RIGHT = 'RIGHT'

ACTIONS = {ACTION_UP: (-1, 0),
           ACTION_DOWN: (1, 0),
           ACTION_LEFT: (0, -1),
           ACTION_RIGHT: (0, 1)}


def arg_max(table):
    return max(table, key=table.get)


class Agent:
    def __init__(self, env):
        self.env = env
        self.reset()
        self.qtable = {}

    def reset(self):
        self.pos = self.env.start
        self.iterations = 0
        self.score = 0

    def do(self, action, learning_rate=1, discount_factor=1):
        pos, reward = self.env.do(self.pos, action)
        if self.pos not in self.qtable:
            self.qtable[self.pos] = {
                ACTION_UP: 0, ACTION_DOWN: 0, ACTION_LEFT: 0, ACTION_RIGHT: 0}
        if pos not in self.qtable:
            self.qtable[pos] = {ACTION_UP: 0, ACTION_DOWN: 0,
                                ACTION_LEFT: 0, ACTION_RIGHT: 0}
        # Q(s, a) += Q(s, a) + alpha * [r + gamma * max Q(s') - Q(s, a)]
        delta = learning_rate * (
            reward + discount_factor * max(self.qtable[pos].values()) - self.qtable[self.pos][action])
        self.qtable[self.pos][action] += delta
        self.pos = pos
        self.reward = reward
        self.score += reward
        self.iterations += 1

    def best_action(self):
        if self.pos in self.qtable:
            return arg_max(self.qtable[self.pos])
        else:
            return choice(list(ACTIONS.keys()))


class Environment:
    def __init__(self, maze):
        self.map = {}
        row, col = 0, 0
        for line in MAZE.strip().split('\n'):
            for char in line:
                self.map[row, col] = char
                if char == MAP_START:
                    self.start = (row, col)
                elif char == MAP_GOAL:
                    self.goal = (row, col)
                col += 1
            self.width = col
            row += 1
            col = 0
        self.height = row

    def do(self, pos, action):
        move = ACTIONS[action]
        new_pos = (pos[0] + move[0], pos[1] + move[1])
        if new_pos in self.map:
            if self.map[new_pos] == MAP_WALL:
                reward = REWARD_WALL
            else:
                pos = new_pos
                if self.map[new_pos] == MAP_GOAL:
                    reward = REWARD_GOAL
                else:
                    reward = REWARD_DEFAULT
        else:
            reward = REWARD_OUT
        return pos, reward


class MazeWindow(arcade.Window):
    sprite_agent: Optional[arcade.Sprite]
    sprite_goal: Optional[arcade.Sprite]
    walls: Optional[arcade.SpriteList[arcade.Sprite]]
    info: Optional[arcade.Text]
    history: list[int]

    def __init__(self, agent: "Agent") -> None:
        width = int(SPRITE_SIZE * SPRITE_SCALE * agent.env.width)
        height = int(SPRITE_SIZE * SPRITE_SCALE * agent.env.height)
        super().__init__(width, height, "Escape from ESGI")
        self.background_color = arcade.csscolor.BLACK
        self.agent = agent
        self.env = agent.env
        self.sprite_agent = None
        self.sprite_goal = None
        self.walls = None
        self.info = None
        self.history = []

    def pos_to_xy(self, pos, sprite):
        return (pos[1] + 0.5) * sprite.width, (self.env.height - pos[0] - .5) * sprite.height

    def setup(self):
        resource = arcade.load_texture(':resources:/images/enemies/bee.png')
        self.sprite_agent = arcade.Sprite(resource, SPRITE_SCALE)
        self.sprite_agent.center_x, self.sprite_agent.center_y = self.pos_to_xy(
            self.agent.pos, self.sprite_agent)

        resource = arcade.load_texture(':resources:/images/tiles/cactus.png')
        self.sprite_goal = arcade.Sprite(resource, SPRITE_SCALE)
        self.sprite_goal.center_x, self.sprite_goal.center_y = self.pos_to_xy(
            self.env.goal, self.sprite_goal)

        self.walls = arcade.SpriteList()
        for pos in self.env.map:
            if self.env.map[pos] == MAP_WALL:
                resource = arcade.load_texture(
                    ':resources:/images/tiles/brickBrown.png')
                sprite = arcade.Sprite(resource, SPRITE_SCALE)
                sprite.center_x, sprite.center_y = self.pos_to_xy(pos, sprite)
                self.walls.append(sprite)

        self.info = arcade.Text(
            f'{self.agent.iterations}', 10, 10, color=arcade.csscolor.BLACK, font_size=20)

    def on_draw(self):
        self.clear()
        self.walls.draw()
        arcade.draw_sprite(self.sprite_goal)
        arcade.draw_sprite(self.sprite_agent)
        self.info.draw()

    def on_update(self, delta_time: float) -> bool | None:
        self.info.text = f'#{self.agent.iterations} Score: {self.agent.score}'
        if self.agent.pos != self.env.goal:
            action = agent.best_action()
            agent.do(action)
            self.sprite_agent.center_x, self.sprite_agent.center_y = self.pos_to_xy(
                agent.pos, self.sprite_agent)

    def on_key_press(self, symbol: int, modifiers: int) -> EVENT_HANDLE_STATE:
        if symbol == arcade.key.R:
            self.history.append(self.agent.score)
            self.agent.reset()
        if symbol == arcade.key.Q:
            self.close()


if __name__ == "__main__":
    env = Environment(MAZE)
    agent = Agent(env)

    window = MazeWindow(agent)
    window.setup()
    arcade.run()

    plt.plot(window.history)
    plt.show()

    # score = 0
    # iterations = 0
    #
    # while agent.pos != env.goal:
    #     random_action = choice(list(ACTIONS.keys()))
    #     agent.do(random_action)
    #     score += agent.reward
    #     iterations += 1
    #
    # print(iterations)
