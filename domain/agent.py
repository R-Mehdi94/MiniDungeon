ACTION_UP = 'UP'
ACTION_DOWN = 'DOWN'
ACTION_LEFT = 'LEFT'
ACTION_RIGHT = 'RIGHT'

ACTIONS = {
    ACTION_UP: (-1, 0),
    ACTION_DOWN: (1, 0),
    ACTION_LEFT: (0, -1),
    ACTION_RIGHT: (0, 1)
}


class Agent:
    def __init__(self, env):
        self.env = env
        self.qtable = {}
        self.reset()

    def reset(self):
        self.pos = self.env.start
        self.has_key = False
        self.score = 0
        self.done = False

    def get_radar(self, pos):
        radar = {}
        for direction, (dr, dc) in ACTIONS.items():
            check_pos = (pos[0] + dr, pos[1] + dc)
            if check_pos in self.map:
                radar[direction] = self.map[check_pos]
            else:
                radar[direction] = None  # en dehors de la map
        return radar

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
