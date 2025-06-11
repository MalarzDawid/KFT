from pathlib import Path

import pygame
import math
import logging
from constants import (
    WIDTH, HEIGHT, CENTER, WHEEL_RADIUS, SEGMENT_COLORS, FONT_SIZE, RESPONSE_FONT_SCALE,
    SMALL_FONT_SCALE, QUESTIONS, PROGRESS_TEXT_POS, RESULT_TEXT_Y, INSTRUCTIONS_Y, TITLE_Y,
    RESPONSE_TEXT_Y_OFFSET, TEXT_BG_ALPHA, TEXT_MARGIN, RESULT_Y_START, RESULT_Y_GAP,
    RESPONSE_Y_GAP, BUTTON_WIDTH, SAVE_BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_Y_OFFSET,
    EXIT_BUTTON_COLOR, SAVE_BUTTON_COLOR, TEXT_RADIUS_SCALE, FONT_SIZE_REDUCTION,
    CIRCLE_RADIUS, CIRCLE_BORDER_COLOR, CIRCLE_FILL_COLOR, INDICATOR_Y_OFFSET,
    INDICATOR_SIZE, INDICATOR_COLOR, BORDER_THICKNESS, PADDING
)
from utils import render_text, draw_button, wrap_text

logger = logging.getLogger(__name__)

