import pygame
import logging

from constants import MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT
from utils import handle_button_click

logger = logging.getLogger(__name__)

class MenuController:
    """Handles menu input and navigation.

    This class manages user interactions with the menu.
    """

    def __init__(self, menu_view):
        """Initialize the MenuController.

        Args:
            menu_view: MenuView instance.
        """
        self.view = menu_view
        logger.info("MenuController initialized")

    def handle_event(self, event):
        """Handle menu input events.

        Args:
            event: Pygame event object.

        Returns:
            str or None: Action name or None if no action.
        """
        buttons = [{"pos": b["pos"], "label": b["label"], "action": b["action"]} for b in self.view.buttons]
        if handle_button_click(event, buttons):
            mouse_pos = event.pos
            for button in self.view.buttons:
                rect = pygame.Rect(
                    button["pos"][0] - MENU_BUTTON_WIDTH // 2,
                    button["pos"][1] - MENU_BUTTON_HEIGHT // 2,
                    MENU_BUTTON_WIDTH,
                    MENU_BUTTON_HEIGHT
                )
                if rect.collidepoint(mouse_pos):
                    logger.info(f"Menu button clicked: {button['action']}")
                    return button["action"]
        return None

    def update(self, dt):
        """Update and render the menu.

        Args:
            dt (float): Delta time in seconds (not used currently).
        """
        self.view.render()