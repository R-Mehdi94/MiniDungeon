from domain.models.action import Action
from domain.models.environment import Environment
from infrastructure.agent import Agent
from infrastructure.data.map_4 import MAP_4


def train_agent_on_map_4_use_case(
    agent: Agent,
    episodes: int = 1000,
    max_steps_per_episode: int = 500,
    learning_rate: float = 0.1,
    discount_factor: float = 0.95,
    initial_exploration_probability: float = 0.5,
    minimum_exploration_probability: float = 0.05,
    exploration_decay_factor: float = 0.995,
) -> None:
    '''
    Trains the agent only on MAP_4 using Q-learning with an epsilon-greedy
    (exploration_probability) policy.
    '''
    environment = Environment(MAP_4)
    exploration_probability: float = initial_exploration_probability

    for episode in range(episodes):
        agent.environment = environment
        agent.reset()

        total_reward: int = 0

        for _ in range(max_steps_per_episode):
            action: Action = agent.choose_action_epsilon_greedy(exploration_probability)
            agent.execute_action_and_learn_from_reward(
                action,
                learning_rate,
                discount_factor,
            )
            total_reward += agent.reward

            if agent.has_finished_episode:
                break

        if (episode + 1) % 50 == 0:
            print(
                f'Episode {episode + 1}/{episodes} - '
                f'exploration_probability={exploration_probability:.3f} - '
                f'total_reward={total_reward}'
            )

        exploration_probability = max(
            minimum_exploration_probability,
            exploration_probability * exploration_decay_factor,
        )
