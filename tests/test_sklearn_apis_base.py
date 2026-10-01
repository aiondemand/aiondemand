import pytest
from aiod.models.apis._sklearn_apis import _ModelPkgSklearnEstimator

class DummyEstimator:
    def get_params(self):
        return {"param1": 1, "param2": "value"}

class DummyModelPkg(_ModelPkgSklearnEstimator):
    def materialize(self):
        # materialize() should return a class/callable that can be instantiated
        return DummyEstimator

def test_model_pkg_sklearn_estimator_tags():
    pkg = DummyModelPkg()
    assert pkg.get_tag("pkg_obj_type") == "multiple"

def test_get_obj_tags():
    pkg = DummyModelPkg()
    assert pkg.get_obj_tags() == {}

def test_get_obj_param_names():
    pkg = DummyModelPkg()
    params = pkg.get_obj_param_names()
    assert isinstance(params, list)
    assert set(params) == {"param1", "param2"}
