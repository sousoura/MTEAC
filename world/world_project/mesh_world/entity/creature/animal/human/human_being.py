from world.entity.entity_import import *
from world.world_project.mesh_world.entity.obj.human_corpse import Human_corpse

"""
    人类类 物种类
    方法用于物种的行为的内部影响
"""


class Human_being(Human, Big_obj):
    # 物种属性
    feeding_habits = ["Fruit"]
    swimming_ability = 4
    life_area = "terrestrial"

    pickable_objs = ["Fruit"]

    # 合成表

    """
        行为合法性判断
    """
    action_list = ["go", "eat", "drink", "attack", "rest", "pick_up", "put_down",
                   "fabricate", "construct", "interaction"]

    def judge_go(self, world_state, command):
        direction = command[1]
        old_position = tuple(self.get_position())
        # 返回一格移动的位置 不考虑半格 可能为浮点或整数 浮点的化将在下面整数化 若出界则为False
        new_position = world_state.position_and_direction_get_adjacent(old_position, direction)

        # 地图边缘判断
        if new_position:
            # 若自己是半格则目的地也会是半格 置整
            new_position = (int(new_position[0]), int(new_position[1]))

            # 半格模式
            # 若在左右半格上
            if old_position[0] % 1 > 0:
                # 方向限制
                if direction == 'left' or direction == 'right':
                    return False
            # 若在上下半格上
            elif old_position[1] % 1 > 0:
                # 方向限制
                if direction == 'down' or direction == 'up':
                    return False

            # 整格模式
            # 攀爬限制 格差
            # 判断落差是否大于生物的爬行能力(水里不用看这个)
            if not "aquatic" and world_state.get_water_map()[new_position[0]][new_position[1]] < 1:
                if abs(world_state.landform_map[int(old_position[0])][int(old_position[1])] -
                       world_state.landform_map[int(new_position[0])][int(new_position[1])]) > \
                        self.get_crawl_ability():
                    return False

            # 地貌限制 水限制
            # 陆生动物下水限制
            if self.life_area == "terrestrial":
                if self.swimming_ability < world_state.get_water_map()[new_position[0]][new_position[1]]:
                    return False

            # 水生动物上岸限制
            if self.life_area == "aquatic":
                if world_state.get_water_map()[new_position[0]][new_position[1]] == 0:
                    return False

            # 实体限制 大物体限制
            if isinstance(self, Big_obj):
                # 大物体互斥规则
                # 如果有大动物挡在前面
                for other_entity in world_state.get_entities_in_position(new_position):
                    if isinstance(other_entity, Big_obj):
                        return False
                for other_entity in \
                        world_state.get_entities_in_position((
                                (old_position[0] + (new_position[0] - old_position[0]) / 2),
                                (old_position[1] + (new_position[1] - old_position[1]) / 2))
                        ):
                    if isinstance(other_entity, Big_obj):
                        return False

            # 挣扎状态判断
            if self.situation == "struggle":
                if random.randrange(100) <= 90:
                    return False

            return True
        else:
            return False

    def judge_eat(self, world_state, command):
        # 吃者
        eator = self
        # 吃的方向
        eat_direction = command[1]
        # 被吃着
        be_eator = command[2]

        # 没有对象
        if be_eator == -1:
            return False

        # 食性不合
        if not self.feeding_habits_judge(be_eator):
            return False

        if not isinstance(be_eator, Food):
            return False

        return True

    def judge_drink(self, world_state, command):
        direction = command[1]
        direction_position = world_state.position_and_direction_get_adjacent(self.get_position(), direction)
        if direction_position:
            return world_state.get_water_map()[int(direction_position[0])][int(direction_position[1])] > 0
        else:
            return False

    def judge_attack(self, world_state, command):
        attacker = self
        attack_direction = command[1]
        be_attackeder = command[2]

        # 没有对象
        if be_attackeder == -1:
            return False

        if not isinstance(be_attackeder, Creature):
            return False

        return True

    def judge_rest(self, world_state, command):
        return True

    def judge_pick_up(self, world_state, command):
        # 拾起者
        picker = self
        # 拾起的方向
        pick_direction = command[1]
        # 被拾起之物
        be_pickor = command[2]

        # 没有对象
        if be_pickor == -1:
            return False

        # 判断可拾起性
        if be_pickor:
            if type(be_pickor).__name__ not in self.pickable_objs:
                return False

        return True

    def judge_put_down(self, world_state, command):
        # 放的方向
        direction = command[1]
        # 放的位置
        direction_position = world_state.position_and_direction_get_adjacent(self.get_position(), direction)

        if not direction_position:
            return False

        return True

    def judge_fabricate(self, world_state, command):
        return True

    def judge_construct(self, world_state, command):
        return True

    def judge_interaction(self, world_state, command):
        return False

    judge_action_method_list = [judge_go, judge_eat, judge_drink, judge_attack, judge_rest,
                                judge_pick_up, judge_put_down,
                                judge_fabricate, judge_construct, judge_interaction]

    """
        行为内部结果执行
    """

    def go_outcome(self, parameter=None, obj=None, degree=None):
        # 这里parameter指的是移动到的新的位置 其它变量置None
        self.move(parameter)

    def eat_outcome(self, parameter=None, obj=None, degree=None):
        # 这里obj是被吃的对象
        self.full_value += 10
        # print(self.full_value)

    def drink_outcome(self, parameter=None, obj=None, degree=None):
        self.drinking_value += 10

    def attack_outcome(self, parameter=None, obj=None, degree=None):
        pass

    def rest_outcome(self, parameter=None, obj=None, degree=None):
        pass

    def pick_up_outcome(self, parameter=None, obj=None, degree=None):
        self.backpack.append(obj)

    def put_down_outcome(self, parameter=None, obj=None, degree=None):
        self.backpack.remove(obj)
        print("put down", obj)
        print(self.backpack)

    def fabricate_outcome(self, parameter=None, obj=None, degree=None):
        pass

    def construct_outcome(self, parameter=None, obj=None, degree=None):
        pass

    def interaction_outcome(self, parameter=None, obj=None, degree=None):
        pass

    action_interior_outcome_method_list = [go_outcome, eat_outcome, drink_outcome, attack_outcome, rest_outcome,
                                           pick_up_outcome, put_down_outcome,
                                           fabricate_outcome, construct_outcome, interaction_outcome]

    """
        行为成本消耗
    """

    def go_cost(self):
        self.body_change(full_value_change=-0.1, drinking_value_change=-0.1)

    def eat_cost(self):
        pass

    def drink_cost(self):
        pass

    def attack_cost(self):
        self.body_change(full_value_change=-0.1, drinking_value_change=-0.1)

    def rest_cost(self):
        pass

    def pick_up_cost(self):
        pass

    def put_down_cost(self):
        pass

    def fabricate_cost(self):
        self.body_change(full_value_change=-0.1, drinking_value_change=-0.1)

    def construct_cost(self):
        self.body_change(full_value_change=-0.1, drinking_value_change=-0.1)

    def interaction_cost(self):
        pass

    action_cost_method_list = [go_cost, eat_cost, drink_cost, attack_cost, rest_cost,
                               pick_up_cost, put_down_cost,
                               fabricate_cost, construct_cost, interaction_cost]

    def __init__(self, position, life, brain, full_value, drinking_value, body_state, gender,
                 crawl_ability, speed, aggressivity, backpack=None):
        super(Human_being, self).__init__(position, life, brain, full_value, drinking_value, body_state,
                                          gender,
                                          crawl_ability, speed, aggressivity)
        self.backpack = backpack
        if not backpack:
            self.backpack = []

    # 得到感知
    '''
        感知的结构： 整个是一个元组 其中：一个元组表示地形 另一个字典表示生物表
    '''

    def get_perception(self, landform_map, things_position):
        return tuple(landform_map), things_position

    def die(self):
        return [Human_corpse(self.get_position(), 20)]

    def get_backpack(self):
        return self.backpack[:]
