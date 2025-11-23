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
    epsilon_decay: float = 0.995
) -> None:
    envs: list[Environment] = [Environment(m) for m in maps]
    epsilon: float = epsilon_start

    for episode in range(episodes):
        current_level: int = 0
        agent.environment = envs[current_level]
        agent.reset()

        total_reward: int = 0

        for _ in range(max_steps_per_episode):
            action: Action = agent.choose_action_epsilon_greedy(epsilon)
            agent.execute_action_and_learn_from_reward(action, learning_rate, discount_factor)
            total_reward += agent.reward

            environment: Environment = agent.environment
            pos: Position = agent.position

            cell_char: str = environment.map.get(pos, ' ')

            if cell_char == MAP_KEY:
                agent.has_key = True

            if cell_char == 'D' and agent.has_key:
                current_level += 1
                if current_level >= len(envs):
                    agent.has_finished_episode = True
                else:
                    next_env = envs[current_level]
                    agent.environment = next_env
                    agent.position = next_env.starting_position
                    agent.has_key = False

            if agent.has_finished_episode:
                break

        if (episode + 1) % 50 == 0:
            print(
                f'Épisode {episode + 1}/{episodes} - '
                f'epsilon={epsilon:.3f} - total_reward={total_reward}'
            )

        epsilon = max(epsilon_min, epsilon * epsilon_decay)
