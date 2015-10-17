__author__ = 'HAL9000'

import pygame
from pygame.locals import *
import time

pygame.init()


class RobotState:
    def __init__(self):
        self.x = 0
        self.v = 0
        self.motor_voltage = 0

    def run_iteration(self, dt):
        self.v = self.v * 0.99 + 0.01 * self.motor_voltage * 2
        self.x += self.v * dt
        print(round(self.x*1000)/1000, round(self.v*1000)/1000)


class Renderer:
    def __init__(self, robot_state):
        self.robot_state = robot_state
        self.screen = pygame.display.set_mode((640, 240), pygame.RESIZABLE)
        self.wheel = pygame.image.load("wheel_small.gif")

    def render_robot(self):
        self.screen.fill((255, 255, 255))

        robot_rect = pygame.Rect((round(self.robot_state.x) + 320, 100), (40, 20))
        pygame.draw.rect(self.screen, (180, 0, 180), robot_rect)

        image = self.wheel.copy()
        image_rect = image.get_rect(center=(120, 120))
        image = pygame.transform.rotate(image, int(self.robot_state.x * -30))
        image_rect = image.get_rect(center=image_rect.center)
        self.screen.blit(image, image_rect)

        pygame.display.flip()


class Simulation:
    def __init__(self, tps, robot_state, renderer):
        self.tps = tps
        self.robot_state = robot_state
        self.start_time = time.time()
        self.executed_ticks = 0
        self.renderer = renderer

    def get_desired_ticks(self):
        current = time.time()
        return int((current - self.start_time) * self.tps)

    def run_iteration(self):
        self.robot_state.run_iteration(1 / self.tps)
        self.executed_ticks += 1

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

            desired_ticks = self.get_desired_ticks()
            while self.executed_ticks < desired_ticks:
                self.run_iteration()
            self.renderer.render_robot()


class Motor:
    def __init__(self, robot_state):
        self.robot_state = robot_state

    def set(self, value):
        self.robot_state.motor_voltage = min(max(-1, value), 1) * 5



class Encoder:
    def __init__(self, robot_state):
        self.robot_state = robot_state

    def get_position(self):
        return self.robot_state.x

    def get_speed(self):
        return self.robot_state.v

g_robot_state = RobotState()
g_motor = Motor(g_robot_state)
g_encoder = Encoder(g_robot_state)
g_renderer = Renderer(g_robot_state)

g_motor.set(1)

sim = Simulation(100, g_robot_state, g_renderer)
sim.run()
