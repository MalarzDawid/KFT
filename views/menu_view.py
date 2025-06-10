import pygame
import logging
from constants import MENU_BG_COLOR, MENU_BUTTON_COLOR, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, TEXT_COLOR
from utils import draw_button

logger = logging.getLogger(__name__)

class MenuView:
    """Handles rendering of the main menu."""
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 40)
        self.buttons = [
            {"label": "Configure Game", "pos": (600, 250), "action": "configure"},
            {"label": "Play Game", "pos": (600, 350), "action": "play"},
        ]
        logger.info("MenuView initialized")

    def render(self):
        """Render the menu."""
        self.screen.fill(MENU_BG_COLOR)
        for button in self.buttons:
            rect = pygame.Rect(button["pos"][0] - MENU_BUTTON_WIDTH // 2, button["pos"][1] - MENU_BUTTON_HEIGHT // 2,
                               MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
            draw_button(self.screen, rect, MENU_BUTTON_COLOR, button["label"], self.font)