import sys

import pygame
import random
import logging

from models.logger import GameState
from utils import load_json_file
from constants import (
    WIDTH, HEIGHT, SPACE_KEY, MOUSE_LEFT_BUTTON, GIF_SCALE_FACTOR, GIF_DISPLAY_TIME,
    FRAME_DELAY_DEFAULT, WAIT_TIME, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_Y_OFFSET,
    SAVE_BUTTON_WIDTH, RESULT_IMAGE_PATH, TEXT_RESP_PATH, SECOND_IN_MS, WHEEL_RADIUS, PADDING
)
from models.spin_wheel import SpinWheelModel
from .media_loader import MediaLoader

logger = logging.getLogger(__name__)

class GameController:
    """Handles game input and coordinates model and view.

    This class manages game logic and state transitions.
    """

    def __init__(self, game_state_model, game_view, config_manager):
        """Initialize the GameController.

        Args:
            game_state_model: GameStateTracker instance.
            game_view: GameView instance.
            config_manager: ConfigManager instance.
        """
        self.game_state = game_state_model
        self.view = game_view
        self.config = config_manager
        self.wheel = None
        self.media_loader = MediaLoader()
        self.responses = load_json_file(TEXT_RESP_PATH)
        self.is_result_saved = False
        self.generate_new_wheel()
        logger.info("GameController initialized")

    def generate_new_wheel(self):
        """Generate a new wheel."""
        data = self.config.config["questions"][self.game_state.current_draw]
        choices = data["answers"][:data["num_answers"]]
        self.wheel = SpinWheelModel(choices)
        logger.info(f"New wheel generated for draw {self.game_state.current_draw + 1}")

    def get_random_response(self, result):
        """Get a random response.

        Args:
            result (str): Result to match.

        Returns:
            str: Random response.
        """
        question_idx = self.game_state.current_draw + 1
        return random.choice(self.responses[f"{question_idx}"][f"{question_idx}/10"])

    def update(self, dt):
        """Update the game state.

        Args:
            dt (float): Delta time in seconds.
        """
        if self.game_state.state == GameState.SPINNING:
            self.wheel.update(dt)
            if not self.wheel.spinning:
                result, idx = self.wheel.get_selected_segment()
                response = self.get_random_response(result)
                self.game_state.add_result(result, response)
                if self.media_loader.load_gif(idx):
                    self.game_state.set_state(GameState.SHOWING_GIF)
                    self.game_state.reset_wait_timer(GIF_DISPLAY_TIME)
                else:
                    self.game_state.set_state(GameState.WAITING)
                    self.game_state.reset_wait_timer(WAIT_TIME)
        elif self.game_state.state == GameState.SHOWING_GIF:
            self.media_loader.update(dt)
            if self.game_state.update_timer(dt):
                self.game_state.increment_draw()
                if self.game_state.state != GameState.RESULTS:
                    self.generate_new_wheel()
                    self.wheel.spin()
                    self.game_state.set_state(GameState.SPINNING)
        elif self.game_state.state == GameState.WAITING:
            if self.game_state.update_timer(dt):
                self.game_state.increment_draw()
                if self.game_state.state != GameState.RESULTS:
                    self.generate_new_wheel()
                    self.wheel.spin()
                    self.game_state.set_state(GameState.SPINNING)
        if self.game_state.state == GameState.SPINNING:
            self.view.render_spinning(self.wheel, self.game_state.current_draw)
        elif self.game_state.state == GameState.WAITING:
            self.view.render_waiting(self.wheel, self.game_state.current_draw, self.game_state.results[-1], not self.wheel.spinning)
        elif self.game_state.state == GameState.SHOWING_GIF:
            self.view.render_gif(self.media_loader, self.game_state.results[-1], self.game_state.result_responses[-1])
        elif self.game_state.state == GameState.RESULTS:
            self.view.render_results(self.game_state.results, self.game_state.result_responses, self.is_result_saved)

    def handle_event(self, event):
        """Handle input events.

        Args:
            event: Pygame event object.
        """
        if self.game_state.state == GameState.SPINNING and not self.wheel.spinning:
            if (event.type == pygame.KEYDOWN and event.key == SPACE_KEY) or \
               (event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_LEFT_BUTTON):
                self.wheel.spin()
                logger.info("Wheel spun by user")
        elif self.game_state.state == GameState.RESULTS:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_LEFT_BUTTON:
                mouse_pos = pygame.mouse.get_pos()
                exit_button = pygame.Rect(WIDTH // 2 - WHEEL_RADIUS, HEIGHT + BUTTON_Y_OFFSET, BUTTON_WIDTH, BUTTON_HEIGHT)
                save_button = pygame.Rect(WIDTH // 2, HEIGHT + BUTTON_Y_OFFSET, SAVE_BUTTON_WIDTH, BUTTON_HEIGHT)
                if exit_button.collidepoint(mouse_pos):
                    logger.info("Exit button clicked")
                    pygame.quit()
                    sys.exit()
                elif save_button.collidepoint(mouse_pos):
                    pygame.image.save(self.view.screen, RESULT_IMAGE_PATH)
                    self.is_result_saved = True
                    logger.info("Results saved")