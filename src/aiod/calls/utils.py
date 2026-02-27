import pandas as pd

from functools import partial, update_wrapper
from typing import Callable, Literal, Tuple

import requests


def format_response(
    response: list | dict, data_format: Literal["pandas", "json"]
) -> pd.Series | pd.DataFrame | dict | list:
    """Format the response data based on the specified format.

    Parameters
    ----------
        response (list | dict): The response data to format.
        data_format (Literal["pandas", "json"]): The desired format for the response.
            For "json" formats, the returned type is a json decoded type, i.e. a dict or a list.

    Returns
    -------
        pd.Series | pd.DataFrame | dict: The formatted response data.

    Raises
    ------
        Exception: If the specified format is invalid or not supported.
    """
    if data_format == "pandas":
        if isinstance(response, dict):
            return pd.Series(response)
        if isinstance(response, list):
            return pd.DataFrame(response)
    elif data_format == "json" and (
        isinstance(response, dict) or isinstance(response, list)
    ):
        return response

    raise Exception(
        f"Format: {data_format} invalid or not supported for responses of {type(response)=}."
    )

class EndpointUndefinedError(Exception):
    """Raised when a function tries to connect to an endpoint that does not exist."""

    pass


class ServerError(RuntimeError):
    """Raised for any server error that does not (yet) have better client-side handling."""

    def __init__(self, response: requests.Response):
        self.status_code = response.status_code
        self.detail = response.json().get("detail")
        self.reference = response.json().get("reference")
        self._response = response
