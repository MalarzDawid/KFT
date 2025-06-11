import unittest
from unittest.mock import Mock, patch
import logging

from controllers.state_manager import StateManager

class TestStateManager(unittest.TestCase):

    def setUp(self):
        """Prepare a fresh StateManager instance for each test."""
        self.manager = StateManager()

    def test_initialization(self):
        """Test that StateManager initializes with correct default values."""
        self.assertEqual(self.manager.current_state, "menu")
        self.assertEqual(self.manager.controllers, {})

    def test_register_controller(self):
        """Test registering a controller for a state."""
        controller = Mock()
        self.manager.register_controller("game", controller)
        self.assertIn("game", self.manager.controllers)
        self.assertEqual(self.manager.controllers["game"], controller)

    def test_set_state_success(self):
        """Test switching to a registered state."""
        controller = Mock()
        self.manager.register_controller("game", controller)
        with patch.object(logging.Logger, 'info') as mock_logger:
            self.manager.set_state("game")
            mock_logger.assert_called_with("Switching state from menu to game")
        self.assertEqual(self.manager.current_state, "game")

    def test_set_state_failure(self):
        """Test switching to an unregistered state."""
        with patch.object(logging.Logger, 'warning') as mock_logger:
            self.manager.set_state("unregistered")
            mock_logger.assert_called_with("State unregistered not registered")
        self.assertEqual(self.manager.current_state, "menu")

    def test_update(self):
        """Test updating the current state's controller."""
        controller = Mock()
        self.manager.register_controller("game", controller)
        self.manager.current_state = "game"
        self.manager.update(0.1)
        controller.update.assert_called_once_with(0.1)

    def test_handle_event_without_action(self):
        """Test handling an event that does not trigger a state change."""
        controller = Mock()
        controller.handle_event.return_value = None
        self.manager.register_controller("game", controller)
        self.manager.current_state = "game"
        result = self.manager.handle_event("event")
        self.assertIsNone(result)

    def test_handle_event_with_action(self):
        """Test handling an event that triggers a state change."""
        controller = Mock()
        controller.handle_event.return_value = "menu"
        self.manager.register_controller("game", controller)
        self.manager.register_controller("menu", Mock())
        self.manager.current_state = "game"
        result = self.manager.handle_event("event")
        self.assertEqual(result, "menu")
        self.assertEqual(self.manager.current_state, "menu")

if __name__ == "__main__":
    unittest.main()