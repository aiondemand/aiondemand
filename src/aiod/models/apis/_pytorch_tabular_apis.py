"""Base package for pytorch_tabular estimators."""

from aiod.models.base import _AiodModelPkg

__all__ = ["_ModelPkgPytorchTabularEstimator"]


class _ModelPkgPytorchTabularEstimator(_AiodModelPkg):
    _tags = {
        "pkg_obj_type": "pytorch_tabular_estimator",
    }

    def _materialize(self):
        """Materialize a sklearn-compatible adapter for the pytorch_tabular model."""
        from skbase.utils.dependencies import _safe_import

        obj_id = self.id
        obj_path = self._obj_dict.get(obj_id)
        if obj_path is None:
            raise ValueError(f"Object with id {obj_id} not found in _obj_dict.")

        pkg_name = self.get_tag("pkg_pypi_name")
        config_cls = _safe_import(obj_path, pkg_name=pkg_name)

        type_of_obj = self._type_of_objs.get(obj_id)
        if type_of_obj not in ("classifier", "regressor"):
            raise ValueError(f"Unknown object type {type_of_obj!r} for {obj_id}.")
        return _make_adapter(config_cls, obj_id, type_of_obj)

    def get_obj_tags(self):
        """Return tags of the object as a dictionary."""
        return {}  # this needs to be implemented

    def get_obj_param_names(self):
        """Return parameter names of the object as a list."""
        return [
            "model_config_params",
            "trainer_config_params",
            "optimizer_config_params",
        ]


def _make_adapter(config_cls, name, estimator_type):
    """Create a concrete adapter class with config baked in as class attr."""
    from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin

    from aiod.models.adapters._tabular_adapter import (
        _PyTorchTabularClassifierAdapter,
        _PyTorchTabularRegressorAdapter,
    )

    if estimator_type == "regressor":
        bases = (_PyTorchTabularRegressorAdapter, RegressorMixin, BaseEstimator)
    else:
        bases = (_PyTorchTabularClassifierAdapter, ClassifierMixin, BaseEstimator)

    cls = type(
        name,
        bases,
        {
            "_model_config_cls": config_cls,
            "__module__": "aiod.models.pytorch_tabular",
            "__doc__": f"Sklearn-compatible {name} powered by pytorch_tabular.",
        },
    )
    return cls
