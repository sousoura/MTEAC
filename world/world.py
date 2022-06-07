from abc import ABCMeta, abstractmethod


"""
    抽象的世界类
        world project中的world.py中的类都需要继承这一超类
        该抽象类规定了world project中的具体的世界类的结构
"""


# 抽象的世界类
class World(metaclass=ABCMeta):
    """
        这三个变量分别规定了
            play_mode       该world project是否有game mode
            backgroundable  该world project是否支持后台
            statistical     该world project是否支持统计功能
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
            让特定id的实体执行ai的命令
        """
        pass

    @abstractmethod
    def evolution(self):
        """
            环境自然演化一回合
        """
        pass

    @abstractmethod
    def get_openai_action_space_and_observation_space(self):
        """
            以openai gym的格式 定义行动空间和状态空间
        """
        import gym
        action_space = gym.spaces.Discrete(1)
        observation_space = gym.spaces.Discrete(1)
        return action_space, observation_space

    @abstractmethod
    def translate_openai_command_to_mteac(self, mteac_state, openai_command):
        """
            将openai 的指令翻译为world project的格式
            若二者相同 则不用翻译
        """
        return openai_command

    @abstractmethod
    def translate_mteac_state_to_openai(self, mteac_state):
        """
            将 world project的state 翻译为openai所要求的格式
        """
        return mteac_state

    @abstractmethod
    def statistics(self, cmd):
        """
            统计方法
                可有可无 若实现了该方法 则可以将statistical赋值为True
                于是就可以在后台中进行统计了
        """
        pass
