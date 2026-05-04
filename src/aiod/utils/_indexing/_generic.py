"""Generic utility for indexing objects by API contract."""

from skbase.lookup import all_objects


def get_contract_inhabitants(
    contract_class,
    package_name: str,
    object_types: object = object,
    modules_to_ignore: list = None,
    return_names: bool = True,
    as_dataframe: bool = False,
    suppress_import_stdout: bool = True,
):
    """
    Find all objects in a given package that conform to an API contract.

    Parameters
    ----------
    contract_class : class
        A contract class inheriting from `_BaseContract` (implements `istypeof`).
    package_name : str
        The package to scan (e.g., 'sklearn', 'sktime', 'xgboost').
    object_types : type or tuple of types, optional (default=object)
        The type(s) of objects to consider during the scan (e.g., `object`,
    modules_to_ignore : list of str, optional
        Modules within the package to skip during the scan.
    return_names : bool, default=True
        Whether to return object names. Only used if as_dataframe is False.
    as_dataframe : bool, default=False
        Whether to return the results as a pandas DataFrame.
    suppress_import_stdout : bool, default=True
        Whether to suppress stdout printout upon import.

    Returns
    -------
    list, tuple, or pd.DataFrame
        Objects satisfying the contract in the requested format.
    """
    # Fetch all objects from the package
    all_package_objects = all_objects(
        package_name=package_name,
        object_types=object_types,
        return_names=return_names,
        as_dataframe=as_dataframe,
        modules_to_ignore=modules_to_ignore,
        suppress_import_stdout=suppress_import_stdout,
    )
    # Filter the objects using the contract
    if as_dataframe:
        mask = all_package_objects["object"].apply(contract_class.istypeof)
        return all_package_objects[mask]

    # Filter for list/tuple return
    valid_inhabitants = [
        (name, obj) if return_names else obj
        for name, obj in all_package_objects
        if contract_class.istypeof(obj)
    ]

    return valid_inhabitants
