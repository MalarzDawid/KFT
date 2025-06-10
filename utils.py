import pygame
from pathlib import Path
import json
import logging
from constants import BORDER_RADIUS, BORDER_THICKNESS, SAVE_BUTTON_BORDER_COLOR

logger = logging.getLogger(__name__)

def load_json_file(file_path):
    """Load a JSON file."""
    try:
        with Path(file_path).open('r', encoding='utf-8-sig') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        raise

def render_text(font, text, color, x, y, surface, center=False):
    """Render text to a surface."""
    text_surface = font.render(text, True, color)
    if center:
        x -= text_surface.get_width() // 2
    surface.blit(text_surface, (x, y))
    return text_surface

def draw_button(surface, rect, color, text, font, border_color=SAVE_BUTTON_BORDER_COLOR):
    """Draw a button."""
    pygame.draw.rect(surface, color, rect, border_radius=BORDER_RADIUS)
    pygame.draw.rect(surface, border_color, rect, BORDER_THICKNESS, border_radius=BORDER_RADIUS)
    text_surface = font.render(text, True, (0, 0, 0))
    surface.blit(text_surface, (
        rect.centerx - text_surface.get_width() // 2,
        rect.centery - text_surface.get_height() // 2
    ))

def wrap_text(text, font, max_width):
    """Wrap text to fit within a width."""
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        width, _ = font.size(test_line)
        if width <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines