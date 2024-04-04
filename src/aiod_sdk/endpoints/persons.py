from aiod_sdk.endpoints.endpoint import Endpoint


class Persons(Endpoint):
    """
    Class for handling person endpoints.

    This class provides methods to interact with person endpoints,
    including retrieving lists of persons, fetching specific persons,
    and retrieving counts of persons.

    Inherits From:
        Endpoint: Provides base functionality for endpoint interactions.

    Attributes:
        name (str): The name of the person endpoint.
        latest_version (str): The latest version of the person endpoint.

    Methods:
        list(offset=0, limit=10, version=None, format='pandas') -> pd.DataFrame | dict:
            Retrieve a list of persons from the catalogue.

        counts(version=None, detailed=False) -> int:
            Retrieve the count of persons.

        get(identifier, version=None, format='pandas') -> pd.Series | dict:
            Retrieve metadata for a specific person.
    """

    name = "persons"
