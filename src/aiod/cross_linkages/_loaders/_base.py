"""Base class for document loaders."""

from skbase.base import BaseObject


class BaseLoader(BaseObject):
    """Abstract base class for all paper loaders.

    Loaders are responsible for:
    - Scraping and downloading documents from a source
    - Processing them into text
    - Returning LangChain Document objects
    """

    def __init__(self):
        super().__init__()

    def load(self, url: str):
        """Load documents from a given URL.

        Parameters
        ----------
        url : str
            Source URL.

        Returns
        -------
        List[Document]
            Extracted documents.
        """
        raise NotImplementedError("Subclasses must implement `load`.")
