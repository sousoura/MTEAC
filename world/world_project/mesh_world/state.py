from world.state import State


class Mesh_state(State):
    def __init__(self, terrain, terrain_size, creatures, obj):
        self.map = terrain
        self.map_size = terrain_size
        self.creatures = creatures
        self.things_position = self.get_things_position()
        self.objects = obj

    # 初始化位置字典
    def get_things_position(self):
        things_position = {}
        for creature in self.creatures:
            things_position[tuple(creature.get_position())] = creature
        return things_position

    # 返回地图的方法
    def get_map(self):
        return self.map[:]

    # 更新新地图
    def renew_map(self, new_map):
        self.map = new_map

    # 更新动物行为
    def animal_action(self):
        for creature in self.creatures:
            cmd = creature.devise_an_act(self.get_perception(creature))
            self.creature_act(creature, cmd)

    # 得到特定某个动物的感知
    def get_perception(self, creature):
        return creature.get_perception(self.map, self.things_position)

    # 分析生物行动命令 并调用相应的执行函数
    def creature_act(self, creature, command):
        if command[0] == 'go':
            self.moving_position(creature, command[1])

    # 生物移动 外部和内部执行
    def moving_position(self, creature, direction):
        if direction == 'down':
            if creature.get_position()[1] < self.map_size[1]:
                old_position = tuple(creature.get_position())
                new_position = (old_position[0], old_position[1] + 1)
                self.things_position[new_position] = self.things_position[old_position]
                del self.things_position[old_position]
                creature.move(new_position)

    def print_show_creature(self):
        for creature in self.creatures:
            print(type(creature).__name__, creature.get_position())
