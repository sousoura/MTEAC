from world.state import State
from world.entity.entity_import import *


"""
    网格状态
        其具有属性：
            地形               用两层列表表示的方块的网格的世界
                地形大小        网格世界的大小
            生物列表            生物对象的列表
                位置-生物字典   由位置找到位置上的生物的字典
            物品列表            存物品对象的列表
        网格世界的方法全都有关于状态的修改或状态
            一回合内各个属性的变化的方法
                动物行为 animal_action和creature_act
                    动物移动        moving_position
                    动物吃          creature_eating
                地形变化            (去掉了)
                ...
            更新属性的方法
                renew_map
            规定空间属性的方法
                规定「相邻」的方法   position_and_direction_get_adjacent
            得到某生物的类型的方法    print_show_creature（注释掉了）
            得到状态属性的方法
                得到各个属性的方法   
                初始化位置词典的方法  init_things_position
"""


class Mesh_state(State):
    def __init__(self, terrain, terrain_size, creatures, objects):
        """
        :param terrain:         类型：二维数组 值为int      意义表示：每个值都是整形 表示高低地形 数字越高地形越高
        :param terrain_size:    类型：二元元组             意义表示：地图大小 第0个值是行数 第1个值是列数
        :param creatures:       类型：列表 值为生物对象      意义表示：世界中的所有生物
        :param objects:         类型：列表 值为物品对象      意义表示：世界中的所有物品
        """
        self.terrain = terrain
        self.terrain_size = terrain_size
        self.creatures = creatures
        self.objects = objects

        # 得到位置字典 方便根据位置找到生物 而不必总是遍历生物表 以空间换时间
        self.things_position = self.init_things_position()

    # 更新新地图
    def renew_map(self, new_map):
        self.terrain = new_map

    """
        输入  player_cmd：玩家指令 为字符串 格式是"第一段_第二段_第三段_..."
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
        for creature in self.creatures:
            # 判断生物是否死亡
            if not creature.is_die():
                cmd = creature.devise_an_act(creature.get_perception(self.terrain, self.things_position))
                # 玩家输入的键盘值控制的对象是谁
                # 这里是有缺陷的 因为所有人类都会受影响 而不是某一个人类
                '''
                    待引入id系统改进
                '''
                if creature.is_id(1):
                    # 判断是否输入指令
                    if not player_cmd:
                        return
                    # 判断指令是否是移动
                    elif player_cmd.split("_")[0] in ['left', 'right', 'up', 'down']:
                        cmd = ["go", player_cmd]
                    # 判断指令类型是否是吃
                    elif player_cmd.split("_")[0] == "eat":
                        cmd = player_cmd.split("_")
                # 根据指令进行操作
                self.creature_act(creature, cmd)
            else:
                del creature

    # 分析生物行动命令的基本类型 并调用相应的执行函数
    def creature_act(self, creature, command):
        if command[0] == 'go':
            self.moving_position(creature, command[1])
        elif command[0] == 'eat':
            # 动物吃生物
            self.creature_eating(creature, command[1])

    """
        输入  某个生物实例 移动的方向
        效果  会分析移动是否合法 如果合法 则移动之 改变生物的位置状态并更新位置表 反之 不移动之
    """
    # 生物移动 外部和内部执行
    def moving_position(self, animal, direction):
        # 判断动作合法性方法
        def judge_action_validity(animal, old_position, new_position):
            # 判断落差是否大于生物的爬行能力
            if abs(self.terrain[old_position[1]][old_position[0]] - self.terrain[new_position[1]][new_position[0]]) > \
                    animal.get_crawl_ability():
                return False

            # 判断目的地属性和自身是否相斥
            # if animal.judge_geomorphic_compatibility(self.terrain[new_position[1]][new_position[0]]):
            #     pass

            # 如果该生物是大物体
            if isinstance(animal, Big_obj):
                # 大物体互斥规则
                # 如果有大动物挡在前面
                if new_position in self.things_position:
                    for other_animal in self.things_position[new_position]:
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
        def normally_move_to_new_position(state, creature, old_position, new_position):
            if new_position in state.things_position:
                state.things_position[new_position].append(creature)
            else:
                state.things_position[new_position] = [creature]
            state.things_position[old_position].remove(creature)
            if len(state.things_position[old_position]) == 0:
                del state.things_position[old_position]
            creature.move(new_position)

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
                if abs(self.terrain[new_position[1]][new_position[0]] -
                       self.terrain[old_position[1]][old_position[0]]) > 1:
                    return False
                # 升一格移动
                elif self.terrain[new_position[1]][new_position[0]] - \
                        self.terrain[old_position[1]][old_position[0]] == 1:
                    return 2
                # 降一格移动
                elif self.terrain[new_position[1]][new_position[0]] - \
                        self.terrain[old_position[1]][old_position[0]] == -1:
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

    # 生物吃
    '''
        输入      吃的主体 方向 客体
    '''
    def creature_eating(self, eator, eat_direction, be_eator=0):
        eat_position = self.position_and_direction_get_new_position(eator.get_position(), eat_direction)
        '''
            目前只能吃在位置上的大生物 待修改
            如果吃的地方什么也不发生 则结束
        '''
        if be_eator == 0:
            if eat_position in self.things_position:
                be_eator = self.things_position[eat_position][0]
            else:
                return
        # 若成功 吃者状态变化 被吃者消失(死亡)
        if eat_position == be_eator.get_position():
            self.things_position[be_eator.get_position()].remove(be_eator)
            self.creatures.remove(be_eator)
            if len(self.things_position[be_eator.get_position()]) == 0:
                del self.things_position[be_eator.get_position()]
            eator.eat(be_eator)
            be_eator.die()
            del be_eator
        # 确认吃的方向有没有该对象 若没有 动作失败
        else:
            pass

    # # print生成生物位置
    # def print_show_creature(self):
    #     for creature in self.creatures:
    #         print(type(creature).__name__, creature.get_position())

    # 返回地图的方法
    def get_terrain(self):
        return self.terrain[:]

    # 返回地图大小
    def get_terrain_size(self):
        return self.terrain_size

    # 返回生物表
    def get_creatures(self):
        return self.creatures

    # 返回物品表
    def get_objects(self):
        return self.objects

    # 获取位置字典
    def get_things_position(self):
        return self.things_position

    # 初始化位置字典
    def init_things_position(self):
        things_position = {}
        for creature in self.creatures:
            if tuple(creature.get_position()) in things_position:
                things_position[tuple(creature.get_position())].append(creature)
            else:
                things_position[tuple(creature.get_position())] = [creature]
        return things_position
