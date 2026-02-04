"""Functions for reviewing asset submissions."""

from http import HTTPStatus
from typing import Literal

import pandas as pd
import requests

from aiod.authentication.authentication import get_token
from aiod.calls.urls import url_to_reviews
from aiod.calls.utils import format_response, ServerError
from aiod.configuration import config


def create_review(
    submission_identifier: int,
    decision: Literal["accepted", "rejected", "retracted"],
    *,
    comment: str = "",
    version: str | None = None,
    data_format: Literal["pandas", "json"] = "pandas",
) -> pd.Series | dict:
    """Create a review for a submission (approve or reject).

    This function is typically used by editors/reviewers to approve or reject
    asset submissions. Regular users submit assets with `aiod.submissions.submit_for_review()`,
    and reviewers use this function to make editorial decisions.
    """
    # Validate comment length
    if len(comment) > 1800:
        raise ValueError("Comment must be 1800 characters or less")

    # Validate decision
    valid_decisions = ["accepted", "rejected", "retracted"]
    if decision not in valid_decisions:
        raise ValueError(f"Decision must be one of {valid_decisions}, got {decision!r}")

    payload = {
        "submission_identifier": submission_identifier,
        "decision": decision,
        "comment": comment,
    }

    url = url_to_reviews(version)
    res = requests.post(
        url,
        headers=get_token().headers,
        json=payload,
        timeout=config.request_timeout_seconds,
    )

    if res.status_code != HTTPStatus.OK:
        raise ServerError(res)

    return format_response(res.json(), data_format)
