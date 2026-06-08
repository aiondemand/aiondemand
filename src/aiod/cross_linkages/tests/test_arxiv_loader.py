"""Test ArxivLoader."""

import pytest

from aiod.cross_linkages._loaders._arxiv import ArxivLoader


@pytest.fixture
def loader():
    """Create an ArxivLoader instance."""
    return ArxivLoader()


def test_extract_id_from_url_valid_abs(loader):
    """Test extracting ID from abs URL."""
    url = "https://arxiv.org/abs/1706.03762"
    assert loader._extract_id_from_url(url) == "1706.03762"


def test_load_invalid_url(loader):
    """Test load with invalid URL raises ValueError."""
    with pytest.raises(ValueError):
        loader.load(123)


def test_load_valid_url(loader):
    """Test load with valid URL returns documents."""
    url = "https://arxiv.org/abs/1706.03762"

    result = loader.load(url)

    assert isinstance(result, list)
    assert len(result) > 0

    doc = result[0]
    assert hasattr(doc, "page_content")
    assert len(doc.page_content) > 0
