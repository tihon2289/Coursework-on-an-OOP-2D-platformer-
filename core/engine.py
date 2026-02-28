import pygame
import sys
from settings import IS_FULLSCREEN, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLORS
from entities.platforms import StaticPlatform, PhasePlatform
from entities.player import Player

class Game:
    def __init__(self):
        pygame.init()
        if IS_FULLSCREEN:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.width = self.screen.get_width()
            self.height = self.screen.get_height()
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.width = SCREEN_WIDTH
            self.height = SCREEN_HEIGHT

            pygame.display.set_caption("Фазовый Прыжок (Тестовый полигон)")
            self.clock = pygame.time.Clock()
            self.running = True

            self.current_phase = "LIGHT"
            self.setup_test_level()

    def setup_test_level(self):
        pass


