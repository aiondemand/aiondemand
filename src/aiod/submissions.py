"""Functions for managing asset submissions for editorial review."""

from http import HTTPStatus
from typing import Literal

import pandas as pd
import requests

from aiod.authentication.authentication import get_token
from aiod.calls.urls import url_to_retract_submission, url_to_submissions
from aiod.calls.utils import format_response, ServerError
from aiod.configuration import config


def submit_for_review(
    asset_identifiers: list[str] | str,
    *,
    comment: str = "",
    version: str | None = None,
) -> int:
    """Submit one or more assets for editorial review.

    Before assets can be published on the AI-on-Demand platform, they must
    be reviewed and approved by an editor. This function submits assets for
    that review process.
    """
    # Normalize input to list
    if isinstance(asset_identifiers, str):
        asset_identifiers = [asset_identifiers]

    # Validate comment length
    if len(comment) > 256:
        raise ValueError("Comment must be 256 characters or less")

    payload = {"asset_identifiers": asset_identifiers, "comment": comment}

    url = url_to_submissions(version)
    res = requests.post(
        url,
        headers=get_token().headers,
        json=payload,
        timeout=config.request_timeout_seconds,
    )

    if res.status_code != HTTPStatus.OK:
        raise ServerError(res)

    # API returns submission object with identifier
    return res.json()["identifier"]


def retract_submission(
    submission_identifier: int,
    *,
    version: str | None = None,
) -> requests.Response:
    """Retract a submission that is under review.

    This sets the submission status back to 'draft', removing it from the
    reviewer's queue. The asset remains in your account but is not published.
    """
    url = url_to_retract_submission(submission_identifier, version)
    res = requests.post(
        url,
        headers=get_token().headers,
        timeout=config.request_timeout_seconds,
    )

    if res.status_code != HTTPStatus.OK:
        raise ServerError(res)

    return res


def list_submissions(
    *,
    mode: Literal["oldest", "newest", "all", "pending", "completed"] = "newest",
    version: str | None = None,
    data_format: Literal["pandas", "json"] = "pandas",
) -> pd.DataFrame | list[dict]:
    """List your submissions for review.

    View all assets you've submitted for editorial review, along with their
    status and any reviewer comments.
    """
    url = url_to_submissions(version)
    params = {"mode": mode}

    res = requests.get(
        url,
        headers=get_token().headers,
        params=params,
        timeout=config.request_timeout_seconds,
    )

    if res.status_code != HTTPStatus.OK:
        raise ServerError(res)

    return format_response(res.json(), data_format)
