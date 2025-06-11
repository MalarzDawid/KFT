import random
import pygame.mixer
from pathlib import Path
import logging
from constants import (
    SPIN_INITIAL_VELOCITY_MIN, SPIN_INITIAL_VELOCITY_MAX, SPIN_VELOCITY_MODIFIER_MIN,
    SPIN_VELOCITY_MODIFIER_MAX, SPIN_ADDITIONAL_ROTATIONS, SPIN_SOUND_PATH, FULL_CIRCLE, ANG_VELOCITY,
    INDICATOR_POSITION
)

logger = logging.getLogger(__name__)

pygame.mixer.init()
SPIN_SOUND = pygame.mixer.Sound(Path(SPIN_SOUND_PATH))

class SpinWheelModel:
    """Manages the spinning wheel's logic.

    This class handles the physics and selection logic of the wheel.
    """

    def __init__(self, segments):
        """Initialize the SpinWheelModel.

        Args:
            segments (list): List of segment labels.
        """
        self.segments = segments
        self.segment_count = len(segments)
        self.segment_angle = FULL_CIRCLE / self.segment_count
        self.angle = 0
        self.target_angle = 0
        self.angular_velocity = ANG_VELOCITY
        self.deceleration = 0
        self.spinning = False
        self.spin_sound = SPIN_SOUND
        logger.info(f"SpinWheelModel initialized with {self.segment_count} segments")

    def spin(self):
        """Start spinning the wheel."""
        if not self.spinning:
            self.spinning = True
            self.spin_sound.play(-1)
            modifier = random.uniform(SPIN_VELOCITY_MODIFIER_MIN, SPIN_VELOCITY_MODIFIER_MAX)
            self.angular_velocity = -random.randint(SPIN_INITIAL_VELOCITY_MIN, SPIN_INITIAL_VELOCITY_MAX) * modifier
            additional_rotation = SPIN_ADDITIONAL_ROTATIONS * modifier * FULL_CIRCLE
            self.target_angle = self.angle - additional_rotation
            self.deceleration = (self.angular_velocity ** 2) / (2 * -additional_rotation)
            logger.info("Wheel spinning started")

    def update(self, dt):
        """Update the wheel's rotation.

        Args:
            dt (float): Delta time in seconds.
        """
        if self.spinning:
            self.angle += self.angular_velocity * dt
            self.angular_velocity -= self.deceleration * dt
            if self.angular_velocity >= 0:
                self.angular_velocity = 0
                self.spinning = False
                self.angle = self.target_angle
                self.spin_sound.stop()
                logger.info("Wheel spinning stopped")
            self.angle %= FULL_CIRCLE

    def get_selected_segment(self):
        """Get the selected segment.

        Returns:
            tuple: (selected segment, index string).
        """
        indicator_position = INDICATOR_POSITION
        adjusted_angle = (FULL_CIRCLE - self.angle % FULL_CIRCLE)
        relative_position = (adjusted_angle + indicator_position) % FULL_CIRCLE
        segment_index = int(relative_position / self.segment_angle)
        idx = random.randint(1, 5)
        selected = self.segments[segment_index % self.segment_count]
        logger.info(f"Selected segment: {selected}, index: {(segment_index % self.segment_count) + 1}.{idx}")
        return selected, f"{(segment_index % self.segment_count) + 1}.{idx}"