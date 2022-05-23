from world.entity.entity_import import *


class Axe(Obj, Equipment):
    def __init__(self, position):
        super(Axe, self).__init__(position)

    def properties_gain(self, subject):
        new_aggressivity_change_value = subject.aggressivity_change_value + 100
        subject.body_attribute_change(aggressivity_change_value=new_aggressivity_change_value)

    def cancel_gain(self, subject):
        new_aggressivity_change_value = subject.aggressivity_change_value - 100
        subject.body_attribute_change(aggressivity_change_value=new_aggressivity_change_value)
