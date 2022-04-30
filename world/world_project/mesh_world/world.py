from world.world import World


"""
    网格世界类
        状态类型为网格状态的世界
"""


class Mesh_world(World):
    def __init__(self, state):
        super(Mesh_world, self).__init__(state)

    # 地图推进一次
    def evolution(self, player_cmd=None):
        self.state.animal_action(player_cmd)
        # self.state.landform_evolution()

    def get_state(self):
        return self.state
