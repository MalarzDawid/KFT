import pygame
from pathlib import Path
import json
import logging
from constants import BORDER_RADIUS, BORDER_THICKNESS, SAVE_BUTTON_BORDER_COLOR, PADDING, MENU_BUTTON_WIDTH, \
    MENU_BUTTON_HEIGHT

logger = logging.getLogger(__name__)

def load_json_file(file_path):
    """Load a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Loaded JSON data.

    Raises:
        FileNotFoundError: If file is missing.
        json.JSONDecodeError: If JSON is invalid.
    """
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
    """Render text to a surface.

    Args:
        font: Pygame font object.
        text (str): Text to render.
        color (tuple): RGB color.
        x (int): X position.
        y (int): Y position.
        surface: Pygame surface.
        center (bool): Center text horizontally if True.

    Returns:
        pygame.Surface: Rendered text surface.
    """
    text_surface = font.render(text, True, color)
    if center:
        x -= text_surface.get_width() // 2
    surface.blit(text_surface, (x, y))
    return text_surface

def draw_button(surface, rect, base_color, text, font, border_color=SAVE_BUTTON_BORDER_COLOR, shadow_offset=4):
    """Draw a button with shadow and hover effect.

    Args:
        surface: Pygame surface.
        rect: Pygame Rect object.
        base_color (tuple): Base color of the button.
        text (str): Button text.
        font: Pygame font object.
        border_color (tuple): Border color.
        shadow_offset (int): Shadow offset.
    """
    # Ensure valid colors
    if not isinstance(base_color, (tuple, list)) or len(base_color) != 3:
        logger.error(f"Invalid base_color: {base_color}, defaulting to (80, 80, 160)")
        base_color = (80, 80, 160)

    # Draw shadow
    shadow_rect = rect.move(shadow_offset, shadow_offset)
    pygame.draw.rect(surface, (50, 50, 50), shadow_rect, border_radius=BORDER_RADIUS)
    # Draw button
    current_color = base_color
    pygame.draw.rect(surface, current_color, rect, border_radius=BORDER_RADIUS)
    pygame.draw.rect(surface, border_color, rect, BORDER_THICKNESS, border_radius=BORDER_RADIUS)
    text_surface = font.render(text, True, (0, 0, 0))
    surface.blit(text_surface, (
        rect.centerx - text_surface.get_width() // 2,
        rect.centery - text_surface.get_height() // 2
    ))

def draw_gradient_background(surface, height, start_color, end_color):
    """Draw a gradient background.

    Args:
        surface: Pygame surface.
        height (int): Height of the gradient.
        start_color (tuple): Starting RGB color.
        end_color (tuple): Ending RGB color.
    """
    for y in range(height):
        ratio = y / height
        color = (
            int(start_color[0] * (1 - ratio) + end_color[0] * ratio),
            int(start_color[1] * (1 - ratio) + end_color[1] * ratio),
            int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        )
        pygame.draw.line(surface, color, (0, y), (surface.get_width(), y))

def handle_button_click(event, buttons):
    """Handle button click events.

    Args:
        event: Pygame event object.
        buttons (list): List of button tuples (x, y, w, h, label) or dicts (pos, w, h, label, action).

    Returns:
        bool: True if a button was clicked.
    """
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        logger.debug(f"Mouse click at {mouse_pos}")
        for button in buttons:
            # Handle both tuple and dict formats
            if isinstance(button, tuple):
                x, y, w, h, label, *_ = button  # Unpack tuple, ignore extra elements
                rect = pygame.Rect(x - w // 2, y - h // 2, w, h)
                button_label = label
            elif isinstance(button, dict):
                x = button["pos"][0]
                y = button["pos"][1]
                w = button.get("w", MENU_BUTTON_WIDTH)
                h = button.get("h", MENU_BUTTON_HEIGHT)
                rect = pygame.Rect(x - w // 2, y - h // 2, w, h)
                button_label = button.get("label", button.get("action", ""))
            else:
                logger.error(f"Unsupported button format: {button}")
                continue

            logger.debug(f"Button rect: {rect}")
            if rect.collidepoint(mouse_pos):
                logger.info(f"Button clicked: {button_label}")
                return True
    return False

def wrap_text(text, font, max_width):
    """Wrap text to fit within a width.

    Args:
        text (str): Text to wrap.
        font: Pygame font object.
        max_width (int): Maximum width in pixels.

    Returns:
        list: List of wrapped text lines.
    """
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