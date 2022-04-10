from world.world import World


class Mesh_world(World):
    def __init__(self, state):
        super(Mesh_world, self).__init__(state)

    def evolution_a_turn(self):
        self.landform_evolution()

    def landform_evolution(self):
        # 从状态中得到地图
        landform_map = self.state.get_map()

        # 地图变化的规则
        # new_map = landform_map

        # 找到所有有1的位置
        move_list = []
        for map_line_index in range(len(landform_map)):
            for map_point_index in range(len(landform_map[map_line_index])):
                if landform_map[map_line_index][map_point_index] == 1:
                    move_list.append((map_line_index, map_point_index))

        # 避免移动冲突 进行倒序
        move_list.reverse()

        # 对这些位置上的1进行移动
        for ones in move_list:
            map_line_index = ones[0]
            map_point_index = ones[1]
            landform_map[map_line_index][map_point_index] = 0
            landform_map[map_line_index][(map_point_index + 1) % len(landform_map[map_line_index])] = 1

        # 更新地图变化
        self.state.renew_map(landform_map)

    def expansion(self):
        # 「可视化」输出
        for map_line in self.state.get_map():
            print(map_line)
        gate = input("按回车键继续 或输入x结束： ")
        if gate == 'x':
            return False
        return True

    def evolution(self):
        gate = self.expansion()
        while gate:
            self.evolution_a_turn()
            gate = self.expansion()
