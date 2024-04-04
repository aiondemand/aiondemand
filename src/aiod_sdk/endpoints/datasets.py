from aiod_sdk.endpoints.endpoint import Endpoint


class Datasets(Endpoint):
    """
    Class for handling dataset endpoints.

    This class provides methods to interact with dataset endpoints,
    including retrieving lists of datasets, fetching specific datasets,
    and retrieving counts of datasets.

    Inherits From:
        Endpoint: Provides base functionality for endpoint interactions.

    Attributes:
        name (str): The name of the dataset endpoint.
        latest_version (str): The latest version of the dataset endpoint.

    Methods:
        list(offset=0, limit=10, version=None, format='pandas') -> pd.DataFrame | dict:
            Retrieve a list of datasets from the catalogue.

        counts(version=None, detailed=False) -> int:
            Retrieve the count of datasets.

        get(identifier, version=None, format='pandas') -> pd.Series | dict:
            Retrieve metadata for a specific dataset.
    """

    name = "datasets"
