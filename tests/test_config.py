import pytest
from pathlib import Path
import tomlkit
from unittest.mock import patch, MagicMock

from aiod.configuration._config import Config, load_configuration, _add_decode_error_note

def test_config_defaults():
    config = Config()
    assert config.api_server == "https://api.aiodp.eu/"
    assert config.version == "v2"
    assert config.auth_server == "https://auth.aiodp.eu/aiod-auth/"
    assert config.realm == "aiod"
    assert config.client_id == "aiod-sdk"
    assert config.request_timeout_seconds == 10

def test_config_subscribe_and_notify():
    config = Config()
    mock_observer = MagicMock()
    
    config.subscribe("api_server", mock_observer)
    
    # Trigger observer
    config.api_server = "http://new.api.server/"
    
    # Should be called with (key, old_value, new_value)
    mock_observer.assert_called_once_with("api_server", "https://api.aiodp.eu/", "http://new.api.server/")

def test_use_localhost():
    config = Config()
    config._use_localhost()
    
    assert config.version == ""
    assert config.auth_server == "http://localhost/aiod-auth/"
    assert config.api_server == "http://localhost/"
    
    config._use_localhost(version="v1")
    assert config.version == "v1"

@patch("aiod.configuration._config._user_config_file", new_callable=lambda: MagicMock(spec=Path))
def test_store_to_file(mock_user_config_file):
    # Mock file read to return empty TOML document
    mock_user_config_file.read_text.return_value = ""
    
    config = Config()
    config.api_server = "http://test-server/"
    
    config._store_to_file("api_server")
    
    mock_user_config_file.write_text.assert_called_once()
    write_args = mock_user_config_file.write_text.call_args[0][0]
    
    # Verify the written content contains the updated api_server
    assert 'api_server = "http://test-server/"' in write_args

def test_store_to_file_invalid_attribute():
    config = Config()
    with pytest.raises(AttributeError):
        config._store_to_file("nonexistent_attribute")

def test_load_configuration(tmp_path):
    config_file = tmp_path / "config.toml"
    config_content = """
    api_server = "https://custom.api/"
    version = "v3"
    request_timeout_seconds = 20
    """
    config_file.write_text(config_content)
    
    # This modifies the global config inside the module
    loaded_config = load_configuration(config_file)
    
    assert loaded_config.api_server == "https://custom.api/"
    assert loaded_config.version == "v3"
    assert loaded_config.request_timeout_seconds == 20

def test_load_configuration_parse_error(tmp_path):
    config_file = tmp_path / "config.toml"
    # Invalid TOML content
    config_content = """
    api_server = "https://custom.api/"
    version : "v3"  # invalid syntax
    """
    config_file.write_text(config_content)
    
    with pytest.raises(tomlkit.exceptions.ParseError):
        load_configuration(config_file)
