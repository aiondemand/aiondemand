from aiod_sdk.endpoints.endpoint import Endpoint


class MLModels(Endpoint):
    """
    Class for handling ML model endpoints.

    This class provides methods to interact with ML model endpoints,
    including retrieving lists of ML models, fetching specific ML models,
    and retrieving counts of ML models.

    Inherits From:
        Endpoint: Provides base functionality for endpoint interactions.

    Attributes:
        name (str): The name of the ML model endpoint.
        latest_version (str): The latest version of the ML model endpoint.

    Methods:
        list(offset=0, limit=10, version=None, format='pandas') -> pd.DataFrame | dict:
            Retrieve a list of ML models from the catalogue.

        counts(version=None, detailed=False) -> int:
            Retrieve the count of ML models.

        get(identifier, version=None, format='pandas') -> pd.Series | dict:
            Retrieve metadata for a specific ML model.
    """

    name = "ml_models"
