import pygame
import sys
import imageio.v2 as imageio
import random
import logging
from pathlib import Path
from constants import (
    WIDTH, HEIGHT, SPACE_KEY, MOUSE_LEFT_BUTTON, GIF_SCALE_FACTOR, GIF_DISPLAY_TIME,
    FRAME_DELAY_DEFAULT, WAIT_TIME, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_Y_OFFSET,
    SAVE_BUTTON_WIDTH, RESULT_IMAGE_PATH, TEXT_RESP_PATH
)
from models.logger import GameState
from models.spin_wheel import SpinWheelModel
from utils import load_json_file

logger = logging.getLogger(__name__)

class GameController:
    """Handles game input and coordinates model and view."""
    def __init__(self, game_state_model, game_view, config_manager):
        self.game_state = game_state_model
        self.view = game_view
        self.config = config_manager
        self.wheel = None
        self.gif_frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = FRAME_DELAY_DEFAULT
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

    def load_gif(self, result):
        """Load a GIF for the result."""
        self.gif_frames = []
        self.current_frame = 0
        safe_result = str(result)
        gif_path = Path('assets') / 'gifs' / f"{safe_result}.gif"
        if not gif_path.exists():
            logger.warning(f"GIF not found: {gif_path}")
            return False
        try:
            gif_reader = imageio.get_reader(gif_path)
            try:
                self.frame_delay = gif_reader.get_meta_data()['duration'] / 1000.0
            except KeyError:
                self.frame_delay = FRAME_DELAY_DEFAULT
            for frame_idx in range(gif_reader.get_length()):
                frame_data = gif_reader.get_data(frame_idx)
                frame_surface = pygame.image.frombuffer(
                    frame_data.tobytes(), frame_data.shape[1::-1], "RGB")
                scale_factor = min(WIDTH / frame_surface.get_width(), HEIGHT / frame_surface.get_height()) * GIF_SCALE_FACTOR
                new_size = (int(frame_surface.get_width() * scale_factor), int(frame_surface.get_height() * scale_factor))
                frame_surface = pygame.transform.scale(frame_surface, new_size)
                self.gif_frames.append(frame_surface)
            logger.info(f"Loaded GIF: {gif_path}")
            return len(self.gif_frames) > 0
        except Exception as e:
            logger.error(f"Error loading GIF {gif_path}: {e}")
            return False

    def get_random_response(self, result):
        """Get a random response."""
        question_idx = self.game_state.current_draw + 1
        return random.choice(self.responses[f"{question_idx}"][f"{result}/10"])

    def update(self, dt):
        """Update the game state."""
        if self.game_state.state == GameState.SPINNING:
            self.wheel.update(dt)
            if not self.wheel.spinning:
                result, idx = self.wheel.get_selected_segment()
                question_idx, _ = idx.split(".")
                response = self.get_random_response(question_idx)
                self.game_state.add_result(result, response)
                if self.load_gif(idx):
                    self.game_state.set_state(GameState.SHOWING_GIF)
                    self.game_state.reset_wait_timer(GIF_DISPLAY_TIME)
                    self.frame_timer = 0
                else:
                    self.game_state.set_state(GameState.WAITING)
                    self.game_state.reset_wait_timer(WAIT_TIME)
        elif self.game_state.state == GameState.SHOWING_GIF:
            self.frame_timer += dt
            if self.frame_timer >= self.frame_delay and self.gif_frames:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
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
        self.view.render_spinning(self.wheel, self.game_state.current_draw) if self.game_state.state == GameState.SPINNING else \
        self.view.render_waiting(self.wheel, self.game_state.current_draw, self.game_state.results[-1], not self.wheel.spinning) if self.game_state.state == GameState.WAITING else \
        self.view.render_gif(self.gif_frames, self.current_frame, self.game_state.results[-1], self.game_state.result_responses[-1]) if self.game_state.state == GameState.SHOWING_GIF else \
        self.view.render_results(self.game_state.results, self.game_state.result_responses, self.is_result_saved)

    def handle_event(self, event):
        """Handle input events."""
        if self.game_state.state == GameState.SPINNING and not self.wheel.spinning:
            if (event.type == pygame.KEYDOWN and event.key == SPACE_KEY) or \
               (event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_LEFT_BUTTON):
                self.wheel.spin()
                logger.info("Wheel spun by user")
        elif self.game_state.state == GameState.RESULTS:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_LEFT_BUTTON:
                mouse_pos = pygame.mouse.get_pos()
                exit_button = pygame.Rect(WIDTH//2 - 300, HEIGHT + BUTTON_Y_OFFSET, BUTTON_WIDTH, BUTTON_HEIGHT)
                save_button = pygame.Rect(WIDTH//2, HEIGHT + BUTTON_Y_OFFSET, SAVE_BUTTON_WIDTH, BUTTON_HEIGHT)
                if exit_button.collidepoint(mouse_pos):
                    logger.info("Exit button clicked")
                    pygame.quit()
                    sys.exit()
                elif save_button.collidepoint(mouse_pos):
                    pygame.image.save(self.view.screen, RESULT_IMAGE_PATH)
                    self.is_result_saved = True
                    logger.info("Results saved")