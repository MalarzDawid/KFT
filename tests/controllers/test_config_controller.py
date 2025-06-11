import unittest
import pygame
from unittest.mock import Mock, patch

from controllers.config_controller import ConfigController, InputHandler, ConfigSaver

class TestInputHandler(unittest.TestCase):

    def setUp(self):
        self.view = Mock()
        self.view.save_button = (10, 10, 100, 30, "Save")
        self.view.back_button = (120, 10, 100, 30, "Back")
        self.view.prompt_box = Mock()
        self.view.color_picker = Mock()
        self.view.music_box = Mock()
        self.view.bg_box = Mock()
        self.view.answer_inputs = [Mock(), Mock()]
        self.handler = InputHandler(self.view)

    


class TestConfigController(unittest.TestCase):

    def setUp(self):
        self.view = Mock()
        self.view.prompt_box = Mock(get_value=Mock(return_value="prompt"))
        self.view.music_box = Mock(get_value=Mock(return_value="music.mp3"))
        self.view.bg_box = Mock(get_value=Mock(return_value="bg.png"))
        self.view.color_picker = Mock(selected_color=(0, 0, 0))
        self.view.answer_inputs = [Mock(get_value=Mock(return_value=2)), Mock(get_value=Mock(return_value=3))]
        self.config_manager = Mock()
        self.state_manager = Mock()
        self.controller = ConfigController(self.view, self.config_manager, self.state_manager)

    def test_handle_event_save(self):
        self.controller.input_handler.done = True
        self.controller.handle_event(Mock())
        self.config_manager.generate_ai_answers.assert_called_once_with("prompt")
        self.config_manager.save_config.assert_called_once_with("prompt", "music.mp3", "bg.png", (0, 0, 0), [2, 3])

    def test_handle_event_back(self):
        self.controller.input_handler.go_back = True
        self.controller.handle_event(Mock())
        self.assertEqual(self.controller.go_back, True)
        self.controller.update(0.1)
        self.state_manager.set_state.assert_called_once_with('menu')

    def test_update_go_back(self):
        self.controller.input_handler.go_back = True
        self.controller.update(0.1)
        self.state_manager.set_state.assert_called_once_with('menu')

    def test_properties(self):
        self.controller.input_handler.done = True
        self.assertTrue(self.controller.is_done)
        self.controller.go_back = True
        self.assertTrue(self.controller.should_go_back)

if __name__ == "__main__":
    unittest.main()
