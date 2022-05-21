from world.exhibitor_super import Exhibitor_super
import pygame
from pygame.key import *
from pygame.locals import *
from pygame.color import *


class Exhibitor(Exhibitor_super):
    def __init__(self, world, size_para):
        self.world = world
        self.size_para = size_para
        self.__init()

    def __init(self):
        # pygame初始化
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        self.clock = pygame.time.Clock()

        self.draw_options = self.world.state.get_draw_options(self.screen)

        self.FPS = 60
        self.balls = []  # 所有的球
        self.ticks_to_next_ball = 10  # 多少帧后出现下一个球
        self.exact = 10  # 一帧计算几次

    def display(self, mode):
        self.my_events()
        self.clear_screen()
        self.draw_objects()
        pygame.display.flip()
        self.clock.tick(self.FPS)
        pygame.display.set_caption("fps: " + str(self.clock.get_fps()))

    def my_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                exit()
            elif event.type == KEYDOWN and event.key == K_p:
                # 截图
                pygame.image.save(self.screen, "bouncing_balls.png")

    def clear_screen(self):
        self.screen.fill(THECOLORS["white"])

    def draw_objects(self):
        self.world.state.space.debug_draw(self.draw_options)

    def set_out(self):
        pass
