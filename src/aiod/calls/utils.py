import pandas as pd

from functools import partial, update_wrapper
from typing import Callable, Literal, Tuple

import requests
from aiod.resources.objects import Asset


def format_response(
    response: list | dict,
    data_format: Literal["pandas", "json", "object"],
    *,
    asset_type: str | None = None,
) -> pd.Series | pd.DataFrame | dict | list | Asset | list[Asset]:
    """Format the response data based on the specified format.

    Parameters
    ----------
        response (list | dict): The response data to format.
        data_format (Literal["pandas", "json", "object"]): The desired format for the response.
            - For "pandas", returns a Series (dict input) or DataFrame (list input).
            - For "json", returns the original decoded JSON type (dict or list).
            - For "object", returns an ``Asset`` (dict input) or list of ``Asset`` (list input).
        asset_type: Optional context to annotate ``Asset`` objects when ``data_format='object'``.

    Returns
    -------
        pd.Series | pd.DataFrame | dict | list | Asset | list[Asset]: The formatted response data.

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
    elif data_format == "object":
        if isinstance(response, dict):
            return Asset.from_dict(asset_type, response)
        if isinstance(response, list):
            return [Asset.from_dict(asset_type, item) for item in response]

    raise Exception(
        f"Format: {data_format} invalid or not supported for responses of {type(response)=}."
    )


def wrap_calls(
    asset_type: str, calls: list[Callable], module: str
) -> Tuple[Callable, ...]:
    wrapper_list = []
    for wrapped in calls:
        wrapper: Callable = partial(wrapped, asset_type=asset_type)
        wrapper = update_wrapper(wrapper, wrapped)
        wrapper.__doc__ = (
            wrapped.__doc__.replace("ASSET_TYPE", asset_type)
            if wrapped.__doc__ is not None
            else ""
        )
        wrapper.__module__ = module
        wrapper_list.append(wrapper)

    return tuple(wrapper_list)


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
