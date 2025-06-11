import pytest
from unittest.mock import Mock
from models.spin_wheel import SpinWheelModel
from constants import FULL_CIRCLE

# Mock pygame.mixer.Sound at the module level to avoid file access during import
@pytest.fixture(autouse=True)
def mock_pygame_sound(mocker):
    mock_sound = Mock()
    mocker.patch('pygame.mixer.Sound', return_value=mock_sound)

def test_spin_wheel_initialization():
    segments = ["A", "B", "C"]
    wheel = SpinWheelModel(segments)
    assert wheel.segment_count == 3
    assert wheel.segment_angle == FULL_CIRCLE / 3
    assert not wheel.spinning
    assert wheel.angle == 0

def test_spin_wheel_spin(mocker):
    segments = ["A", "B", "C"]
    # Ensure pygame.mixer.Sound is mocked for this test too
    mock_sound = Mock(play=Mock())
    mocker.patch('pygame.mixer.Sound', return_value=mock_sound)
    mocker.patch('random.uniform', return_value=1.0)
    mocker.patch('random.randint', return_value=900)

    wheel = SpinWheelModel(segments)
    wheel.spin()
    assert wheel.spinning
    assert wheel.angular_velocity < 0
    assert wheel.target_angle < 0