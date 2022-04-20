from world.world_generator import World_generator
from world.mesh_world.world import Mesh_world as World
from world.mesh_world.state import Mesh_state as State


# 网格世界的世界生成器类
class Concrete_world_generator(World_generator):
    def generate_a_world(self, terrain_types_number, terrain_size, creature_para, obj_para):
        state = State(self.generate_a_state(terrain_types_number, terrain_size, creature_para, obj_para))
        return World(state)

    def generate_a_state(self, terrain_types_number, terrain_size, creature_para, obj_para):
        terrain = self.randomMatrix(terrain_types_number, terrain_size[0], terrain_size[1])
        feature_list = []
        obj_list = []
        if creature_para == "random_feature":
            ''' 这里生成生物表 '''
            pass
        else:
            ''' 参数生成 '''
            pass
        if obj_para == "random_obj":
            ''' 这里生成物体表 '''
            pass
        else:
            ''' 参数生成 '''
            pass
        return State()

    def randomMatrix(self, terrain_types_number, columns, rows):
        import random
        matrix = []
        for i in range(columns):
            matrix.append([])
            for j in range(rows):
                matrix[i].append(random.randrange(terrain_types_number))
        return matrix
