import pygame
from settings import TILE_SIZE
from entities.platforms import StaticPlatform, PhasePlatform
from entities.hazards import PhaseSpike, StaticSpike
from entities.items import Portal, Decoration, Key 
from entities.player import Player

class Level:
    def __init__(self, filepath):
        self.filepath = filepath
        self.player = None
        self.portal = None
        self.width = 0
        self.height = 0

    def load(self):
        all_sprites = pygame.sprite.Group()
        platforms = pygame.sprite.Group()
        hazards = pygame.sprite.Group()
        decorations = pygame.sprite.Group()
        keys_group = pygame.sprite.Group()

        with open(self.filepath, 'r', encoding='utf-8') as file:
            level_data = [line.strip() for line in file.readlines()]

        self.height = len(level_data) * TILE_SIZE
        self.width = len(level_data[0]) * TILE_SIZE if self.height > 0 else 0

        # Парсим матрицу уровня
        for row_index, row in enumerate(level_data):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                # Кусок кода в core/level_parser.py
                if cell == '[':
                    platform = StaticPlatform(x, y, TILE_SIZE, TILE_SIZE, block_type="left")
                    all_sprites.add(platform)
                    platforms.add(platform)
                elif cell == 'G':
                    platform = StaticPlatform(x, y, TILE_SIZE, TILE_SIZE, block_type="mid")
                    all_sprites.add(platform)
                    platforms.add(platform)
                elif cell == ']':
                    platform = StaticPlatform(x, y, TILE_SIZE, TILE_SIZE, block_type="right")
                    all_sprites.add(platform)
                    platforms.add(platform)
                elif cell == 'B':
                    platform = StaticPlatform(x, y, TILE_SIZE, TILE_SIZE, block_type="deep")
                    all_sprites.add(platform)
                    platforms.add(platform)
                elif cell == '1':
                    platform = StaticPlatform(x, y, TILE_SIZE, TILE_SIZE, block_type="pattern_1")
                    all_sprites.add(platform)
                    platforms.add(platform)
                elif cell == '2':
                    platform = StaticPlatform(x, y, TILE_SIZE, TILE_SIZE, block_type="pattern_2")
                    all_sprites.add(platform)
                    platforms.add(platform)
                elif cell == '3':
                    platform = StaticPlatform(x, y, TILE_SIZE, TILE_SIZE, block_type="pattern_3")
                    all_sprites.add(platform)
                    platforms.add(platform)
                elif cell == '4':
                    platform = StaticPlatform(x, y, TILE_SIZE, TILE_SIZE, block_type="pattern_4")
                    all_sprites.add(platform)
                    platforms.add(platform)
                elif cell == '{':
                    platform = StaticPlatform(x, y, TILE_SIZE, TILE_SIZE, block_type="float_left")
                    all_sprites.add(platform)
                    platforms.add(platform)
                elif cell == '=':
                    platform = StaticPlatform(x, y, TILE_SIZE, TILE_SIZE, block_type="float_mid")
                    all_sprites.add(platform)
                    platforms.add(platform)
                elif cell == '}':
                    platform = StaticPlatform(x, y, TILE_SIZE, TILE_SIZE, block_type="float_right")
                    all_sprites.add(platform)
                    platforms.add(platform)
                elif cell == 'L':
                    platform = PhasePlatform(x, y, TILE_SIZE, TILE_SIZE, "LIGHT")
                    all_sprites.add(platform)
                    platforms.add(platform)
                elif cell == 'S':
                    platform = PhasePlatform(x, y, TILE_SIZE, TILE_SIZE, "SHADOW")
                    all_sprites.add(platform)
                    platforms.add(platform)
                elif cell == '@':
                    self.player = Player(x, y)
                    all_sprites.add(self.player)
                elif cell == '^':
                    spike = StaticSpike(x, y, TILE_SIZE, TILE_SIZE)
                    all_sprites.add(spike)
                    hazards.add(spike)
                elif cell == 'D':
                    self.portal = Portal(x, y, TILE_SIZE, TILE_SIZE)
                    all_sprites.add(self.portal)
                elif cell == 'K':
                    key_item = Key(x + 15, y + 15, 30, 30)
                    all_sprites.add(key_item)
                    keys_group.add(key_item)
                elif cell == 'a':
                    decor = Decoration(x, y, TILE_SIZE, TILE_SIZE, 1)
                    all_sprites.add(decor)
                    decorations.add(decor)
                elif cell == 'b':
                    decor = Decoration(x, y, TILE_SIZE, TILE_SIZE, 2)
                    all_sprites.add(decor)
                    decorations.add(decor)
                elif cell == 'c':
                    decor = Decoration(x, y, TILE_SIZE, TILE_SIZE, 3)
                    all_sprites.add(decor)
                    decorations.add(decor)
                elif cell == 'd':
                    decor = Decoration(x, y, TILE_SIZE, TILE_SIZE, 4)
                    all_sprites.add(decor)
                    decorations.add(decor)

        return self.player, self.portal, all_sprites, platforms, hazards, decorations, keys_group, self.width, self.height