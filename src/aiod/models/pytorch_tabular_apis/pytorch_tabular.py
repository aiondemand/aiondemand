# ruff: noqa: E501
"""PyTorch Tabular models - sklearn-compatible packaging."""

from aiod.models.apis import _ModelPkgPytorchTabularEstimator


class AiodPkg__PyTorchTabular(_ModelPkgPytorchTabularEstimator):
    """All pytorch_tabular models, exposed as sklearn-compatible estimators."""

    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "pytorch_tabular",
        "pkg_pypi_name": "pytorch_tabular",
        "object_types": ["classifier", "regressor"],
    }

    _obj_dict = {
        "CategoryEmbeddingClassifier": "pytorch_tabular.models.CategoryEmbeddingModelConfig",
        "CategoryEmbeddingRegressor": "pytorch_tabular.models.CategoryEmbeddingModelConfig",
        "TabNetClassifier": "pytorch_tabular.models.TabNetModelConfig",
        "TabNetRegressor": "pytorch_tabular.models.TabNetModelConfig",
        "FTTransformerClassifier": "pytorch_tabular.models.FTTransformerConfig",
        "FTTransformerRegressor": "pytorch_tabular.models.FTTransformerConfig",
        "AutoIntClassifier": "pytorch_tabular.models.AutoIntConfig",
        "AutoIntRegressor": "pytorch_tabular.models.AutoIntConfig",
        "NodeClassifier": "pytorch_tabular.models.NodeConfig",
        "NodeRegressor": "pytorch_tabular.models.NodeConfig",
        "GANDALFClassifier": "pytorch_tabular.models.GANDALFConfig",
        "GANDALFRegressor": "pytorch_tabular.models.GANDALFConfig",
        "TabTransformerClassifier": "pytorch_tabular.models.TabTransformerConfig",
        "TabTransformerRegressor": "pytorch_tabular.models.TabTransformerConfig",
        "DANetClassifier": "pytorch_tabular.models.DANetConfig",
        "DANetRegressor": "pytorch_tabular.models.DANetConfig",
        "GatedAdditiveTreeEnsembleClassifier": "pytorch_tabular.models.GatedAdditiveTreeEnsembleConfig",
        "GatedAdditiveTreeEnsembleRegressor": "pytorch_tabular.models.GatedAdditiveTreeEnsembleConfig",
    }

    _type_of_objs = {
        "CategoryEmbeddingClassifier": "classifier",
        "CategoryEmbeddingRegressor": "regressor",
        "TabNetClassifier": "classifier",
        "TabNetRegressor": "regressor",
        "FTTransformerClassifier": "classifier",
        "FTTransformerRegressor": "regressor",
        "AutoIntClassifier": "classifier",
        "AutoIntRegressor": "regressor",
        "NodeClassifier": "classifier",
        "NodeRegressor": "regressor",
        "GANDALFClassifier": "classifier",
        "GANDALFRegressor": "regressor",
        "TabTransformerClassifier": "classifier",
        "TabTransformerRegressor": "regressor",
        "DANetClassifier": "classifier",
        "DANetRegressor": "regressor",
        "GatedAdditiveTreeEnsembleClassifier": "classifier",
        "GatedAdditiveTreeEnsembleRegressor": "regressor",
    }
