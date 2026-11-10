"""Integration tests for the Category Encoders index (issue #57)."""

import importlib

import pytest
from skbase.utils.dependencies import _check_soft_dependencies

from aiod import get
from aiod.models._registry._cls_lookup import _get_class, _id_lookup
from aiod.models.sklearn_apis.category_encoders import (
    AiodPkg__CategoryEncoders,
    AiodPkg__GLMMEncoder,
)

HAS_ENCODERS = _check_soft_dependencies("category_encoders>=2.8.1", severity="none")
HAS_STATSMODELS = _check_soft_dependencies("statsmodels", severity="none")
ENCODER_REFERENCES = {
    **AiodPkg__CategoryEncoders._obj_dict,
    "GLMMEncoder": AiodPkg__GLMMEncoder._obj,
}


@pytest.mark.skipif(not HAS_ENCODERS, reason="requires category-encoders>=2.8.1")
@pytest.mark.parametrize("identifier,reference", ENCODER_REFERENCES.items())
def test_encoder_lookup_and_construction(identifier, reference):
    """Resolve real public classes and pass constructor parameters through get."""
    if identifier == "GLMMEncoder" and not HAS_STATSMODELS:
        pytest.skip("GLMMEncoder requires statsmodels")

    module, name = reference.rsplit(".", 1)
    expected = getattr(importlib.import_module(module), name)

    assert get(identifier) is expected
    encoder = get(f"{identifier}(cols=['color'])")
    assert type(encoder) is expected
    assert encoder.get_params()["cols"] == ["color"]


@pytest.mark.parametrize("name", ["OneHotEncoder", "OrdinalEncoder", "TargetEncoder"])
def test_existing_sklearn_identifiers(name):
    """Adding the index must not replace scikit-learn's encoder identifiers."""
    pytest.importorskip("sklearn")
    from sklearn import preprocessing

    assert get(name) is getattr(preprocessing, name)


@pytest.mark.skipif(not HAS_ENCODERS, reason="requires category-encoders>=2.8.1")
@pytest.mark.parametrize(
    "identifier", ["BinaryEncoder", "CategoryEncodersTargetEncoder"]
)
def test_encoder_pipeline(identifier):
    """Use indexed encoders in a crafted pipeline and transform actual data."""
    import pandas as pd
    from pandas.testing import assert_frame_equal
    from sklearn.pipeline import Pipeline

    data = pd.DataFrame({"color": ["red", "blue", "red", "green"]})
    target = pd.Series([0, 1, 0, 1])
    pipeline = get(f"Pipeline(steps=[('encoder', {identifier}(cols=['color']))])")

    reference = AiodPkg__CategoryEncoders._obj_dict[identifier]
    module, name = reference.rsplit(".", 1)
    expected = getattr(importlib.import_module(module), name)(cols=["color"])

    assert isinstance(pipeline, Pipeline)
    assert_frame_equal(
        pipeline.fit_transform(data, target), expected.fit_transform(data, target)
    )


@pytest.mark.skipif(HAS_ENCODERS, reason="requires category-encoders to be absent")
def test_missing_category_encoders():
    """Keep the index discoverable and report the missing optional dependency."""
    assert "BinaryEncoder" in _id_lookup()
    with pytest.raises(ModuleNotFoundError, match="category_encoders"):
        _get_class("BinaryEncoder")

    with pytest.raises(RuntimeError) as exc:
        get("BinaryEncoder()")
    assert isinstance(exc.value.__cause__, ModuleNotFoundError)


@pytest.mark.skipif(
    not HAS_ENCODERS or HAS_STATSMODELS,
    reason="requires category-encoders without statsmodels",
)
def test_missing_glmm_dependency():
    """Only GLMM requires statsmodels; ordinary encoders remain usable."""
    assert get("BinaryEncoder").__name__ == "BinaryEncoder"
    with pytest.raises(ModuleNotFoundError, match="statsmodels"):
        _get_class("GLMMEncoder")
