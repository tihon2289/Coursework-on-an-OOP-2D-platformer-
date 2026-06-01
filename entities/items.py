import pygame
import os
from entities.base import GameObject

class Collectible(GameObject):
    pass

class Key(Collectible):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (255, 255, 0)) 
        self.image = self._load_image("assets/images/key.png", width, height)

    def _load_image(self, path, w, h):
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.fill((255, 215, 0)) 
        if os.path.exists(path):
            loaded = pygame.image.load(path).convert_alpha()
            surf = pygame.transform.scale(loaded, (w, h))
        return surf


class Portal(Collectible):
    def __init__(self, x, y, width, height):
        super().__init__(x, y - height, width, height * 2, (0, 0, 0))
        self.is_open = False
        
        self.locked_image = self._assemble_portal(
            "assets/images/portal_top_locked.png", 
            "assets/images/portal_bottom_locked.png", 
            width, height, (100, 100, 100) 
        )
        
        self.unlocked_image = self._assemble_portal(
            "assets/images/portal_top.png", 
            "assets/images/portal_bottom.png", 
            width, height, (0, 250, 250) # Голубой цвет
        )
        
        # Изначально портал закрыт
        self.image = self.locked_image

    def _assemble_portal(self, top_path, bottom_path, w, h, fallback_color):
        surf = pygame.Surface((w, h * 2), pygame.SRCALPHA)
        
        # Верхняя часть
        top_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        top_surf.fill(fallback_color)
        if os.path.exists(top_path):
            top_surf = pygame.transform.scale(pygame.image.load(top_path).convert_alpha(), (w, h))
            
        # Нижняя часть
        bot_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        bot_surf.fill(fallback_color)
        if os.path.exists(bottom_path):
            bot_surf = pygame.transform.scale(pygame.image.load(bottom_path).convert_alpha(), (w, h))
            
        surf.blit(top_surf, (0, 0))
        surf.blit(bot_surf, (0, h))
        return surf

    def open_portal(self):
        self.is_open = True
        self.image = self.unlocked_image # Меняем картинку!

    def update(self):
        pass

class Decoration(GameObject):
    def __init__(self, x, y, width, height, dec_type):
        super().__init__(x, y, width, height, (0, 0, 0, 0))
        if dec_type == 1:
            img_light, img_shadow = "assets/images/plant_1_light.png", "assets/images/plant_1_shadow.png"
        elif dec_type == 2:
            img_light, img_shadow = "assets/images/plant_2_light.png", "assets/images/plant_2_shadow.png"
        elif dec_type == 3:
            img_light, img_shadow = "assets/images/plant_3_light.png", "assets/images/plant_3_shadow.png"
        else:
            img_light, img_shadow = "assets/images/plant_4_light.png", "assets/images/plant_4_shadow.png"

        self.image_light = self._load_image(img_light, width, height)
        self.image_shadow = self._load_image(img_shadow, width, height)
        self.image = self.image_light

    def _load_image(self, path, w, h):
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        if os.path.exists(path):
            surf = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (w, h))
        return surf

    def update(self, current_phase):
        self.image = self.image_light if current_phase == "LIGHT" else self.image_shadow