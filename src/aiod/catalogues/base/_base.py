"""Base class for Catalogues."""

from __future__ import annotations

from abc import abstractmethod
from typing import Any, Dict, List, Union

import aiod
from aiod.base import _BasePkg

__all__ = ["BaseCatalogue"]


class BaseCatalogue(_BasePkg):
    """Base class for catalogue objects.

    A catalogue stores collections of object specifications grouped by category.
    Subclasses implement `_list`, which defines the available items.

    Items can be returned either as:
    - specification strings (default), or
    - instantiated objects (via `craft`), if `as_object=True`.
    """

    _tags: Dict[str, Any] = {
        "authors": ["aiod developers"],
        "maintainers": ["aiod developers"],
        "object_type": "catalogue",
        "catalogue_type": None,
        "n_items": None,
        "info:name": "",
        "info:description": "",
        "info:source": "",  # DOI
    }

    def __init__(self) -> None:
        """Initialize the catalogue with an empty object cache."""
        super().__init__()
        self._cached_objects: Dict[str, List[Any]] | None = None

    @abstractmethod
    def _list(self) -> Dict[str, List[Union[str, Any]]]:
        """Return the default items for this catalogue.

        Returns
        -------
        dict[str, list[str | Any]]
            Dictionary mapping category names to lists of items.
            Items may be specification strings or pre-instantiated objects.
        """
        ...

    def list(
        self,
        object_type: str = "all",
        as_object: bool = False,
    ) -> List[Union[str, Any]]:
        """Retrieve items from the catalogue.

        Parameters
        ----------
        object_type : str, default="all"
            Category of objects to retrieve.

            - "all": return items from all categories.
            - Otherwise: must match one of `available_categories()`.

        as_object : bool, default=False
            If True, return instantiated objects.
            If False, return specification strings or object names.

        Returns
        -------
        list[str] or list[Any]
            List of specification names (default) or instantiated objects.
        """
        names_dict = self._list()

        if object_type != "all" and object_type not in names_dict:
            raise KeyError(
                f"Invalid object_type '{object_type}'. "
                f"Available keys: {list(names_dict.keys())}"
            )

        items: List[Union[str, Any]] = (
            [item for sublist in names_dict.values() for item in sublist]
            if object_type == "all"
            else names_dict[object_type]
        )

        if not as_object:
            return [
                item
                if isinstance(item, str)
                else (item.__name__ if callable(item) else type(item).__name__)
                for item in items
            ]

        # as_object=True
        if self._cached_objects is None:
            self._cached_objects = {}

        if object_type not in self._cached_objects:
            processed: List[Any] = []
            for item in items:
                if isinstance(item, str):
                    processed.append(aiod.get(item))
                else:
                    processed.append(item)
            self._cached_objects[object_type] = processed

        return self._cached_objects[object_type]

    def available_categories(self) -> List[str]:
        """Return available item categories in the catalogue.

        Returns
        -------
        list[str]
            Category names defined by `_list()`.
        """
        return list(self._list().keys())

    def __len__(self) -> int:
        """Return total number of items across all categories."""
        return len(self.list("all"))

    def __contains__(self, name: str) -> bool:
        """Check whether a specification name exists in the catalogue.

        Parameters
        ----------
        name : str
            Specification string to check.

        Returns
        -------
        bool
            True if present, False otherwise.
        """
        return name in self.list("all")
