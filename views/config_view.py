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
    CONFIG_MUSIC_Y, CONFIG_BG_IMAGE_Y, BORDER_RADIUS, BORDER_THICKNESS, CONFIG_FONT_SIZE,
    LABEL_FONT_SIZE, PADDING, INPUT_BOX_OFFSET, WIDTH, HEIGHT, CONFIG_PROMPT_X
)
from utils import render_text, draw_button, draw_gradient_background

logger = logging.getLogger(__name__)

class ModernInputBox:
    """Input box for configuration UI with shadow effect.

    This class manages an input field with shadow and event handling.
    """
    def __init__(self, x, y, w, h, text='', numeric=False, label='', placeholder=''):
        """Initialize the ModernInputBox.

            Args:
                x (int): X position.
                y (int): Y position.
                w (int): Width.
                h (int): Height.
                text (str): Initial text.
                numeric (bool): Whether input is numeric.
                label (str): Label text.
                placeholder (str): Placeholder text.
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = INPUT_COLOR_INACTIVE
        self.color_active = INPUT_COLOR_ACTIVE
        self.color = self.color_inactive
        self.text = str(text) if text else ''
        self.label = label
        self.placeholder = placeholder
        self.font = pygame.font.SysFont("Roboto", CONFIG_FONT_SIZE)
        self.label_font = pygame.font.SysFont("Roboto", LABEL_FONT_SIZE)
        self.txt_surface = self.font.render(self.text or placeholder, True,
                                            TEXT_COLOR if self.text else (150, 150, 170))
        self.active = False
        self.numeric = numeric
        self.padding = PADDING
        self.bg_color = INPUT_BG_COLOR

    def handle_event(self, event):
        """Handle input events.

        Args:
            event: Pygame event object.

        Returns:
            bool: True if input is active.
        """
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
        """Draw the input box with shadow.

        Args:
            screen: Pygame surface to draw on.
        """
        if self.label:
            render_text(self.label_font, self.label, LABEL_COLOR, self.rect.x, self.rect.y - INPUT_BOX_OFFSET, screen)
        # Draw shadow
        shadow_rect = self.rect.move(4, 4)
        pygame.draw.rect(screen, (30, 30, 40), shadow_rect, border_radius=BORDER_RADIUS)
        # Draw input box
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=BORDER_RADIUS)
        pygame.draw.rect(screen, self.color, self.rect, BORDER_THICKNESS, border_radius=BORDER_RADIUS)
        screen.blit(self.txt_surface, (self.rect.x + self.padding, self.rect.y + (self.rect.height - self.txt_surface.get_height()) // 2))

    def get_value(self):
        """Get the input value.

        Returns:
            str or int: Input value, converted to int if numeric and valid.
        """
        return int(self.text) if self.numeric and self.text.isdigit() else self.text

class ModernColorPicker:
    """Color picker for configuration UI with shadow effect.

    This class manages color selection with visual feedback.
    """
    def __init__(self, x, y, colors, label=''):
        """Initialize the ModernColorPicker.

            Args:
                x (int): X position.
                y (int): Y position.
                colors (list): List of color tuples.
                label (str): Label text.
        """
        self.colors = colors
        self.rects = [(pygame.Rect(x + i * 45, y, 35, 35), color) for i, color in enumerate(colors)]
        self.selected_color = colors[0]
        self.label = label
        self.label_font = pygame.font.SysFont("Roboto", LABEL_FONT_SIZE)

    def handle_event(self, event):
        """Handle color selection events.

        Args:
            event: Pygame event object.

        Returns:
            bool: True if a color was selected.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            for rect, color in self.rects:
                if rect.collidepoint(event.pos):
                    self.selected_color = color
                    return True
        return False

    def draw(self, screen):
        """Draw the color picker with shadow.

        Args:
            screen: Pygame surface to draw on.
        """
        if self.label:
            render_text(self.label_font, self.label, LABEL_COLOR, self.rects[0][0].x, self.rects[0][0].y - 25, screen)
        for rect, color in self.rects:
            # Draw shadow
            shadow_rect = rect.move(2, 2)
            pygame.draw.rect(screen, (30, 30, 40), shadow_rect, border_radius=5)
            # Draw color box
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
        self.screen_width, self.screen_height = WIDTH, HEIGHT
        self.fonts = self._load_fonts()
        self._init_controls()
        logger.info("ConfigView initialized")

    def _load_fonts(self):
        return {
            'title': pygame.font.SysFont("Roboto", 26),
            'small': pygame.font.SysFont("Roboto", 20),
            'tiny': pygame.font.SysFont("Roboto", 16),
            'input': pygame.font.SysFont("Roboto", CONFIG_FONT_SIZE),
            'label': pygame.font.SysFont("Roboto", LABEL_FONT_SIZE),
        }

    def _init_controls(self):
        cfg = self.config
        # Input boxes
        self.prompt_box = ModernInputBox(
            CONFIG_PROMPT_X, CONFIG_PROMPT_Y,
            CONFIG_INPUT_WIDTH, CONFIG_INPUT_HEIGHT,
            cfg.get("prompt", "Star Wars"), label="Uniwersum:", placeholder="Podaj nazwę uniwersum..."
        )
        self.music_box = ModernInputBox(
            800, CONFIG_MUSIC_Y, 360, CONFIG_INPUT_HEIGHT,
            cfg.get("music", "music.mp3"), label="Plik muzyczny:", placeholder="Podaj nazwę pliku..."
        )
        self.bg_box = ModernInputBox(
            800, CONFIG_BG_IMAGE_Y, 360, CONFIG_INPUT_HEIGHT,
            cfg.get("bg_img", "bg.png"), label="Plik tła:", placeholder="Podaj nazwę pliku..."
        )
        # Number of answers per question
        self.answer_inputs = []
        for i, _ in enumerate(QUESTIONS):
            y = 150 + i * 45
            num = (cfg['questions'][i]['num_answers'] if i < len(cfg.get('questions', [])) else 5)
            box = ModernInputBox(
                655, y, CONFIG_NUM_INPUT_WIDTH, CONFIG_NUM_INPUT_HEIGHT,
                str(num), numeric=True
            )
            self.answer_inputs.append(box)
        # Color picker
        colors = [(30, 30, 60), (60, 30, 60), (30, 60, 30), (60, 30, 30), (30, 30, 30), (60, 60, 30)]
        self.color_picker = ModernColorPicker(800, CONFIG_COLOR_PICKER_Y, colors, label="Kolor tła:")
        # Buttons
        self.save_button = self._make_button(CONFIG_BUTTON_X, CONFIG_BUTTON_Y, 180, 50,
                                             "Zapisz i Generuj", CONFIG_BUTTON_COLOR, CONFIG_BUTTON_HOVER_COLOR)
        self.back_button = self._make_button(CONFIG_BUTTON_X + 30, CONFIG_BACK_BUTTON_Y, 150, 50,
                                             "Powrót", BACK_BUTTON_COLOR, BACK_BUTTON_HOVER_COLOR)

    def _make_button(self, x, y, w, h, text, color, hover_color):
        return {'rect': pygame.Rect(x, y, w, h), 'text': text,
                'color': color, 'hover': hover_color}

    def render(self):
        self._draw_background()
        self._draw_main_panel()
        self._draw_questions_panel()
        self._draw_inputs()
        self._draw_buttons()
        self._draw_prompt_preview()

    def _draw_background(self):
        draw_gradient_background(self.screen, self.screen_height, CONFIG_BG_COLOR, (50, 50, 100))

    def _draw_main_panel(self):
        panel = pygame.Rect(CONFIG_PANEL_X, CONFIG_PANEL_Y,
                            CONFIG_PANEL_WIDTH, CONFIG_PANEL_HEIGHT)
        pygame.draw.rect(self.screen, CONFIG_PANEL_COLOR, panel, border_radius=BORDER_RADIUS)
        pygame.draw.rect(self.screen, (60, 60, 80), panel, BORDER_THICKNESS, border_radius=BORDER_RADIUS)
        render_text(self.fonts['title'], "KONFIGURACJA", TEXT_COLOR,
                    self.screen_width / 2, 10, self.screen, center=True)

    def _draw_questions_panel(self):
        rect = pygame.Rect(CONFIG_QUESTIONS_RECT_X,
                           CONFIG_QUESTIONS_RECT_Y + 10,
                           CONFIG_QUESTIONS_RECT_WIDTH,
                           CONFIG_QUESTIONS_RECT_HEIGHT)
        pygame.draw.rect(self.screen, (45, 45, 65), rect, border_radius=BORDER_RADIUS)
        render_text(self.fonts['small'], "Pytania i liczba odpowiedzi", LABEL_COLOR,
                    rect.centerx, CONFIG_QUESTIONS_RECT_Y + PADDING + 4,
                    self.screen, center=True)
        for i, text in enumerate(QUESTIONS):
            y = 160 + i * 45
            circle_pos = (95, y + 12)
            pygame.draw.circle(self.screen, CONFIG_ACCENT_COLOR, circle_pos, 15)
            render_text(self.fonts['small'], f"{i+1}", TEXT_COLOR,
                        circle_pos[0], circle_pos[1] - 6, self.screen, center=True)
            render_text(self.fonts['small'], text, TEXT_COLOR, 120, y + 6, self.screen)
            self.answer_inputs[i].rect.y = y
            self.answer_inputs[i].draw(self.screen)

    def _draw_inputs(self):
        self.prompt_box.draw(self.screen)
        self.color_picker.draw(self.screen)
        self.music_box.draw(self.screen)
        self.bg_box.draw(self.screen)

    def _draw_buttons(self):
        mouse = pygame.mouse.get_pos()
        for btn in (self.save_button, self.back_button):
            shadow = btn['rect'].move(4, 4)
            pygame.draw.rect(self.screen, (40, 40, 50), shadow, border_radius=BORDER_RADIUS)
            color = btn['hover'] if btn['rect'].collidepoint(mouse) else btn['color']
            draw_button(self.screen, btn['rect'], color, btn['text'], self.fonts['title'])

    def _draw_prompt_preview(self):
        prompt = (f"Jesteś twórcą wideo w stylu 'Spin the wheel'. "
                  f"Odpowiadasz na poniższe pytania, korzystając wyłącznie z uniwersum {self.prompt_box.text}. "
                  "Odpowiadaj tylko w formacie JSON, bez żadnych wyjaśnień...")
        panel = pygame.Rect(40, 660, 720, 90)
        pygame.draw.rect(self.screen, (45, 45, 65), panel, border_radius=BORDER_RADIUS)
        render_text(self.fonts['small'], "Podgląd zapytania AI", LABEL_COLOR,
                    panel.x + 20, panel.y + 10, self.screen)
        self._render_multiline(prompt, panel.x + 20, panel.y + 35, self.fonts['tiny'], LABEL_COLOR, max_width=650)

    def _render_multiline(self, text, x, y, font, color, max_width):
        words = text.split()
        line = ''
        for word in words:
            test = (line + ' ' + word).strip()
            if font.size(test)[0] < max_width:
                line = test
            else:
                render_text(font, line, color, x, y, self.screen)
                y += font.get_linesize()
                line = word
        if line:
            render_text(font, line, color, x, y, self.screen)