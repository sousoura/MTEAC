# ctypes，用于python和c++的交互
import ctypes

import pymunk
import pymunk.pygame_util
import random

if __name__ == "__main__":
    import sys
    import os

    CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]  # 当前目录
    config_path = CURRENT_DIR.rsplit('\\', 2)[0]  # 上三级目录
    sys.path.insert(0, config_path)
    from state import State
    from world.entity.entity_import import *
    """
        here "blank_world"
    """
    from world.world_project.blank_world.entity.blank_entities import *
else:
    from world.state import State
    from world.entity.entity_import import *
    """
        here "blank_world"
    """
    from world.world_project.blank_world.entity.blank_entities import *


class Physics_state(State):

    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 900.0)

        self.FPS = 60
        self.balls = []  # 所有的球
        self.ticks_to_next_ball = 10  # 多少帧后出现下一个球
        self.exact = 10  # 一帧计算几次

    def create_static_obj(self):
        static_body = self.space.static_body
        static_lines = [
            pymunk.Segment(static_body, (111.0, 280.0), (407.0, 246.0), 0.0),
            pymunk.Segment(static_body, (407.0, 246.0), (407.0, 343.0), 0.0)
        ]
        for line in static_lines:
            line.elasticity = 0.95  # 弹性系数 0-1
            line.friction = 0.9  # 摩擦系数 0-1
        self.space.add(static_lines)

    def create_obj(self):
        mass = 10  # 质量
        radius = 25  # 半径
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        x = random.randint(115, 350)
        body.position = x, 400
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 0.9
        self.space.add(body, shape)
        self.balls.append(shape)

    def update_balls(self):
        # 根据需要创建/移除球。每帧只调用一次。
        self.ticks_to_next_ball -= 1
        if self.ticks_to_next_ball <= 0:
            self.create_obj()
            ticks_to_next_ball = 100
        # 移除低于100的球
        balls_to_remove = [ball for ball in self.balls if ball.body.position.y < 100]
        for ball in balls_to_remove:
            self.space.remove(ball, ball.body)
            self.balls.remove(ball)

    def step(self):
        self.update_balls()
        for x in range(self.exact):
            self.space.step(1 / self.FPS / self.exact)

    def get_draw_options(self, screen):
        # 在pygame上创建画板
        draw_options = pymunk.pygame_util.DrawOptions(screen)
        return draw_options
