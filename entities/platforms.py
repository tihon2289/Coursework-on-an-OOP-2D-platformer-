import pygame
import os
from entities.base import BasePlatform
from settings import COLORS

class StaticPlatform(BasePlatform):
    def __init__(self, x, y, width, height, block_type="mid"):
        super().__init__(x, y, width, height, COLORS["STATIC"])
        self.is_active = True
        
        if block_type == "left":
            img_light, img_shadow = "assets/images/grass_left_light.png", "assets/images/grass_left_shadow.png"
        elif block_type == "right":
            img_light, img_shadow = "assets/images/grass_right_light.png", "assets/images/grass_right_shadow.png"
        elif block_type == "mid":
            img_light, img_shadow = "assets/images/grass_mid_light.png", "assets/images/grass_mid_shadow.png"
        elif block_type == "deep":
            img_light, img_shadow = "assets/images/dirt_deep_light.png", "assets/images/dirt_deep_shadow.png"
            
        elif block_type == "float_left":
            img_light, img_shadow = "assets/images/float_left_light.png", "assets/images/float_left_shadow.png"
        elif block_type == "float_mid":
            img_light, img_shadow = "assets/images/float_mid_light.png", "assets/images/float_mid_shadow.png"
        elif block_type == "float_right":
            img_light, img_shadow = "assets/images/float_right_light.png", "assets/images/float_right_shadow.png"
            
        elif block_type == "pattern_1":
            img_light, img_shadow = "assets/images/pattern_1_light.png", "assets/images/pattern_1_shadow.png"
        elif block_type == "pattern_2":
            img_light, img_shadow = "assets/images/pattern_2_light.png", "assets/images/pattern_2_shadow.png"
        elif block_type == "pattern_3":
            img_light, img_shadow = "assets/images/pattern_3_light.png", "assets/images/pattern_3_shadow.png"
        elif block_type == "pattern_4":
            img_light, img_shadow = "assets/images/pattern_4_light.png", "assets/images/pattern_4_shadow.png"

        self.image_light = self._load_img(img_light, width, height, COLORS["LIGHT_PLATFORM"])
        self.image_shadow = self._load_img(img_shadow, width, height, COLORS["SHADOW_PLATFORM"])
        
        self.image = self.image_light
        self.rect = self.image.get_rect(topleft=(x, y))

    def _load_img(self, path, width, height, fallback_color):
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        surf.fill(fallback_color)
        if os.path.exists(path):
            loaded = pygame.image.load(path).convert_alpha()
            surf = pygame.transform.scale(loaded, (width, height))
        return surf

    def update(self, current_phase):
        if current_phase == "LIGHT":
            self.image = self.image_light
        else:
            self.image = self.image_shadow


class PhasePlatform(BasePlatform):
    def __init__(self, x, y, width, height, phase_type):
        color = COLORS["LIGHT_PLATFORM"] if phase_type == "LIGHT" else COLORS["SHADOW_PLATFORM"]
        img_path = "assets/images/dirt_deep_light.png" if phase_type == "LIGHT" else "assets/images/dirt_deep_shadow.png"
        
        super().__init__(x, y, width, height, color, image_path=img_path)
        self.phase_type = phase_type
        self.original_image = self.image.copy()

    def update(self, current_phase):
        if current_phase == self.phase_type:
            self.is_active = True
            self.image.set_alpha(128) 
        else:
            self.is_active = False
            self.image.set_alpha(0) 