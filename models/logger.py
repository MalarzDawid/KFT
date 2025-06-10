import logging
from enum import Enum

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GameState(Enum):
    SPINNING = "spinning"
    WAITING = "waiting"
    SHOWING_GIF = "showing_gif"
    RESULTS = "results"

class GameStateTracker:
    """Manages and tracks the game state."""
    def __init__(self, total_draws):
        self.state = GameState.SPINNING
        self.current_draw = 0
        self.total_draws = total_draws
        self.results = []
        self.result_responses = []
        self.wait_timer = 0
        logger.info(f"GameStateModel initialized with {total_draws} draws")

    def set_state(self, new_state):
        """Set the game state."""
        logger.info(f"State changed from {self.state} to {new_state}")
        self.state = new_state

    def increment_draw(self):
        """Increment the current draw."""
        self.current_draw += 1
        if self.current_draw >= self.total_draws:
            self.set_state(GameState.RESULTS)
        logger.info(f"Current draw incremented to {self.current_draw}/{self.total_draws}")

    def add_result(self, result, response):
        """Add a result and response."""
        self.results.append(result)
        self.result_responses.append(response)
        logger.info(f"Added result: {result}, response: {response}")

    def reset_wait_timer(self, duration):
        """Reset the wait timer."""
        self.wait_timer = duration
        logger.info(f"Wait timer set to {duration} seconds")

    def update_timer(self, dt):
        """Update the wait timer."""
        self.wait_timer -= dt
        return self.wait_timer <= 0