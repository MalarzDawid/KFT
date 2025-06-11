import unittest
from unittest.mock import MagicMock, patch
import pygame

from controllers.config_controller import InputHandler, ConfigSaver, ConfigController
from utils import handle_button_click

class DummyEvent:
    def __init__(self, type):
        self.type = type

class TestInputHandler(unittest.TestCase):
    def setUp(self):
        # Create a dummy view with necessary attributes
        self.view = MagicMock()
        # Buttons use pygame.Rect for collision
        self.view.save_button = {"rect": pygame.Rect(10, 10, 50, 30)}
        self.view.back_button = {"rect": pygame.Rect(70, 10, 50, 30)}
        # Subcomponents must have handle_event
        self.view.prompt_box = MagicMock()
        self.view.color_picker = MagicMock()
        self.view.color_picker.handle_event = MagicMock()
        self.view.music_box = MagicMock()
        self.view.music_box.handle_event = MagicMock()
        self.view.bg_box = MagicMock()
        self.view.bg_box.handle_event = MagicMock()
        self.view.answer_inputs = []
        self.handler = InputHandler(self.view)

    @patch('pygame.mouse.get_pos')
    def test_save_button_click_sets_done(self, mock_get_pos):
        # Position mouse within save button rect
        mock_get_pos.return_value = (15, 15)
        event = DummyEvent(pygame.MOUSEBUTTONDOWN)
        self.handler.handle_event(event)
        self.assertTrue(self.handler.done)
        self.assertFalse(self.handler.go_back)

    @patch('pygame.mouse.get_pos')
    def test_back_button_click_sets_go_back(self, mock_get_pos):
        # Position mouse within back button rect
        mock_get_pos.return_value = (75, 15)
        event = DummyEvent(pygame.MOUSEBUTTONDOWN)
        self.handler.handle_event(event)
        self.assertTrue(self.handler.go_back)
        self.assertFalse(self.handler.done)

class TestConfigSaver(unittest.TestCase):
    def setUp(self):
        self.config_manager = MagicMock()
        self.saver = ConfigSaver(self.config_manager)

    def test_save_calls_manager_methods(self):
        prompt = "Hello"
        music = "song.mp3"
        bg_img = "bg.png"
        bg_color = (255, 255, 255)
        answer_counts = [1, 2, 3]
        self.saver.save(prompt, music, bg_img, bg_color, answer_counts)
        self.config_manager.generate_ai_answers.assert_called_once_with(prompt)
        self.config_manager.save_config.assert_called_once_with(
            prompt, music, bg_img, bg_color, answer_counts
        )

class TestConfigController(unittest.TestCase):
    def setUp(self):
        # Prepare view with all required fields
        self.view = MagicMock()
        self.view.save_button = {"rect": pygame.Rect(0,0,10,10)}
        self.view.back_button = {"rect": pygame.Rect(0,0,10,10)}
        self.view.prompt_box = MagicMock()
        self.view.prompt_box.get_value.return_value = "Prompt"
        self.view.prompt_box.handle_event = MagicMock()
        self.view.music_box = MagicMock()
        self.view.music_box.get_value.return_value = "song.mp3"
        self.view.music_box.handle_event = MagicMock()
        self.view.bg_box = MagicMock()
        self.view.bg_box.get_value.return_value = "bg.png"
        self.view.bg_box.handle_event = MagicMock()
        self.view.color_picker = MagicMock()
        self.view.color_picker.selected_color = (0, 0, 0)
        self.view.color_picker.handle_event = MagicMock()
        # Simulate two answer input boxes
        a1, a2 = MagicMock(), MagicMock()
        a1.get_value.return_value = 5
        a1.handle_event = MagicMock()
        a2.get_value.return_value = 10
        a2.handle_event = MagicMock()
        self.view.answer_inputs = [a1, a2]

        self.config_manager = MagicMock()
        self.state_manager = MagicMock()
        self.controller = ConfigController(
            self.view, self.config_manager, self.state_manager
        )

    def test_save_flow(self):
        # Simulate save button click
        self.controller.input_handler.done = True
        event = DummyEvent(pygame.MOUSEBUTTONDOWN)
        # Handle event triggers save
        self.controller.handle_event(event)
        # Check save was called on saver
        self.config_manager.generate_ai_answers.assert_called_once_with("Prompt")
        self.config_manager.save_config.assert_called_once_with(
            "Prompt", "song.mp3", "bg.png", (0, 0, 0), [5, 10]
        )
        # State change on update
        self.controller.update(dt=0)
        self.state_manager.set_state.assert_called_with('menu')

    def test_go_back_flow(self):
        # Simulate back button click
        self.controller.input_handler.go_back = True
        event = DummyEvent(pygame.MOUSEBUTTONDOWN)
        self.controller.handle_event(event)
        self.controller.update(dt=0)
        self.state_manager.set_state.assert_called_with('menu')

if __name__ == '__main__':
    unittest.main()
