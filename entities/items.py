import pygame
from base import GameObject


class Collectible(GameObject):
    pass


class Anchor(Collectible):
    def __init__(self, x, y):
        super().__init__(x,y, 20, 20, (255, 215, 0))


class Portal(Collectible):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 60, (50, 200, 50))
        self.is_open = False

    def update(self, anchors_collected, total_anchors):
        if total_anchors >= anchors_collected:
            self.is_open = True
            self.image.fill((0, 250, 250))
