from abc import ABCMeta, abstractmethod


"""
    抽象的世界生成器类
    世界生成器用于初始化参数化生成世界
    由于抽象方法不够抽象 待修改
"""


# 抽象的世界生成器类 目前只有 生成世界这一个方法
class World_generator(metaclass=ABCMeta):
    @abstractmethod
    def generate_a_world(self, *generate_parameters):
        pass

    @abstractmethod
    def generate_a_world_by_state(self, *generate_parameters):
        pass
