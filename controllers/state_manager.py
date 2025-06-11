import logging

logger = logging.getLogger(__name__)

class StateManager:
    """Manages application states and transitions.

    This class coordinates state changes and controller updates.
    """

    def __init__(self):
        """Initialize the StateManager."""
        self.current_state = "menu"
        self.controllers = {}

    def register_controller(self, state, controller):
        """Register a controller for a specific state.

        Args:
            state (str): State name.
            controller: Controller instance.
        """
        self.controllers[state] = controller

    def set_state(self, new_state):
        """Change the current state.

        Args:
            new_state (str): New state to transition to.
        """
        if new_state in self.controllers:
            logger.info(f"Switching state from {self.current_state} to {new_state}")
            self.current_state = new_state
        else:
            logger.warning(f"State {new_state} not registered")

    def update(self, dt):
        """Update the current state's controller.

        Args:
            dt (float): Delta time in seconds.
        """
        if self.current_state in self.controllers:
            self.controllers[self.current_state].update(dt)

    def handle_event(self, event):
        """Handle events for the current state's controller.

        Args:
            event: Pygame event object.

        Returns:
            str or None: Action name or None if no action.
        """
        if self.current_state in self.controllers:
            action = self.controllers[self.current_state].handle_event(event)
            if action and action in self.controllers:
                self.set_state(action)
            return action
        return None