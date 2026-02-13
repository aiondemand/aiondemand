"""Dummy classification catalogue."""

from __future__ import annotations

__all__ = ["DummyClassificationCatalogue"]

from typing import Any, Dict, List, Union

from aiod.catalogues.base import BaseCatalogue


class DummyClassificationCatalogue(BaseCatalogue):
    """Dummy catalogue of classification components.

    This catalogue provides example classifier specifications
    for testing and demonstration purposes.
    """

    _tags: Dict[str, Any] = {
        "authors": ["jgyasu"],
        "maintainers": ["jgyasu"],
        "object_type": "catalogue",
        "catalogue_type": "mixed",
        "n_items": 5,
        "n_classifiers": 5,
        "python_dependencies": ["scikit-learn"],
    }

    def _list(self) -> Dict[str, List[Union[str, Any]]]:
        """Return classifier specifications grouped by category.

        Returns
        -------
        dict[str, list[str]]
            Dictionary with a single category `"classifier"`,
            containing sklearn classifier specification strings.
        """
        classifiers: List[str] = [
            "LogisticRegression(max_iter=1000)",
            "RandomForestClassifier(n_estimators=100)",
            "RandomForestClassifier(n_estimators=200)",
            "SVC()",
            "KNeighborsClassifier(n_neighbors=5)",
        ]

        return {
            "classifier": classifiers,
        }
