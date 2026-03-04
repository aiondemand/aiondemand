"""Model retrieval utility for classes and objects."""


def get(id: str):
    """Retrieve model object with unique identifier.

    Parameter
    ---------
    id : str
        unique identifier of object to retrieve

    Returns
    -------
    object or class
        retrieved object

    Raises
    ------
    ModuleNotFoundError
        if dependencies of object to retrieve are not satisfied
    """
    from aiod.models._registry._craft import craft

    # todo: add logic for dependency checking
    return craft(id)
