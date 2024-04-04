from aiod_sdk.endpoints.endpoint import Endpoint


class Projects(Endpoint):
    """
    Class for handling project endpoints.

    This class provides methods to interact with project endpoints,
    including retrieving lists of projects, fetching specific projects,
    and retrieving counts of projects.

    Inherits From:
        Endpoint: Provides base functionality for endpoint interactions.

    Attributes:
        name (str): The name of the project endpoint.
        latest_version (str): The latest version of the project endpoint.

    Methods:
        list(offset=0, limit=10, version=None, format='pandas') -> pd.DataFrame | dict:
            Retrieve a list of projects from the catalogue.

        counts(version=None, detailed=False) -> int:
            Retrieve the count of projects.

        get(identifier, version=None, format='pandas') -> pd.Series | dict:
            Retrieve metadata for a specific project.
    """

    name = "projects"
