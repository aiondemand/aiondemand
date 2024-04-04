from aiod_sdk.endpoints.endpoint import Endpoint


class CaseStudies(Endpoint):
    """
    Class for handling case studies endpoints.

    This class provides methods to interact with case studies endpoints,
    including retrieving lists of case studies, fetching specific case studies,
    and retrieving counts of case studies.

    Inherits From:
        Endpoint: Provides base functionality for endpoint interactions.

    Attributes:
        name (str): The name of the dataset endpoint.
        latest_version (str): The latest version of the dataset endpoint.

    Methods:
        list(offset=0, limit=10, version=None, format='pandas') -> pd.DataFrame | dict:
            Retrieve a list of case studies from the catalogue.

        counts(version=None, detailed=False) -> int:
            Retrieve the count of case studies.

        get(identifier, version=None, format='pandas') -> pd.Series | dict:
            Retrieve metadata for a specific dataset.
    """

    name = "case_studies"
