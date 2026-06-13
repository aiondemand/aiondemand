"""Dummy classification catalogue."""

from __future__ import annotations

__all__ = ["DummyClassificationCatalogue"]

from typing import Any

from aiod.catalogues.base import BaseCatalogue


class DummyClassificationCatalogue(BaseCatalogue):
    """Dummy catalogue of classification components.

    This catalogue provides example classifier specifications
    for testing and demonstration purposes.
    """

    _tags: dict[str, Any] = {
        "authors": ["jgyasu"],
        "maintainers": ["jgyasu"],
        "object_type": "catalogue",
        "catalogue_type": "mixed",
        "n_items": 5,
        "n_classifiers": 5,
        "python_dependencies": ["scikit-learn"],
    }

    def _fetch(self) -> dict[str, list[str | Any]]:
        """Return classifier specifications grouped by category.

        Returns
        -------
        dict[str, list[str]]
            Dictionary with a single category `"classifier"`,
            containing sklearn classifier specification strings.
        """
        classifiers: list[str] = [
            "LogisticRegression(max_iter=1000)",
            "RandomForestClassifier(n_estimators=100)",
            "RandomForestClassifier(n_estimators=200)",
            "SVC()",
            "KNeighborsClassifier(n_neighbors=5)",
        ]

        return {
            "classifier": classifiers,
        }
