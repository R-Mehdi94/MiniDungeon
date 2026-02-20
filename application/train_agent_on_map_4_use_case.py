from domain.models.action import Action
from domain.models.environment import Environment
from infrastructure.agent import Agent
from infrastructure.data.map_4 import MAP_4


def train_agent_on_map_4_use_case(
        agent: Agent,

        new_experience_weight: float = 0.1,
        future_reward_weight: float = 0.95,
        initial_exploration_rate: float = 0.5,

) -> None:
    '''
    Runs the training of the agent on the training map.

    :param Agent agent: The agent to train. Its internal state and knowledge are updated across all episodes and maps.
    :param int episode_count: Number of training episodes to run. Each episode starts on the first map and continues until the agent finishes the episode or reaches the maximum number of steps.
    :param int max_steps_per_episode: Maximum number of steps allowed in a single episode. This prevents episodes from running indefinitely if the agent keeps wandering without finishing.
    :param float new_experience_weight: The learning rate. Between 0 and 1. Controls the strength of the new experience in relation to what the agent already knew. The higher the learning rate, the faster the agent "forgets" the old quality and adjusts to what it has just experienced.
    :param float future_reward_weight: This parameter, also known as discount factor, is used to weight the future rewards. Between 0 and 1. The higher this value is, the more importance is given to future rewards compared to immediate rewards.
    :param float initial_exploration_rate: The rate of the agent to do a random exploration action. It should not be 0 at the start of learning, otherwise the agent will always repeat the same mistakes and never explore the dungeon.
    :param float minimum_exploration_rate: The minimum exploration rate allowed.
    :param float exploration_decay_factor: The factor used to decay the exploration rate across episodes. It must be between 0 and 1. The smaller it is, the more the agent will rely on the knowledge acquired from previous episodes.
    '''
    environment = Environment(MAP_4)
    exploration_rate: float = initial_exploration_rate

    agent.environment = environment
    agent.reset()

    total_reward: int = 0

    action: Action = agent.choose_best_action()
    agent.execute_action_and_learn_from_reward(
        action,
        new_experience_weight,
        future_reward_weight,
    )
    total_reward += agent.reward

    print(

        f'exploration_rate={exploration_rate:.3f} - '
        f'total_reward={total_reward}'
    )