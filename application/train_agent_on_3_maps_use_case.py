from domain.models.action import Action
from domain.models.environment import Environment
from domain.models.map_constants import MAP_KEY
from domain.models.position import Position
from infrastructure.agent import Agent


def train_agent_on_3_maps_use_case(
    agent: Agent,
    maps: list[list[str]],
    episodes: int = 1000,
    max_steps_per_episode: int = 500,
    learning_rate: float = 0.1,
    discount_factor: float = 0.95,
    epsilon_start: float = 0.5,
    epsilon_min: float = 0.05,
    epsilon_decay: float = 0.995,
) -> None:
    envs: list[Environment] = [Environment(m) for m in maps]
    epsilon: float = epsilon_start

    for episode in range(episodes):
        current_level: int = 0
        agent.set_env(envs[current_level])
        agent.reset()

        total_reward: int = 0

        for _ in range(max_steps_per_episode):
            action: Action = agent.choose_action_epsilon_greedy(epsilon)
            agent.do(action, learning_rate, discount_factor)
            total_reward += agent.get_reward()

            env: Environment = agent.get_env()
            pos: Position = agent.get_pos()

            cell_char: str = env.get_map().get(pos, ' ')

            if cell_char == MAP_KEY:
                agent.set_has_key(True)

            if cell_char == 'D' and agent.get_has_key():
                current_level += 1
                if current_level >= len(envs):
                    agent.set_done(True)
                else:
                    next_env = envs[current_level]
                    agent.set_env(next_env)
                    agent.set_pos(next_env.get_start())
                    agent.set_has_key(False)

            if agent.is_done():
                break

        if (episode + 1) % 50 == 0:
            print(
                f'Épisode {episode + 1}/{episodes} - '
                f'epsilon={epsilon:.3f} - total_reward={total_reward}'
            )

        epsilon = max(epsilon_min, epsilon * epsilon_decay)
