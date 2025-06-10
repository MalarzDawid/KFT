import pygame
import logging
from constants import (
    CONFIG_BG_COLOR, CONFIG_PANEL_COLOR, CONFIG_ACCENT_COLOR, CONFIG_BUTTON_COLOR,
    CONFIG_BUTTON_HOVER_COLOR, BACK_BUTTON_COLOR, BACK_BUTTON_HOVER_COLOR,
    INPUT_COLOR_INACTIVE, INPUT_COLOR_ACTIVE, INPUT_BG_COLOR, LABEL_COLOR, TEXT_COLOR,
    QUESTIONS, CONFIG_INPUT_WIDTH, CONFIG_INPUT_HEIGHT, CONFIG_NUM_INPUT_WIDTH,
    CONFIG_NUM_INPUT_HEIGHT, CONFIG_BUTTON_X, CONFIG_BUTTON_Y, CONFIG_BACK_BUTTON_Y,
    CONFIG_PANEL_X, CONFIG_PANEL_Y, CONFIG_PANEL_WIDTH, CONFIG_PANEL_HEIGHT,
    CONFIG_QUESTIONS_RECT_X, CONFIG_QUESTIONS_RECT_Y, CONFIG_QUESTIONS_RECT_WIDTH,
    CONFIG_QUESTIONS_RECT_HEIGHT, CONFIG_PROMPT_Y, CONFIG_COLOR_PICKER_Y,
    CONFIG_MUSIC_Y, CONFIG_BG_IMAGE_Y, BORDER_RADIUS, BORDER_THICKNESS
)
from utils import render_text, draw_button

logger = logging.getLogger(__name__)

