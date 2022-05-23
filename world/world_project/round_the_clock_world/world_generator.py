import random
import math

from world.world_generator import World_generator
from world.world_project.round_the_clock_world.mods import *
from world.world_project.round_the_clock_world.entity.round_the_clock_entities import *

"""
    世界类型为网格世界的世界的世界生成器
        世界生成器的职能为生成或初始化世界和状态
        把数据或任何东西变成世界或状态对象
"""

"""
    特别注意：
        当表示二维数组的大小时
            如 map_size 为 (rows, columns)
                rows            代表了高度   代表了有几行      为高度
                columns         代表了宽度   代表了每行的长度   为宽度
        当表示二维数组的坐标时
            如 position 为 (row_index, column_index)
                row_index       代表了所在行数                 为纵坐标
                column_index    代表了所在的行数的第几个        为横坐标
"""


# 网格世界的世界生成器类
class Concrete_world_generator(World_generator):
    """
        输入构建参数 生成状态 根据状态生成一个世界
        返回一个世界
    """

    def generate_a_world(self, maximum_height, map_size, landform_para, water_para, terrain_para,
                         animals_para, plants_para, obj_para):
        state = self.generate_a_state(maximum_height, map_size, landform_para, water_para, terrain_para,
                                      animals_para, plants_para, obj_para)
        print("世界参数为:", "最大高度:", maximum_height, "地图大小:", map_size)
        return World(state)

    def generate_a_state(self, maximum_height, terrain_size, landform_para, water_para, terrain_para,
                         animals_para, plants_para, obj_para):

        """
            定义相邻以及防止越界
            row_index是行数 表示在第几行 高
            col_index是列数 表示在第几列 宽
        """

        def define_adjacent(row_index, col_index):
            left = col_index - 1
            if left < 0:
                left = 0

            right = col_index + 1
            if right >= terrain_size[1]:
                right = terrain_size[1] - 1

            up = row_index - 1
            if up < 0:
                up = 0

            down = row_index + 1
            if down >= terrain_size[0]:
                down = terrain_size[0] - 1

            return left, right, up, down

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

        def generate_landform_map(landform_para, maximum_height, rows, columns,
                                  peaks_para=None, mountains_para=None, valleys_para=None, pits_para=None):
            """
                :param landform_para: 生成模式的参数 可以为字符串或元组 为字符串的话可以为"default_landform"之类的 为元组时为生成参数
                :param maximum_height: 地图的最高高度
                :param columns: 地图有几列
                :param rows: 地图有几行
                :param peaks_para:
                :param mountains_para:
                :param valleys_para:
                :param pits_para:
                :return:

                eve在这里码代码 修改generate_landform_map函数 以及 landform类
                函数要创建一个height_map二维数组 结构是[[1, 4, 6, ...], [12, 5, 6, ...], ...]
                其中每个位置上的数字代表位置上的高度

                当landform_para == "default_landform"时采取默认的生成方式
                现在还没有定义别的生成方式

                现在想要加的是在landform里面加其它地形类型
                    现在已经有的是peak山峰
                    想用同样的原理生成山脉 山谷和坑
            """

            import random
            from world.world_project.mesh_world.landform import Peak
            # from world.world_project.mesh_world.landform import Pit

            # 普通陆地高度
            normal_land_height = 3
            print("\t默认陆地高度为:", normal_land_height)

            # 生成完全平面世界
            height_map = [[normal_land_height for i in range(columns)][:] for m in range(rows)]

            if landform_para == "default_landform":
                # 生成山峰们
                if not peaks_para:
                    peaks = []
                    # 决定山峰的数量 数量越多越接近山地 否则越接近平原
                    peaks_num = max(int(math.log(columns * rows, 2)), 1)
                    print("\t山峰数量为:", peaks_num)
                    # peaks_num = 1

                    # 随机生成数个山峰
                    # 山峰具有属性： 峰值 峰面大小 坡度 范围
                    Peak.init_random_seed(12456)
                    Peak.init_map_size((rows, columns))
                    Peak.init_high_range((2, (maximum_height - normal_land_height - 2) ** 0.5))
                    for peak_id in range(peaks_num):
                        peaks.append(Peak.init_new_landform())

                # 生成坑地们
                if not pits_para:
                    pits = []

                """
                    地形对地图的影响
                    开始改3们
                """
                # 地形影响
                for row_index in range(rows):
                    for column_index in range(columns):
                        affect_sum = 0
                        # 每个山峰对该点的影响
                        for peak in peaks:
                            affect_sum += peak.affect((row_index, column_index))
                        height_map[row_index][column_index] += int(affect_sum)
                        height_map[row_index][column_index] = min(height_map[row_index][column_index], maximum_height)

            return height_map

        # 生成水地圖
        def generate_water_map(water_para, landform_map):
            water_map = [[0 for a in range(terrain_size[1])] for i in range(terrain_size[0])]
            if water_para == "default_water":
                for row_index in range(terrain_size[0]):
                    for column_index in range(terrain_size[1]):
                        if landform_map[row_index][column_index] <= maximum_height / 1.2:
                            water_map[row_index][column_index] = 2

            builder_state = \
                self.building_a_state(maximum_height, landform_map, water_map,
                                      [[0 for a in range(terrain_size[1])] for b in range(terrain_size[0])],
                                      terrain_size, [], [], [])
            import time as Time
            start = Time.time()
            print("\t开始进行水流预演")
            for time in range(500):
                print("\t装在进行第", time, "次水流预演")
                builder_state.water_flow()
                # builder_state.water_flow_old()
            print("\t水流预演完毕")
            end = Time.time()
            print(end - start)

            return builder_state.get_water_map()

        # 生成地貌地圖
        def generate_terrain_map(terrain_para, landform_map, water_map):
            terrain_map = [[3 for a in range(terrain_size[1])] for i in range(terrain_size[0])]
            if terrain_para == "default_terrain":
                for row_index in range(terrain_size[0]):
                    for column_index in range(terrain_size[1]):
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
                        left, right, up, down = define_adjacent(row_index=row_index, col_index=column_index)

                        if random.randrange(0, maximum_height * 700) > landform_map[row_index][column_index]:
                            if water_map[row_index][column_index] >= 2:
                                terrain_map[row_index][column_index] = 6
                                # 水多的地方一定概率生成碎地
                                if random.randrange(1, 1000) > 998:
                                    terrain_map[row_index][column_index] = 1
                                    terrain_map[up][column_index] = 1
                                    terrain_map[row_index][down] = 1
                                    terrain_map[up][down] = 1
                                    terrain_map[down][column_index] = 1
                                    terrain_map[row_index][right] = 1
                                    terrain_map[down][right] = 1
                                    terrain_map[down][down] = 1
                                    terrain_map[up][right] = 1
                            elif water_map[row_index][column_index] >= 1:
                                terrain_map[row_index][column_index] = 5
                            elif water_map[row_index][column_index] > 0.1:
                                terrain_map[row_index][column_index] = 4
                            else:
                                if random.randrange(1, 1000) >= 999:
                                    terrain_map[row_index][column_index] = 2
                            # 随机生成沙地
                        # 生成石地
                        else:
                            if random.randrange(1, 12) > 2:
                                terrain_map[row_index][column_index] = 0
                                terrain_map[up][column_index] = 0
                                terrain_map[row_index][left] = 0
                                terrain_map[up][left] = 0
                                terrain_map[down][column_index] = 0
                                terrain_map[row_index][right] = 0
                                terrain_map[down][right] = 0
                                terrain_map[down][left] = 0
                                terrain_map[up][right] = 0
                            else:
                                terrain_map[row_index][column_index] = 1
                                terrain_map[up][column_index] = 1
                                terrain_map[row_index][left] = 1
                                terrain_map[up][left] = 1
                                terrain_map[down][column_index] = 1
                                terrain_map[row_index][right] = 1
                                terrain_map[down][right] = 1
                                terrain_map[down][left] = 1
                                terrain_map[up][right] = 1

            # print()
            # for line in terrain_map:
            #     print(line)

            return terrain_map

        def generate_animals(animals_para):
            animals_list = []

            ''' 如果不给定具体参数 就用默认的生成方法 '''
            if animals_para == "random_animals":
                ''' 这里生成生物表 '''
                """
                    由于自动引入系统 会有红线 但是其实不是错误
                """
                random_animals(animals_list)

            else:
                ''' 参数生成 '''
                pass

            return animals_list

        # 生成動物
        def random_animals(animal_list):
            animal_list.append(Human_being(position=[3, 3], life=100, brain=Human_brain(),
                                           full_value=70, drinking_value=70, body_state=0, gender=True,
                                           crawl_ability=1, speed=2, aggressivity=50
                                           ))
            animal_list.append(Wolf(position=[1, 15], life=100, brain=Wolf_brain(),
                                    full_value=70, drinking_value=70, body_state=0, gender=True,
                                    crawl_ability=1, speed=2, aggressivity=50
                                    ))
            animal_list.append(Alpaca(position=[10, 10], life=100, brain=Alpaca_brain(),
                                      full_value=70, drinking_value=70, body_state=0,
                                      gender=True,
                                      crawl_ability=4, speed=1, aggressivity=5
                                      ))
            animal_list.append(Wolf(position=[1, 3], life=100, brain=Wolf_brain(),
                                    full_value=70, drinking_value=70, body_state=0, gender=True,
                                    crawl_ability=1, speed=2, aggressivity=50
                                    ))
            animal_list.append(Human_being(position=[3, 4], life=100, brain=Human_brain(),
                                           full_value=70, drinking_value=70, body_state=0,
                                           gender=True,
                                           crawl_ability=1, speed=2, aggressivity=50
                                           ))
            animal_list.append(Human_being(position=[3, 5], life=100, brain=Human_brain(),
                                           full_value=70, drinking_value=70, body_state=0,
                                           gender=True,
                                           crawl_ability=1, speed=2, aggressivity=50
                                           ))
            animal_list.append(Human_being(position=[2, 4], life=100, brain=Human_brain(),
                                           full_value=70, drinking_value=70, body_state=0,
                                           gender=True,
                                           crawl_ability=1, speed=2, aggressivity=50
                                           ))
            animal_list.append(Mouse(position=[10, 4], life=100, brain=Mouse_brain(),
                                     full_value=70, drinking_value=70, body_state=0,
                                     gender=True,
                                     crawl_ability=4, speed=1, aggressivity=5
                                     ))
            animal_list.append(Mouse(position=[2, 10], life=100, brain=Mouse_brain(),
                                     full_value=70, drinking_value=70, body_state=0,
                                     gender=True,
                                     crawl_ability=4, speed=1, aggressivity=5
                                     ))
            animal_list.append(Fish(position=[6, 45], life=100, brain=Fish_brain(),
                                    full_value=70, drinking_value=70, body_state=0,
                                    gender=True,
                                    crawl_ability=1, speed=1, aggressivity=5
                                    ))
            animal_list.append(Fish(position=[43, 45], life=100, brain=Fish_brain(),
                                    full_value=70, drinking_value=70, body_state=0,
                                    gender=True,
                                    crawl_ability=1, speed=1, aggressivity=5
                                    ))

        # 生成植物
        def generate_plants(plants_para, landform_map, water_map, terrain_map):
            plants_list = []

            if plants_para == "random_plants":
                for row_index in range(terrain_size[0]):
                    for col_index in range(terrain_size[1]):
                        """
                            定义相邻以及防止越界
                        """
                        left, right, up, down = define_adjacent(col_index=col_index, row_index=row_index)
                        """
                            列数 col_index 就是横坐标
                            行数 row_index 就是纵坐标
                        """
                        # 水深的地方长水草
                        if terrain_map[row_index][col_index] > 4:
                            if random.randrange(1, 10000) >= 9000:
                                plants_list.append(Algae((row_index, col_index)))
                        # 水浅的地方既可能长水草也可能长普通草
                        elif terrain_map[row_index][col_index] == 4:
                            if random.randrange(1, 10000) >= 9890:
                                plants_list.append(Algae((row_index, col_index)))
                            elif random.randrange(1, 10000) >= 9890:
                                plants_list.append(Grass((row_index, col_index)))
                        # 普通土地长草和树
                        elif terrain_map[row_index][col_index] == 3:
                            # 长草
                            if random.randrange(1, 10000) >= 9890:
                                plants_list.append(Grass((row_index, col_index)))
                            # 长草地
                            elif random.randrange(1, 10000) >= 9900:
                                plants_list.append(Grassland((row_index, col_index)))
                                # 草地旁边的单个草
                                plants_list.append(Grass((up, col_index)))
                                plants_list.append(Grass((row_index, right)))
                                plants_list.append(Grass((down, col_index)))
                                plants_list.append(Grass((row_index, left)))
                                plants_list.append(Grass((up, left)))
                                plants_list.append(Grass((up, right)))
                                plants_list.append(Grass((down, right)))
                                plants_list.append(Grass((down, left)))
                            # 长树
                            elif random.randrange(1, 10000) >= 9990:
                                plants_list.append(Birch((row_index, col_index)))
                            # 长树林
                            elif random.randrange(1, 10000) >= 9990:
                                plants_list.append(Birch_wood((row_index, col_index)))
                                # 林子旁边的单个树
                                plants_list.append(Birch((up, col_index)))
                                plants_list.append(Birch((row_index, right)))
                                plants_list.append(Birch((down, col_index)))
                                plants_list.append(Birch((row_index, left)))
                                plants_list.append(Birch((up, left)))
                                plants_list.append(Birch((up, right)))
                                plants_list.append(Birch((down, right)))
                                plants_list.append(Birch((down, left)))

            return plants_list

        # 生成物品
        def generate_objs(obj_para):
            obj_list = []
            if obj_para == "random_obj":
                ''' 这里生成物体表 '''
                obj_list.append(Stone([5, 5]))
                obj_list.append(Wood([5, 5]))
                obj_list.append(Wood([5, 5]))
                obj_list.append(Wood([5, 5]))
                obj_list.append(Wood([5, 5]))
                obj_list.append(Wood([5, 5]))
                obj_list.append(Axe([5, 5]))
                obj_list.append(Cart([8, 8]))
            else:
                ''' 参数生成 '''
                pass

            return obj_list

        # 生成地图
        print("正在生成地势...")
        landform_map = generate_landform_map(landform_para, maximum_height, terrain_size[0], terrain_size[1])
        print("正在生成水高...")
        water_map = generate_water_map(water_para, landform_map)
        print("正在生成地貌...")
        terrain_map = generate_terrain_map(terrain_para, landform_map, water_map)

        # 生成实体
        print("正在生成动物...")
        animals_list = generate_animals(animals_para)
        print("正在生成植物...")
        plants_list = generate_plants(plants_para, landform_map, water_map, terrain_map)
        print("正在生成物品...")
        obj_list = generate_objs(obj_para)
        print("状态生成完毕！")

        return self.building_a_state(maximum_height, landform_map, water_map, terrain_map, terrain_size,
                                     animals_list, plants_list, obj_list)

    """
        输入属性值作为参数 生成状态
        返回一个状态
    """

    # 读档时用既有信息建造一个世界
    def building_a_state(self, maximum_height, landform_map, water_map, terrain_map, terrain_size, animals_list,
                         plants_list, obj_list):
        return State(maximum_height, landform_map, water_map, terrain_map, terrain_size, animals_list,
                     plants_list, obj_list)

    # 以state构造世界
    def generate_a_world_by_state(self, state):
        return World(state)

    def default_generate_a_world(self):
        return self.generate_a_world(maximum_height=30, map_size=(50, 100),
                                     animals_para="random_animals", plants_para="random_plants",
                                     obj_para="random_obj",
                                     water_para="default_water",
                                     landform_para="default_landform",
                                     terrain_para="default_terrain")
