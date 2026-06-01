import pygame
import os
from entities.base import Entity
from settings import COLORS

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, COLORS["PLAYER"])
        self.jump_power = -17
        self.speed = 10
        self.facing_right = True
        
        self.state = "idle" 
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 5 

        self.idle_image = self._load_image("assets/images/player_stand.png")
        self.run_frames = []
        self.run_frames.append(self._load_image("assets/images/player_walk1.png"))
        self.run_frames.append(self._load_image("assets/images/player_walk2.png"))
        self.run_frames.append(self._load_image("assets/images/player_walk3.png"))
        self.run_frames.append(self._load_image("assets/images/player_walk4.png"))
        self.run_frames.append(self._load_image("assets/images/player_walk5.png"))

        self.image = self.idle_image

        self.jump_sound = self._load_sound("assets/sounds/jump.wav")
        self.step_sound = self._load_sound("assets/sounds/step.wav")
        if self.step_sound:
            self.step_sound.set_volume(0.3) 

    def _load_image(self, path):
        surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        surf.fill(COLORS["PLAYER"]) 
        if os.path.exists(path):
            loaded = pygame.image.load(path).convert_alpha()
            surf = pygame.transform.scale(loaded, (self.rect.width, self.rect.height))
        return surf

    def _load_sound(self, path):
        if os.path.exists(path):
            return pygame.mixer.Sound(path)
        print(f"ОШИБКА: Нет звука {path}!")
        return None

    def update(self, keys, platforms):
        self.velocity_x = 0
        is_moving = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -self.speed
            self.facing_right = False
            is_moving = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.speed
            self.facing_right = True
            is_moving = True

        if is_moving:
            self.state = "run"
        else:
            self.state = "idle"

        self._animate()

        self.rect.x += self.velocity_x
        self._check_collisions_x(platforms)

        self.apply_gravity()
        self._check_collisions_y(platforms)

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.is_grounded:
            self.velocity_y = self.jump_power
            self.is_grounded = False
            if self.jump_sound:
                self.jump_sound.play() 

    def _animate(self):
        if self.state == "idle":
            current_image = self.idle_image
            self.current_frame = 0 
        elif self.state == "run":
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.current_frame += 1
                
                if self.is_grounded and self.step_sound:
                    self.step_sound.play()
                
                if self.current_frame >= len(self.run_frames):
                    self.current_frame = 0
            current_image = self.run_frames[self.current_frame]

        if not self.facing_right:
            self.image = pygame.transform.flip(current_image, True, False)
        else:
            self.image = current_image

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