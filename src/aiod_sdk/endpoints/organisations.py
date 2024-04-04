from aiod_sdk.endpoints.endpoint import Endpoint


class Organisations(Endpoint):
    """
    Class for handling organisation endpoints.

    This class provides methods to interact with organisation endpoints,
    including retrieving lists of organisations, fetching specific organisations,
    and retrieving counts of organisations.

    Inherits From:
        Endpoint: Provides base functionality for endpoint interactions.

    Attributes:
        name (str): The name of the organisation endpoint.
        latest_version (str): The latest version of the organisation endpoint.

    Methods:
        list(offset=0, limit=10, version=None, format='pandas') -> pd.DataFrame | dict:
            Retrieve a list of organisations from the catalogue.

        counts(version=None, detailed=False) -> int:
            Retrieve the count of organisations.

        get(identifier, version=None, format='pandas') -> pd.Series | dict:
            Retrieve metadata for a specific organisation.
    """

    name = "organisations"
