import pytest
from unittest.mock import mock_open, patch
from models.config_manager import ConfigManager
import json

@pytest.fixture
def config_manager():
    return ConfigManager()

def test_load_config_existing_file(mocker, config_manager):
    mock_config = {
        "prompt": "Star Wars",
        "music": "music.mp3",
        "bg_img": "bg.png",
        "bg_color": [60, 30, 30],
        "questions": [{"text": "Question 1", "num_answers": 2, "answers": ["A", "B"]}]
    }
    mocker.patch('utils.load_json_file', return_value=mock_config)
    config = config_manager.load_config()
    assert config == mock_config
    assert config_manager.config == mock_config

def test_load_config_file_not_found(mocker, config_manager):
    mocker.patch('utils.load_json_file', side_effect=FileNotFoundError)
    config = config_manager.load_config()
    assert config == {
        "questions": [],
        "bg_img": "None",
        "bg_color": [60, 30, 30],
        "prompt": "",
        "music": ""
    }