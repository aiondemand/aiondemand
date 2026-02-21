"""Tests for models.get."""

import pytest

from skbase.utils.dependencies import _check_soft_dependencies


pytest.mark.skipif(not _check_soft_dependencies("scikit-learn", severity="none"))
def test_get_basic_usage():
    from sklearn.ensemble import RandomForestClassifier

    from aiod.models import get

    rfc_from_get = get("RandomForestClassifier")
    assert rfc_from_get == RandomForestClassifier

