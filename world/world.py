from abc import ABCMeta, abstractmethod


"""
    Abstract world class
        World class in world.py in the world project need to inherit this superclass
        This abstract class specifies the structure of the concrete world class in the world project
"""


# Abstract world class
class World(metaclass=ABCMeta):
    """
        These three class variables specify
            play_mode       Whether the world project support game mode
            backgroundable  Whether the world project supports background
            statistical     Whether the world project supports statistic function
    """
    play_mode = False
    backgroundable = False
    statistical = False

    @abstractmethod
    def __init__(self, state):
        self.state = state

    @abstractmethod
    def take_action(self, player_cmd, ai_id):
        """
            Let the entity with a specific id execute the command of ai
        """
        pass

    @abstractmethod
    def evolution(self):
        """
            One round of evolution of the environment itself
        """
        pass

    @abstractmethod
    def get_openai_action_space_and_observation_space(self):
        """
            Define action space and state space in openai gym format
        """
        import gym
        action_space = gym.spaces.Discrete(1)
        observation_space = gym.spaces.Discrete(1)
        return action_space, observation_space

    @abstractmethod
    def translate_openai_command_to_mteac(self, mteac_state, openai_command):
        """
            Translate openai's instructions into world project format
            If the two are the same, no translation is required
        """
        return openai_command

    @abstractmethod
    def translate_mteac_state_to_openai(self, mteac_state):
        """
            Translate the state of the world project into the format required by openai
        """
        return mteac_state

    @abstractmethod
    def statistics(self, cmd):
        """
            statistic function
                It is optional, if you implement this method, you can assign statistical to True
        """
        pass
