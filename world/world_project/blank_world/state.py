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
    from world.world_project.mesh_world.entity.mesh_entities import *
else:
    from world.state import State
    from world.entity.entity_import import *
    from world.world_project.mesh_world.entity.mesh_entities import *


class Blank_state(State):
    # 有 terrain_range + 1 种地形
    terrain_range = 0
    # 有 entity_type_num 种实体
    entity_type_num = 0

    mteac_command_list = []

    mteac_direction_list = []

    entity_types = []

    def __init__(self, terrain_size):

        pass

        super(Blank_state, self).__init__(terrain_size)

        # c++代码模块
        CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]  # 当前目录
        config_path = CURRENT_DIR.rsplit('\\', 3)[0]  # 上三级目录

        dll_name = "MTEAC-C++.dll"
        self.pDll = ctypes.CDLL(config_path + "/c++/" + dll_name)
        self.Double_Len = ctypes.c_double * (self.terrain_size[0] * self.terrain_size[1])
        self.in_water_map = self.Double_Len()
        self.in_landform_map = self.Double_Len()

    # 返回地图大小
    def get_terrain_size(self):
        return self.terrain_size