class GameView:
    """Handles rendering of the game UI.

    This class is responsible for rendering different game states.
    """

    def __init__(self, screen, config):
        """Initialize the GameView.

        Args:
            screen: Pygame surface for rendering.
            config (dict): Configuration data.
        """
        self.screen = screen
        self.config = config
        self.font = pygame.font.SysFont("Arial", FONT_SIZE, bold=True)
        self.response_font = pygame.font.SysFont("Arial", int(FONT_SIZE * RESPONSE_FONT_SCALE))
        self.small_font = pygame.font.SysFont("Arial", int(FONT_SIZE * SMALL_FONT_SCALE), bold=True)
        logger.info("GameView initialized")

    def render_background(self):
        """Render the background."""
        self.screen.fill(tuple(self.config["bg_color"]))
        if self.config["bg_img"] != "None":
            try:
                img_path = Path('assets') / 'backgrounds' / self.config["bg_img"]
                img = pygame.image.load(img_path)
                self.screen.fill((128, 128, 128))
                self.screen.blit(img, (0, 0), None, pygame.BLEND_RGB_ADD)
            except FileNotFoundError:
                logger.error(f"Background image not found: {self.config['bg_img']}")
            except pygame.error as e:
                logger.error(f"Error loading background image: {e}")

    def render_spinning(self, wheel_model, current_draw):
        """Render the spinning state.

        Args:
            wheel_model: SpinWheelModel instance.
            current_draw (int): Current draw index.
        """
        self.render_background()
        self._draw_wheel(wheel_model)
        render_text(self.font, QUESTIONS[current_draw], (0, 0, 0), *PROGRESS_TEXT_POS, self.screen)

    def render_waiting(self, wheel_model, current_draw, result, can_spin):
        """Render the waiting state.

        Args:
            wheel_model: SpinWheelModel instance.
            current_draw (int): Current draw index.
            result (str): Current result.
            can_spin (bool): Whether spinning is allowed.
        """
        self.render_spinning(wheel_model, current_draw)
        render_text(self.font, f"Result: {result}", (0, 0, 0), WIDTH // 2, RESULT_TEXT_Y, self.screen, center=True)
        if can_spin:
            render_text(self.font, "Press SPACE or click to spin", (0, 0, 0), WIDTH // 2, INSTRUCTIONS_Y, self.screen, center=True)

    def render_gif(self, media_loader, result, response):
        """Render the GIF state.

        Args:
            media_loader: MediaLoader instance.
            result (str): Current result.
            response (str): Current response.
        """
        self.render_background()
        if media_loader.current_frame_surface:
            frame_rect = media_loader.current_frame_surface.get_rect(center=CENTER)
            self.screen.blit(media_loader.current_frame_surface, frame_rect)
        render_text(self.font, f"Result: {result}", (0, 0, 0), WIDTH // 2, 30, self.screen, center=True)
        text_bg_rect = pygame.Rect(0, HEIGHT + RESPONSE_TEXT_Y_OFFSET, WIDTH, 80)
        s = pygame.Surface((text_bg_rect.width, text_bg_rect.height), pygame.SRCALPHA)
        s.fill((0, 0, 0, TEXT_BG_ALPHA))
        self.screen.blit(s, text_bg_rect)
        max_width = WIDTH - TEXT_MARGIN
        lines = wrap_text(response, self.response_font, max_width)
        line_height = self.response_font.get_height()
        for i, line in enumerate(lines):
            render_text(self.response_font, line, (255, 255, 255), WIDTH // 2,
                        HEIGHT + RESPONSE_TEXT_Y_OFFSET + (i * line_height), self.screen, center=True)

    def render_results(self, results, responses, is_saved):
        """Render the results state.

        Args:
            results (list): List of results.
            responses (list): List of responses.
            is_saved (bool): Whether results are saved.
        """
        self.render_background()
        render_text(self.font, "Final Results", (0, 0, 0), WIDTH // 2, TITLE_Y, self.screen, center=True)
        result_y = RESULT_Y_START
        for i, (result, response) in enumerate(zip(results, responses)):
            render_text(self.small_font, f"Draw {i+1}: {result}", (0, 0, 0), WIDTH // 2, result_y, self.screen, center=True)
            result_y += RESULT_Y_GAP
            render_text(self.small_font, f'"{response}"', (80, 80, 80), WIDTH // 2, result_y, self.screen, center=True)
            result_y += RESPONSE_Y_GAP
        exit_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH - PADDING, HEIGHT + BUTTON_Y_OFFSET, BUTTON_WIDTH, BUTTON_HEIGHT)
        save_rect = pygame.Rect(WIDTH // 2 + PADDING, HEIGHT + BUTTON_Y_OFFSET, SAVE_BUTTON_WIDTH, BUTTON_HEIGHT)
        draw_button(self.screen, exit_rect, EXIT_BUTTON_COLOR, "Zakończ", self.font)
        draw_button(self.screen, save_rect, SAVE_BUTTON_COLOR if is_saved else EXIT_BUTTON_COLOR, "Zapisz wynik", self.font)

    def _draw_wheel(self, wheel_model):
        """Draw the wheel based on the model.

        Args:
            wheel_model: SpinWheelModel instance.
        """
        for i in range(wheel_model.segment_count):
            start_angle = math.radians(wheel_model.angle + i * wheel_model.segment_angle)
            end_angle = math.radians(wheel_model.angle + (i + 1) * wheel_model.segment_angle)
            points = [CENTER]
            for angle in [start_angle, end_angle]:
                x = CENTER[0] + WHEEL_RADIUS * math.cos(angle)
                y = CENTER[1] - WHEEL_RADIUS * math.sin(angle)
                points.append((int(x), int(y)))
            color = SEGMENT_COLORS[i % len(SEGMENT_COLORS)]
            pygame.draw.polygon(self.screen, color, points)
            pygame.draw.polygon(self.screen, (0, 0, 0), points, BORDER_THICKNESS)
            mid_angle = (start_angle + end_angle) / 2
            text_radius = WHEEL_RADIUS * TEXT_RADIUS_SCALE
            text_x = CENTER[0] + text_radius * math.cos(mid_angle)
            text_y = CENTER[1] - text_radius * math.sin(mid_angle)
            text_font = pygame.font.SysFont("Arial", FONT_SIZE - FONT_SIZE_REDUCTION, bold=True)
            text_surface = text_font.render(wheel_model.segments[i], True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(text_x, text_y))
            self.screen.blit(text_surface, text_rect)
        pygame.draw.circle(self.screen, CIRCLE_FILL_COLOR, CENTER, CIRCLE_RADIUS)
        pygame.draw.circle(self.screen, CIRCLE_BORDER_COLOR, CENTER, CIRCLE_RADIUS, BORDER_THICKNESS)
        indicator_point = (CENTER[0], CENTER[1] - WHEEL_RADIUS + INDICATOR_Y_OFFSET)
        indicator_points = [
            indicator_point,
            (indicator_point[0] - INDICATOR_SIZE, indicator_point[1] - INDICATOR_SIZE),
            (indicator_point[0] + INDICATOR_SIZE, indicator_point[1] - INDICATOR_SIZE)
        ]
        pygame.draw.polygon(self.screen, INDICATOR_COLOR, indicator_points)
        pygame.draw.polygon(self.screen, (0, 0, 0), indicator_points, BORDER_THICKNESS)