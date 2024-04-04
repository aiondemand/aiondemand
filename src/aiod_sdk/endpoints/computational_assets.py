from aiod_sdk.endpoints.endpoint import Endpoint


class ComputationalAssets(Endpoint):
    """
    Class for handling computational asset endpoints.

    This class provides methods to interact with computational asset endpoints,
    including retrieving lists of computational assets, fetching specific computational assets,
    and retrieving counts of computational assets.

    Inherits From:
        Endpoint: Provides base functionality for endpoint interactions.

    Attributes:
        name (str): The name of the computational asset endpoint.
        latest_version (str): The latest version of the computational asset endpoint.

    Methods:
        list(offset=0, limit=10, version=None, format='pandas') -> pd.DataFrame | dict:
            Retrieve a list of computational assets from the catalogue.

        counts(version=None, detailed=False) -> int:
            Retrieve the count of computational assets.

        get(identifier, version=None, format='pandas') -> pd.Series | dict:
            Retrieve metadata for a specific computational asset.
    """

    name = "computational_assets"
