from abc import ABCMeta, abstractmethod


"""
    抽象的世界生成器类
        世界生成器用于初始化参数化生成世界
        如果不使用存档/读档器 则只有default_generate_a_world会在生成世界的时候被调用
            default_generate_a_world规定了一个世界生成时的初始状态
        该类待改进
"""


# 抽象的世界生成器类 目前只有 生成世界这一个方法
class World_generator(metaclass=ABCMeta):
    @abstractmethod
    def generate_a_world(self, *generate_parameters):
        pass

    @abstractmethod
    def generate_a_world_by_state(self, *generate_parameters):
        pass

    @abstractmethod
    def default_generate_a_world(self, *generate_parameters):
        pass
