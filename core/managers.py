import pygame
from settings import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT


class PhaseManager:

    def __init__(self):
        self.current_phase = "LIGHT"

    def toggle(self):
        if self.current_phase == "LIGHT":
            self.current_phase = "SHADOW"
        else:
            self.current_phase = "LIGHT"

    def get_bg_color(self):
        return COLORS["LIGHT_BG"] if self.current_phase == "LIGHT" else COLORS["SHADOW_BG"]


class Camera:
    def __init__(self, level_width, level_height, screen_w, screen_h):
        self.level_width = level_width
        self.level_height = level_height

        self.screen_w = screen_w
        self.screen_h = screen_h

        self.offset_x = 0
        self.offset_y = 0

    def apply(self, entity):
        return entity.rect.move(self.offset_x, self.offset_y)

    def update(self, target):
        x = -target.rect.centerx + int(self.screen_w / 2)
        y = -target.rect.centery + int(self.screen_h / 2)

        if self.level_width < self.screen_w:
            x = (self.screen_w - self.level_width) // 2
        else:
            x = min(0, x)
            x = max(-(self.level_width - self.screen_w), x)

        if self.level_height < self.screen_h:
            y = self.screen_h - self.level_height
        else:
            y = min(0, y)
            y = max(-(self.level_height - self.screen_h), y)

        self.offset_x = x
        self.offset_y = y
