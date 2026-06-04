from dataclasses import dataclass
from datetime import datetime, timezone

from aiod._client import AiodNotFoundError, client
from aiod.calls.urls import server_url


@dataclass
class Bookmark:
    """Reference to an asset on AI-on-Demand.

    Attributes
    ----------
    identifier: str
        The identifier of the asset on AI-on-Demand, e.g., 'data_xyz...'
    created: datetime
        The datetime when the bookmark was originally created.
    """

    identifier: str
    created: datetime


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
    try:
        res = client.post(
            _bookmarks_url(),
            params={"resource_identifier": identifier},
        )
    except AiodNotFoundError:
        raise KeyError(f"Could not find asset with identifier {identifier!r}.")

    return Bookmark(
        identifier=res.json()["resource_identifier"],
        created=datetime.fromisoformat(res.json()["created_at"]).replace(
            tzinfo=timezone.utc
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
    client.delete(
        _bookmarks_url(),
        params={"resource_identifier": identifier},
    )
    # The delete endpoint does not error if the bookmark does not exist


def get_list() -> list[Bookmark]:
    """Return a list of the user's bookmarks.

    Returns
    -------
    :
        The list of bookmarks.
    """
    res = client.get(_bookmarks_url())
    return [
        Bookmark(
            identifier=bookmark["resource_identifier"],
            created=datetime.fromisoformat(bookmark["created_at"]).replace(
                tzinfo=timezone.utc
            ),
        )
        for bookmark in res.json()
    ]
