"""Global get dispatch utility."""

__all__ = ["get"]

def get(id: str):
    """Retrieve model or dataset by identifier.

    For models, pass the class name directly, e.g., "RandomForestClassifier".

    For datasets, use pattern "source:identifier"
    ex.: "openml:31" loads OpenML dataset with ID 31

    Parameters
    ----------
    id: 
        If it contains a ":" it resolves to dataset loader.
        Otherwise, resolves as a model identifier.

    Returns
    -------
    object
        For models: the model class.
        For datasets: a dataset loader instance.
    """
    if ":" in id:
        source, identifier = id.split(":", 1)
        source = source.strip().lower()
        identifier = identifier.strip()

        if source == "openml":
            return _get_openml_dataset(identifier)
        else:
            raise ValueError(f"Unknown dataset source '{source}'. ")

    from aiod.models._registry._get import get as _model_get

    return _model_get(id)

def _get_openml_dataset(identifier):
    """Create an OpenMLDataset for the given ID."""
    from aiod.data import OpenMLDataset

    try:
        dataset_id = int(identifier)
    except ValueError:
        raise ValueError(
            f"OpenML identifier must be an integer dataset ID, got '{identifier}'."
        ) from None

    return OpenMLDataset(dataset_id=dataset_id)
