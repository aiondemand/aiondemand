"""Base class for document scrapers/downloaders."""

from pathlib import Path

from skbase.base import BaseObject


class BaseDownloader(BaseObject):
    """Abstract base class for all document scrapers/downloaders.

    Subclasses must implement the `download` method to fetch a document
    from a given URL and store it locally.
    """

    def __init__(self):
        super().__init__()

    async def download(
        self,
        url: str,
        output_dir: Path,
        retries: int = 3,
    ) -> Path:
        """Download a document from a URL.

        Parameters
        ----------
        url : str
            Source URL of the document.
        output_dir : Path
            Directory where the downloaded file should be stored.
        retries : int, default=3
            Number of retry attempts in case of failure.

        Returns
        -------
        Path
            Local filesystem path to the downloaded file.

        Raises
        ------
        NotImplementedError
            Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement `download`.")
