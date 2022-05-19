import random
# ctypes，用于python和c++的交互
import ctypes
# 用于将多维数组转为一维数组
from itertools import chain

if __name__ == "__main__":
    import sys
    import os

    CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]  # 当前目录
    config_path = CURRENT_DIR.rsplit('\\', 2)[0]  # 上三级目录
    sys.path.insert(0, config_path)
    from state import State
else:
    from world.state import State
    from world.entity.entity_import import *
    from world.world_project.mesh_world.entity.mesh_entities import *

"""
    网格状态
        其具有属性：
            地形               用两层列表表示的方块的网格的世界
                高低地形        某个格子的高度 目前用整数表示 以后会变成小数
                水地图          某个地方的水高 水每回合会流动
                地貌地形        某个格子是泥地 沙地还是石头地
            生物列表            生物对象的列表
                动物表
                植被表          某个各自的有没有树木 是不是草地
                    地形大小     网格世界的大小
                位置-动物、植物字典   由位置找到位置上的生物的字典
            物品列表            存物品对象的列表
        网格世界的方法全都有关于状态的修改或状态
            一回合内各个属性的变化的方法
                动物行为 animal_action和animal_act
                    动物移动        moving_a_pace
                    动物吃          animal_eating
                地形变化            (去掉了)
                ...
            更新属性的方法
                renew_map
            规定空间属性的方法
                规定「相邻」的方法   position_and_direction_get_adjacent
            得到某生物的类型的方法    print_show_animal（注释掉了）
            得到状态属性的方法
                得到各个属性的方法   
                初始化位置词典的方法  init_things_position
"""


