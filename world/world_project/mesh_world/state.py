from world.state import State


class Mesh_state(State):
    def __init__(self, terrain, terrain_size, creatures, objs):
        self.terrain = terrain
        self.terrain_size = terrain_size
        self.creatures = creatures
        self.things_position = self.init_things_position()
        self.objects = objs

    # 更新新地图
    def renew_map(self, new_map):
        self.terrain = new_map

    # 更新动物行为
    # 一回合内的动物运动
    def animal_action(self, player_cmd):
        # 遍历生物表
        for creature in self.creatures:
            # 判断生物是否死亡
            if not creature.is_die():
                cmd = creature.devise_an_act(self.get_perception(creature))
                # 玩家输入的键盘值控制的对象是谁
                # 这里是有缺陷的 因为所有人类都会受影响 而不是某一个人类
                '''
                    待引入id系统改进
                '''
                if type(creature).__name__ == "Wolf":
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

    # 得到特定某个动物的感知
    def get_perception(self, creature):
        return creature.get_perception(self.terrain, self.things_position)

    # 分析生物行动命令 并调用相应的执行函数
    def creature_act(self, creature, command):
        if command[0] == 'go':
            self.moving_position(creature, command[1])
        elif command[0] == 'eat':
            # 动物吃生物
            self.creature_eating(creature, command[1])

    # 生物移动 外部和内部执行
    def moving_position(self, creature, direction):
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

        old_position = tuple(creature.get_position())
        new_position = self.position_and_direction_get_new_position(old_position, direction)
        # 判断移动的条件
        # 判断是否出界
        if new_position:
            # 判断移动合法性
            normally_move_to_new_position(self, creature, old_position, new_position)

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
        结构为：吃的主体 方向 客体
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

    # print生成生物位置
    def print_show_creature(self):
        for creature in self.creatures:
            print(type(creature).__name__, creature.get_position())

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
