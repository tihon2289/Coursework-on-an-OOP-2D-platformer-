# --- СТАРТ ФАЙЛА core/engine.py ---
import pygame
import sys
import os

from settings import IS_FULLSCREEN, SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from core.managers import PhaseManager, Camera
from core.level_parser import Level
from core.db_manager import DatabaseManager
from ui.hud import UIManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        if IS_FULLSCREEN:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.set_caption("Фазовый Прыжок")
        self.clock = pygame.time.Clock()
        self.running = True

        self.ui = UIManager(self.screen.get_width(), self.screen.get_height())
        self.db = DatabaseManager()
        
        self.state = "AUTH"
        self.current_user_id = None
        self.current_username = ""
        self.current_progress = 0
        self.user_stars = {} # Хранит звезды пользователя

        self.current_level_path = "assets/levels/level_01.txt"
        self.current_level_num = 1
        
        # Таймер
        self.start_ticks = 0
        self.elapsed_time = 0
        self.earned_stars = 0

        self.player = None
        self.portal = None
        self.camera = None
        self.phase_manager = PhaseManager()
        
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.decorations = pygame.sprite.Group()
        self.keys_group = pygame.sprite.Group()
        
        self.total_keys = 0
        self.collected_keys = 0

        self.bg_base_light = self._load_bg("assets/images/bg_base_light.png", False)
        self.bg_pattern_light = self._load_bg("assets/images/bg_pattern_light.png", True)
        self.bg_top_light = self._load_bg("assets/images/bg_top_light.png", True)

        self.bg_base_shadow = self._load_bg("assets/images/bg_base_shadow.png", False)
        self.bg_pattern_shadow = self._load_bg("assets/images/bg_pattern_shadow.png", True)
        self.bg_top_shadow = self._load_bg("assets/images/bg_top_shadow.png", True)

        self.music_path = "assets/sounds/bg_music.mp3"
        if os.path.exists(self.music_path):
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.set_volume(0.2)

    def _load_bg(self, path, use_alpha):
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha() if use_alpha else pygame.image.load(path).convert()
            return pygame.transform.scale(img, (self.screen.get_width(), self.screen.get_height()))
        return None

    def load_level(self, filepath):
        if not os.path.exists(filepath):
            # Если уровня не существует, возвращаемся в меню
            self.state = "MENU"
            return

        self.phase_manager = PhaseManager()
        level = Level(filepath)
        self.player, self.portal, self.all_sprites, self.platforms, self.hazards, self.decorations, self.keys_group, lvl_w, lvl_h = level.load()
        self.camera = Camera(lvl_w, lvl_h, self.screen.get_width(), self.screen.get_height())
        
        self.total_keys = len(self.keys_group)
        self.collected_keys = 0
        if self.total_keys == 0 and self.portal:
            self.portal.open_portal()
            
        self.current_level_path = filepath
        # Определяем номер уровня из названия файла
        try: self.current_level_num = int(filepath.split("_")[-1].split(".")[0])
        except: self.current_level_num = 1
        
        self.start_ticks = pygame.time.get_ticks() # ЗАПУСК ТАЙМЕРА
        self.state = "PLAYING"
        
        if os.path.exists(self.music_path):
            pygame.mixer.music.play(-1)

    def calculate_stars(self, time_taken):
        # Логика выдачи звезд (Спидран)
        if time_taken <= 15.0: return 3   # Быстрее 15 сек = 3 звезды
        elif time_taken <= 30.0: return 2 # Быстрее 30 сек = 2 звезды
        else: return 1                    # Медленнее = 1 звезда

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.state == "AUTH":
                self.ui.input_login.handle_event(event)
                self.ui.input_password.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "PLAYING":
                        self.state = "MENU"
                        pygame.mixer.music.stop()
                    else:
                        self.running = False
                if event.key == pygame.K_SPACE and self.state == "PLAYING":
                    self.phase_manager.toggle()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                if self.state == "AUTH":
                    username = self.ui.input_login.text
                    password = self.ui.input_password.text
                    if self.ui.btn_auth_login.rect.collidepoint(mouse_pos):
                        success, u_id, prog, msg = self.db.login(username, password)
                        self.ui.auth_message = msg
                        if success:
                            self.current_user_id = u_id
                            self.current_progress = prog
                            self.current_username = username
                            self.user_stars = self.db.get_user_stars(u_id) # Загружаем звезды!
                            self.state = "MENU"
                    elif self.ui.btn_auth_reg.rect.collidepoint(mouse_pos):
                        success, msg = self.db.register(username, password)
                        self.ui.auth_message = msg

                elif self.state == "MENU":
                    if self.ui.btn_play.rect.collidepoint(mouse_pos):
                        self.load_level(self.current_level_path)
                    elif self.ui.btn_levels.rect.collidepoint(mouse_pos):
                        self.user_stars = self.db.get_user_stars(self.current_user_id) # Обновляем звезды
                        self.state = "LEVEL_SELECT"
                    elif self.ui.btn_logout.rect.collidepoint(mouse_pos):
                        self.current_user_id = None
                        self.ui.input_login.text, self.ui.input_password.text, self.ui.auth_message = "", "", ""
                        self.state = "AUTH"
                    elif self.ui.btn_quit.rect.collidepoint(mouse_pos):
                        self.running = False

                elif self.state == "LEVEL_SELECT":
                    if self.ui.btn_lvl_1.rect.collidepoint(mouse_pos):
                        self.load_level("assets/levels/level_01.txt")
                    elif self.ui.btn_lvl_2.rect.collidepoint(mouse_pos) and self.current_progress >= 1:
                        self.load_level("assets/levels/level_02.txt")
                    elif self.ui.btn_lvl_3.rect.collidepoint(mouse_pos) and self.current_progress >= 2:
                        self.load_level("assets/levels/level_03.txt")
                    elif self.ui.btn_back.rect.collidepoint(mouse_pos):
                        self.state = "MENU"

                elif self.state == "GAME_OVER":
                    if self.ui.btn_restart.rect.collidepoint(mouse_pos):
                        self.load_level(self.current_level_path)
                    elif self.ui.btn_menu.rect.collidepoint(mouse_pos):
                        self.state = "MENU"

                elif self.state == "VICTORY":
                    # Кнопка "СЛЕДУЮЩИЙ УРОВЕНЬ"
                    if self.ui.btn_next.rect.collidepoint(mouse_pos):
                        next_lvl_path = f"assets/levels/level_0{self.current_level_num + 1}.txt"
                        self.load_level(next_lvl_path)
                    elif self.ui.btn_restart.rect.collidepoint(mouse_pos):
                        self.load_level(self.current_level_path)
                    elif self.ui.btn_menu.rect.collidepoint(mouse_pos):
                        self.state = "MENU"

    def update(self):
        if self.state != "PLAYING" or self.player is None:
            return

        # Обновляем таймер
        self.elapsed_time = (pygame.time.get_ticks() - self.start_ticks) / 1000.0

        keys = pygame.key.get_pressed()

        for platform in self.platforms: platform.update(self.phase_manager.current_phase)
        for hazard in self.hazards:
            if hasattr(hazard, 'update'): hazard.update(self.phase_manager.current_phase)
        for decor in self.decorations:
            if hasattr(decor, 'update'): decor.update(self.phase_manager.current_phase)

        self.player.update(keys, self.platforms)
        self.camera.update(self.player)

        collected = pygame.sprite.spritecollide(self.player, self.keys_group, True)
        for key in collected:
            self.collected_keys += 1
            key.kill()
            if self.collected_keys >= self.total_keys and self.portal:
                self.portal.open_portal()

        for hazard in self.hazards:
            if hazard.is_active and self.player.rect.colliderect(hazard.rect):
                self.state = "GAME_OVER"
                pygame.mixer.music.stop()

        if self.portal and self.portal.is_open and self.player.rect.colliderect(self.portal.rect):
            self.state = "VICTORY"
            pygame.mixer.music.stop()
            
            # РАСЧЕТ И СОХРАНЕНИЕ ЗВЕЗД
            self.earned_stars = self.calculate_stars(self.elapsed_time)
            self.db.update_progress(self.current_user_id, self.current_level_num, self.earned_stars)
            
            if self.current_level_num > self.current_progress:
                self.current_progress = self.current_level_num

        if self.player.rect.top > self.camera.screen_h + 1000:
            self.state = "GAME_OVER"
            pygame.mixer.music.stop()

    def draw(self):
        if self.state in ["PLAYING", "GAME_OVER", "VICTORY"]:
            if self.phase_manager.current_phase == "LIGHT":
                base, pattern, top = self.bg_base_light, self.bg_pattern_light, self.bg_top_light
            else:
                base, pattern, top = self.bg_base_shadow, self.bg_pattern_shadow, self.bg_top_shadow
            
            if base: self.screen.blit(base, (0, 0))
            else: self.screen.fill(self.phase_manager.get_bg_color())
            if pattern: self.screen.blit(pattern, (0, 0))
            if top: self.screen.blit(top, (0, 0))

            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, self.camera.apply(sprite))

            if self.state == "PLAYING":
                self.ui.draw_hud(self.screen, self.phase_manager.current_phase, self.collected_keys, self.total_keys, self.elapsed_time)

        if self.state == "AUTH":
            self.ui.draw_auth(self.screen)
        elif self.state == "MENU":
            self.ui.draw_main_menu(self.screen, self.current_username)
        elif self.state == "LEVEL_SELECT":
            self.ui.draw_level_select(self.screen, self.current_progress, self.user_stars)
        elif self.state == "GAME_OVER":
            self.ui.draw_game_over(self.screen)
        elif self.state == "VICTORY":
            self.ui.draw_victory(self.screen, self.elapsed_time, self.earned_stars)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()