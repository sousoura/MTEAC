from world.world import World


class Mesh_world(World):
    def __init__(self, state):
        super(state, self).__init__(self, state)

    def evolution_a_turn(self):
        print("mesh evolution_a_turn")

    def expansion(self):
        print("mesh expansion")

    def evolution(self):
        print("I am in evolution")
