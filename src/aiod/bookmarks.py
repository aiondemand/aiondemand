import datetime as dt
from dataclasses import dataclass
from http import HTTPStatus

import requests

from aiod.authentication import get_token
from aiod.calls.urls import server_url
from aiod.calls.utils import ServerError


@dataclass
class Bookmark:
    """Reference to an asset on AI-on-Demand.

    Attributes
    ----------
    identifier: str
        The identifier of the asset on AI-on-Demand, e.g., 'data_xyz...'
    created: datetime.datetime
        The datetime when the bookmark was originally created.
    """

    identifier: str
    created: dt.datetime


def _bookmarks_url() -> str:
    return server_url() + "bookmarks"


def register(identifier: str) -> Bookmark:
    """Bookmark the asset with `identifier` for the user.

    Parameters
    ----------
    identifier:
        The identifier of the asset on AI-on-Demand, e.g., 'data_xyz...'

    Returns
    -------
    :
        A `Bookmark` that denotes the time the bookmark was created.

    Raises
    ------
    KeyError
        If the identifier is not recognized by AI-on-Demand.
    ServerError
        If any other server-side error occurs.
    """
    res = requests.post(
        _bookmarks_url(),
        params=dict(resource_identifier=identifier),
        headers=get_token().headers,
    )
    if res.status_code == HTTPStatus.NOT_FOUND:
        raise KeyError(f"Could not find asset with identifier {identifier!r}.")
    if res.status_code != HTTPStatus.OK:
        raise ServerError(res)

    return Bookmark(
        identifier=res.json()["resource_identifier"],
        created=dt.datetime.fromisoformat(res.json()["created_at"]).replace(
            tzinfo=dt.UTC
        ),
    )


def delete(identifier: str):
    """Remove the bookmark for the asset with `identifier` for the user.

    This method does not raise an error if the identifier is not recognized by AI-on-Demand,
    or if the identifier is valid but the user has not bookmarked it.

    Parameters
    ----------
    identifier:
        The identifier of the asset on AI-on-Demand, e.g., 'data_xyz...'


    Raises
    ------
    ServerError
        If any other server-side error occurs.
    """
    res = requests.delete(
        _bookmarks_url(),
        params=dict(resource_identifier=identifier),
        headers=get_token().headers,
    )
    # The delete endpoint does not error if the bookmark does not exist
    if res.status_code != HTTPStatus.OK:
        raise ServerError(res)


def get_list() -> list[Bookmark]:
    """Return a list of the user's bookmarks.

    Returns
    -------
    :
        The list of bookmarks.
    """
    res = requests.get(
        _bookmarks_url(),
        headers=get_token().headers,
    )
    if res.status_code != HTTPStatus.OK:
        raise ServerError(res)
    return [
        Bookmark(
            identifier=bookmark["resource_identifier"],
            created=dt.datetime.fromisoformat(bookmark["created_at"]).replace(
                tzinfo=dt.UTC
            ),
        )
        for bookmark in res.json()
    ]
