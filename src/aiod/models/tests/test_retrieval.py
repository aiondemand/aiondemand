"""Test model retrieval from AIoD indexed packages."""

import pytest

from skbase.utils.dependencies import _safe_import

from aiod.models._get import get

RandomForestClassifier = _safe_import(
    import_path="sklearn.ensemble.RandomForestClassifier", pkg_name="scikit-learn"
)
GradientBoostingRegressor = _safe_import(
    import_path="sklearn.ensemble.GradientBoostingRegressor", pkg_name="scikit-learn"
)
SVC = _safe_import(import_path="sklearn.svm.SVC", pkg_name="scikit-learn")


class TestModelRetrieval:
    @pytest.mark.parametrize(
        "model_id, expected_class",
        [
            ("RandomForestClassifier", RandomForestClassifier),
            ("SVC", SVC),
            ("GradientBoostingRegressor", GradientBoostingRegressor),
        ],
    )
    def test_get_sklearn_models(self, model_id, expected_class):
        """
        Tests that aiod.get successfully retrieves and imports
        scikit-learn classes by their string ID.
        """
        retrieved_class = get(model_id)

        assert retrieved_class is expected_class

    def test_get_non_existent_model(self):
        """
        Tests that requesting a non-existent ID raises a ValueError.
        """
        with pytest.raises(ValueError, match="does not exist"):
            get("ThisModelDoesNotExist")

    def test_caching_behavior(self):
        """
        Verify that _id_lookup is cached (lru_cache) and we get
        consistent results on subsequent calls.
        """
        cls1 = get("KMeans")
        cls2 = get("KMeans")
        assert cls1 is cls2
