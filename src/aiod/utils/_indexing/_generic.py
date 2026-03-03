"""Generic utility for indexing objects by API contract."""

from skbase.lookup import all_objects


def get_contract_inhabitants(
    contract_class, 
    package_name: str, 
    modules_to_ignore: list = None,
    as_dataframe: bool = False,
    return_names: bool = True,
    suppress_import_stdout: bool = True
):
    """
    Find all objects in a given package that conform to an API contract.

    Parameters
    ----------
    contract_class : class
        A contract class inheriting from `_BaseContract` (implements `istypeof`).
    package_name : str
        The package to scan (e.g., 'sklearn', 'sktime', 'xgboost').
    modules_to_ignore : list of str, optional
        Modules within the package to skip during the scan.
    as_dataframe : bool, default=False
        Whether to return the results as a pandas DataFrame.
    return_names : bool, default=True
        Whether to return object names. Only used if as_dataframe is False.
    suppress_import_stdout : bool, default=True
        Whether to suppress stdout printout upon import.

    Returns
    -------
    list, tuple, or pd.DataFrame
        Objects satisfying the contract in the requested format.
    """
    # 1. Fetch all objects from the package
    all_package_objects = all_objects(
        package_name=package_name,
        object_types=object,
        return_names=True,
        as_dataframe=as_dataframe,
        modules_to_ignore=modules_to_ignore,
        suppress_import_stdout=suppress_import_stdout,
    )
    print(f"Scanned package '{package_name}' and found {len(all_package_objects)} objects before filtering by contract.")
    # 2. Filter the objects using the contract
    if as_dataframe:
        mask = all_package_objects["object"].apply(contract_class.istypeof)
        return all_package_objects[mask]
    
    # 3. Filter for list/tuple return
    valid_inhabitants = [
        (name, obj) if return_names else obj 
        for name, obj in all_package_objects 
        if contract_class.istypeof(obj)
    ]
    print(f"Found {len(valid_inhabitants)} objects in '{package_name}' that satisfy the contract '{contract_class.__name__}'.")

    return valid_inhabitants