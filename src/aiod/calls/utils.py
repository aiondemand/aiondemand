from collections.abc import Callable
from functools import partial, update_wrapper
from typing import Literal

import asyncio
import pandas as pd
import requests
import aiohttp
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from aiod.configuration import config


def get_requests_session() -> requests.Session:
    """Create a requests Session with automatic retries."""
    session = requests.Session()
    retry_strategy = Retry(
        total=config.retry_total,
        backoff_factor=config.retry_backoff_factor,
        status_forcelist=config.retry_status_forcelist,
        allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


async def robust_request(session: aiohttp.ClientSession, method: str, url: str, **kwargs):
    """Perform an async request with automatic retries."""
    for attempt in range(config.retry_total + 1):
        try:
            async with session.request(method, url, **kwargs) as response:
                if response.status in config.retry_status_forcelist:
                    if attempt < config.retry_total:
                        sleep_time = config.retry_backoff_factor * (2**attempt)
                        await asyncio.sleep(sleep_time)
                        continue
                    else:
                        return await response.json()
                return await response.json()
        except aiohttp.ClientError:
            if attempt < config.retry_total:
                sleep_time = config.retry_backoff_factor * (2**attempt)
                await asyncio.sleep(sleep_time)
            else:
                raise


def format_response(response: list | dict, data_format: Literal["pandas", "json"]) -> pd.Series | pd.DataFrame | dict | list:
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
    elif data_format == "json" and (isinstance(response, dict) or isinstance(response, list)):
        return response

    raise Exception(f"Format: {data_format} invalid or not supported for responses of {type(response)=}.")


def wrap_calls(asset_type: str, calls: list[Callable], module: str) -> tuple[Callable, ...]:
    wrapper_list = []
    for wrapped in calls:
        wrapper: Callable = partial(wrapped, asset_type=asset_type)
        wrapper = update_wrapper(wrapper, wrapped)
        wrapper.__doc__ = wrapped.__doc__.replace("ASSET_TYPE", asset_type) if wrapped.__doc__ is not None else ""
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
