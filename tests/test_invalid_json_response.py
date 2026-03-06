import requests
import pytest
from unittest.mock import patch, Mock

from aiod.calls.calls import get_list


@patch("requests.get")
def test_get_list_invalid_json(mock_get):
    mock_response = Mock()
    mock_response.status_code = 502
    mock_response.text = "Bad Gateway"
    mock_response.json.side_effect = requests.exceptions.JSONDecodeError(
        "Expecting value", "", 0
    )

    mock_get.return_value = mock_response

    with pytest.raises(RuntimeError):
        get_list(asset_type="datasets")