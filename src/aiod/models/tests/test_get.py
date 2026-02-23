"""Tests for models.get."""

import pytest
from skbase.utils.dependencies import _check_soft_dependencies


@pytest.mark.skipif(
    not _check_soft_dependencies("scikit-learn", severity="none"),
    reason="run only if scikit-learn is installed",
)
def test_get_basic_usage():
    """Test basic get usage if soft dependencies are present.

    When called with a class ID, the class should be retrieved directly.
    """
    from sklearn.ensemble import RandomForestClassifier

    from aiod.models import get

    rfc_from_get = get("RandomForestClassifier")
    assert rfc_from_get == RandomForestClassifier


@pytest.mark.skipif(
    _check_soft_dependencies("scikit-learn", severity="none"),
    reason="run only if scikit-learn is not installed",
)
def test_get_basic_usage_softdep_not_present():
    """Test get when soft dependency is not present.

    This should raise an error message, prompting the user
    to install the correct dependency.
    """
    from aiod.models import get

    with pytest.raises(ModuleNotFoundError, match=r"scikit-learn"):
        get("RandomForestClassifier")
