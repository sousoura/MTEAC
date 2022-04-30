"""
    大脑可以用来思考和记忆
        得出行动的策略
        记忆情况
"""


from abc import ABCMeta, abstractmethod


class Brain(metaclass=ABCMeta):
    def __init__(self):
        self.memory = None

    @ abstractmethod
    def devise_an_act(self, perception, self_information):
        pass
