"""User-facing utilities for querying paper–algorithm relationships."""

from __future__ import annotations

from typing import Literal

from aiod.cross_linkages.pub_algo_registry import PUB_ALGORITHM_REGISTRY
from aiod.models import get

ReturnMode = Literal["ids", "classes", "instances"]


def get_from_pub(doi: str, return_as: ReturnMode = "ids") -> list[object]:
    """Retrieve algorithms associated with a publication.

    Parameters
    ----------
    doi : str
        DOI of the publication.

    return_as : {"ids", "classes", "instances"}, default="ids"
        Determines the format of the returned results.

        - "ids": return algorithm identifiers as strings.
        - "classes": return classes.
        - "instances": return instantiated objects.

    Returns
    -------
    list
        List of identifiers, classes, or instantiated objects.

    Examples
    --------
    >>> aiod.get_from_pub('10.1023/A:1010933404324')
    ['RandomForestClassifier']
    >>> aiod.get_from_pub('10.1023/A:1010933404324', return_as="instances")
    [RandomForestClassifier()]
    >>> aiod.get_from_pub('10.1023/A:1010933404324', return_as="classes")
    [sklearn.ensemble._forest.RandomForestClassifier]
    """
    algos = PUB_ALGORITHM_REGISTRY.get(doi, [])

    if return_as == "ids":
        return list(algos)

    if return_as == "classes":
        return [get(a) for a in algos]

    if return_as == "instances":
        return [get(f"{a}()") for a in algos]

    raise ValueError(f"Unknown return mode: {return_as}")


def get_pubs_for(algorithm: str) -> list[str]:
    """Retrieve publications associated with a given algorithm.

    Parameters
    ----------
    algorithm : str
        Algorithm class names.

    Returns
    -------
    list[str]
        List of DOIs that reference the algorithm.

    Examples
    --------
    >>> aiod.get_pubs_for("RandomForestClassifier")
    ['10.1023/A:1010933404324']
    """
    result: list[str] = []

    for doi, algos in PUB_ALGORITHM_REGISTRY.items():
        if algorithm in algos:
            result.append(doi)

    return result
