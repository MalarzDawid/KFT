import pygame
import logging

logger = logging.getLogger(__name__)

class ConfigController:
    """Handles configuration input and updates."""
    def __init__(self, config_view, config_manager):
        self.view = config_view
        self.config_manager = config_manager
        self.done = False
        self.go_back = False
        logger.info("ConfigController initialized")

    def handle_event(self, event):
        """Handle configuration input events."""
        mouse_pos = pygame.mouse.get_pos()
        save_rect = pygame.Rect(self.view.save_button[0], self.view.save_button[1], self.view.save_button[2], self.view.save_button[3])
        back_rect = pygame.Rect(self.view.back_button[0], self.view.back_button[1], self.view.back_button[2], self.view.back_button[3])
        if event.type == pygame.MOUSEBUTTONDOWN:
            if save_rect.collidepoint(mouse_pos):
                self.save()
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

    def save(self):
        """Save the configuration."""
        answer_counts = [input_box.get_value() for input_box in self.view.answer_inputs]
        self.config_manager.generate_ai_answers(self.view.prompt_box.get_value())
        self.config_manager.save_config(
            self.view.prompt_box.get_value(),
            self.view.music_box.get_value(),
            self.view.bg_box.get_value(),
            self.view.color_picker.selected_color,
            answer_counts
        )

    def update(self):
        """Update and render the configuration UI."""
        self.view.render()