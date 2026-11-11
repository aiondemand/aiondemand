"""Regression tests for configuration error handling across Python versions."""

import pytest
from tomlkit.exceptions import ParseError

from aiod.configuration._config import load_configuration

# Regression for https://github.com/aiondemand/aiondemand/issues/272.


def test_config_parse_error_is_preserved(tmp_path):
    """Malformed TOML must raise its parse error, including on Python 3.10."""
    config_file = tmp_path / "config.toml"
    config_file.write_text('version : "v3"\n')

    with pytest.raises(ParseError) as caught:
        load_configuration(config_file)

    assert caught.value.line == 1
    assert "Unexpected character" in str(caught.value)


@pytest.mark.skipif(
    not hasattr(Exception, "add_note"), reason="exception notes require Python 3.11"
)
def test_config_parse_error_retains_diagnostic_note(tmp_path):
    """Newer Python versions still report the file, source line, and caret."""
    config_file = tmp_path / "config.toml"
    config_file.write_text('version = "v2"\nrequest_timeout_seconds : 10\n')

    with pytest.raises(ParseError) as caught:
        load_configuration(config_file)

    note = caught.value.__notes__[0]
    assert str(config_file) in note
    assert "line 2:" in note
    assert "request_timeout_seconds : 10" in note
    assert "^" in note
