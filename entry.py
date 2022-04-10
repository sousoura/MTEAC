import importlib


def get_generator(generator_file):
    generator_file = 'world.' + generator_file + '.' + generator_file + '_generator'
    generator_module = importlib.import_module(generator_file)
    # from world.mesh_world.mesh_world_generator import Concrete_world_generator as Generator
    return generator_module.Concrete_world_generator()


def get_world(generator):
    return generator.generate_a_world()


def run():
    generator = get_generator("mesh_world")
    world = get_world(generator)
    world.evolution()
