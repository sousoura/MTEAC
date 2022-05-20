from world.entity.entity_import import *


class Bucket(Obj, Container):
    # 可以放进空间的物品
    containable_objs = ["Fruit", "Stone", "Wood", "Axe"]

    def __init__(self, position):
        super(Bucket, self).__init__(position)
        Container.__init__(self)
