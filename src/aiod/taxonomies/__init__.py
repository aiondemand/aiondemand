"""Access any taxonomy defined by AI-on-Demand.

Some metadata fields in AI-on-Demand only accept a limited set of values.
These values are defined in *hierarchical taxonomies*.
The **taxonomy** defines terms with a unique name and a definition.
For example, in the taxonomy of 'Scientific Domains', one might define a
term 'Chemical Sciences' with the definition 'The scientific study of
the properties and behavior of matter.'.
The fact that the taxonomy is **hierarchical** means that each term may
have subterms defined which can further specify the entry. For example,
'Chemical Sciences' could be a subterm of 'Natural Sciences', with
'Biology' and 'Physics' being other subterms ("siblings").


Examples
--------
```python title="Minimal Example"
import aiod
aiod.taxonomies.news_categories()
```

```python title="Output"
[
  Term(taxonomy='news categories', term='Business', definition='', subterms=[
    Term(taxonomy='news categories', term='Funding', definition='', subterms=[]),
    ...,  # more subterms, which each may have subterms
  ]),
  ...,  # more terms
]
```

Notes
-----
Defined taxonomies differ by version of the REST API.
This module lists all taxonomies for all supported versions of the REST API.
If you access a taxonomy that is not available for your defined version, an
EndpointUndefinedError is raised.
"""

import dataclasses
import functools
import sys
from http import HTTPStatus
from typing import TypedDict

import requests

from aiod.calls.urls import server_url
from aiod.calls.utils import EndpointUndefinedError
from aiod.configuration import config

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

    Attributes
    ----------
    taxonomy: str
        Name of the taxonomy from which the term originates, e.g., 'industrial sectors'.
    term: str
        A unique name for the term, e.g., 'Clinical Medicine'.
    definition: str
        A description further clarifying the meaning of the term, e.g.,
        'The branch of medicine that deals with the [...].'.
    subterms: list[Term]
        A list of subterms which provide a finer granularity.
        This list may be empty.
    """

    taxonomy: str
    term: str
    definition: str
    subterms: list["Term"]

    def __eq__(self, other):
        return self.taxonomy == other.taxonomy and self.term == other.term


class _TermDict(TypedDict):
    term: str
    definition: str
    subterms: list["_TermDict"]


def _parse_term(term: _TermDict, taxonomy: str) -> Term:
    subterms = [_parse_term(t, taxonomy) for t in term["subterms"]]
    return Term(
        taxonomy=taxonomy,
        term=term["term"],
        definition=term["definition"],
        subterms=subterms,
    )


def _get_taxonomy(name: str):
    # Since taxonomies rarely change, we cache the result in memory.
    @functools.cache
    def get_taxonomy() -> list["Term"]:
        response = requests.get(
            f"{server_url()}{name}",
            timeout=config.request_timeout_seconds,
        )
        if response.status_code == HTTPStatus.NOT_FOUND:
            raise EndpointUndefinedError()
        if response.status_code != HTTPStatus.OK:
            raise RuntimeError(
                f"Unexpected response from ({response.status_code}, {response.json()})"
            )
        return [_parse_term(term, name.replace("_", " ")) for term in response.json()]

    get_taxonomy.__wrapped__.__doc__ = f"""
    Return the hierarchical taxonomy of {name.replace("_", " ")}.

    This function uses caching, and only the first call will result in a
    call to the server.
    The cache does not persist between Python sessions.
    You can clear the cache anytime by calling

    `aiod.taxonomies.{name}.cache_clear()`.

    Returns
    -------
    list[Term]
        A hierarchical taxonomy, each entry has a 'term', 'definition', and 'subterms'.
        The 'term' is a short unique name representing the entry.
        The 'definition' provides additional text to clarify the meaning for the term.
        'Subterms' provides terms which are part of this term, and may themselves have
        subterms as well.

    Raises
    ------
    EndpointUndefinedError
        If the taxonomy is not available for the configured version of the REST API.

    RuntimeError
        For unexpected server responses.
    """
    return get_taxonomy


for _taxonomy in _TAXONOMIES:
    setattr(_mod, _taxonomy, _get_taxonomy(_taxonomy))


__all__ = _TAXONOMIES + ["Term"]
