"""OpenML API contracts."""

from aiod.contracts.openml._base import _BaseOpenMLContract
from aiod.contracts.utils import ContractError


class openml_dataset(_BaseOpenMLContract):  # noqa: N801
    _tags = {
        "scitype_name": "openml_dataset",
        "short_descr": "scitype for OpenML dataset contract",
        "parent_scitype": "openml",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from openml.datasets import OpenMLDataset

        if not isinstance(obj, OpenMLDataset):
            raise ContractError(f"{obj} is not an instance of OpenMLDataset")

        return True


class openml_regression_dataset(_BaseOpenMLContract):  # noqa: N801
    _tags = {
        "scitype_name": "openml_regression_dataset",
        "short_descr": "scitype for OpenML regression dataset contract",
        "parent_scitype": "openml",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:

        if obj.retrieve_class_labels(obj.default_target_attribute) is not None:
            raise ContractError(f"{obj} has class labels")

        return True


class openml_classification_dataset(_BaseOpenMLContract):  # noqa: N801
    _tags = {
        "scitype_name": "openml_classification_dataset",
        "short_descr": "scitype for OpenML classification dataset contract",
        "parent_scitype": "openml",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:

        if obj.retrieve_class_labels(obj.default_target_attribute) is None:
            raise ContractError(f"{obj} has no class labels")

        return True
