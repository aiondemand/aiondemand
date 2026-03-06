import pytest
from aiod.configuration import Config, config
def test_attribute_error_message():
    c = Config()
    with pytest.raises(AttributeError, match="Cannot store unknown attribute"):
        c._store_to_file("nonexistent_attribute")