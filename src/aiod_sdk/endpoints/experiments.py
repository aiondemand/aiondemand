from aiod_sdk.endpoints.endpoint import Endpoint


class Experiments(Endpoint):
    """
    Class for handling experiment endpoints.

    This class provides methods to interact with experiment endpoints,
    including retrieving lists of experiments, fetching specific experiments,
    and retrieving counts of experiments.

    Inherits From:
        Endpoint: Provides base functionality for endpoint interactions.

    Attributes:
        name (str): The name of the experiment endpoint.
        latest_version (str): The latest version of the experiment endpoint.

    Methods:
        list(offset=0, limit=10, version=None, format='pandas') -> pd.DataFrame | dict:
            Retrieve a list of experiments from the catalogue.

        counts(version=None, detailed=False) -> int:
            Retrieve the count of experiments.

        get(identifier, version=None, format='pandas') -> pd.Series | dict:
            Retrieve metadata for a specific experiment.
    """

    name = "experiments"
