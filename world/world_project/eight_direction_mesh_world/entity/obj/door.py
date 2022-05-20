from world.entity.entity_import import *


class Door(Obj, Big_obj):
    def __init__(self, position):
        super(Door, self).__init__(position)
        # True意味着门开着 False意味着关着
        self.switch = True
