from aiod_sdk.endpoints.endpoint import Endpoint


class Events(Endpoint):
    """
    Class for handling event endpoints.

    This class provides methods to interact with event endpoints,
    including retrieving lists of events, fetching specific events,
    and retrieving counts of events.

    Inherits From:
        Endpoint: Provides base functionality for endpoint interactions.

    Attributes:
        name (str): The name of the event endpoint.
        latest_version (str): The latest version of the event endpoint.

    Methods:
        list(offset=0, limit=10, version=None, format='pandas') -> pd.DataFrame | dict:
            Retrieve a list of events from the catalogue.

        counts(version=None, detailed=False) -> int:
            Retrieve the count of events.

        get(identifier, version=None, format='pandas') -> pd.Series | dict:
            Retrieve metadata for a specific event.
    """

    name = "events"