class ModernInputBox:
    """Input box for configuration UI."""
    def __init__(self, x, y, w, h, text='', numeric=False, label='', placeholder=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = INPUT_COLOR_INACTIVE
        self.color_active = INPUT_COLOR_ACTIVE
        self.color = self.color_inactive
        self.text = str(text) if text else ''
        self.label = label
        self.placeholder = placeholder
        self.font = pygame.font.SysFont("Arial", 20)
        self.label_font = pygame.font.SysFont("Arial", 18)
        self.txt_surface = self.font.render(self.text or placeholder, True,
                                            TEXT_COLOR if self.text else (150, 150, 170))
        self.active = False
        self.numeric = numeric
        self.padding = 10
        self.bg_color = INPUT_BG_COLOR

    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
                self.color = self.color_inactive
            elif self.numeric and event.unicode.isdigit():
                self.text += event.unicode
            elif not self.numeric:
                self.text += event.unicode
            self.txt_surface = self.font.render(self.text or self.placeholder, True,
                                                TEXT_COLOR if self.text else (150, 150, 170))
        return self.active

    def draw(self, screen):
        """Draw the input box."""
        if self.label:
            render_text(self.label_font, self.label, LABEL_COLOR, self.rect.x, self.rect.y - 25, screen)
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=4)
        border_thickness = 2 if self.active else 1
        pygame.draw.rect(screen, self.color, self.rect, border_thickness, border_radius=4)
        screen.blit(self.txt_surface, (self.rect.x + self.padding, self.rect.y + (self.rect.height - self.txt_surface.get_height()) // 2))

    def get_value(self):
        """Get the input value."""
        return int(self.text) if self.numeric and self.text.isdigit() else self.text

class ModernColorPicker:
    """Color picker for configuration UI."""
    def __init__(self, x, y, colors, label=''):
        self.colors = colors
        self.rects = [(pygame.Rect(x + i * 45, y, 35, 35), color) for i, color in enumerate(colors)]
        self.selected_color = colors[0]
        self.label = label
        self.label_font = pygame.font.SysFont("Arial", 18)

    def handle_event(self, event):
        """Handle color selection events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for rect, color in self.rects:
                if rect.collidepoint(event.pos):
                    self.selected_color = color
                    return True
        return False

    def draw(self, screen):
        """Draw the color picker."""
        if self.label:
            render_text(self.label_font, self.label, LABEL_COLOR, self.rects[0][0].x, self.rects[0][0].y - 25, screen)
        for rect, color in self.rects:
            pygame.draw.rect(screen, color, rect, border_radius=5)
            if color == self.selected_color:
                pygame.draw.rect(screen, TEXT_COLOR, rect, 2, border_radius=5)
                check_x = rect.centerx - 7
                check_y = rect.centery - 3
                pygame.draw.line(screen, TEXT_COLOR, (check_x, check_y), (check_x + 5, check_y + 5), 2)
                pygame.draw.line(screen, TEXT_COLOR, (check_x + 5, check_y + 5), (check_x + 12, check_y - 7), 2)

class ConfigView:
    """Handles rendering of the configuration UI."""
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.font = pygame.font.SysFont("Arial", 26)
        self.small_font = pygame.font.SysFont("Arial", 20)
        self.tiny_font = pygame.font.SysFont("Arial", 16)
        self.prompt_box = ModernInputBox(250, CONFIG_PROMPT_Y, CONFIG_INPUT_WIDTH, CONFIG_INPUT_HEIGHT,
                                         config.get("prompt", "Star Wars"), label="Uniwersum:", placeholder="Podaj nazwę uniwersum...")
        self.color_picker = ModernColorPicker(800, CONFIG_COLOR_PICKER_Y, [
            (30, 30, 60), (60, 30, 60), (30, 60, 30), (60, 30, 30), (30, 30, 30), (60, 60, 30)
        ], label="Kolor tła:")
        self.music_box = ModernInputBox(800, CONFIG_MUSIC_Y, 360, CONFIG_INPUT_HEIGHT,
                                        config.get("music", "music.mp3"), label="Plik muzyczny:", placeholder="Podaj nazwę pliku...")
        self.bg_box = ModernInputBox(800, CONFIG_BG_IMAGE_Y, 360, CONFIG_INPUT_HEIGHT,
                                     config.get("bg_img", "bg.png"), label="Plik tła:", placeholder="Podaj nazwę pliku...")
        self.answer_inputs = [
            ModernInputBox(650, 150 + i * 45, CONFIG_NUM_INPUT_WIDTH, CONFIG_NUM_INPUT_HEIGHT,
                           str(config["questions"][i]["num_answers"] if i < len(config["questions"]) else 5), numeric=True)
            for i in range(len(QUESTIONS))
        ]
        self.save_button = (CONFIG_BUTTON_X, CONFIG_BUTTON_Y, 180, 50, "Zapisz i Generuj", CONFIG_BUTTON_COLOR, CONFIG_BUTTON_HOVER_COLOR)
        self.back_button = (CONFIG_BUTTON_X + 30, CONFIG_BACK_BUTTON_Y, 150, 50, "Powrót", BACK_BUTTON_COLOR, BACK_BUTTON_HOVER_COLOR)
        logger.info("ConfigView initialized")

    def render(self):
        """Render the configuration screen."""
        self.screen.fill(CONFIG_BG_COLOR)
        main_panel = pygame.Rect(CONFIG_PANEL_X, CONFIG_PANEL_Y, CONFIG_PANEL_WIDTH, CONFIG_PANEL_HEIGHT)
        pygame.draw.rect(self.screen, CONFIG_PANEL_COLOR, main_panel, border_radius=BORDER_RADIUS)
        pygame.draw.rect(self.screen, (60, 60, 80), main_panel, BORDER_THICKNESS, border_radius=BORDER_RADIUS)
        render_text(self.font, "Konfiguracja Gry", TEXT_COLOR, 400, 20, self.screen, center=True)
        questions_rect = pygame.Rect(CONFIG_QUESTIONS_RECT_X, CONFIG_QUESTIONS_RECT_Y, CONFIG_QUESTIONS_RECT_WIDTH, CONFIG_QUESTIONS_RECT_HEIGHT)
        pygame.draw.rect(self.screen, (45, 45, 65), questions_rect, border_radius=6)
        render_text(self.small_font, "Pytania i liczba odpowiedzi", (220, 220, 240), questions_rect.centerx, 135, self.screen, center=True)
        for i, text in enumerate(QUESTIONS):
            y = 150 + i * 45
            circle_pos = (90, y + 12)
            pygame.draw.circle(self.screen, CONFIG_ACCENT_COLOR, circle_pos, 15)
            render_text(self.small_font, f"{i+1}", TEXT_COLOR, circle_pos[0], circle_pos[1], self.screen, center=True)
            render_text(self.small_font, f"{i+1}. {text}", TEXT_COLOR, 120, y, self.screen)
            self.answer_inputs[i].rect.y = y
            self.answer_inputs[i].draw(self.screen)
        self.prompt_box.draw(self.screen)
        self.color_picker.draw(self.screen)
        self.music_box.draw(self.screen)
        self.bg_box.draw(self.screen)
        save_rect = pygame.Rect(*self.save_button[:4])
        back_rect = pygame.Rect(*self.back_button[:4])
        draw_button(self.screen, save_rect, self.save_button[5], self.save_button[4], self.font)
        draw_button(self.screen, back_rect, self.back_button[5], self.back_button[4], self.font)
        ai_prompt = f'Jesteś twórcą wideo w stylu "Spin the wheel". Odpowiadasz na poniższe pytania, korzystając wyłącznie z uniwersum {self.prompt_box.text}. Odpowiadaj tylko w formacie JSON, bez żadnych wyjaśnień, opisów czy dodatkowych komentarzy.'
        prompt_panel = pygame.Rect(40, 660, 720, 90)
        pygame.draw.rect(self.screen, (45, 45, 65), prompt_panel, border_radius=6)
        render_text(self.small_font, "Podgląd zapytania AI", (220, 220, 240), prompt_panel.x + 10, prompt_panel.y + 5, self.screen)
        words = ai_prompt.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = (current_line + " " + word).strip()
            if self.tiny_font.size(test_line)[0] < 700:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        for i, line in enumerate(lines):
            render_text(self.tiny_font, line, (200, 200, 220), prompt_panel.x + 10, prompt_panel.y + 30 + i * 20, self.screen)