from aiod_sdk.endpoints.endpoint import Endpoint


class Publications(Endpoint):
    """
    Class for handling publication endpoints.

    This class provides methods to interact with publication endpoints,
    including retrieving lists of publications, fetching specific publications,
    and retrieving counts of publications.

    Inherits From:
        Endpoint: Provides base functionality for endpoint interactions.

    Attributes:
        name (str): The name of the publication endpoint.
        latest_version (str): The latest version of the publication endpoint.

    Methods:
        list(offset=0, limit=10, version=None, format='pandas') -> pd.DataFrame | dict:
            Retrieve a list of publications from the catalogue.

        counts(version=None, detailed=False) -> int:
            Retrieve the count of publications.

        get(identifier, version=None, format='pandas') -> pd.Series | dict:
            Retrieve metadata for a specific publication.
    """

    name = "publications"
