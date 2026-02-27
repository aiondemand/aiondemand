# ruff: noqa: N803
"""Sklearn-compatible adapters for pytorch_tabular models."""


class _PyTorchTabularBaseAdapter:
    """Base sklearn-compatible adapter for pytorch_tabular models.

    Parameters
    ----------
    model_config_params : dict or None, optional
        Parameters passed to the model config constructor.
        ``task`` is forced by the subclass.
    trainer_config_params : dict or None, optional
        Parameters passed to ``TrainerConfig``.
    optimizer_config_params : dict or None, optional
        Parameters passed to ``OptimizerConfig``.
    """

    _model_config_cls = None
    _estimator_type = None
    _task = None

    def __init__(
        self,
        model_config_params=None,
        trainer_config_params=None,
        optimizer_config_params=None,
    ):
        self.model_config_params = model_config_params
        self.trainer_config_params = trainer_config_params
        self.optimizer_config_params = optimizer_config_params

    def _build_tabular_model(self, X, y):
        """Construct the internal pytorch_tabular TabularModel."""
        import pandas as pd
        from pytorch_tabular import TabularModel
        from pytorch_tabular.config import (
            DataConfig,
            OptimizerConfig,
            TrainerConfig,
        )

        if self._model_config_cls is None:
            raise TypeError(f"{type(self).__name__}._model_config_cls is not set. ")

        if isinstance(X, pd.DataFrame):
            continuous_cols = X.select_dtypes(include="number").columns.tolist()
            categorical_cols = X.select_dtypes(
                include=["category", "object"]
            ).columns.tolist()
        else:
            X = pd.DataFrame(X, columns=[f"feat_{i}" for i in range(X.shape[1])])
            continuous_cols = X.columns.tolist()
            categorical_cols = []

        target_col = "__target__"

        data_config = DataConfig(
            target=[target_col],
            continuous_cols=continuous_cols,
            categorical_cols=categorical_cols,
        )

        model_config_params = {
            **(self.model_config_params or {}),
            "task": self._task,
        }
        model_config = self._model_config_cls(**model_config_params)

        trainer_config = TrainerConfig(**(self.trainer_config_params or {}))
        optimizer_config = OptimizerConfig(**(self.optimizer_config_params or {}))

        self._tabular_model = TabularModel(
            data_config=data_config,
            model_config=model_config,
            trainer_config=trainer_config,
            optimizer_config=optimizer_config,
        )

        self._target_col = target_col
        self._continuous_cols = continuous_cols
        self._categorical_cols = categorical_cols

        return X

    def _prepare_df(self, X, y=None):
        """Convert X (and optionally y) into a single DataFrame."""
        import pandas as pd

        if isinstance(X, pd.DataFrame):
            df = X.copy()
        else:
            df = pd.DataFrame(X, columns=[f"feat_{i}" for i in range(X.shape[1])])

        if y is not None:
            df[self._target_col] = y

        return df


class _PyTorchTabularClassifierAdapter(_PyTorchTabularBaseAdapter):
    """Sklearn-compatible classifier adapter for a pytorch_tabular model."""

    _task = "classification"
    _estimator_type = "classifier"

    def fit(self, X, y):
        """Fit the classifier.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training features.
        y : array-like of shape (n_samples,)
            Target class labels.

        Returns
        -------
        self
            Fitted estimator.
        """
        import numpy as np

        self.classes_ = np.unique(y)
        X = self._build_tabular_model(X, y)
        train_df = self._prepare_df(X, y)
        self._tabular_model.fit(train=train_df)
        return self

    def predict(self, X):
        """Predict target values or class labels.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples to predict.

        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Predictions.
        """
        df = self._prepare_df(X)
        result = self._tabular_model.predict(df)
        return result["__target___prediction"].values

    def predict_proba(self, X):
        """Predict class probabilities.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples to predict.

        Returns
        -------
        proba : ndarray of shape (n_samples, n_classes)
            Predicted class probabilities.
        """
        df = self._prepare_df(X)
        result = self._tabular_model.predict(df, ret_logits=True)
        prob_cols = [c for c in result.columns if "probability" in c.lower()]
        if prob_cols:
            return result[prob_cols].values
        logit_cols = [c for c in result.columns if "logit" in c.lower()]
        if logit_cols:
            from scipy.special import softmax

            return softmax(result[logit_cols].values, axis=1)
        raise ValueError("Could not extract probabilities from prediction result.")


class _PyTorchTabularRegressorAdapter(_PyTorchTabularBaseAdapter):
    """Sklearn-compatible regressor adapter for a pytorch_tabular model."""

    _task = "regression"
    _estimator_type = "regressor"

    def fit(self, X, y):
        """Fit the model.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training features.
        y : array-like of shape (n_samples,)
            Target values.

        Returns
        -------
        self
            Fitted estimator.
        """
        X = self._build_tabular_model(X, y)
        train_df = self._prepare_df(X, y)
        self._tabular_model.fit(train=train_df)
        return self

    def predict(self, X):
        """Predict target values or class labels.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples to predict.

        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Predictions.
        """
        df = self._prepare_df(X)
        result = self._tabular_model.predict(df)
        return result["__target___prediction"].values
