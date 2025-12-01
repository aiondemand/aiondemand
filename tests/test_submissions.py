"""Tests for submission management functionality."""

import pytest
import responses

from aiod import submissions
from aiod.authentication import NotAuthenticatedError


class TestSubmissions:
    """Test submission management functions."""

    @responses.activate
    def test_submit_single_asset(self, valid_refresh_token):
        """Test submitting a single asset for review."""
        # Mock the submission endpoint
        responses.add(
            responses.POST,
            "http://not.set/not_set/submissions",
            json={"identifier": 42, "request_date": "2025-11-29T10:00:00"},
            status=200,
        )

        submission_id = submissions.submit_for_review("data_abc123")
        assert submission_id == 42

        # Verify request body
        request_body = responses.calls[-1].request.body.decode()
        assert '"asset_identifiers": ["data_abc123"]' in request_body
        assert '"comment": ""' in request_body

    @responses.activate
    def test_submit_multiple_assets(self, valid_refresh_token):
        """Test submitting multiple assets together."""
        responses.add(
            responses.POST,
            "http://not.set/not_set/submissions",
            json={"identifier": 43},
            status=200,
        )

        asset_ids = ["data_abc123", "data_def456", "data_ghi789"]
        submission_id = submissions.submit_for_review(asset_ids)
        assert submission_id == 43

        request_body = responses.calls[-1].request.body
        assert "data_abc123" in request_body.decode()
        assert "data_def456" in request_body.decode()
        assert "data_ghi789" in request_body.decode()

    @responses.activate
    def test_submit_with_comment(self, valid_refresh_token):
        """Test submitting with a reviewer comment."""
        responses.add(
            responses.POST,
            "http://not.set/not_set/submissions",
            json={"identifier": 44},
            status=200,
        )

        comment = "Fixed typos in description fields"
        submission_id = submissions.submit_for_review("data_abc123", comment=comment)
        assert submission_id == 44

        request_body = responses.calls[-1].request.body
        assert comment in request_body.decode()

    def test_submit_comment_too_long(self, valid_refresh_token):
        """Test that overly long comments are rejected."""
        long_comment = "x" * 257  # Max is 256
        with pytest.raises(ValueError, match="256 characters"):
            submissions.submit_for_review("data_abc123", comment=long_comment)

    def test_submit_requires_authentication(self, no_token):
        """Test that submission requires authentication."""
        with pytest.raises(NotAuthenticatedError):
            submissions.submit_for_review("data_abc123")

    @responses.activate
    def test_retract_submission(self, valid_refresh_token):
        """Test retracting a submission."""
        responses.add(
            responses.POST,
            "http://not.set/not_set/submissions/retract/42",
            json={},
            status=200,
        )

        response = submissions.retract_submission(42)
        assert response.status_code == 200

    def test_retract_requires_authentication(self, no_token):
        """Test that retraction requires authentication."""
        with pytest.raises(NotAuthenticatedError):
            submissions.retract_submission(42)

    @responses.activate
    def test_list_submissions_default(self, valid_refresh_token):
        """Test listing submissions with default parameters."""
        mock_submissions = [
            {
                "identifier": 1,
                "request_date": "2025-11-29T10:00:00",
                "comment": "First submission",
            },
            {
                "identifier": 2,
                "request_date": "2025-11-29T11:00:00",
                "comment": "Second submission",
            },
        ]

        responses.add(
            responses.GET,
            "http://not.set/not_set/submissions?mode=newest",
            json=mock_submissions,
            status=200,
        )

        result = submissions.list_submissions()
        assert len(result) == 2
        assert result.iloc[0]["identifier"] == 1
        assert result.iloc[1]["identifier"] == 2

    @responses.activate
    def test_list_submissions_modes(self, valid_refresh_token):
        """Test different filter modes for listing submissions."""
        for mode in ["oldest", "newest", "all", "pending", "completed"]:
            responses.add(
                responses.GET,
                f"http://not.set/not_set/submissions?mode={mode}",
                json=[],
                status=200,
            )

        for mode in ["oldest", "newest", "all", "pending", "completed"]:
            result = submissions.list_submissions(mode=mode)
            assert len(result) == 0

    @responses.activate
    def test_list_submissions_json_format(self, valid_refresh_token):
        """Test listing submissions in JSON format."""
        mock_submissions = [{"identifier": 1, "request_date": "2025-11-29T10:00:00"}]

        responses.add(
            responses.GET,
            "http://not.set/not_set/submissions?mode=newest",
            json=mock_submissions,
            status=200,
        )

        result = submissions.list_submissions(data_format="json")
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["identifier"] == 1

    def test_list_requires_authentication(self, no_token):
        """Test that listing submissions requires authentication."""
        with pytest.raises(NotAuthenticatedError):
            submissions.list_submissions()
