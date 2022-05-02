from world.world_generator import World_generator
from world.world_project.mesh_world.mods import *
from world.world_project.mesh_world.entity.mesh_entities import *

"""
    世界类型为网格世界的世界的世界生成器
        世界生成器的职能为生成或初始化世界和状态
        把数据或任何东西变成世界或状态对象
"""


# 网格世界的世界生成器类
class Concrete_world_generator(World_generator):
    """
        输入构建参数 生成状态 根据状态生成一个世界
        返回一个世界
    """
    def generate_a_world(self, terrain_types_number, terrain_size, creature_para, obj_para):
        state = self.generate_a_state(terrain_types_number, terrain_size, creature_para, obj_para)
        return World(state)

    def generate_a_state(self, maximum_height, terrain_size, creature_para, obj_para):
        """ 随机生成特定大小的网格世界 """
        def randomMatrix(maximum_height, columns, rows):
            import random
            matrix = []
            for i in range(rows):
                matrix.append([])
                for j in range(columns):
                    matrix[i].append(random.randrange(maximum_height))
            return matrix

        """
            找到山峰 山脉 谷地 和 坑地的位置 然后生成地图
        """
        def high_low_terrain_generator(maximum_height, columns, rows,
                                       peaks=None, mountains=None, valleys=None, pits=None):
            import random
            from world.world_project.mesh_world.topograph import Peak
            # from topograph import Pit

            # 普通陆地高度
            normal_land_height = 3
            # 生成完全平面世界
            height_map = [[normal_land_height for i in range(rows)][:] for m in range(columns)]

            # 生成山峰们
            if not peaks:
                peaks = []
                # 决定山峰的数量 数量越多越接近山地 否则越接近平原
                peaks_num = max(columns * rows // 1000, 1)
                # peaks_num = 1

                # 随机生成数个山峰
                # 山峰具有属性： 峰值 峰面大小 坡度 范围
                Peak.init_random_seed(122213)
                Peak.init_map_size((rows, columns))
                Peak.init_high_range((2, maximum_height - normal_land_height - 2))
                for peak_id in range(peaks_num):
                    peaks.append(Peak.init_new_topograph())

            # 生成坑地们
            if not pits:
                pits = []

            # 地形影响
            for row_index in range(len(height_map)):
                for point_index in range(len(height_map[row_index])):
                    affect_sum = 0
                    # 每个山峰对该点的影响
                    for peak in peaks:
                        affect_sum += peak.affect((point_index, row_index))
                    height_map[row_index][point_index] += int(affect_sum)
                    height_map[row_index][point_index] = min(height_map[row_index][point_index], maximum_height)

            return height_map

        topograph = high_low_terrain_generator(maximum_height, terrain_size[0], terrain_size[1])
        creature_list = []
        obj_list = []

        ''' 如果不给定具体参数 就用默认的生成方法 '''
        if creature_para == "random_creature":
            ''' 这里生成生物表 '''
            """
                由于自动引入系统 会有红线 但是其实不是错误
            """
            creature_list.append(Wolf([1, 2], 5, brain=Wolf_brain()))
            creature_list.append(Wolf([4, 4], 5, brain=Wolf_brain()))
            creature_list.append(Human_being([3, 3], 5, brain=Human_brain()))
            creature_list.append(Human_being([3, 4], 5, brain=Human_brain()))
            creature_list.append(Human_being([3, 5], 5, brain=Human_brain()))
            creature_list.append(Human_being([2, 4], 5, brain=Human_brain()))

        else:
            ''' 参数生成 '''
            pass
        if obj_para == "random_obj":
            ''' 这里生成物体表 '''
            pass
        else:
            ''' 参数生成 '''
            pass
        return State(topograph, terrain_size, creature_list, obj_list)

    """
        输入属性值作为参数 生成状态
        返回一个状态
    """
    # 读档时用既有信息建造一个世界
    def building_a_state(self, terrain, terrain_size, creature_list, obj_list):
        return State(terrain, terrain_size, creature_list, obj_list)

    # 以state构造世界
    def generate_a_world_by_state(self, state):
        return World(state)
