import pygame
from entities.base import Entity
from settings import COLORS


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, COLORS["PLAYER"], speed = 6)
        self.jump_power = -12

    def update(self, keys, platforms):
        self.velocity_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -self.speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.speed

        self.rect.x += self.velocity_x
        self._check_collisions_x(platforms)

        self.apply_gravity()
        self._check_collisions_y(platforms)

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.is_grounded:
            self.velocity_y = self.jump_power
            self.is_grounded = False

    def _check_collisions_x(self, platforms):
        for platform in platforms:
            if platform.rect.colliderect(self.rect) and platform.is_active:
                if self.velocity_x > 0:
                    self.rect.right = platform.rect.left
                elif self.velocity_x < 0:
                    self.rect.left = platform.rect.right

    def _check_collisions_y(self, platforms):
        self.is_grounded = False
        for platform in platforms:
            if platform.rect.colliderect(self.rect) and platform.is_active:
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.is_grounded = True
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

