"""Tests for bug fixes in src/aiod/calls/urls.py.

Covers:
  - Issue #174: url_to_search should preserve user query casing
  - Issue #169: url_to_get_content should handle distribution_idx=0 correctly
"""

import pytest

from aiod.calls.urls import url_to_get_content, url_to_search


class TestUrlToSearchCasing:
    """Tests for Issue #174 — search queries must preserve original casing."""

    def test_mixed_case_query_preserved(self):
        """User query 'Robotics' should NOT be lowercased to 'robotics'."""
        url = url_to_search("datasets", "Robotics")
        assert "search_query=Robotics" in url

    def test_uppercase_query_preserved(self):
        """Fully uppercase queries should be preserved."""
        url = url_to_search("datasets", "NLP")
        assert "search_query=NLP" in url

    def test_lowercase_query_unchanged(self):
        """Lowercase queries should remain lowercase (no regression)."""
        url = url_to_search("datasets", "robotics")
        assert "search_query=robotics" in url

    def test_camelcase_query_preserved(self):
        """CamelCase queries should be preserved."""
        url = url_to_search("models", "TimeSeriesForecasting")
        assert "search_query=TimeSeriesForecasting" in url

    def test_query_with_spaces_preserved(self):
        """Queries with spaces should preserve casing (spaces get encoded)."""
        url = url_to_search("datasets", "Deep Learning")
        # urllib encodes spaces as + or %20, but casing must be preserved
        assert "Deep" in url and "Learning" in url

    def test_search_url_structure(self):
        """Verify the overall URL structure is correct."""
        url = url_to_search("datasets", "test")
        assert "search/datasets?" in url
        assert "search_query=test" in url

    def test_search_with_platform_filter(self):
        """Platform filters should work alongside casing preservation."""
        url = url_to_search("datasets", "MyQuery", platforms=["openml"])
        assert "search_query=MyQuery" in url
        assert "platforms=openml" in url

    def test_search_with_pagination(self):
        """Pagination params should be included correctly."""
        url = url_to_search("datasets", "Test", offset=10, limit=20)
        assert "search_query=Test" in url
        assert "offset=10" in url
        assert "limit=20" in url


class TestUrlToGetContentDistributionIdx:
    """Tests for Issue #169 — distribution_idx=0 must not be skipped."""

    def test_distribution_idx_zero_included(self):
        """distribution_idx=0 should produce '/content/0' in the URL."""
        url = url_to_get_content("datasets", "abc123", distribution_idx=0)
        assert url.endswith("/content/0"), f"Expected URL to end with /content/0, got: {url}"

    def test_distribution_idx_one(self):
        """distribution_idx=1 should produce '/content/1' (basic sanity check)."""
        url = url_to_get_content("datasets", "abc123", distribution_idx=1)
        assert url.endswith("/content/1"), f"Expected URL to end with /content/1, got: {url}"

    def test_distribution_idx_large_number(self):
        """Large distribution indices should work correctly."""
        url = url_to_get_content("datasets", "abc123", distribution_idx=99)
        assert url.endswith("/content/99"), f"Expected URL to end with /content/99, got: {url}"

    def test_content_url_structure(self):
        """Verify the overall content URL structure is correct."""
        url = url_to_get_content("datasets", "data_123", distribution_idx=0)
        assert "datasets/data_123/content/0" in url
