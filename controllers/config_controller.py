import pygame
import logging
from utils import handle_button_click

logger = logging.getLogger(__name__)

class InputHandler:
    """Handles input events for configuration UI.

    This class manages user interactions with the configuration interface.
    """

    def __init__(self, view):
        """Initialize the InputHandler.

        Args:
            view: ConfigView instance.
        """
        self.view = view
        self.done = False
        self.go_back = False

    def handle_event(self, event):
        """Handle configuration input events.

        Args:
            event: Pygame event object.
        """
        buttons = [self.view.save_button, self.view.back_button]
        if handle_button_click(event, buttons):
            mouse_pos = pygame.mouse.get_pos()
            save_rect = pygame.Rect(*self.view.save_button[:4])
            back_rect = pygame.Rect(*self.view.back_button[:4])
            if save_rect.collidepoint(mouse_pos):
                self.done = True
                logger.info("Save button clicked")
            elif back_rect.collidepoint(mouse_pos):
                self.go_back = True
                logger.info("Back button clicked")
        self.view.prompt_box.handle_event(event)
        self.view.color_picker.handle_event(event)
        self.view.music_box.handle_event(event)
        self.view.bg_box.handle_event(event)
        for input_box in self.view.answer_inputs:
            input_box.handle_event(event)

    @property
    def is_done(self):
        """Check if configuration is done.

        Returns:
            bool: True if done.
        """
        return self.done

    @property
    def should_go_back(self):
        """Check if user wants to go back.

        Returns:
            bool: True if go back is requested.
        """
        return self.go_back

class ConfigSaver:
    """Handles saving configuration and generating AI answers.

    This class manages persistence and AI interaction for configuration.
    """

    def __init__(self, config_manager):
        """Initialize the ConfigSaver.

        Args:
            config_manager: ConfigManager instance.
        """
        self.config_manager = config_manager

    def save(self, prompt, music, bg_img, bg_color, answer_counts):
        """Save the configuration.

        Args:
            prompt (str): Universe prompt.
            music (str): Music file path.
            bg_img (str): Background image path.
            bg_color (tuple): Background color.
            answer_counts (list): Number of answers per question.
        """
        self.config_manager.generate_ai_answers(prompt)
        self.config_manager.save_config(prompt, music, bg_img, bg_color, answer_counts)
        logger.info("Configuration saved")

class ConfigController:
    """Coordinates configuration input and updates.

    This class integrates input handling and saving logic.
    """

    def __init__(self, config_view, config_manager, state_manager):
        """Initialize the ConfigController.

        Args:
            config_view: ConfigView instance.
            config_manager: ConfigManager instance.
        """
        self.view = config_view
        self.config_manager = config_manager
        self.state_manager = state_manager
        self.input_handler = InputHandler(config_view)
        self.config_saver = ConfigSaver(config_manager)
        logger.info("ConfigController initialized")

    def handle_event(self, event):
        """Handle configuration input events.

        Args:
            event: Pygame event object.
        """
        self.input_handler.handle_event(event)
        if self.input_handler.is_done:
            self.save()
        self.go_back = self.input_handler.should_go_back

    def save(self):
        """Save the configuration."""
        answer_counts = [input_box.get_value() for input_box in self.view.answer_inputs]
        self.config_saver.save(
            self.view.prompt_box.get_value(),
            self.view.music_box.get_value(),
            self.view.bg_box.get_value(),
            self.view.color_picker.selected_color,
            answer_counts
        )

    def update(self, dt):
        """Update and render the configuration UI."""
        if self.input_handler.should_go_back:
            self.state_manager.set_state('menu')

        if self.input_handler.is_done:
            self.state_manager.set_state('menu')
        self.view.render()

    @property
    def is_done(self):
        """Check if configuration is done.

        Returns:
            bool: True if done.
        """
        return self.input_handler.is_done

    @property
    def should_go_back(self):
        """Check if user wants to go back.

        Returns:
            bool: True if go back is requested.
        """
        return self.go_back