import importlib


# 通过世界类型名得到相应的世界生成器
def get_generator(generator_file):
    generator_file = 'world.world_project.' + generator_file + '.' + 'world_generator'
    generator_module = importlib.import_module(generator_file)
    # from world.mesh_world.mesh_world_generator import Concrete_world_generator as Generator
    return generator_module.Concrete_world_generator()


def get_world(generator):
    # 世界生成器生成世界
    # 输入参数为 地形类型的数量 地图大小 生物生成参数 物品生成参数
    return generator.generate_a_world(2, (5, 5), "random_creature", "random_obj")


def run():
    # 根据世界类型生成世界
    generator = get_generator("mesh_world")
    # 通过世界生成器生成世界
    world = get_world(generator)
    # 世界开始不停运作
    world.evolution()
