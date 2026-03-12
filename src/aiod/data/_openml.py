"""OpenML dataset dispatcher."""


def _get_openml_dataset(identifier):
    """Get an OpenML dataset by ID or name.

    Parameters
    ----------
    identifier : str or int
        OpenML dataset ID (integer) or name (string).
        Examples: "31", "credit-g"

    Returns
    -------
    openml.OpenMLDataset
        A native OpenML dataset object.

    Raises
    ------
    ValueError
        If the identifier is invalid or dataset not found.
    """
    try:
        import openml
    except ImportError as e:
        msg = (
            "openml-python is required to load OpenML datasets. "
            "Install it with: pip install openml"
        )
        raise ImportError(msg) from e

    try:
        dataset_id = int(identifier)
        return openml.datasets.get_dataset(dataset_id)
    except ValueError:
        # Not an integer, try as a name string
        return openml.datasets.get_dataset(identifier)
