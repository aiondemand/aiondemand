"""Adapters for scikit-learn dataset loaders."""

from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__SklearnDatasets(_ModelPkgSklearnEstimator):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "scikit-learn",
        "pkg_pypi_name": "scikit-learn",
        "object_types": ["dataset"],
    }

    _obj_dict = {
        "load_breast_cancer": "sklearn.datasets.load_breast_cancer",
        "load_diabetes": "sklearn.datasets.load_diabetes",
        "load_digits": "sklearn.datasets.load_digits",
        "load_iris": "sklearn.datasets.load_iris",
        "load_linnerud": "sklearn.datasets.load_linnerud",
        "load_wine": "sklearn.datasets.load_wine",
        "fetch_california_housing": "sklearn.datasets.fetch_california_housing",
        "make_blobs": "sklearn.datasets.make_blobs",
        "make_classification": "sklearn.datasets.make_classification",
        "make_regression": "sklearn.datasets.make_regression",
    }

    _type_of_objs = {
        "load_breast_cancer": "dataset",
        "load_diabetes": "dataset",
        "load_digits": "dataset",
        "load_iris": "dataset",
        "load_linnerud": "dataset",
        "load_wine": "dataset",
        "fetch_california_housing": "dataset",
        "make_blobs": "dataset",
        "make_classification": "dataset",
        "make_regression": "dataset",
    }

    _objs_by_type = {
        "dataset": [
            "load_breast_cancer",
            "load_diabetes",
            "load_digits",
            "load_iris",
            "load_linnerud",
            "load_wine",
            "fetch_california_housing",
            "make_blobs",
            "make_classification",
            "make_regression",
        ],
    }