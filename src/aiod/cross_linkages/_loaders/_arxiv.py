"""Arxiv document loader."""

import re

from langchain_community.document_loaders import ArxivLoader as LangChainArxivLoader
from skbase.utils.dependencies import _safe_import

from aiod.cross_linkages._loaders._base import BaseLoader

Document = _safe_import("langchain_core.documents.Document", pkg_name="langchain")


class ArxivLoader(BaseLoader):
    """Loader for Arxiv papers using LangChain's community loader.

    Returns
    -------
    List[Document]
        List containing Langchain Document wrapping the paper content and metadata.
    """

    _tags = {
        "python_dependencies": [
            "langchain",
            "langchain_community",
        ],
    }

    def __init__(self):
        super().__init__()

    def _extract_id_from_url(self, url: str) -> str:
        """Extract the arXiv ID from various URL formats."""
        match = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5}(?:v\d+)?)", url)

        if match:
            return match.group(1)

        raise ValueError(
            f"Could not parse a valid ArXiv ID from the provided link: {url}"
        )

    def load(self, url: str):
        """Load Arxiv paper into LangChain Documents using a URL.

        Parameters
        ----------
        url : str
            The full arXiv URL (e.g., "https://arxiv.org/abs/1706.03762").

        Returns
        -------
        List[Document]
            List containing one Document with full paper content.
        """
        if not isinstance(url, str) or "arxiv.org" not in url:
            raise ValueError("Please provide a valid arxiv.org link.")

        arxiv_id = self._extract_id_from_url(url)

        loader = LangChainArxivLoader(query=arxiv_id, load_max_docs=1)
        documents = loader.load()

        return documents
