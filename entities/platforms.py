import pygame
from entities.base import BasePlatform
from settings import COLORS


class StaticPlatform(BasePlatform):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, COLORS["STATIC"])
        self.is_active = True


class PhasePlatform(BasePlatform):
    def __init__(self, x, y, width, height, phase_type):
        color = COLORS["LIGHT_PLATFORM"] if phase_type == "LIGHT" else COLORS["DARK_PLATFORM"]
        super().__init__(x, y, width, height, color)
        self.phase_type = phase_type
        self.original_image = self.image.copy()

    def update(self, current_phase):
        if current_phase == self.phase_type:
            self.is_active = True
            self.image.set_alpha(255)
        else:
            self.is_active = False
            self.image.set_alpha(30)