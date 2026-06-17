"""Global get dispatch utility."""

from aiod.data._openml import _get_openml_dataset

__all__ = ["get"]


def get(id: str):
    """Retrieve model or dataset by identifier.

    For models, pass the class name directly, e.g., "RandomForestClassifier".

    For datasets, use OpenML URI format:
    - "openml://31" — OpenML dataset by ID
    - "openml://credit-g" — OpenML dataset by name

    Parameters
    ----------
    id : str
        Identifier string. Models are class names.
        OpenML datasets use "openml://<id-or-name>" format.

    Returns
    -------
    object
        For models: the model class.
        For OpenML datasets: a native openml.OpenMLDataset instance.

    Examples
    --------
    >>> clf = get("RandomForestClassifier")  # doctest: +SKIP
    >>> ds = get("openml://31")  # doctest: +SKIP
    """
    if id.startswith("openml://"):
        identifier = id.replace("openml://", "", 1)

        return _get_openml_dataset(identifier)

    from aiod.models._registry._get import get as get_model

    return get_model(id)
