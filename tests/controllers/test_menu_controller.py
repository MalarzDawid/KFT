import unittest
from unittest.mock import Mock, patch
import pygame

from controllers.menu_controller import MenuController

class TestMenuController(unittest.TestCase):

    def setUp(self):
        """Prepare a fresh MenuController instance for each test."""
        self.menu_view = Mock()
        # Mock the buttons list in the view
        self.menu_view.buttons = [
            {"pos": (100, 100), "label": "Start", "action": "start"},
            {"pos": (100, 200), "label": "Exit", "action": "exit"}
        ]
        self.controller = MenuController(self.menu_view)

    def test_initialization(self):
        """Test that MenuController initializes with correct view."""
        self.assertEqual(self.controller.view, self.menu_view)

    def test_update(self):
        """Test that update calls render on the view."""
        self.controller.update(0.1)
        self.menu_view.render.assert_called_once()


if __name__ == "__main__":
    unittest.main()