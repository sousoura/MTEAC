from abc import ABCMeta, abstractmethod


class Exhibitor_super:
    @abstractmethod
    def __init__(self, world, size_para):
        pass

    @abstractmethod
    def display(self, mode):
        pass

    @abstractmethod
    def set_out(self):
        pass
