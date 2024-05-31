import pandas as pd
import requests
from typing import Literal

from aiod.configuration import config


def asset_counts(
    version: str | None = None, data_format: Literal["pandas", "json"] = "pandas"
) -> pd.DataFrame | dict:
    """
    Retrieve counts of assets.

    This method sends a GET request to the counts endpoint to retrieve counts of assets.

    Parameters:
        version (str | None): The version of the counts endpoint (default is None).
        format (Literal["pandas", "json"]): The desired format for the response (default is "pandas").
            For "json" format, the returned type is a json decoded type, in this case a dict.

    Returns:
        pd.DataFrame | dict: Counts as a Pandas data frame or a dictionary.
    """
    version = version or config.version
    url = f"{config.api_base_url}counts"
    if version:
        url += "/" + version

    res = requests.get(url)

    if data_format == "pandas":
        return pd.DataFrame(res.json())
    elif data_format == "json" and isinstance(res.json(), dict):
        return res.json()

    raise Exception(
        f"Format: {data_format} invalid or not supported for responses of {type(res.json())=}."
    )
