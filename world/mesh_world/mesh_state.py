from world.state import State


class Mesh_state(State):
    def __init__(self, map):
        self.map = map

    def get_map(self):
        return self.map[:]

    def renew_map(self, new_map):
        self.map = new_map
