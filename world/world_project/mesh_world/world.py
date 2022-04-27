from world.world import World


class Mesh_world(World):
    def __init__(self, state):
        super(Mesh_world, self).__init__(state)

    # 时间推进一次
    def evolution_a_turn(self, player_cmd):
        self.animal_action(player_cmd)
        self.landform_evolution()

    # 一回合内的动物运动
    def animal_action(self, player_cmd):
        self.state.animal_action(player_cmd)

    # 地图变化一次
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
            landform_map[map_line_index][map_point_index] -= 1
            landform_map[map_line_index][(map_point_index + 1) % len(landform_map[map_line_index])] += 1

        # 更新地图变化
        self.state.renew_map(landform_map)

    def expansion(self):
        # 「可视化」输出
        for map_line in self.state.get_map():
            print(map_line)
        self.state.print_show_creature()
        # gate = input("按回车键继续 或输入x结束： ")
        # if gate == 'x':
        #     return False
        # return True

        return self.visualization()

    # 地图不断推进
    def evolution(self):
        player_cmd = self.expansion()
        # 用gate判断是否结束
        while player_cmd:
            self.evolution_a_turn(player_cmd)
            player_cmd = self.expansion()

    # 可视化 读入状态 由状态类实现 地形地图和生物列表 然后可视化
    def visualization(self):
        return self.state.visualization()
