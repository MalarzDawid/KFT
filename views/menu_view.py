import pygame
import logging
from constants import MENU_BG_COLOR, MENU_BUTTON_HEIGHT, TEXT_COLOR, MENU_BUTTON_SPACING, MENU_BUTTON_WIDTH, \
    SAVE_BUTTON_BORDER_COLOR, MENU_BUTTONS_OFFSET
from utils import draw_button

logger = logging.getLogger(__name__)

class MenuView:
    """Handles rendering of the main menu."""
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Roboto", 44, bold=True)
        self.button_font = pygame.font.SysFont("Roboto", 28, bold=True)
        self.screen_width, self.screen_height = self.screen.get_size()
        self.buttons = [
            {"label": "CONFIGURE", "action": "configure"},
            {"label": "PLAY", "action": "play"},
        ]
        total_height = len(self.buttons) * MENU_BUTTON_HEIGHT + (len(self.buttons) - 1) * MENU_BUTTON_SPACING
        start_y = (self.screen_height - total_height) / 2
        for i, button in enumerate(self.buttons):
            button["pos"] = (self.screen_width // 2, start_y + i * (MENU_BUTTON_HEIGHT + MENU_BUTTON_SPACING) + MENU_BUTTONS_OFFSET)
        self.hovered_button = None
        logger.info("MenuView initialized")

    def render(self):
        """Render the menu with gradient background and hover effects."""
        # Gradient background
        for y in range(self.screen_height):
            ratio = y / self.screen_height
            color = (
                int(MENU_BG_COLOR[0] * (1 - ratio) + 50 * ratio),
                int(MENU_BG_COLOR[1] * (1 - ratio) + 50 * ratio),
                int(MENU_BG_COLOR[2] * (1 - ratio) + 100 * ratio)
            )
            pygame.draw.line(self.screen, color, (0, y), (self.screen_width, y))

        # Title
        title = self.font.render("GAME MENU", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        self.screen.blit(title, title_rect)

        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_button = None
        for button in self.buttons:
            rect = pygame.Rect(
                button["pos"][0] - MENU_BUTTON_WIDTH // 2,
                button["pos"][1] - MENU_BUTTON_HEIGHT // 2,
                MENU_BUTTON_WIDTH,
                MENU_BUTTON_HEIGHT
            )
            # Check hover
            is_hovered = rect.collidepoint(mouse_pos)
            if is_hovered:
                self.hovered_button = button["action"]

            # Button colors
            button_color = (100, 100, 200) if is_hovered else (80, 80, 160)
            shadow_color = (50, 50, 100)

            # Draw shadow
            shadow_rect = rect.move(4, 4)
            draw_button(self.screen, shadow_rect, shadow_color, "", self.button_font, SAVE_BUTTON_BORDER_COLOR)
            # Draw button
            draw_button(self.screen, rect, button_color, button["label"], self.button_font, SAVE_BUTTON_BORDER_COLOR)

    def get_hovered_action(self):
        """Return the action of the currently hovered button."""
        return self.hovered_button