def get_generator(generator_file):
    from world.mesh_world.mesh_world_generator import Concrete_world_generator as Generator
    return Generator()


def get_world(generator):
    return generator.generate_a_world()


def run():
    generator = get_generator("mesh_world")
    world = get_world(generator)
    world.evolution()
