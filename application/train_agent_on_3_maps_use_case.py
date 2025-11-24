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
    new_experience_weight: float = 0.1,
    future_reward_weight: float = 0.95,
    initial_exploration_rate: float = 0.5,
    minimum_exploration_rate: float = 0.05,
    exploration_decay_factor: float = 0.995
) -> None:
    '''
    Runs the training of the agent on the 3 maps of the dungeon.

    :param Agent agent: The agent to train. Its internal state and knowledge are updated across all episodes and maps.
    :param list[list[str]] maps: The dungeon maps used as training levels.
    :param int episode_count: Number of training episodes to run. Each episode starts on the first map and continues until the agent finishes the episode or reaches the maximum number of steps.
    :param int max_steps_per_episode: Maximum number of steps allowed in a single episode. This prevents episodes from running indefinitely if the agent keeps wandering without finishing.
    :param float new_experience_weight: The learning rate. Between 0 and 1. Controls the strength of the new experience in relation to what the agent already knew. The higher the learning rate, the faster the agent "forgets" the old quality and adjusts to what it has just experienced.
    :param float future_reward_weight: This parameter, also known as discount factor, is used to weight the future rewards. Between 0 and 1. The higher this value is, the more importance is given to future rewards compared to immediate rewards.
    :param float initial_exploration_rate: The probability of the agent to do a random exploration action. It should not be 0 at the start of learning, otherwise the agent will always repeat the same mistakes and never explore the dungeon.
    :param float minimum_exploration_rate: The minimum exploration probability allowed.
    :param float exploration_decay_factor: The factor used to decay the exploration probability across episodes. It must be between 0 and 1. The smaller it is, the more the agent will rely on the knowledge acquired from previous episodes.
    '''
    environments: list[Environment] = [Environment(m) for m in maps]
    exploration_rate: float = initial_exploration_rate

    for episode in range(episode_count):
        current_level: int = 0
        agent.environment = environments[current_level]
        agent.reset()

        total_reward: int = 0

        for _ in range(max_steps_per_episode):
            action: Action = agent.choose_action_from_knowledge_or_random(exploration_rate)
            agent.execute_action_and_learn_from_reward(
                action,
                new_experience_weight,
                future_reward_weight,
            )
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
                f'Episode {episode + 1}/{episode_count} - '
                f'exploration_rate={exploration_rate:.3f} - '
                f'total_reward={total_reward}'
            )

        exploration_rate = max(
            minimum_exploration_rate,
            exploration_rate * exploration_decay_factor,
        )
