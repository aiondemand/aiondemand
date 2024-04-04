from aiod_sdk.endpoints.endpoint import Endpoint


class Teams(Endpoint):
    """
    Class for handling team endpoints.

    This class provides methods to interact with team endpoints,
    including retrieving lists of teams, fetching specific teams,
    and retrieving counts of teams.

    Inherits From:
        Endpoint: Provides base functionality for endpoint interactions.

    Attributes:
        name (str): The name of the team endpoint.
        latest_version (str): The latest version of the team endpoint.

    Methods:
        list(offset=0, limit=10, version=None, format='pandas') -> pd.DataFrame | dict:
            Retrieve a list of teams from the catalogue.

        counts(version=None, detailed=False) -> int:
            Retrieve the count of teams.

        get(identifier, version=None, format='pandas') -> pd.Series | dict:
            Retrieve metadata for a specific team.
    """

    name = "teams"
