"""Base class for sklearn dataset loaders."""

from inspect import isfunction, signature

from skbase.base import BaseObject


class BaseSklearnDataset(BaseObject):
    """Base class for datasets wrapping sklearn loader functions."""

    _tags = {
        "object_type": "dataset",
        "name": None,
        "python_dependencies": "scikit-learn",
    }

    loader_func = None

    def __init__(self):
        super().__init__()

    def get_loader_func(self):
        """Return loader function."""
        if hasattr(type(self), "loader_func") and isfunction(type(self).loader_func):
            return type(self).loader_func
        return self.loader_func

    def load(self, *args):
        """Load dataset.

        Parameters
        ----------
        *args : str
            Available keys: "X", "y"

        Returns
        -------
        object or tuple
            Requested dataset components.
        """
        if len(args) == 0:
            args = ("X", "y")

        valid_keys = self.keys()
        for arg in args:
            if arg not in valid_keys:
                raise ValueError(f"Invalid key {arg}. Valid keys: {valid_keys}")

        X, y = self._load_dataset()

        cache = {"X": X, "y": y}
        res = [cache[key] for key in args]

        if len(res) == 1:
            return res[0]

        return tuple(res)

    def keys(self):
        """Return available dataset components."""
        return ["X", "y"]

    def _load_dataset(self):
        """Execute sklearn loader and return (X, y)."""
        loader = self.get_loader_func()
        params = signature(loader).parameters

        if "return_X_y" in params:
            X, y = loader(return_X_y=True)
        else:
            bunch = loader()
            X = bunch.data
            y = bunch.target

        return X, y

    def __getitem__(self, key):
        return self.load(key)
