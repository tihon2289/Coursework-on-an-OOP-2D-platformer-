import pygame
from entities.base import GameObject
from settings import COLORS


class Hazards(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.is_active = True


class PhaseSpike(Hazards):
    def __init__(self, x, y, width, height, phase_type):
        color = COLORS["LIGHT_PLATFORM"] if phase_type == "LIGHT" else COLORS["DARK_PLATFORM"]
        super().__init__(x, y, width, height, color)
        self.phase_type = phase_type

    def update(self, current_phase):
        if current_phase == self.phase_type:
            self.is_active = True
            self.image.set_alpha(255)
        else:
            self.is_active = False
            self.image.set_alpha(30)
