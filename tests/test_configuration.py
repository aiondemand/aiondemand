import logging

from aiod.configuration import _config
from aiod.configuration._config import Config, load_configuration


def _write_config_file(tmp_path, content: str):
    config_file = tmp_path / "config.toml"
    config_file.write_text(content)
    return config_file


def test_load_configuration_warns_on_unknown_key(tmp_path, caplog, monkeypatch):
    """Unknown keys in the config TOML are ignored with a warning. See #245."""
    monkeypatch.setattr(_config, "config", Config())
    config_file = _write_config_file(
        tmp_path,
        'api_server = "http://test-server/"\napi_sever = "http://typo/"\n',
    )
    with caplog.at_level(logging.WARNING):
        load_configuration(config_file)
    assert _config.config.api_server == "http://test-server/"
    assert not hasattr(_config.config, "api_sever")
    assert any(
        "api_sever" in record.getMessage() and record.levelno == logging.WARNING
        for record in caplog.records
    )


def test_load_configuration_accepts_known_keys_without_warning(
    tmp_path, caplog, monkeypatch
):
    """Valid configuration keys load silently. See #245."""
    monkeypatch.setattr(_config, "config", Config())
    config_file = _write_config_file(
        tmp_path, 'api_server = "http://test-server/"\nversion = "v2"\n'
    )
    with caplog.at_level(logging.WARNING):
        load_configuration(config_file)
    assert _config.config.api_server == "http://test-server/"
    assert _config.config.version == "v2"
    assert not caplog.records
