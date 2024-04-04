from aiod_sdk.endpoints.endpoint import Endpoint


class Contacts(Endpoint):
    """
    Class for handling contact endpoints.

    This class provides methods to interact with contact endpoints,
    including retrieving lists of contacts, fetching specific contacts,
    and retrieving counts of contacts.

    Inherits From:
        Endpoint: Provides base functionality for endpoint interactions.

    Attributes:
        name (str): The name of the contact endpoint.
        latest_version (str): The latest version of the contact endpoint.

    Methods:
        list(offset=0, limit=10, version=None, format='pandas') -> pd.DataFrame | dict:
            Retrieve a list of contacts from the catalogue.

        counts(version=None, detailed=False) -> int:
            Retrieve the count of contacts.

        get(identifier, version=None, format='pandas') -> pd.Series | dict:
            Retrieve metadata for a specific contact.
    """

    name = "contacts"
