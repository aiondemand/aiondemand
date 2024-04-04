from aiod_sdk.endpoints.endpoint import Endpoint


class Platforms(Endpoint):
    """
    Class for handling platform endpoints.

    This class provides methods to interact with platform endpoints,
    including retrieving lists of platforms, fetching specific platforms,
    and retrieving counts of platforms.

    Inherits From:
        Endpoint: Provides base functionality for endpoint interactions.

    Attributes:
        name (str): The name of the platform endpoint.
        latest_version (str): The latest version of the platform endpoint.

    Methods:
        list(offset=0, limit=10, version=None, format='pandas') -> pd.DataFrame | dict:
            Retrieve a list of platforms from the catalogue.

        counts(version=None, detailed=False) -> int:
            Retrieve the count of platforms.

        get(identifier, version=None, format='pandas') -> pd.Series | dict:
            Retrieve metadata for a specific platform.
    """

    name = "platforms"
