# --- СТАРТ ФАЙЛА entities/hazards.py ---
import pygame
from entities.base import GameObject
from settings import COLORS

class Hazards(GameObject):
    # Добавили image_path
    def __init__(self, x, y, width, height, color, image_path=None):
        super().__init__(x, y, width, height, color, image_path)
        self.is_active = True

class StaticSpike(Hazards):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (255, 0, 0), image_path="assets/images/spikesLow.png")

class PhaseSpike(Hazards):
    def __init__(self, x, y, width, height, phase_type):
        color = COLORS["LIGHT_PLATFORM"] if phase_type == "LIGHT" else COLORS["SHADOW_PLATFORM"]
        img_path = "assets/images/spike_light.png" if phase_type == "LIGHT" else "assets/images/spike_shadow.png"
        
        super().__init__(x, y, width, height, color, image_path=img_path)
        self.phase_type = phase_type

    def update(self, current_phase):
        if current_phase == self.phase_type:
            self.is_active = True
            self.image.set_alpha(255) 
        else:
            self.is_active = False
            self.image.set_alpha(0)   