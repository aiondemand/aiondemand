"""Tests for review functionality."""

import pytest
import responses

from aiod import reviews
from aiod.authentication import NotAuthenticatedError


class TestReviews:
    """Test review functions."""

    @responses.activate
    def test_create_review_accept(self, valid_refresh_token):
        """Test creating an approval review."""
        mock_review = {
            "identifier": 1,
            "submission_identifier": 42,
            "decision": "accepted",
            "comment": "Looks good!",
            "decision_date": "2025-11-29T10:00:00",
            "reviewer_identifier": "user_reviewer123",
        }

        responses.add(
            responses.POST,
            "http://not.set/not_set/reviews",
            json=mock_review,
            status=200,
        )

        result = reviews.create_review(
            submission_identifier=42,
            decision="accepted",
            comment="Looks good!",
            data_format="json",
        )

        assert result["identifier"] == 1
        assert result["decision"] == "accepted"
        assert result["submission_identifier"] == 42

        # Verify request body
        request_body = responses.calls[-1].request.body.decode()
        assert '"submission_identifier": 42' in request_body
        assert '"decision": "accepted"' in request_body
        assert "Looks good!" in request_body

    @responses.activate
    def test_create_review_reject(self, valid_refresh_token):
        """Test creating a rejection review."""
        mock_review = {
            "identifier": 2,
            "submission_identifier": 43,
            "decision": "rejected",
            "comment": "Please fix the license field",
            "decision_date": "2025-11-29T10:00:00",
            "reviewer_identifier": "user_reviewer123",
        }

        responses.add(
            responses.POST,
            "http://not.set/not_set/reviews",
            json=mock_review,
            status=200,
        )

        result = reviews.create_review(
            submission_identifier=43,
            decision="rejected",
            comment="Please fix the license field",
            data_format="json",
        )

        assert result["decision"] == "rejected"
        assert result["submission_identifier"] == 43

    @responses.activate
    def test_create_review_retracted(self, valid_refresh_token):
        """Test creating a retracted review."""
        mock_review = {
            "identifier": 3,
            "submission_identifier": 44,
            "decision": "retracted",
            "comment": "",
            "decision_date": "2025-11-29T10:00:00",
            "reviewer_identifier": "user_reviewer123",
        }

        responses.add(
            responses.POST,
            "http://not.set/not_set/reviews",
            json=mock_review,
            status=200,
        )

        result = reviews.create_review(
            submission_identifier=44, decision="retracted", data_format="json"
        )

        assert result["decision"] == "retracted"

    @responses.activate
    def test_create_review_pandas_format(self, valid_refresh_token):
        """Test creating a review with pandas format."""
        mock_review = {
            "identifier": 4,
            "submission_identifier": 45,
            "decision": "accepted",
            "comment": "",
            "decision_date": "2025-11-29T10:00:00",
            "reviewer_identifier": "user_reviewer123",
        }

        responses.add(
            responses.POST,
            "http://not.set/not_set/reviews",
            json=mock_review,
            status=200,
        )

        result = reviews.create_review(
            submission_identifier=45, decision="accepted", data_format="pandas"
        )

        # Should return a Series
        assert result["identifier"] == 4
        assert result["decision"] == "accepted"

    def test_create_review_invalid_decision(self, valid_refresh_token):
        """Test that invalid decisions are rejected."""
        with pytest.raises(ValueError, match="Decision must be one of"):
            reviews.create_review(
                submission_identifier=42,
                decision="maybe",  # Invalid
            )

    def test_create_review_comment_too_long(self, valid_refresh_token):
        """Test that overly long comments are rejected."""
        long_comment = "x" * 1801  # Max is 1800
        with pytest.raises(ValueError, match="1800 characters"):
            reviews.create_review(
                submission_identifier=42, decision="accepted", comment=long_comment
            )

    def test_create_review_requires_authentication(self, no_token):
        """Test that creating a review requires authentication."""
        with pytest.raises(NotAuthenticatedError):
            reviews.create_review(submission_identifier=42, decision="accepted")

    @responses.activate
    def test_create_review_without_comment(self, valid_refresh_token):
        """Test creating a review without a comment."""
        mock_review = {
            "identifier": 5,
            "submission_identifier": 46,
            "decision": "accepted",
            "comment": "",
            "decision_date": "2025-11-29T10:00:00",
            "reviewer_identifier": "user_reviewer123",
        }

        responses.add(
            responses.POST,
            "http://not.set/not_set/reviews",
            json=mock_review,
            status=200,
        )

        result = reviews.create_review(
            submission_identifier=46, decision="accepted", data_format="json"
        )

        assert result["comment"] == ""

        # Verify request body has empty comment
        request_body = responses.calls[-1].request.body.decode()
        assert '"comment": ""' in request_body
