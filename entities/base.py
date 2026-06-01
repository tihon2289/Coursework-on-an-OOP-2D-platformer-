import pygame
import os
from settings import GRAVITY, MAX_FALL_SPEED

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, image_path=None):
        super().__init__()
        
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill(color)
        
        if image_path and os.path.exists(image_path):
            loaded_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(loaded_image, (width, height))
            
        self.rect = self.image.get_rect(topleft=(x, y))
        self.original_image = self.image.copy() 

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Entity(GameObject):
    def __init__(self, x, y, width, height, color, image_path=None):
        super().__init__(x, y, width, height, color, image_path)
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 0
        self.is_grounded = False

    def apply_gravity(self):
        self.velocity_y += GRAVITY
        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED
        self.rect.y += self.velocity_y

class BasePlatform(GameObject):
    def __init__(self, x, y, width, height, color, image_path=None):
        super().__init__(x, y, width, height, color, image_path)
        self.is_active = True

    def update(self, *args, **kwargs):
        pass