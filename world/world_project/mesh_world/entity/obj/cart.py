from world.entity.entity_import import *


class Cart(Obj, Container):
    # 可以放进空间的物品
    containable_objs = ["Fruit", "Stone", "Wood", "Axe", "Bucket"]

    def __init__(self, position):
        super(Cart, self).__init__(position)
        Container.__init__(self)
