# --- СТАРТ ФАЙЛА ui/hud.py ---
import pygame
import math

class TextInputBox:
    def __init__(self, x, y, width, height, placeholder="", is_password=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = (50, 60, 80)
        self.color_active = (100, 150, 255)
        self.color = self.color_inactive
        self.text = ""
        self.placeholder = placeholder
        self.font = pygame.font.SysFont("arial", 40, bold=True)
        self.active = False
        self.is_password = is_password

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < 15 and event.unicode.isprintable():
                self.text += event.unicode

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
        display_text = "*" * len(self.text) if self.is_password and self.text else self.text
        if self.text == "" and not self.active:
            txt_surf = self.font.render(self.placeholder, True, (150, 150, 150))
        else:
            txt_surf = self.font.render(display_text, True, (255, 255, 255))
        surface.blit(txt_surf, (self.rect.x + 10, self.rect.y + 15))


class Button:
    def __init__(self, x, y, width, height, text, font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont("arial", font_size, bold=True)
        self.color = (70, 80, 100)
        self.hover_color = (100, 150, 255)
        self.text_color = (255, 255, 255)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=12)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


class UIManager:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.title_font = pygame.font.SysFont("arial", 80, bold=True)
        self.hud_font = pygame.font.SysFont("arial", 36, bold=True)

        btn_w, btn_h = 420, 60
        center_x = self.screen_w // 2 - btn_w // 2
        start_y = self.screen_h // 2 - 100 

        # АВТОРИЗАЦИЯ
        self.input_login = TextInputBox(center_x, start_y, btn_w, btn_h, "Логин (Англ)")
        self.input_password = TextInputBox(center_x, start_y + 80, btn_w, btn_h, "Пароль", is_password=True)
        self.btn_auth_login = Button(center_x, start_y + 160, 200, btn_h, "Войти", 30)
        self.btn_auth_reg = Button(center_x + 220, start_y + 160, 200, btn_h, "Создать", 30)
        self.auth_message = ""

        # МЕНЮ
        self.btn_play = Button(center_x, start_y, btn_w, btn_h, "Играть")
        self.btn_levels = Button(center_x, start_y + 80, btn_w, btn_h, "Выбор уровня")
        self.btn_logout = Button(center_x, start_y + 160, btn_w, btn_h, "Сменить аккаунт")
        self.btn_quit = Button(center_x, start_y + 240, btn_w, btn_h, "Выход")

        # УРОВНИ
        self.btn_lvl_1 = Button(center_x, start_y - 40, btn_w, btn_h, "Уровень 1")
        self.btn_lvl_2 = Button(center_x, start_y + 40, btn_w, btn_h, "Уровень 2")
        self.btn_lvl_3 = Button(center_x, start_y + 120, btn_w, btn_h, "Уровень 3")
        self.btn_back = Button(center_x, start_y + 200, btn_w, btn_h, "Назад")

        # ЭКРАНЫ СМЕРТИ / ПОБЕДЫ
        self.btn_next = Button(self.screen_w // 2 - 320, start_y + 200, 200, btn_h, "Следующий", 30)
        self.btn_restart = Button(self.screen_w // 2 - 100, start_y + 200, 200, btn_h, "Рестарт", 30)
        self.btn_menu = Button(self.screen_w // 2 + 120, start_y + 200, 200, btn_h, "В меню", 30)

    # === ФУНКЦИЯ РИСОВАНИЯ ЗВЕЗДЫ ===
    def _draw_star(self, surface, x, y, size, filled=True):
        outer_radius = size
        inner_radius = size * 0.4
        points = []
        # Вычисляем 10 точек для 5-конечной звезды
        for i in range(10):
            angle = math.radians(i * 36 - 90) # Начинаем сверху
            r = outer_radius if i % 2 == 0 else inner_radius
            px = x + math.cos(angle) * r
            py = y + math.sin(angle) * r
            points.append((px, py))
            
        color = (255, 215, 0) if filled else (100, 100, 100) # Золотая или серая
        if filled:
            pygame.draw.polygon(surface, color, points)
        else:
            pygame.draw.polygon(surface, color, points, max(2, int(size*0.15))) # Только контур

    def draw_hud(self, surface, current_phase, keys_collected, keys_total, timer):
        time_text = self.hud_font.render(f"Время: {timer:.1f} сек", True, (255, 255, 255))
        surface.blit(time_text, (20, 20))

        phase_color = (255, 255, 0) if current_phase == "LIGHT" else (200, 0, 255)
        phase_text = self.hud_font.render(f"Фаза: {current_phase}", True, phase_color)
        surface.blit(phase_text, (20, 60))

        key_color = (0, 255, 0) if keys_collected == keys_total else (255, 200, 0)
        key_text = self.hud_font.render(f"Ключи: {keys_collected} / {keys_total}", True, key_color)
        surface.blit(key_text, (20, 100))

    def _draw_title(self, surface, text, color=(255, 255, 255)):
        title_surf = self.title_font.render(text, True, color)
        title_rect = title_surf.get_rect(center=(self.screen_w // 2, self.screen_h // 2 - 200))
        surface.blit(title_surf, title_rect)

    def draw_auth(self, surface):
        surface.fill((20, 20, 30))
        self._draw_title(surface, "АВТОРИЗАЦИЯ")
        self.input_login.draw(surface)
        self.input_password.draw(surface)
        self.btn_auth_login.draw(surface)
        self.btn_auth_reg.draw(surface)

        if self.auth_message:
            msg_color = (100, 255, 100) if "Успеш" in self.auth_message else (255, 100, 100)
            msg_surf = self.hud_font.render(self.auth_message, True, msg_color)
            msg_rect = msg_surf.get_rect(center=(self.screen_w // 2, self.screen_h // 2 + 150))
            surface.blit(msg_surf, msg_rect)

    def draw_main_menu(self, surface, username):
        surface.fill((30, 30, 40))
        self._draw_title(surface, f"ПРИВЕТ, {username.upper()}!")
        self.btn_play.draw(surface)
        self.btn_levels.draw(surface)
        self.btn_logout.draw(surface)
        self.btn_quit.draw(surface)

    def draw_level_select(self, surface, progress, user_stars):
        surface.fill((30, 30, 40))
        self._draw_title(surface, "ВЫБОР УРОВНЯ")
        
        self.btn_lvl_1.text = "Уровень 1"
        self.btn_lvl_2.text = "Уровень 2" if progress >= 1 else "Уровень 2 (Заблокирован)"
        self.btn_lvl_3.text = "Уровень 3" if progress >= 2 else "Уровень 3 (Заблокирован)"
        
        self.btn_lvl_1.draw(surface)
        self.btn_lvl_2.draw(surface)
        self.btn_lvl_3.draw(surface)
        
        # Рисуем мини-звездочки прямо на кнопках уровней!
        btn_list = [self.btn_lvl_1, self.btn_lvl_2, self.btn_lvl_3]
        for i, btn in enumerate(btn_list):
            lvl_num = i + 1
            if progress >= (lvl_num - 1): # Если уровень разблокирован
                stars_earned = user_stars.get(lvl_num, 0)
                # Рисуем 3 маленькие звезды с правой стороны кнопки
                for s in range(3):
                    star_x = btn.rect.right - 90 + (s * 30)
                    star_y = btn.rect.centery
                    self._draw_star(surface, star_x, star_y, 10, filled=(s < stars_earned))
                    
        self.btn_back.draw(surface)

    def draw_game_over(self, surface):
        surface.fill((50, 0, 0))
        self._draw_title(surface, "ВЫ ПОГИБЛИ", (255, 100, 100))
        self.btn_restart.draw(surface)
        self.btn_menu.draw(surface)

    def draw_victory(self, surface, time_taken, stars):
        surface.fill((0, 50, 0))
        self._draw_title(surface, "УРОВЕНЬ ПРОЙДЕН!", (100, 255, 100))
        
        time_text = self.hud_font.render(f"Время: {time_taken:.1f} сек", True, (255, 255, 255))
        surface.blit(time_text, time_text.get_rect(center=(self.screen_w // 2, self.screen_h // 2 - 100)))
        
        # Рисуем 3 БОЛЬШИЕ ЗВЕЗДЫ по центру экрана
        star_y = self.screen_h // 2 - 30
        star_start_x = self.screen_w // 2 - 80
        for i in range(3):
            self._draw_star(surface, star_start_x + (i * 80), star_y, 30, filled=(i < stars))

        self.btn_next.draw(surface)
        self.btn_restart.draw(surface)
        self.btn_menu.draw(surface)