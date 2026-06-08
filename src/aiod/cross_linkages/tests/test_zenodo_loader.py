"""Test ZenodoLoader."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from aiod.cross_linkages import ZenodoLoader


@pytest.fixture
def loader(tmp_path: Path):
    """Create a ZenodoLoader with a temporary download directory."""
    return ZenodoLoader(download_dir=tmp_path)


def test_extract_record_id_valid(loader):
    url = "https://zenodo.org/records/1234567"
    assert loader._extract_record_id(url) == "1234567"


def test_extract_record_id_invalid(loader):
    with pytest.raises(ValueError):
        loader._extract_record_id("https://invalid.com")


def test_get_pdf_url(loader):
    """Test API parsing for PDF URL extraction."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "files": [
            {
                "key": "paper.pdf",
                "links": {"self": "http://example.com/paper.pdf"},
            }
        ]
    }
    mock_response.raise_for_status.return_value = None

    with patch("httpx.Client.get", return_value=mock_response):
        pdf_url = loader._get_pdf_url("123")

    assert pdf_url == "http://example.com/paper.pdf"


def test_no_pdf_found(loader):
    """Ensure error is raised if no PDF exists in record."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"files": []}
    mock_response.raise_for_status.return_value = None

    with patch("httpx.Client.get", return_value=mock_response):
        with pytest.raises(ValueError):
            loader._get_pdf_url("123")
