from unittest.mock import Mock
from utils import handle_button_click

def test_handle_button_click_no_click():
    event_mock = Mock(type=1)  # Not MOUSEBUTTONDOWN
    buttons = [(100, 100, 50, 50, "Test")]
    result = handle_button_click(event_mock, buttons)
    assert not result