"""OpenML dataset dispatcher."""


def _get_openml_dataset(identifier):
    """Get an OpenML dataset by ID or name.

    Parameters
    ----------
    identifier : str or int
        OpenML dataset ID (integer) or name (string).
        Examples: 31, "credit-g"

    Returns
    -------
    openml.OpenMLDataset
        A native OpenML dataset object.

    Raises
    ------
    ImportError
        If openml-python is not installed.
    Exception
        If the identifier is invalid or dataset not found.
    """
    import openml

    return openml.datasets.get_dataset(identifier)
