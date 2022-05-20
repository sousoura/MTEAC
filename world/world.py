from abc import ABCMeta, abstractmethod


"""
    抽象的世界类
    不同的世界类型中有具体的世界类 会继承抽象的世界类
    世界具有状态属性和变化方法
        状态属性是状态类的实例 修改状态类可以改变世界的组成和变化规律
        变化方法规定了世界运行一次的变化
"""


# 抽象的世界类
class World(metaclass=ABCMeta):
    play_mode = False
    backgroundable = False
    statistical = False

    @abstractmethod
    def __init__(self, state):
        self.state = state

    @abstractmethod
    def take_action(self):
        pass

    @abstractmethod
    def evolution(self):
        pass

    @abstractmethod
    def get_openai_action_space_and_observation_space(self):
        pass

    @abstractmethod
    def translate_openai_command_to_mteac(self, mteac_state, openai_command):
        pass

    @abstractmethod
    def translate_mteac_state_to_openai(self, mteac_state):
        pass

    @abstractmethod
    def statistics(self, cmd):
        pass
