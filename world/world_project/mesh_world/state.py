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
                    动物移动        moving_position
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
    def __init__(self, landform_map, water_map, terrain_map, terrain_size, animals, plants, objects):
        """
        :param landform_map:   类型：二维数组 值为int      意义表示：每个值都是整形 表示高低地形 数字越高地形越高
        :param terrain_size:    类型：二元元组             意义表示：地图大小 第0个值是行数 第1个值是列数
        :param animals:       类型：列表 值为动物对象      意义表示：世界中的所有生物
        :param objects:         类型：列表 值为物品对象      意义表示：世界中的所有物品
        """
        # 地图
        self.landform_map = landform_map
        self.water_map = water_map
        self.terrain_map = terrain_map

        # 地图属性
        self.terrain_size = terrain_size
        self.legal_direction = ["up", "down", "left", "right"]

        # 实体表
        self.animals = animals
        self.plants = plants
        self.objects = objects

        # 得到位置字典 方便根据位置找到生物 而不必总是遍历生物表 以空间换时间
        self.animals_position = self.init_position_list(self.animals)
        self.plants_position = self.init_position_list(self.plants)
        self.objs_position = self.init_position_list(self.objects)

    # 更新新地图
    def renew_map(self, new_map):
        self.landform_map = new_map

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

    # 更新动物行为
    # 一回合内的动物运动
    def animal_action(self, player_cmd):
        # 遍历生物表
        for animal in self.animals:
            # 判断生物是否死亡
            if not animal.is_die():
                cmd = animal.devise_an_act(animal.get_perception(self.landform_map, self.animals_position))
                # 玩家输入的键盘值控制的对象是谁
                # 这里是有缺陷的 因为所有人类都会受影响 而不是某一个人类
                '''
                    待引入id系统改进
                '''
                if animal.is_id(1):
                    # 判断是否输入指令
                    if not player_cmd:
                        return
                    # 判断指令是否是移动
                    elif player_cmd[0] == "go":
                        cmd = player_cmd
                    # 判断指令类型是否是吃
                    elif player_cmd[0] == "eat":
                        cmd = player_cmd
                # 根据指令进行操作
                self.animal_act(animal, cmd)
            else:
                del animal

    # 分析生物行动命令的基本类型 并调用相应的执行函数
    def animal_act(self, animal, command):
        """
           ["go", 方向]
        """
        if command[0] == 'go':
            self.moving_position(animal, command[1])
        elif command[0] == 'eat':
            # 动物吃生物
            self.animal_eating(animal, command[1], command[2])

    """
        输入  某个生物实例 移动的方向
        效果  会分析移动是否合法 如果合法 则移动之 改变生物的位置状态并更新位置表 反之 不移动之
    """

    def moving_position(self, animal, direction):
        for a_pace in range(animal.get_pace()):
            self.moving_a_pace(animal, direction)

    # 生物移动 外部和内部执行
    def moving_a_pace(self, animal, direction):
        # 判断动作合法性方法
        def judge_action_validity(animal, old_position, new_position):
            # 判断落差是否大于生物的爬行能力
            if abs(self.landform_map[round(old_position[1])][round(old_position[0])] -
                   self.landform_map[round(new_position[1])][round(new_position[0])]) > \
                    animal.get_crawl_ability():
                return False

            # 判断目的地属性和自身是否相斥
            # if animal.judge_geomorphic_compatibility(self.terrain[new_position[1]][new_position[0]]):
            #     pass

            # 如果该生物是大物体
            if isinstance(animal, Big_obj):
                # 大物体互斥规则
                # 如果有大动物挡在前面
                if new_position in self.animals_position:
                    for other_animal in self.animals_position[new_position]:
                        if isinstance(other_animal, Big_obj):
                            return False

                # if new_position in self.big_objs:
                #     return False

                # 禁止大物体进入的地貌 （已改为在相斥判断中的大物体类中进行判断）

            # 该生物是小物体的情况
            else:
                pass
                # 禁止一切物体进入的地貌（已改为在相斥判断中进行判断）

            return True

        # 得到新位置后移动到新位置
        def normally_move_to_new_position(state, animal, old_position, new_position):
            if new_position in state.animals_position:
                state.animals_position[new_position].append(animal)
            else:
                state.animals_position[new_position] = [animal]
            state.animals_position[old_position].remove(animal)
            if len(state.animals_position[old_position]) == 0:
                del state.animals_position[old_position]
            animal.move(new_position)

        old_position = tuple(animal.get_position())
        new_position = self.position_and_direction_get_new_position(old_position, direction)
        """
            条件判断不全在条件判断函数中 职能不够集中 待优化
        """
        # 判断是否出界
        if new_position:
            # 判断移动的条件是否满足
            if judge_action_validity(animal, old_position, new_position):
                # 判断移动合法性
                normally_move_to_new_position(self, animal, old_position, new_position)

    # old_position + direction = new_position
    def position_and_direction_get_new_position(self, old_position, direction):
        # 判断移动合法性和移动种类
        def judge_movement_legality(old_position, new_position):
            """
                移动判断是否合法 属于哪一类
                之所以返回2和-2是因为1和0对应了True和False
            """
            if new_position:
                # 移动格差过大 不合法
                if abs(self.landform_map[new_position[1]][new_position[0]] -
                       self.landform_map[old_position[1]][old_position[0]]) > 1:
                    return False
                # 升一格移动
                elif self.landform_map[new_position[1]][new_position[0]] - \
                        self.landform_map[old_position[1]][old_position[0]] == 1:
                    return 2
                # 降一格移动
                elif self.landform_map[new_position[1]][new_position[0]] - \
                        self.landform_map[old_position[1]][old_position[0]] == -1:
                    return -2
                # 同级移动
                return True
            # 新位置超出地图 为空对象
            return False

        # 若在左右半格上
        if old_position[0] % 1 > 0:
            stride = 0.5
            if direction == 'right':
                if old_position[0] < self.terrain_size[0] - 1:
                    return old_position[0] + stride, old_position[1]
            elif direction == 'left':
                if old_position[0] > 0:
                    return old_position[0] - stride, old_position[1]
        # 若在上下半格上
        elif old_position[1] % 1 > 0:
            stride = 0.5
            if direction == 'down':
                if old_position[1] < self.terrain_size[1] - 1:
                    return old_position[0], old_position[1] + stride
            elif direction == 'up':
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
    '''
        输入      吃的主体 方向 客体
    '''

    def animal_eating(self, eator, eat_direction, be_eator=0):
        if be_eator == -1:
            return

        eat_position = self.position_and_direction_get_new_position(eator.get_position(), eat_direction)
        '''
            目前只能吃在位置上的大生物 待修改
            如果吃的地方什么也不发生 则结束
        '''
        if be_eator == 0:
            if eat_position in self.animals_position:
                be_eator = self.animals_position[eat_position][0]
            else:
                pass
        # 若成功 吃者状态变化 被吃者消失(死亡)
        if eat_position == be_eator.get_position():
            if isinstance(be_eator, Plant):
                self.plants_position[be_eator.get_position()].remove(be_eator)
                self.plants.remove(be_eator)
                if len(self.plants_position[be_eator.get_position()]) == 0:
                    del self.plants_position[be_eator.get_position()]
                eator.eat(be_eator)
                be_eator.die()
                del be_eator
            elif isinstance(be_eator, Animal):
                self.animals_position[be_eator.get_position()].remove(be_eator)
                self.animals.remove(be_eator)
                if len(self.animals_position[be_eator.get_position()]) == 0:
                    del self.animals_position[be_eator.get_position()]
                eator.eat(be_eator)
                be_eator.die()
                del be_eator
            elif isinstance(be_eator, Obj):
                self.objs_position[be_eator.get_position()].remove(be_eator)
                self.objects.remove(be_eator)
                if len(self.objs_position[be_eator.get_position()]) == 0:
                    del self.objs_position[be_eator.get_position()]
                eator.eat(be_eator)
                del be_eator
        # 确认吃的方向有没有该对象 若没有 动作失败
        else:
            pass

    # # print生成生物位置
    # def print_show_animal(self):
    #     for animal in self.animals:
    #         print(type(animal).__name__, animal.get_position())

    """
        ***
            以下是水地图的更新
        ***
    """
    def water_flow(self):
        # 遍历水地图
        for row_index in range(self.terrain_size[1]):
            for col_index in range(self.terrain_size[0]):
                # 若自身相对水高低于0.1 则被土地吸收
                if self.water_map[row_index][col_index] < 0.1:
                    self.water_map[row_index][col_index] = 0
                    continue
                # 得到自己的绝对水高
                absolute_water_high = self.water_map[row_index][col_index] + self.landform_map[row_index][col_index]
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
                    current_water_amount = self.water_map[row_index][col_index]
                    self.water_map[row_index][col_index] = 0
                    while len(adjacent_absolute_water_highs) > 0 and current_water_amount > 0:
                        # 等分水量
                        equant_water_amount = current_water_amount / len(adjacent_absolute_water_highs)
                        kill_positions = []
                        for position in adjacent_absolute_water_highs:
                            # 两边流平的情况
                            if adjacent_absolute_water_highs[position] + equant_water_amount > \
                                    self.landform_map[row_index][col_index]:
                                # 流一个水差
                                water_head = \
                                    self.landform_map[row_index][col_index] - adjacent_absolute_water_highs[position]
                                # if water_head < 0:
                                #     water_head = 0
                                current_water_amount -= water_head
                                self.water_map[position[0]][position[1]] += water_head
                                kill_positions.append(position)
                            # 全给的情况
                            else:
                                current_water_amount -= equant_water_amount
                                self.water_map[position[0]][position[1]] += equant_water_amount

                        for position in kill_positions:
                            adjacent_absolute_water_highs.pop(position)

                        if current_water_amount < 0.01:
                            current_water_amount = 0

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
        if direction == 'down':
            if old_position[1] < self.terrain_size[1] - 1:
                return old_position[0], old_position[1] + 1
        elif direction == 'up':
            if old_position[1] > 0:
                return old_position[0], old_position[1] - 1
        elif direction == 'right':
            if old_position[0] < self.terrain_size[0] - 1:
                return old_position[0] + 1, old_position[1]
        elif direction == 'left':
            if old_position[0] > 0:
                return old_position[0] - 1, old_position[1]

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

    # 初始化位置字典
    def init_position_list(self, entity_list):
        things_position = {}
        for animal in entity_list:
            if tuple(animal.get_position()) in things_position:
                things_position[tuple(animal.get_position())].append(animal)
            else:
                things_position[tuple(animal.get_position())] = [animal]
        return things_position


if __name__ == "__main__":
    landform_map = [
        [5, 5, 5, 5, 5],
        [5, 1, 1, 1, 5],
        [5, 1, 5, 1, 5],
        [5, 1, 1, 1, 1],
        [5, 5, 5, 5, 5],
    ]
    water_map = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ]
    terrain_size = (5, 5)
    animals = []
    objects = []
    state = Mesh_state(landform_map, water_map, terrain_size, animals, objects)
    while True:
        state.water_flow()
        input()
