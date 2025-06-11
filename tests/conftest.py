import pytest

@pytest.fixture(autouse=True)
def mock_pygame(mocker):
    mocker.patch('pygame.init')
    mocker.patch('pygame.display.set_mode')
    mocker.patch('pygame.font.SysFont')
    mocker.patch('pygame.mixer.init')
    mocker.patch('pygame.mixer.Sound')
    mocker.patch('pygame.image.load')
    mocker.patch('pygame.image.save')
    yield