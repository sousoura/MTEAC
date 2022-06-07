from abc import ABCMeta, abstractmethod


"""
    可视化器的超类
        该抽象类定义了world project中的可视化器的格式
        display()会在MTEAC类中的render()方法中被调用
        __init__的world参数是world project中的world的实例
"""
class Exhibitor_super:
    @abstractmethod
    def __init__(self, world, size_para):
        pass

    @abstractmethod
    def display(self, mode):
        """
            当有多个可视化方案时 可以通过mode参数选择
        """
        pass

    @abstractmethod
    def set_out(self):
        """
            退出可视化的方法
        """
        pass