class Mesh_state(State):
    # 有 terrain_range + 1 种地形
    terrain_range = 6
    # 有 entity_type_num 种实体
    entity_type_num = 22

    def __init__(self, maximum_height, landform_map, water_map, terrain_map, terrain_size, animals, plants, objects):
        """
        :param landform_map:   类型：二维数组 值为int      意义表示：每个值都是整形 表示高低地形 数字越高地形越高
        :param terrain_size:    类型：二元元组             意义表示：地图大小 第0个值是行数 第1个值是列数
        :param animals:       类型：列表 值为动物对象      意义表示：世界中的所有生物
        :param objects:         类型：列表 值为物品对象      意义表示：世界中的所有物品
        """
        # 地图
        self.maximum_height = maximum_height
        self.landform_map = landform_map
        self.water_map = water_map
        self.terrain_map = terrain_map

        # 地图属性
        super(Mesh_state, self).__init__(terrain_size)
        self.legal_direction = ["up", "down", "left", "right", "stay"]

        # 实体表
        self.animals = animals
        self.plants = plants
        self.objects = objects

        # 得到位置字典 方便根据位置找到生物 而不必总是遍历生物表 以空间换时间
        self.animals_position = self.init_position_list(self.animals)
        self.plants_position = self.init_position_list(self.plants)
        self.objs_position = self.init_position_list(self.objects)

        # c++代码模块
        self.pDll = ctypes.CDLL("c++/MTEAC-C++.dll")
        self.Double_Len = ctypes.c_double*(self.terrain_size[0]*self.terrain_size[1])
        self.in_water_map = self.Double_Len()
        self.in_landform_map = self.Double_Len()

    """
        ***
            以下是动物的运动
        ***
        输入  player_cmd：玩家指令 为数组 格式是[第一段, 第二段, 第三段_...]
                一般默认第一段为动作类型 第二段为动作对象 第三段为动作参数
            中间的if 如果该生物被判断为是玩家控制的 就会使用玩家指令 否则就使用大脑返回的指令
            指令分段 不同段用_隔开
                第一段是类型 目前只有eat和go
                    go的第二段是四个方向中的一个
                    eat的第二段也是 作为吃这个动作的方向 第三段是吃的对象 不过还没有实现
        效果  某个动作被执行的效果
    """

    def player_action(self, player_cmd):
        # 判断是否输入指令
        if not player_cmd:
            return

        if len(self.animals) == 0:
            print("死光光咯")
            return

        player = self.animals[0]
        if not player.is_id(1):
            print("警告：玩家不在第一位")
            return
        if not player.is_die():
            cmd = player_cmd
            # 根据指令进行操作
            self.animal_action_command_analysis_and_execute(player, cmd)
            player.post_turn_change()

    # 更新动物行为
    # 一回合内的动物运动
    def animal_action(self):
        # 遍历生物表
        for animal in self.animals:
            # 判断生物是否死亡
            if not animal.is_die():
                cmd = animal.devise_an_act(animal.get_perception(self.landform_map, self.animals_position))
                """
                    判断该对象是不是玩家
                    判断有没有指令
                """
                if animal.is_id(1):
                    continue
                # 根据指令进行操作
                self.animal_action_command_analysis_and_execute(animal, cmd)
                animal.post_turn_change()
            else:
                self.creature_die(animal)
                del animal

    # 分析生物行动命令的基本类型 并调用相应的执行函数
    def animal_action_command_analysis_and_execute(self, animal, command):
        """
            command指令的数据结构类似: ["go", 方向]
            首先进行合法性判断 然后进行行为本身
        """

        """
           基本行为的行为次数判断
        """
        def basic_act_number(animal, command):
            time = 1
            if command[0] == "go":
                time = animal.get_pace()
            return time

        """
            行为合法性判断方法
        """
        def judge_action_validity(animal, command):
            return animal.judge_action_validity(self, command)

        # 判断基本行为执行几次
        # 中间行为不合法则中断后面的行为
        for time in range(int(basic_act_number(animal, command))):
            # 产生尝试该行为造成的成本
            animal.action_cost(command[0])
            if judge_action_validity(animal, command):
                self.animal_action_command_execute(animal, command)
            else:
                break

    # 执行指令 改变世界和生物的状态
    def animal_action_command_execute(self, animal, command):
        if command[0] == 'go':
            # 走一步
            self.moving_a_pace(animal, command[1])
        elif command[0] == 'eat':
            # 动物吃生物
            self.animal_eating(animal, command[2])
        elif command[0] == 'drink':
            # 动物喝水
            self.animal_drinking(animal, command[1])
        elif command[0] == 'attack':
            # 动物攻击
            self.animal_attack(animal, command[2])
        elif command[0] == 'rest':
            # 动物休息
            self.animal_rest(animal)
        elif isinstance(animal, Human):
            if command[0] in animal.action_list:
                # 人类行为
                self.human_action(animal, command)

    """
        输入  某个生物实例 移动的方向
        效果  会分析移动是否合法 如果合法 则移动之 改变生物的位置状态并更新位置表 反之 不移动之
    """
    # 生物移动 外部和内部执行
    def moving_a_pace(self, animal, direction):
        old_position = tuple(animal.get_position())
        new_position = self.position_and_direction_get_new_position(old_position, direction)

        # 执行移动 改变状态（但是不改变生物的属性）
        self.change_animal_position(animal, old_position, new_position)
        # 行动成功对于动物的内部影响
        animal.action_interior_outcome(action_type="go", parameter=new_position)

    # old_position + direction = new_position
    def position_and_direction_get_new_position(self, old_position, direction):
        # 判断移动合法性和移动种类
        def judge_movement_legality(old_position, new_position):
            """
                移动判断是否合法 属于哪一类
                之所以返回2和-2是因为1和0对应了True和False
            """
            if new_position:
                # 升一格移动
                if self.landform_map[new_position[0]][new_position[1]] - \
                        self.landform_map[old_position[0]][old_position[1]] == 1:
                    return 2
                # 降一格移动
                elif self.landform_map[new_position[0]][new_position[1]] - \
                        self.landform_map[old_position[0]][old_position[1]] == -1:
                    return -2
                # 同级移动
                return True
            # 新位置超出地图 为空对象
            # 冗余判断
            return False

        if direction == 'stay':
            return tuple(old_position)

        # 若在左右半格上
        if old_position[0] % 1 > 0:
            stride = 0.5
            if direction == 'down':
                if old_position[0] < self.terrain_size[0] - 1:
                    return old_position[0] + stride, old_position[1]
            elif direction == 'up':
                if old_position[0] > 0:
                    return old_position[0] - stride, old_position[1]
        # 若在上下半格上
        elif old_position[1] % 1 > 0:
            stride = 0.5
            if direction == 'right':
                if old_position[1] < self.terrain_size[1] - 1:
                    return old_position[0], old_position[1] + stride
            elif direction == 'left':
                if old_position[1] > 0:
                    return old_position[0], old_position[1] - stride
        # 若不在半格上
        else:
            old_position = (int(old_position[0]), int(old_position[1]))
            adjacent = self.position_and_direction_get_adjacent(old_position, direction)
            # 若升格移动
            kakusa = judge_movement_legality(old_position, adjacent)
            if kakusa == 2:
                return old_position[0] + (adjacent[0] - old_position[0]) * 0.5, \
                       old_position[1] + (adjacent[1] - old_position[1]) * 0.5
            # 若降格移动
            elif kakusa == -2:
                return adjacent
            # 若平级移动
            elif kakusa:
                return adjacent

        return False

    # 生物吃
    """
        生物的吃行为
        输入      吃的主体 方向 客体
    """

    def animal_eating(self, eator, be_eator):

        # 动物内部改变 吃者和被吃者状态变化
        eator.action_interior_outcome("eat", obj=be_eator)
        # 若被吃完 被吃者消失(死亡)
        if be_eator.be_ate(eator):
            # 地图改变
            self.eliminate_exist_in_map(be_eator)
            del be_eator

    # 生物喝
    """
        生物的喝水行为
        输入      吃的主体 方向
    """

    def animal_drinking(self, drinker, direction):
        drinker.action_interior_outcome("drink", parameter=direction)

    # 生物攻击
    """
        生物的喝水行为
        输入      吃的主体 攻击的对象
    """

    def animal_attack(self, attacker, be_attackeder):
        # 动物内部改变 攻击者和被攻击者状态变化
        attacker.action_interior_outcome("attack", obj=be_attackeder)
        be_attackeder.be_attack(attacker.get_aggressivity())

        # 若被杀死 被杀者消失(死亡)
        if be_attackeder.is_die():
            # 地图改变
            self.creature_die(be_attackeder)
            del be_attackeder

    # 生物休息
    def animal_rest(self, rester):
        pass

    # 人类行为
    def human_action(self, human, command):
        def human_pick_up(state, human, obj):
            human.action_interior_outcome("pick_up", obj=obj)
            state.eliminate_exist_in_map(obj)

        def human_put_down(state, human, direction, obj):
            human.action_interior_outcome("put_down", obj=obj)
            new_position = state.position_and_direction_get_adjacent(human.get_position(), direction)
            state.add_exist_to_map(obj, new_position)
            obj.new_position(new_position)

        def human_construct(state, human, direction, objs):
            # 生成新物品
            new_position = self.position_and_direction_get_adjacent(human.get_position(), direction)[:]
            item_names = human.composed_table[names_orderly_tuplize(objs)]
            for item_name in item_names:
                self.add_exist_to_map(globals()[item_name](new_position))
            # 抹去成本物体的存在
            human.action_interior_outcome("construct", obj=objs)
            for item in objs:
                if item in state.objects:
                    state.eliminate_exist_in_map(item)

        def human_collect_things(state, human, direction):
            gether_things = []

            # 得到收集处
            direction = command[1]
            direction_position = state.position_and_direction_get_adjacent(human.get_position(), direction)

            # 收集处是否有森林
            if tuple(direction_position) in state.get_plants_position():
                for plant in state.get_plants_position()[tuple(direction_position)]:
                    if isinstance(plant, (Birch_wood,)):
                        gether_things.append(Wood(human.get_position()))
                        human.action_interior_outcome("collect", obj=gether_things)
                        return

            # 收集处是否是可收集地貌
            if direction_position:
                terrain_type = state.get_terrain_map()[int(direction_position[0])][int(direction_position[1])]
                thing_type = ["Stone", "Sandpile", "Soil_pile"][human.collectable.index(terrain_type)]

                """
                    待补充：目前还没有桶 人无法捡起沙子和泥土
                """
                if thing_type == "Stone":
                    gether_things.append(Stone(human.get_position()))
                    human.action_interior_outcome("collect", obj=gether_things)
                    return
                else:
                    print("暂不能收集沙子和泥土")

        def human_push(state, human, derection, obj):
            human_old_position = tuple(human.get_position())
            human_new_position = state.position_and_direction_get_new_position(human_old_position, derection)

            # 执行移动 改变状态（但是不改变生物的属性）
            state.change_animal_position(human, human_old_position, human_new_position)
            # 行动成功对于动物的内部影响
            human.action_interior_outcome(action_type="push", parameter=human_new_position)

            obj_old_position = tuple(obj.get_position())
            obj_new_position = state.position_and_direction_get_adjacent(obj_old_position, derection)

            if obj_new_position in state.objs_position:
                state.objs_position[obj_new_position].append(obj)
            else:
                state.objs_position[obj_new_position] = [obj]

            state.objs_position[obj_old_position].remove(obj)
            if len(state.objs_position[obj_old_position]) == 0:
                del state.objs_position[obj_old_position]

            obj.new_position(list(obj_new_position))

        if command[0] == "pick_up":
            human_pick_up(self, human, command[2])

        elif command[0] == "put_down":
            human_put_down(self, human, command[1], command[2])

        elif command[0] == "handling":
            human.action_interior_outcome("handling", obj=command[2])

        elif command[0] == "fabricate":
            human.action_interior_outcome("fabricate", obj=command[2])

        elif command[0] == "construct":
            human_construct(self, human, command[1], command[2])

        elif command[0] == "collect":
            human_collect_things(self, human, command[1])

        elif command[0] == "push":
            human_push(self, human, command[1], command[2])

    """
        ***
            以下是水地图的更新
        ***
    """

    # double * c_water_flow(int terrain_row, int terrain_col, double * in_water_map, double * in_landform_map, char * in_legal_direction)

    def water_flow(self):
        # 数据初始化

        legal_direction = ctypes.c_char_p()
        for y in range(0, self.terrain_size[0]):
            for x in range(0, self.terrain_size[1]):
                self.in_water_map[y * self.terrain_size[1] + x] = self.water_map[y][x]
                self.in_landform_map[y * self.terrain_size[1] + x] = self.landform_map[y][x]


        legal_str = "\n".join(self.legal_direction)
        legal_str += "\0"
        legal_direction.value = legal_str.encode("utf-8")

        # for char in legal_direction.value:
        #     print(char)


        self.pDll.c_water_flow.restype = ctypes.POINTER(ctypes.c_double)
        # c++代码返回的会是一维数组形式的水地图
        # s = input("input 312312312s1")
        map_array = self.pDll.c_water_flow(self.terrain_size[0], self.terrain_size[1],
                                      self.in_water_map, self.in_landform_map, legal_direction)
        # for num in map_array:
        #     print(num,end=" ")
        # print(" ")
        # print(map_array)

        # self.water_map = []
        for y in range(0, self.terrain_size[0]):
            for x in range(0, self.terrain_size[1]):
                self.water_map[y][x] = (map_array[x + y * self.terrain_size[1]])

    def water_flow_old(self):
        # 遍历水地图
        for row_index in range(self.terrain_size[0]):
            for col_index in range(self.terrain_size[1]):
                # 若自身相对水高低于0.1 则被土地吸收
                if self.water_map[row_index][col_index] < 0.1:
                    self.water_map[row_index][col_index] = 0
                    continue

                # 得到自己的绝对水高
                absolute_water_high = self.water_map[row_index][col_index] + self.landform_map[row_index][col_index]
                land_high = self.landform_map[row_index][col_index]

                # 得到所有合法方向的位置
                """
                    得到的位置的数据结构由输入的位置的数据结构决定
                        故而此处是 (row_index, col_index)
                """
                adjacent_positions = []
                for direction in self.legal_direction:
                    adjacent_position = self.position_and_direction_get_adjacent((row_index, col_index), direction)
                    if adjacent_position:
                        adjacent_positions. \
                            append(adjacent_position)

                # 判断所有合法方向的绝对水高 并只保留可流的位置
                """
                    此处的数据结构： {位置：绝对水高}
                """
                adjacent_absolute_water_highs = {}
                sum_absolute_water_high = absolute_water_high

                for adjacent_position in adjacent_positions:
                    adjacent_absolute_water_high = \
                        self.water_map[adjacent_position[0]][adjacent_position[1]] + \
                        self.landform_map[adjacent_position[0]][adjacent_position[1]]
                    # 只保留高度更低的 因为水往低处流
                    if adjacent_absolute_water_high < absolute_water_high:
                        adjacent_absolute_water_highs[adjacent_position] = adjacent_absolute_water_high
                        sum_absolute_water_high += adjacent_absolute_water_high


                # 如果四面都更高则水不流
                if len(adjacent_absolute_water_highs) == 0:
                    continue

                # 进行一个均值的求
                avg_absolute_water_high = sum_absolute_water_high / (len(adjacent_absolute_water_highs) + 1)

                # 若不可流平
                if avg_absolute_water_high < self.landform_map[row_index][col_index]:
                    # 当前剩余水量，流干为之
                    water_amount = self.water_map[row_index][col_index]
                    self.water_map[row_index][col_index] = 0

                    adjacent_drop_highs = {}
                    sum_drop_high = 0

                    for position in adjacent_absolute_water_highs:
                        drop_high = land_high - adjacent_absolute_water_highs[position]
                        if drop_high > 0:
                            sum_drop_high += drop_high
                            adjacent_drop_highs[position] = drop_high

                    # 将字典变为数组 并排好序
                    # {'a':21, 'b':5, 'c':3, 'd':54, 'e':74, 'f':0}
                    # 变为
                    # [('f', 0), ('c', 3), ('b', 5), ('a', 21), ('d', 54), ('e', 74)]
                    adjacent_drop_highs = sorted(adjacent_drop_highs.items(), key=lambda d: d[1], reverse=False)
                    drop_highs = tuple([i[1] for i in adjacent_drop_highs])
                    drop_num = len(adjacent_drop_highs)

                    # # 计算阿尔法们
                    # drop_high_each = [adjacent_drop_highs[ind + 1] - adjacent_drop_highs[ind]
                    #                   for ind in range(len(adjacent_drop_highs) - 1)]
                    # drop_high_each.append(land_high - adjacent_drop_highs[-1])

                    for step in range(len(adjacent_drop_highs)):
                        if water_amount < sum(drop_highs[:step + 1]):
                            for ind in range(step - 1):
                                position = adjacent_drop_highs[ind][0]
                                self.water_map[position[0]][position[1]] += drop_highs[ind]
                                water_amount -= drop_highs[ind]
                            position = adjacent_drop_highs[step - 1][0]
                            self.water_map[position[0]][position[1]] += water_amount
                            break

                # 若可流平
                else:
                    # 进行一个水的流
                    # 流自己
                    self.water_map[row_index][col_index] += \
                        round(max(avg_absolute_water_high - absolute_water_high,
                                  - self.water_map[row_index][col_index]), 3)

                    self.water_map[row_index][col_index] = \
                        round(self.water_map[row_index][col_index], 3)

                    # 流相邻部分
                    for position in adjacent_absolute_water_highs:
                        self.water_map[position[0]][position[1]] += \
                            max(avg_absolute_water_high -
                                self.water_map[position[0]][position[1]] -
                                self.landform_map[position[0]][position[1]],
                                -self.water_map[position[0]][position[1]])
                        self.water_map[position[0]][position[1]] = round(self.water_map[position[0]][position[1]], 3)

    # 这里定义了相邻的概念
    '''
        输入的旧坐标不能在半格上
    '''

    def position_and_direction_get_adjacent(self, old_position, direction):
        if direction == "stay":
            return old_position
        if direction == 'right':
            if old_position[1] < self.terrain_size[1] - 1:
                return old_position[0], old_position[1] + 1
        elif direction == 'left':
            if old_position[1] > 0:
                return old_position[0], old_position[1] - 1
        elif direction == 'down':
            if old_position[0] < self.terrain_size[0] - 1:
                return old_position[0] + 1, old_position[1]
        elif direction == 'up':
            if old_position[0] > 0:
                return old_position[0] - 1, old_position[1]
        return False

    # 返回地图的方法
    def get_landform_map(self):
        return self.landform_map[:]

    # 返回地图大小
    def get_terrain_size(self):
        return self.terrain_size

    # 返回水地图
    def get_water_map(self):
        return self.water_map[:]

    # 返回地貌图
    def get_terrain_map(self):
        return self.terrain_map[:]

    # 返回生物表
    def get_animals(self):
        return self.animals

    # 返回物品表
    def get_objects(self):
        return self.objects

    # 获取动物位置字典
    def get_animals_position(self):
        return self.animals_position

    # 获取植物位置字典
    def get_plants_position(self):
        return self.plants_position

    # 得到整个生物表
    def get_creatures_position(self):
        creatures_position = {}
        # 动物表里的都挑出来和植物表里的有相同的合起来
        for position in self.animals_position:
            if position in self.plants_position:
                creatures_position[position] = self.animals_position[position] + self.plants_position[position]
            else:
                creatures_position[position] = self.animals_position[position]

        # 弄植物表的 不过避免增加过已经有的
        for position in self.plants_position:
            if position not in self.animals_position:
                creatures_position[position] = self.plants_position[position]
        return creatures_position

    # 得到物体字典
    def get_objs_position(self):
        return self.objs_position

    # 得到具体某个位置的实体
    def get_entities_in_position(self, position):
        entities = []
        if position in self.animals_position:
            entities += self.animals_position[position]
        if position in self.plants_position:
            entities += self.plants_position[position]
        if position in self.objs_position:
            entities += self.objs_position[position]
        return entities

    # 根据id得到实体
    def get_entity_by_id(self, id):
        for animal in self.animals:
            if animal.get_id() == id:
                return animal

        for plant in self.plants:
            if plant.get_id() == id:
                return plant

        for obj in self.objects:
            if obj.get_id() == id:
                return obj

        return False

    # 更新新地图
    def renew_map(self, new_map):
        self.landform_map = new_map

    # 削除一个东西的存在
    def eliminate_exist_in_map(self, entity):
        entity_position_list, entity_list = self.determine_entities_category(entity)

        if entity_position_list != -1:
            entity_position_list[tuple(entity.get_position())].remove(entity)
            entity_list.remove(entity)
            if len(entity_position_list[tuple(entity.get_position())]) == 0:
                del entity_position_list[tuple(entity.get_position())]
            del entity

    # 增加一个新东西到地图
    def add_exist_to_map(self, entity, position=None):
        entity_position_list, entity_list = self.determine_entities_category(entity)
        if not position:
            die_position = entity.get_position()
        else:
            die_position = position

        if entity_position_list != -1:
            entity_list.append(entity)
            if die_position in entity_position_list:
                entity_position_list[die_position].append(entity)
            else:
                entity_position_list[die_position] = [entity]

    # 判断实体类别
    # 如果实体没有被登记为实体 则返回负一
    def determine_entities_category(self, entity):
        entity_position_list = -1
        entity_list = -1

        if isinstance(entity, Animal):
            entity_position_list = self.animals_position
            entity_list = self.animals
        elif isinstance(entity, Plant):
            entity_position_list = self.plants_position
            entity_list = self.plants
        elif isinstance(entity, Obj):
            entity_position_list = self.objs_position
            entity_list = self.objects

        return entity_position_list, entity_list

    # 改变动物位置的工具函数
    def change_animal_position(self, animal, old_position, new_position):
        if new_position in self.animals_position:
            self.animals_position[new_position].append(animal)
        else:
            self.animals_position[new_position] = [animal]

        self.animals_position[old_position].remove(animal)
        if len(self.animals_position[old_position]) == 0:
            del self.animals_position[old_position]
        # animal.move(new_position)

    # 动物死亡后消失
    def creature_die(self, creature):
        die_position = tuple(creature.get_position())
        corpse = creature.die()
        if corpse:
            for remain in corpse:
                self.add_exist_to_map(remain)

        self.eliminate_exist_in_map(creature)

    # 初始化位置字典
    def init_position_list(self, entity_list):
        things_position = {}
        for entity in entity_list:
            if tuple(entity.get_position()) in things_position:
                things_position[tuple(entity.get_position())].append(entity)
            else:
                things_position[tuple(entity.get_position())] = [entity]
        return things_position

    # 植物每回合的变化
    def plant_change(self):
        for plant in self.plants:
            products = plant.post_turn_change()
            if products:
                for product in products:
                    self.add_exist_to_map(product)


def names_orderly_tuplize(objs_list):
    def get_onj_name(obj):
        return type(obj).__name__

    objs_name_list = [get_onj_name(obj) for obj in objs_list]
    objs_name_list.sort()
    return tuple(objs_name_list)


if __name__ == "__main__":
    landform_map = [
        [5, 5, 5, 5, 5],
        [5, 1, 1, 1, 5],
        [5, 1, 1, 1, 5],
        [5, 1, 1, 1, 5],
        [5, 5, 5, 5, 5],
    ]
    water_map = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ]
    terrain_map = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ]
    terrain_size = (5, 5)
    animals = []
    plants = []
    objects = []
    state = Mesh_state(landform_map, water_map, terrain_map, terrain_size, animals, plants, objects)
    print(1)
    for line in state.get_water_map():
        print(line)
    input()
    while True:
        state.water_flow()
        # state.water_flow_old()
        for line in state.get_water_map():
            print(line)
        input()
