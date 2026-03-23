"""Base interface for document converters."""

from pathlib import Path

from skbase.base import BaseObject


class DocumentConverter(BaseObject):
    """Abstract base class for document conversion strategies."""

    def __init__(self):
        super().__init__()

    def convert(self, input_path: Path, output_dir: Path) -> Path:
        """Convert a document to another format.

        Parameters
        ----------
        input_path : Path
            Path to input document.
        output_dir : Path
            Directory where output should be saved.

        Returns
        -------
        Path
            Path to converted document.
        """
        raise NotImplementedError("Subclasses must implement `convert`.")
