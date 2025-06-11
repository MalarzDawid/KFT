from unittest.mock import Mock
from controllers.game_controller import GameController

def test_game_controller_initialization(mocker):
    # Mock load_json_file to avoid file access
    mock_load_json = mocker.patch('controllers.game_controller.load_json_file')
    mock_load_json.return_value = {"mocked": "data"}  # Return a mock dictionary

    # Configure the mock for config_manager and game_state
    game_state_mock = Mock()
    game_state_mock.current_draw = 0  # Set current_draw to an integer
    game_view_mock = Mock()
    config_manager_mock = Mock()
    config_manager_mock.config = {"questions": [{"answers": ["A", "B"], "num_answers": 2}]}  # Set the config attribute

    # Mock SpinWheelModel to avoid pygame.mixer initialization
    mock_spin_wheel = mocker.patch('controllers.game_controller.SpinWheelModel')
    mock_spin_wheel.return_value = Mock(segments=["A", "B"])  # Mock the instance with expected segments

    controller = GameController(game_state_mock, game_view_mock, config_manager_mock)
    assert controller.game_state == game_state_mock
    assert controller.view == game_view_mock
    assert controller.config == config_manager_mock
    # Verify that load_json_file was called with the expected path
    mock_load_json.assert_called_once_with('data/TextResp.json')
    # Verify that SpinWheelModel was called
    mock_spin_wheel.assert_called_once()

def test_game_controller_generate_new_wheel(mocker):
    # Mock load_json_file to avoid file access
    mock_load_json = mocker.patch('controllers.game_controller.load_json_file')
    mock_load_json.return_value = {"mocked": "data"}  # Return a mock dictionary

    game_state_mock = Mock(current_draw=0)
    game_view_mock = Mock()
    mock_spin_wheel = mocker.patch('controllers.game_controller.SpinWheelModel')
    mock_spin_wheel.return_value = Mock(segments=["A", "B"])  # Mock the instance with expected segments
    config_manager_mock = Mock()
    config_manager_mock.config = {"questions": [{"answers": ["A", "B"], "num_answers": 2}]}  # Set the config attribute
    controller = GameController(game_state_mock, game_view_mock, config_manager_mock)
    controller.generate_new_wheel()
    assert controller.wheel is not None
    assert len(controller.wheel.segments) == 2