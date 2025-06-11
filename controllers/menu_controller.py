import pygame
import logging

from constants import MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT

logger = logging.getLogger(__name__)

class MenuController:
    """Handles menu input and navigation."""
    def __init__(self, menu_view):
        self.view = menu_view
        logger.info("MenuController initialized")

    def handle_event(self, event):
        """Handle menu input events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for button in self.view.buttons:
                rect = pygame.Rect(button["pos"][0] - MENU_BUTTON_WIDTH // 2, button["pos"][1] - MENU_BUTTON_HEIGHT // 2,
                                   MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
                if rect.collidepoint(x, y):
                    logger.info(f"Menu button clicked: {button['action']}")
                    return button["action"]
        return None

    def update(self):
        """Update and render the menu."""
        self.view.render()