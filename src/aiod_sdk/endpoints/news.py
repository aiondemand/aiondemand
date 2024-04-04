from aiod_sdk.endpoints.endpoint import Endpoint


class News(Endpoint):
    """
    Class for handling news endpoints.

    This class provides methods to interact with news endpoints,
    including retrieving lists of news, fetching specific news,
    and retrieving counts of news.

    Inherits From:
        Endpoint: Provides base functionality for endpoint interactions.

    Attributes:
        name (str): The name of the news endpoint.
        latest_version (str): The latest version of the news endpoint.

    Methods:
        list(offset=0, limit=10, version=None, format='pandas') -> pd.DataFrame | dict:
            Retrieve a list of news from the catalogue.

        counts(version=None, detailed=False) -> int:
            Retrieve the count of news.

        get(identifier, version=None, format='pandas') -> pd.Series | dict:
            Retrieve metadata for a specific news.
    """

    name = "news"
