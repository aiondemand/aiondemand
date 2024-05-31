import pandas as pd

from functools import partial, update_wrapper
from typing import Callable, Literal, Tuple


def format_response(
    response: list | dict, data_format: Literal["pandas", "json"]
) -> pd.Series | pd.DataFrame | dict | list:
    """
    Format the response data based on the specified format.

    Parameters:
        response (list | dict): The response data to format.
        data_format (Literal["pandas", "json"]): The desired format for the response.
            For "json" formats, the returned type is a json decoded type, i.e. a dict or a list.

    Returns:
        pd.Series | pd.DataFrame | dict: The formatted response data.

    Raises:
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


def wrap_calls(asset_type: str, calls: list[Callable], module: str) -> Tuple[Callable, ...]:
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
