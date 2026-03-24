"""Arxiv document loader."""

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

    def load(self, identifier: str, search_by: str = "id"):
        """Load Arxiv paper into LangChain Documents.

        Parameters
        ----------
        identifier : str
            The arXiv ID (e.g., "1706.03762") or a DOI.
        search_by : str, default="id"
            Set to 'id' for arXiv ID, or 'doi' for DOI lookup.

        Returns
        -------
        List[Document]
            List containing one Document with full paper content.
        """
        if search_by.lower() == "doi":
            query = f"doi:{identifier}"
        else:
            query = identifier

        loader = LangChainArxivLoader(query=query, load_max_docs=1)
        documents = loader.load()

        return documents
