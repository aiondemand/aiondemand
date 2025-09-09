""" Access any taxonomy defined by AI-on-Demand

Warning:
    Defined taxonomies differ by version of the REST API.
    This module lists all taxonomies for all supported versions of the REST API.
    If you access a taxonomy that is not available for your defined version, an
    EndpointUndefinedError is raised.
"""
from __future__ import annotations

import dataclasses
import functools
import sys
from http import HTTPStatus
from typing import TypedDict

import requests

from aiod.calls.urls import server_url
from aiod.calls.utils import EndpointUndefinedError

_mod = sys.modules[__name__]
_TAXONOMIES = [
    "licenses",
    "industrial_sectors",
    "news_categories",
    "number_of_employees",
    "publication_types",
    "research_areas",
    "scientific_domains",
    "turnovers",
]


@dataclasses.dataclass
class Term:
    """Describes a specific term in a hierarchical taxonomy.

    Properties:
     term: str
        A unique name for the term, e.g., 'Clinical Medicine'.
    definition: str
        A description further clarifying the meaning of the term, e.g.,
        'The branch of medicine that deals with the [...].'.
    subterms: list[Term]
        A list of subterms which provide a finer granularity.
        This list may be empty.
    """

    term: str
    definition: str
    subterms: list[Term]


class _TermDict(TypedDict):
    term: str
    definition: str
    subterms: list[_TermDict]


def _parse_term(term: _TermDict) -> Term:
    subterms = [_parse_term(t) for t in term["subterms"]]
    return Term(term=term["term"], definition=term["definition"], subterms=subterms)


def _get_taxonomy(name: str):
    @functools.cache
    def get_taxonomy() -> list[Term]:
        response = requests.get(f"{server_url()}{name}")
        if response.status_code == HTTPStatus.NOT_FOUND:
            raise EndpointUndefinedError()
        if response.status_code != HTTPStatus.OK:
            raise RuntimeError(
                f"Unexpected response from ({response.status_code}, {response.json()})"
            )
        return [_parse_term(term) for term in response.json()]

    get_taxonomy.__doc__ = f"""
    Return the hierarchical taxonomy of {name.replace('_', ' ')}.

    Returns: list[Term]
        A hierarchical taxonomy, each entry has a 'term', 'definition', and 'subterms'.
        The 'term' is a short unique name representing the entry.
        The 'definition' provides additional text to clarify the meaning for the term.
        'Subterms' provides terms which are part of this term, and may themselves have subterms as well.
    Raises:
        EndpointUndefinedError: If the taxonomy is not available for the configured version of the REST API.
        RuntimeError: For other unexpected errors.
    """
    return get_taxonomy


for taxonomy in _TAXONOMIES:
    setattr(_mod, taxonomy, _get_taxonomy(taxonomy))


__all__ = _TAXONOMIES + ["Term"]
