from abc import ABCMeta, abstractmethod


"""
    The superclass for Exhibitor
        This abstract class defines the format of the Exhibitor in the world project
        display() will be called in the render() method of the MTEAC class
        The world parameter of __init__ is the instance of the world in the world project
"""
class Exhibitor_super:
    @abstractmethod
    def __init__(self, world, size_para):
        pass

    @abstractmethod
    def display(self, mode):
        """
            When there are multiple visualization schemes, it can be selected by the mode parameter
        """
        pass

    @abstractmethod
    def set_out(self):
        """
            Ways to exit visualization
        """
        pass
