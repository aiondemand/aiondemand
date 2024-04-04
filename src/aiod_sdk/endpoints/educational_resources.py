from aiod_sdk.endpoints.endpoint import Endpoint


class EducationalResources(Endpoint):
    """
    Class for handling educational resource endpoints.

    This class provides methods to interact with educational resource endpoints,
    including retrieving lists of educational resources, fetching specific educational resources,
    and retrieving counts of educational resources.

    Inherits From:
        Endpoint: Provides base functionality for endpoint interactions.

    Attributes:
        name (str): The name of the educational resource endpoint.
        latest_version (str): The latest version of the educational resource endpoint.

    Methods:
        list(offset=0, limit=10, version=None, format='pandas') -> pd.DataFrame | dict:
            Retrieve a list of educational resources from the catalogue.

        counts(version=None, detailed=False) -> int:
            Retrieve the count of educational resources.

        get(identifier, version=None, format='pandas') -> pd.Series | dict:
            Retrieve metadata for a specific educational resource.
    """

    name = "educational_resources"
