import sys
from abc import ABC

sys.path.append("..")
from world.state import State


class Mesh_state(State, ABC):
    def __init__(self):
        self.a = 0
