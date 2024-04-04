from aiod_sdk.endpoints.endpoint import Endpoint


class Services(Endpoint):
    """
    Class for handling service endpoints.

    This class provides methods to interact with service endpoints,
    including retrieving lists of services, fetching specific services,
    and retrieving counts of services.

    Inherits From:
        Endpoint: Provides base functionality for endpoint interactions.

    Attributes:
        name (str): The name of the service endpoint.
        latest_version (str): The latest version of the service endpoint.

    Methods:
        list(offset=0, limit=10, version=None, format='pandas') -> pd.DataFrame | dict:
            Retrieve a list of services from the catalogue.

        counts(version=None, detailed=False) -> int:
            Retrieve the count of services.

        get(identifier, version=None, format='pandas') -> pd.Series | dict:
            Retrieve metadata for a specific service.
    """

    name = "services"
