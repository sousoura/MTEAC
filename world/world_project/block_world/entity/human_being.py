from world.entity.entity_import import *


class Human_being(Human):
    def __init__(self, position):
        super(Human_being, self).__init__(position)

    def move(self, new_position):
        self.position = new_position

    def action_cost(self):
        pass

    def action_interior_outcome(self):
        pass

    def body_attribute_change(self):
        pass

    def body_change(self):
        pass

    def die(self):
        pass

    def judge_action_validity(self):
        pass

    def post_turn_change(self):
        pass
