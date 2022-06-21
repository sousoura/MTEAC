from abc import ABCMeta, abstractmethod


"""
    Abstract world generator class
        The world generator is used to generate a world
        If not use saver/loader then only default_generate_a_world will be called when generating the world
            default_generate_a_world specifies the initial state when a world is generated
        This class is waiting to be improved
"""


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
