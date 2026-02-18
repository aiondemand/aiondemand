"""Cross-linkage between estimators (ml_models) and papers (publications).

This module provides functions to discover and manage relationships between
ML model assets (estimators, algorithms) and publication assets (papers).

Three types of relations are supported:

- ``proposes``: The paper proposes the algorithm (primary citation).
- ``related``: The paper is a variant or precursor of the algorithm.
- ``uses``: The algorithm is used in the paper (e.g., benchmarking, application).

Examples
--------
```python title="Find papers for a model"
import aiod

# Get all papers linked to a specific ML model
papers = aiod.cross_linkage.get_publications_for_model("model_abc123")

# Get only the primary citation paper(s)
primary = aiod.cross_linkage.get_publications_for_model(
    "model_abc123",
    relation_type=aiod.cross_linkage.RelationType.proposes,
)
```

```python title="Find models for a paper"
import aiod

# Get all ML models linked to a specific paper
models = aiod.cross_linkage.get_models_for_publication("pub_xyz789")
```

```python title="Register and delete a link (auth required)"
import aiod

aiod.create_token()
link_id = aiod.cross_linkage.register_link(
    model_identifier="model_abc123",
    publication_identifier="pub_xyz789",
    relation_type=aiod.cross_linkage.RelationType.proposes,
)
aiod.cross_linkage.delete_link(link_id)
```
"""

from enum import Enum
from typing import Literal

import pandas as pd

import aiod.calls.calls as _calls


class RelationType(str, Enum):
    """The type of relation between an ml_model (estimator) and a publication (paper).

    Attributes
    ----------
    proposes : str
        The paper proposes the algorithm (primary citation).
        Example: the original Random Forest paper for ``RandomForestClassifier``.
    related : str
        The paper is a variant or precursor of the algorithm.
        Example: a paper describing a different random forest variant.
    uses : str
        The algorithm is used in the paper, but is not the subject of the paper.
        Example: a benchmarking study or application paper.
    """

    proposes = "proposes"
    related = "related"
    uses = "uses"


def _resolve_relation(relation_type: "RelationType | str | None") -> str | None:
    if isinstance(relation_type, RelationType):
        return relation_type.value
    return relation_type


def get_publications_for_model(
    model_identifier: str,
    *,
    relation_type: "RelationType | str | None" = None,
    version: str | None = None,
    data_format: Literal["pandas", "json"] = "pandas",
) -> "pd.DataFrame | list[dict]":
    """Retrieve publications (papers) linked to a specific ml_model (estimator).

    Parameters
    ----------
    model_identifier
        The AIoD identifier of the ml_model asset, e.g., ``'model_abc123'``.
    relation_type
        Filter by relation type. One of ``RelationType.proposes``,
        ``RelationType.related``, or ``RelationType.uses``.
        If ``None``, all linked publications are returned (default is ``None``).
    version
        The version of the endpoint (default is ``None``).
    data_format
        The desired format for the response (default is ``"pandas"``).
        For ``"json"`` format, the returned type is a list of dicts.

    Returns
    -------
    :
        The linked publications in the specified format.

    Raises
    ------
    KeyError
        If the model identifier cannot be found.
    """
    return _calls.get_publications_for_model(
        model_identifier,
        relation_type=_resolve_relation(relation_type),
        version=version,
        data_format=data_format,
    )


def get_models_for_publication(
    publication_identifier: str,
    *,
    relation_type: "RelationType | str | None" = None,
    version: str | None = None,
    data_format: Literal["pandas", "json"] = "pandas",
) -> "pd.DataFrame | list[dict]":
    """Retrieve ml_models (estimators) linked to a specific publication (paper).

    Parameters
    ----------
    publication_identifier
        The AIoD identifier of the publication asset, e.g., ``'pub_xyz789'``.
    relation_type
        Filter by relation type. One of ``RelationType.proposes``,
        ``RelationType.related``, or ``RelationType.uses``.
        If ``None``, all linked ml_models are returned (default is ``None``).
    version
        The version of the endpoint (default is ``None``).
    data_format
        The desired format for the response (default is ``"pandas"``).
        For ``"json"`` format, the returned type is a list of dicts.

    Returns
    -------
    :
        The linked ml_models in the specified format.

    Raises
    ------
    KeyError
        If the publication identifier cannot be found.
    """
    return _calls.get_models_for_publication(
        publication_identifier,
        relation_type=_resolve_relation(relation_type),
        version=version,
        data_format=data_format,
    )


def register_link(
    model_identifier: str,
    publication_identifier: str,
    relation_type: "RelationType | str",
    *,
    version: str | None = None,
) -> str:
    """Register a cross-link between an ml_model (estimator) and a publication (paper).

    Requires authentication. Call ``aiod.create_token()`` first.

    Parameters
    ----------
    model_identifier
        The AIoD identifier of the ml_model asset.
    publication_identifier
        The AIoD identifier of the publication asset.
    relation_type
        The type of relation. One of ``RelationType.proposes``,
        ``RelationType.related``, or ``RelationType.uses``.
    version
        The version of the endpoint (default is ``None``).

    Returns
    -------
    str
        The identifier of the newly created cross-link.

    Raises
    ------
    KeyError
        If either identifier is not found.
    aiod.authentication.NotAuthenticatedError
        If no token has been set.
    """
    return _calls.register_cross_link(
        model_identifier,
        publication_identifier,
        _resolve_relation(relation_type),
        version=version,
    )


def delete_link(
    link_identifier: str,
    *,
    version: str | None = None,
):
    """Delete a cross-link between an ml_model and a publication.

    Requires authentication. Call ``aiod.create_token()`` first.

    Parameters
    ----------
    link_identifier
        The identifier of the cross-link to delete.
    version
        The version of the endpoint (default is ``None``).

    Raises
    ------
    KeyError
        If the link identifier is not found.
    aiod.authentication.NotAuthenticatedError
        If no token has been set.
    """
    return _calls.delete_cross_link(link_identifier, version=version)


__all__ = [
    "RelationType",
    "get_publications_for_model",
    "get_models_for_publication",
    "register_link",
    "delete_link",
]
