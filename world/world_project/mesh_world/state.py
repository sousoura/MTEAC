from world.state import State
from world.world_project.mesh_world.exhibitor import Exhibitor


class Mesh_state(State):
    def __init__(self, terrain, terrain_size, creatures, obj):
        self.terrain = terrain
        self.terrain_size = terrain_size
        self.creatures = creatures
        self.things_position = self.get_things_position()
        self.objects = obj
        self.exhibitor = Exhibitor(self.terrain_size, (1000, 1000))

    # 初始化位置字典
    def get_things_position(self):
        things_position = {}
        for creature in self.creatures:
            if tuple(creature.get_position()) in things_position:
                things_position[tuple(creature.get_position())].append(creature)
            else:
                things_position[tuple(creature.get_position())] = [creature]
        return things_position

    # 返回地图的方法
    def get_map(self):
        return self.terrain[:]

    # 更新新地图
    def renew_map(self, new_map):
        self.terrain = new_map

    # 更新动物行为
    def animal_action(self, player_cmd):
        for creature in self.creatures:
            if not creature.is_die():
                cmd = creature.devise_an_act(self.get_perception(creature))
                # 玩家输入的键盘值控制的对象是谁
                # 这里是有缺陷的 因为所有人类都会受影响 而不是某一个人类
                if type(creature).__name__ == "Wolf":
                    if player_cmd.split("_")[0] in ['left', 'right', 'up', 'down']:
                        cmd = ["go", player_cmd]
                    elif player_cmd.split("_")[0] == "eat":
                        cmd = player_cmd.split("_")
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
        def move_to_new_position(state, creature, old_position, new_position):
            if new_position:
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
        move_to_new_position(self, creature, old_position, new_position)

    # old_position + direction = new_position
    def position_and_direction_get_new_position(self, old_position, direction):
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

    # 可视化 关闭时返回False
    def visualization(self):
        return self.exhibitor.display(self.terrain, self.things_position)
