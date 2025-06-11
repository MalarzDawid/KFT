import pygame
import logging
from constants import MENU_BG_COLOR, MENU_BUTTON_HEIGHT, TEXT_COLOR, MENU_BUTTON_SPACING, MENU_BUTTON_WIDTH, \
    SAVE_BUTTON_BORDER_COLOR, MENU_BUTTONS_OFFSET
from utils import draw_button, draw_gradient_background

logger = logging.getLogger(__name__)

class MenuView:
    """Handles rendering of the main menu.

    This class is responsible for rendering the menu interface.
    """

    def __init__(self, screen):
        """Initialize the MenuView.

        Args:
            screen: Pygame surface for rendering.
        """
        self.screen = screen
        self.font = pygame.font.SysFont("Roboto", 44, bold=True)
        self.button_font = pygame.font.SysFont("Roboto", 28, bold=True)
        self.screen_width, self.screen_height = self.screen.get_size()
        self.buttons = [
            {"label": "CONFIGURE", "action": "config", "w": MENU_BUTTON_WIDTH, "h": MENU_BUTTON_HEIGHT},
            {"label": "PLAY", "action": "game", "w": MENU_BUTTON_WIDTH, "h": MENU_BUTTON_HEIGHT},  # Zmiana z "play" na "game"
        ]
        total_height = len(self.buttons) * MENU_BUTTON_HEIGHT + (len(self.buttons) - 1) * MENU_BUTTON_SPACING
        start_y = (self.screen_height - total_height) / 2
        for i, button in enumerate(self.buttons):
            button["pos"] = (self.screen_width // 2, start_y + i * (MENU_BUTTON_HEIGHT + MENU_BUTTON_SPACING) + MENU_BUTTONS_OFFSET)
        self.hovered_button = None
        logger.info("MenuView initialized")

    def render(self):
        """Render the menu with gradient background and hover effects."""
        draw_gradient_background(self.screen, self.screen_height, MENU_BG_COLOR, (50, 50, 100))

        # Title
        title = self.font.render("GAME MENU", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        self.screen.blit(title, title_rect)

        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_button = None
        for button in self.buttons:
            rect = pygame.Rect(
                button["pos"][0] - button["w"] // 2,
                button["pos"][1] - button["h"] // 2,
                button["w"],
                button["h"]
            )
            # Check hover
            is_hovered = rect.collidepoint(mouse_pos)
            if is_hovered:
                self.hovered_button = button["action"]

            # Draw button
            draw_button(self.screen, rect, (100, 100, 200), button["label"],
                        self.button_font, border_color=SAVE_BUTTON_BORDER_COLOR)