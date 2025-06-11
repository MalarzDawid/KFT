import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import numpy as np

from controllers.media_loader import MediaLoader

class TestMediaLoader(unittest.TestCase):

    def setUp(self):
        """Prepare a fresh MediaLoader instance for each test."""
        self.loader = MediaLoader()


    @patch('pathlib.Path.exists')
    def test_load_gif_not_found(self, mock_exists):
        """Test loading a non-existent GIF."""
        mock_exists.return_value = False
        result = self.loader.load_gif(1)
        self.assertFalse(result)
        self.assertEqual(len(self.loader.gif_frames), 0)

    @patch('pathlib.Path.exists')
    @patch('imageio.v2.get_reader')
    def test_load_gif_error(self, mock_get_reader, mock_exists):
        """Test error during GIF loading."""
        mock_exists.return_value = True
        mock_get_reader.side_effect = Exception("Test error")
        result = self.loader.load_gif(1)
        self.assertFalse(result)
        self.assertEqual(len(self.loader.gif_frames), 0)

    def test_update(self):
        """Test updating the frame timer."""
        self.loader.gif_frames = [Mock(), Mock()]
        self.loader.frame_delay = 0.5
        self.loader.update(0.3)
        self.assertEqual(self.loader.frame_timer, 0.3)
        self.loader.update(0.3)
        self.assertEqual(self.loader.frame_timer, 0.0)
        self.assertEqual(self.loader.current_frame, 1)

    def test_current_frame_surface(self):
        """Test getting the current frame surface."""
        mock_surface = Mock()
        self.loader.gif_frames = [mock_surface]
        self.assertEqual(self.loader.current_frame_surface, mock_surface)
        self.loader.gif_frames = []
        self.assertIsNone(self.loader.current_frame_surface)

if __name__ == "__main__":
    unittest.main()