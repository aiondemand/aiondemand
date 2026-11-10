"""Category Encoders transformer packages."""

from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__CategoryEncoders(_ModelPkgSklearnEstimator):
    """Index encoders without replacing existing scikit-learn identifiers."""

    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "category_encoders>=2.8.1",
        "pkg_pypi_name": "category_encoders",
        "object_types": ["transformer"],
    }

    # Prefix names shared with scikit-learn to preserve existing lookups (#57).
    _obj_dict = {
        "BackwardDifferenceEncoder": "category_encoders.BackwardDifferenceEncoder",
        "BaseNEncoder": "category_encoders.BaseNEncoder",
        "BinaryEncoder": "category_encoders.BinaryEncoder",
        "CatBoostEncoder": "category_encoders.CatBoostEncoder",
        "CategoryEncodersOneHotEncoder": "category_encoders.OneHotEncoder",
        "CategoryEncodersOrdinalEncoder": "category_encoders.OrdinalEncoder",
        "CategoryEncodersTargetEncoder": "category_encoders.TargetEncoder",
        "CountEncoder": "category_encoders.CountEncoder",
        "GrayEncoder": "category_encoders.GrayEncoder",
        "HashingEncoder": "category_encoders.HashingEncoder",
        "HelmertEncoder": "category_encoders.HelmertEncoder",
        "JamesSteinEncoder": "category_encoders.JamesSteinEncoder",
        "LeaveOneOutEncoder": "category_encoders.LeaveOneOutEncoder",
        "MEstimateEncoder": "category_encoders.MEstimateEncoder",
        "PolynomialEncoder": "category_encoders.PolynomialEncoder",
        "QuantileEncoder": "category_encoders.QuantileEncoder",
        "RankHotEncoder": "category_encoders.RankHotEncoder",
        "SumEncoder": "category_encoders.SumEncoder",
        "SummaryEncoder": "category_encoders.SummaryEncoder",
        "WOEEncoder": "category_encoders.WOEEncoder",
    }

    _type_of_objs = dict.fromkeys(_obj_dict, "transformer")
    _objs_by_type = {"transformer": list(_obj_dict)}


class AiodPkg__GLMMEncoder(_ModelPkgSklearnEstimator):
    """Index GLMM separately because it also requires statsmodels."""

    _tags = {
        "pkg_id": "GLMMEncoder",
        "python_dependencies": ["category_encoders>=2.8.1", "statsmodels"],
        "pkg_pypi_name": "category_encoders",
        "object_types": ["transformer"],
    }

    _obj = "category_encoders.GLMMEncoder"
