from world.world_generator import World_generator
from world.world_project.mesh_world.world import Mesh_world as World
from world.world_project.mesh_world.state import Mesh_state as State
from world.world_project.mesh_world.entity.creature.animal.wolf import Wolf
from world.world_project.mesh_world.entity.creature.animal.wolf_brain import Wolf_brain
from world.world_project.mesh_world.entity.creature.animal.human.human_being import Human_being
from world.world_project.mesh_world.entity.creature.animal.human.human_brain import Human_brain


# 网格世界的世界生成器类
class Concrete_world_generator(World_generator):
    def generate_a_world(self, terrain_types_number, terrain_size, creature_para, obj_para):
        state = self.generate_a_state(terrain_types_number, terrain_size, creature_para, obj_para)
        return World(state)

    ''' 生成一个世界 '''
    def generate_a_state(self, terrain_types_number, terrain_size, creature_para, obj_para):
        terrain = self.randomMatrix(terrain_types_number, terrain_size[0], terrain_size[1])
        creature_list = []
        obj_list = []

        ''' 如果不给定具体参数 就用默认的生成方法 '''
        if creature_para == "random_creature":
            ''' 这里生成生物表 '''
            creature_list.append(Wolf([1, 2], 5, brain=Wolf_brain()))
            creature_list.append(Human_being([3, 3], 5, brain=Human_brain()))

        else:
            ''' 参数生成 '''
            pass
        if obj_para == "random_obj":
            ''' 这里生成物体表 '''
            pass
        else:
            ''' 参数生成 '''
            pass
        return State(terrain, terrain_size, creature_list, obj_list)

    # 读档时用既有信息建造一个世界
    def building_a_state(self, terrain, terrain_size, creature_list, obj_list):
        return State(terrain, terrain_size, creature_list, obj_list)

    ''' 随机生成特定大小的网格世界 '''
    def randomMatrix(self, terrain_types_number, columns, rows):
        import random
        matrix = []
        for i in range(columns):
            matrix.append([])
            for j in range(rows):
                matrix[i].append(random.randrange(terrain_types_number))
        return matrix

    # 以state构造世界
    def generate_a_world_by_state(self, state):
        return World(state)
