import pytest

from aiod.models.apis import _ModelPkgSklearnEstimator
from aiod.models.sklearn_apis.xgboost import AiodPkg__XGBClassifier
from aiod.models.sklearn_apis.auto_sklearn import AiodPkg__AutoSklearnClassifier
from aiod.models.sklearn_apis.lightgbm import AiodPkg__LightGBM


def test_xgboost_wrapper_definition():
    pkg = AiodPkg__XGBClassifier()
    assert isinstance(pkg, _ModelPkgSklearnEstimator)
    assert pkg.get_tag("pkg_id") == "XGBClassifier"
    assert pkg.get_tag("python_dependencies") == "xgboost"
    assert pkg.get_tag("pkg_pypi_name") == "xgboost"
    assert AiodPkg__XGBClassifier._obj == "xgboost.XGBClassifier"


def test_autosklearn_wrapper_definition():
    pkg = AiodPkg__AutoSklearnClassifier()
    assert isinstance(pkg, _ModelPkgSklearnEstimator)
    assert pkg.get_tag("pkg_id") == "AutoSklearnClassifier"
    assert pkg.get_tag("python_dependencies") == "auto-sklearn"
    assert pkg.get_tag("pkg_pypi_name") == "auto-sklearn"
    assert AiodPkg__AutoSklearnClassifier._obj == "autosklearn.classification.AutoSklearnClassifier"


def test_lightgbm_wrapper_definition():
    pkg = AiodPkg__LightGBM()
    assert isinstance(pkg, _ModelPkgSklearnEstimator)
    assert pkg.get_tag("pkg_id") == "__multiple"
    assert pkg.get_tag("python_dependencies") == "lightgbm"
    assert pkg.get_tag("pkg_pypi_name") == "lightgbm"
    
    assert "LGBMClassifier" in AiodPkg__LightGBM._obj_dict
    assert "LGBMRegressor" in AiodPkg__LightGBM._obj_dict
    assert AiodPkg__LightGBM._type_of_objs["LGBMClassifier"] == "classifier"
    
    assert "LGBMClassifier" in AiodPkg__LightGBM._objs_by_type["classifier"]
    assert "LGBMRegressor" in AiodPkg__LightGBM._objs_by_type["regressor"]
