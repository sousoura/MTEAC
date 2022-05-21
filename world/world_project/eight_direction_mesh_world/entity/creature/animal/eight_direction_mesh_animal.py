"""
    动物是会运动 会行动的生物
"""
import random

from world.entity.creature.creature import Creature
from world.entity.big_obj import Big_obj
from world.entity.obj.food import Food
from abc import ABCMeta, abstractmethod

from world.entity.creature.animal.animal import Animal


class Eight_direction_mesh_animal(Animal, metaclass=ABCMeta):
    # 物种属性
    feeding_habits = []
    swimming_ability = 1
    life_area = "terrestrial"

    """
        行为合法性判断
    """
    action_list = ["go", "eat", "drink", "attack", "rest"]

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
        eator = self
        eat_direction = command[1]
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

    judge_action_method_list = [judge_go, judge_eat, judge_drink, judge_attack, judge_rest]

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

    action_interior_outcome_method_list = [go_outcome, eat_outcome, drink_outcome, attack_outcome, rest_outcome]

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

    action_cost_method_list = [go_cost, eat_cost, drink_cost, attack_cost, rest_cost]

    def __init__(self, position, life, brain, full_value, drinking_value, body_state, gender,
                 crawl_ability, speed, aggressivity, carapace=0):
        super(Animal, self).__init__(position, life, carapace)

        """
            目前動物的屬性設計:
                基本属性
                    位置
                    大脑

                合法行为集      类别          移动 攻击 吃 交配 喝水 休息
                    对应的行为影响方法

                状态属性
                    生命值          数值          float 0~100
                    饱腹值          数值          float 0~100
                    饮水值          数值          float 0~100
                    身体状态        数字 类别      健康 受伤 饥饿 缺水

                属性属性（个体差异）
                    性别           布尔

                能力属性
                    速度            数值           int
                    跃力            数值           int
                    攻击力          数值           int

                物种属性
                    食性            数组           能吃的物种的数量
                    大小（待修改）   布尔            True为女 False为男
                    水性            数值元组        能适应多深的水 在水里待多长时间 游泳速度等
                    生活场所         数字 类别       能不能上岸 能不能潜水：陆地生物 海洋生物 飞行生物 两栖生物
                    地貌兼容性（待修改）
                    飞行（待加）

                外部状态
                    身体情况        挣扎          "normal", "struggle"
        """

        # 基本属性
        self.brain = brain

        # 状态属性
        self.full_value = full_value
        self.drinking_value = drinking_value
        self.body_state = body_state

        # 个体属性
        self.gender = gender

        # 能力属性
        self.crawl_ability = crawl_ability
        self.speed = speed
        self.aggressivity = aggressivity

        self.crawl_ability_change_value = 0
        self.speed_change_value = 0
        self.aggressivity_change_value = 0

        self.geomorphic_compatibility = None

        # 行动状态属性
        """
            步距模式 每走一次的格数
                默认为一 随时可以在速度范围之内调
        """
        self.pace = 1

        # 境况状态
        self.situation = "normal"

    def move(self, new_position):
        self.position = new_position

    @abstractmethod
    def get_perception(self, landform_map, things_position):
        pass

    # 想出一个行为
    def devise_an_act(self, perception):
        return self.brain.devise_an_act(perception, self)

    def get_speed(self):
        return self.speed + self.speed_change_value

    def get_crawl_ability(self):
        return self.crawl_ability

    def judge_geomorphic_compatibility(self):
        return True

    def change_pace(self, num):
        if isinstance(num, int):
            if 0 < num <= self.speed + self.speed_change_value:
                self.pace = num

    def get_pace(self):
        return self.pace

    def get_aggressivity(self):
        return self.aggressivity

    """
        待改进为用isinstance判断
    """

    @classmethod
    def feeding_habits_judge(cls, eat_object):
        return type(eat_object).__name__ in cls.feeding_habits

    # 判断行动合法性 属性对行动的影响体现在此
    # 判断行为是否因为动物内因的困难而无法进行
    def judge_action_validity(self, world_state, command):
        action_type_num = self.action_list.index(command[0])
        return self.judge_action_method_list[action_type_num](self, world_state, command)

    # 执行一类动作的成本 能量消耗
    def action_cost(self, action_type):
        action_type_num = self.action_list.index(action_type)
        self.action_cost_method_list[action_type_num](self)

    # 动作成功的影响
    def action_interior_outcome(self, action_type, parameter=None, obj=None, degree=None):
        action_type_num = self.action_list.index(action_type)
        self.action_interior_outcome_method_list[action_type_num](self, parameter=parameter, obj=obj, degree=degree)

    """
        改变身体状态的工具函数
    """

    def body_change(self, full_value_change=0.0, drinking_value_change=0.0,
                    life_change_value=0.0, body_state_change=False):
        if self.full_value > 0:
            self.full_value += full_value_change
            self.full_value = max(0, self.full_value)
        if self.drinking_value > 0:
            self.drinking_value += drinking_value_change
            self.drinking_value = max(0, self.drinking_value)
        if self.life > 0:
            self.life += life_change_value
            self.life = max(0, self.life)
        if body_state_change:
            self.body_state = body_state_change

    """
        改变身体属性的工具函数
    """

    def body_attribute_change(self,
                              crawl_ability_change_value=None,
                              speed_change_value=None,
                              aggressivity_change_value=None):
        if crawl_ability_change_value is not None:
            self.crawl_ability_change_value = crawl_ability_change_value

        if speed_change_value is not None:
            self.speed_change_value = speed_change_value

        if aggressivity_change_value is not None:
            self.aggressivity_change_value = aggressivity_change_value

    def post_turn_change(self):
        crawl_ability_change_value = self.crawl_ability_change_value
        speed_change_value = self.speed_change_value
        aggressivity_change_value = self.aggressivity_change_value
        life_change_value = 0

        if self.full_value > 0:
            self.body_change(full_value_change=-0.1)
            if self.full_value <= 30:
                crawl_ability_change_value -= 0.5
                speed_change_value -= 0.5
                aggressivity_change_value -= 0.5
            elif self.full_value <= 10:
                crawl_ability_change_value -= 1
                speed_change_value -= 1
                aggressivity_change_value -= 1
                life_change_value -= 1
        else:
            crawl_ability_change_value -= 2
            speed_change_value -= 2
            aggressivity_change_value -= 2
            life_change_value -= 2

        if self.drinking_value > 0:
            self.body_change(full_value_change=-0.1)
            if self.drinking_value <= 30:
                crawl_ability_change_value -= 0.5
                speed_change_value -= 0.5
                aggressivity_change_value -= 0.5
            elif self.drinking_value <= 10:
                crawl_ability_change_value -= 1
                speed_change_value -= 1
                aggressivity_change_value -= 1
                life_change_value -= 1
        else:
            crawl_ability_change_value -= 2
            speed_change_value -= 2
            aggressivity_change_value -= 2
            life_change_value -= 2

        self.body_change(life_change_value=life_change_value)
        self.body_attribute_change(crawl_ability_change_value=crawl_ability_change_value,
                                   speed_change_value=speed_change_value,
                                   aggressivity_change_value=aggressivity_change_value)

    @abstractmethod
    def die(self):
        pass
