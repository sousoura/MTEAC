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
                """
                    判断该对象是不是玩家
                    判断有没有指令
                """
                if animal.is_id(1):
                    # 判断是否输入指令
                    if not player_cmd:
                        continue
                    # 判断指令是否是移动
                    else:
                        cmd = player_cmd
                # 根据指令进行操作
                self.animal_action_command_analysis_and_execute(animal, cmd)
                animal.post_turn_change()
            else:
                self.animal_die(animal, self.animals_position, self.animals)
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
                if self.landform_map[new_position[1]][new_position[0]] - \
                        self.landform_map[old_position[1]][old_position[0]] == 1:
                    return 2
                # 降一格移动
                elif self.landform_map[new_position[1]][new_position[0]] - \
                        self.landform_map[old_position[1]][old_position[0]] == -1:
                    return -2
                # 同级移动
                return True
            # 新位置超出地图 为空对象
            # 冗余判断
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
    """
        生物的吃行为
        输入      吃的主体 方向 客体
    """

    def animal_eating(self, eator, be_eator):
        # 被吃完后 被吃者消失
        def state_eat_change(eator, be_eator, position_list, eat_obj_list):
            position_list[be_eator.get_position()].remove(be_eator)
            eat_obj_list.remove(be_eator)
            if len(position_list[be_eator.get_position()]) == 0:
                del position_list[be_eator.get_position()]
            del be_eator

        # 动物内部改变 吃者和被吃者状态变化
        eator.action_interior_outcome("eat", obj=be_eator)
        # 若被吃完 被吃者消失(死亡)
        if be_eator.be_ate(eator):
            # 地图改变
            if isinstance(be_eator, Plant):
                state_eat_change(eator, be_eator, self.plants_position, self.plants)
            elif isinstance(be_eator, Obj):
                state_eat_change(eator, be_eator, self.objs_position, self.objects)
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
            if isinstance(be_attackeder, Plant):
                self.animal_die(attacker, be_attackeder, self.plants_position, self.plants)
            elif isinstance(be_attackeder, Animal):
                self.animal_die(attacker, be_attackeder, self.animals_position, self.animals)
            del be_attackeder

    # 生物休息
    def animal_rest(self, rester):
        pass

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
    def animal_die(self, creature, creature_position_list, creature_list):
        die_position = tuple(creature.get_position())
        corpse = creature.die()
        if corpse:
            self.objects.append(corpse)
            if die_position in self.objs_position:
                self.objs_position[die_position].append(corpse)
            else:
                self.objs_position[die_position] = [corpse]

        creature_position_list[creature.get_position()].remove(creature)
        creature_list.remove(creature)
        if len(creature_position_list[creature.get_position()]) == 0:
            del creature_position_list[creature.get_position()]
        del creature


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
