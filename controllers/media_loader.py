import imageio.v2 as imageio
import pygame
from pathlib import Path
import logging
from constants import WIDTH, HEIGHT, GIF_SCALE_FACTOR, SECOND_IN_MS, FRAME_DELAY_DEFAULT

logger = logging.getLogger(__name__)

class MediaLoader:
    """Handles loading of media assets like GIFs.

    This class manages media loading and animation.
    """

    def __init__(self):
        """Initialize the MediaLoader."""
        self.gif_frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = FRAME_DELAY_DEFAULT

    def load_gif(self, result):
        """Load a GIF for the given result.

        Args:
            result (str): Result identifier.

        Returns:
            bool: True if GIF loaded successfully.
        """
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
                self.frame_delay = gif_reader.get_meta_data()['duration'] / SECOND_IN_MS
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
            return True
        except Exception as e:
            logger.error(f"Error loading GIF {gif_path}: {e}")
            return False

    def update(self, dt):
        """Update frame timer for GIF animation.

        Args:
            dt (float): Delta time in seconds.
        """
        if self.gif_frames:
            self.frame_timer += dt
            if self.frame_timer >= self.frame_delay:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.gif_frames)

    @property
    def current_frame_surface(self):
        """Get the current GIF frame.

        Returns:
            pygame.Surface or None: Current frame or None if no frames.
        """
        return self.gif_frames[self.current_frame] if self.gif_frames else None