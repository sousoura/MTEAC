import random

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
    def generate_a_world(self, maximum_height, map_size, landform_para, water_para, terrain_para, creature_para, obj_para):
        state = self.generate_a_state(maximum_height, map_size, landform_para, water_para, terrain_para, creature_para, obj_para)
        return World(state)

    def generate_a_state(self, maximum_height, terrain_size, landform_para, water_para, terrain_para, creature_para, obj_para):
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
        def generate_landform_map(maximum_height, columns, rows,
                                       peaks=None, mountains=None, valleys=None, pits=None):
            import random
            from world.world_project.mesh_world.landform import Peak
            # from landform import Pit

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
                    peaks.append(Peak.init_new_landform())

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

        def generate_water_map(water_para, landform_map):
            water_map = [[0 for a in range(terrain_size[1])] for i in range(terrain_size[0])]
            if water_para == "default_water":
                for row_index in range(len(landform_map)):
                    for col_index in range(len(landform_map[row_index])):
                        if landform_map[row_index][col_index] <= maximum_height / 1.2:
                            water_map[row_index][col_index] = 1

            builder_state = \
                self.building_a_state(landform_map, water_map,
                                      [[0 for a in range(terrain_size[0])] for b in range(terrain_size[1])],
                                      terrain_size, [], [])

            for time in range(100):
                builder_state.water_flow()

            return builder_state.get_water_map()

        def generate_terrain_map(terrain_para, landform_map, water_map):
            terrain_map = [[3 for a in range(terrain_size[1])] for i in range(terrain_size[0])]
            if terrain_para == "default_terrain":
                for row_index in range(terrain_size[1]):
                    for col_index in range(terrain_size[0]):
                        # 湿地生成
                        """
                            水深处为水底
                            水浅处为沼泽
                            湿处为湿地/泥地
                        """
                        # 所有地方都有小概率生成石地
                        # 99% 的概率不生成石地

                        """
                            定义相邻以及防止越界
                        """

                        left = row_index - 1
                        if left < 0:
                            left = 0

                        right = row_index + 1
                        if right >= terrain_size[0]:
                            right = terrain_size[0] - 1

                        up = col_index - 1
                        if up < 0:
                            up = 0

                        down = col_index + 1
                        if down >= terrain_size[1]:
                            down = terrain_size[1] - 1


                        if random.randrange(0, maximum_height * 700) > landform_map[row_index][col_index]:
                            if water_map[row_index][col_index] >= 2:
                                terrain_map[row_index][col_index] = 6
                                # 水多的地方一定概率生成碎地
                                if random.randrange(1, 1000) > 998:
                                    terrain_map[row_index][col_index] = 1
                                    terrain_map[right][col_index] = 1
                                    terrain_map[row_index][down] = 1
                                    terrain_map[right][down] = 1
                                    terrain_map[left][col_index] = 1
                                    terrain_map[row_index][up] = 1
                                    terrain_map[left][up] = 1
                                    terrain_map[left][down] = 1
                                    terrain_map[right][up] = 1
                            elif water_map[row_index][col_index] >= 1:
                                terrain_map[row_index][col_index] = 5
                            elif water_map[row_index][col_index] > 0.1:
                                terrain_map[row_index][col_index] = 4
                            else:
                                if random.randrange(1, 1000) >= 999:
                                    terrain_map[row_index][col_index] = 2
                            # 随机生成沙地
                        # 生成石地
                        else:
                            if random.randrange(1, 12) > 2:
                                terrain_map[row_index][col_index] = 0
                                terrain_map[right][col_index] = 0
                                terrain_map[row_index][down] = 0
                                terrain_map[right][down] = 0
                                terrain_map[left][col_index] = 0
                                terrain_map[row_index][up] = 0
                                terrain_map[left][up] = 0
                                terrain_map[left][down] = 0
                                terrain_map[right][up] = 0
                            else:
                                terrain_map[row_index][col_index] = 1
                                terrain_map[right][col_index] = 1
                                terrain_map[row_index][down] = 1
                                terrain_map[right][down] = 1
                                terrain_map[left][col_index] = 1
                                terrain_map[row_index][up] = 1
                                terrain_map[left][up] = 1
                                terrain_map[left][down] = 1
                                terrain_map[right][up] = 1

            # print()
            # for line in terrain_map:
            #     print(line)

            return terrain_map

        def random_creature(creature_list):
            creature_list.append(Wolf([1, 2], 5, brain=Wolf_brain()))
            creature_list.append(Wolf([4, 4], 5, brain=Wolf_brain()))
            creature_list.append(Human_being([3, 3], 5, brain=Human_brain()))
            creature_list.append(Human_being([3, 4], 5, brain=Human_brain()))
            creature_list.append(Human_being([3, 5], 5, brain=Human_brain()))
            creature_list.append(Human_being([2, 4], 5, brain=Human_brain()))

        def generate_creatures(creature_list):
            ''' 如果不给定具体参数 就用默认的生成方法 '''
            if creature_para == "random_creature":
                ''' 这里生成生物表 '''
                """
                    由于自动引入系统 会有红线 但是其实不是错误
                """
                random_creature(creature_list)

            else:
                ''' 参数生成 '''
                pass
            if obj_para == "random_obj":
                ''' 这里生成物体表 '''
                pass
            else:
                ''' 参数生成 '''
                pass

        landform_map = generate_landform_map(maximum_height, terrain_size[0], terrain_size[1])
        water_map = generate_water_map(water_para, landform_map)
        terrain_map = generate_terrain_map(terrain_para, landform_map, water_map)
        creature_list = []
        obj_list = []
        generate_creatures(creature_list)

        return self.building_a_state(landform_map, water_map, terrain_map, terrain_size, creature_list, obj_list)

    """
        输入属性值作为参数 生成状态
        返回一个状态
    """
    # 读档时用既有信息建造一个世界
    def building_a_state(self, landform_map, water_map, terrain_map, terrain_size, creature_list, obj_list):
        return State(landform_map, water_map, terrain_map, terrain_size, creature_list, obj_list)

    # 以state构造世界
    def generate_a_world_by_state(self, state):
        return World(state)
