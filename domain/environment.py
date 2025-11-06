MAP_START = 'P'
MAP_WALL = "W"
MAP_GOAL = "T"
MAP_KEY = "K"

REWARD_WALL = -10
REWARD_DEFAULT = -1
REWARD_KEY = 10
REWARD_GOAL = 1000
REWARD_OUT = -10


class Environment:
    def __init__(self, map_layout):
        self.map = {}
        row, col = 0, 0
        for line in map_layout:

            for char in line:
                self.map[row, col] = char
                if char == MAP_START:
                    self.start = (row, col)
                elif char == MAP_KEY:
                    self.key = (row, col)
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
                if self.map[new_pos] == MAP_KEY:
                    reward = REWARD_KEY

                elif self.map[new_pos] == MAP_GOAL:
                    reward = REWARD_GOAL
                else:
                    reward = REWARD_DEFAULT
        else:
            reward = REWARD_OUT
        return pos, reward
