# ctypes，用于python和c++的交互
import ctypes

if __name__ == "__main__":
    import sys
    import os

    CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]  # 当前目录
    config_path = CURRENT_DIR.rsplit('\\', 2)[0]  # 上三级目录
    sys.path.insert(0, config_path)
    from state import State
    from world.entity.entity_import import *
    """
        here "blank_world"
    """
    from world.world_project.blank_world.entity.blank_entities import *
else:
    from world.state import State
    from world.entity.entity_import import *
    """
        here "blank_world"
    """
    from world.world_project.blank_world.entity.blank_entities import *


class Blank_state(State):

    def __init__(self):
        pass
