from domain.models.action import Action
from domain.models.environment import Environment
from domain.models.map_constants import MAP_KEY
from domain.models.position import Position
from infrastructure.agent import Agent


def train_agent_on_3_maps_use_case(
    agent: Agent,
    maps: list[list[str]],
    episode_count: int = 1000,
    max_steps_per_episode: int = 500,
    learning_rate: float = 0.1,
    discount_factor: float = 0.95,
    initial_exploration_probability: float = 0.5,
    minimum_exploration_probability: float = 0.05,
    exploration_decay_factor: float = 0.995
) -> None:
    '''
    Runs the training of the agent on the 3 maps of the dungeon.

    :param float initial_exploration_probability: The probability of the agent to do a random action exploration. It should not be 0 to allow, at the start of the learning, the agent to expore the dungeon, otherwise it will do everytime the same mistakes.
    :param float minimum_exploration_probability: The minimum of exploration probability allowed.
    :param float exploration_decay_factor: The factor to decay the probability of the agent to do an exploration random action over the episodes. It is between 0 and 1. The more it is close to 0, the more the agent will rely on its knowledge collected from previous episodes.
    :return: None
    :rtype: None
    '''
    environments: list[Environment] = [Environment(m) for m in maps]
    exploration_probability: float = initial_exploration_probability

    for episode in range(episode_count):
        current_level: int = 0
        agent.environment = environments[current_level]
        agent.reset()

        total_reward: int = 0

        for _ in range(max_steps_per_episode):
            action: Action = agent.choose_action_epsilon_greedy(exploration_probability)
            agent.execute_action_and_learn_from_reward(action, learning_rate, discount_factor)
            total_reward += agent.reward

            environment: Environment = agent.environment
            pos: Position = agent.position

            cell_char: str = environment.map.get(pos, ' ')

            if cell_char == MAP_KEY:
                agent.has_key = True

            if cell_char == 'D' and agent.has_key:
                current_level += 1
                if current_level >= len(environments):
                    agent.has_finished_episode = True
                else:
                    next_env = environments[current_level]
                    agent.environment = next_env
                    agent.position = next_env.starting_position
                    agent.has_key = False

            if agent.has_finished_episode:
                break

        if (episode + 1) % 50 == 0:
            print(
                f'Épisode {episode + 1}/{episode_count} - '
                f'epsilon={exploration_probability:.3f} - total_reward={total_reward}'
            )

        exploration_probability = max(minimum_exploration_probability, exploration_probability * exploration_decay_factor)
