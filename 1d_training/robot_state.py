import pygame
from pygame.locals import *
import time

from robot_code import setup
from robot_code import loop
from robot_code import get_robot_hooks

pygame.init()


class RobotState:
    def __init__(self):
        self.x = 0
        self.v = 0
        self.motor_voltage = 0

    def run_iteration(self, dt):
        self.v = self.v * 0.99 + 0.005 * self.motor_voltage
        self.x += self.v * dt


class Renderer:
    def __init__(self, robot_state):
        self.robot_state = robot_state
        self.screen = pygame.display.set_mode((640, 240), pygame.RESIZABLE)
        self.wheel = pygame.image.load("wheel_small.gif")
        self.font = pygame.font.Font(None, 20)

    def render_robot(self):
        self.screen.fill((255, 255, 255))

        image = self.wheel.copy()
        image_rect = image.get_rect(center=(120, 120))
        image = pygame.transform.rotate(image, int(self.robot_state.x * -60))
        image_rect = image.get_rect(center=image_rect.center)
        self.screen.blit(image, image_rect)

        robot_screen_x_pos = round(self.robot_state.x * 100) + 280
        robot_rect = pygame.Rect((robot_screen_x_pos, 80), (40, 20))
        pygame.draw.rect(self.screen, (180, 0, 180), robot_rect)
        pygame.draw.circle(self.screen, (0, 0, 0), (robot_screen_x_pos + 10, 100), 5)
        pygame.draw.circle(self.screen, (0, 0, 0), (robot_screen_x_pos + 30, 100), 5)

        rounded_position = round(self.robot_state.x * 100) / 100
        stats = self.font.render("Position: " + str(rounded_position), 1, (0, 0, 0))
        self.screen.blit(stats, (310, 180))

        pygame.draw.line(self.screen, (0, 0, 0), (320, 125), (320, 130))
        pygame.draw.line(self.screen, (0, 0, 0), (420, 125), (420, 130))
        pygame.draw.line(self.screen, (0, 0, 0), (520, 125), (520, 130))
        pygame.draw.line(self.screen, (0, 0, 0), (620, 125), (620, 130))

        m0 = self.font.render("0m", 1, (0, 0, 0))
        m1 = self.font.render("1m", 1, (0, 0, 0))
        m2 = self.font.render("2m", 1, (0, 0, 0))
        m3 = self.font.render("3m", 1, (0, 0, 0))

        self.screen.blit(m0, (310, 140))
        self.screen.blit(m1, (410, 140))
        self.screen.blit(m2, (510, 140))
        self.screen.blit(m3, (610, 140))

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
        self.renderer.render_robot()
        loop()

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
MOTOR = Motor(g_robot_state)
ENCODER = Encoder(g_robot_state)
g_renderer = Renderer(g_robot_state)

get_robot_hooks(MOTOR, ENCODER)

sim = Simulation(50, g_robot_state, g_renderer)

setup()

sim.run()
