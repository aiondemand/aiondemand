"""OpenML dataset loader."""

from skbase.base import BaseObject


class OpenMLDataset(BaseObject):
    """Dataset loader for any OpenML dataset.

    Loads a dataset from openml.org by its integer dataset ID.
    """

    _tags = {
        "object_type": "dataset",
        "python_dependencies": "openml",
    }

    def __init__(self, dataset_id, target=None):
        self.dataset_id = dataset_id
        self.target = target
        super().__init__()

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
        """Fetch dataset from OpenML and return (X, y)."""
        import openml

        dataset = openml.datasets.get_dataset(self.dataset_id)

        target = self.target
        if target is None:
            target = dataset.default_target_attribute

        X, y, _, _ = dataset.get_data(target=target)
        return X, y

    def __getitem__(self, key):
        return self.load(key)
